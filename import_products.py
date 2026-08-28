#!/usr/bin/env python3
"""
Magmi-style bulk product importer for PyGento.

Same shape (and the same fix) as every other importer in this benchmark
family (GoGento, gogento-rust, laragento): parse a CSV, resolve SKUs
against catalog_product_entity, bulk-insert new entities (relying on
MySQL/InnoDB's consecutive-auto-increment-lock guarantee for a multi-row
insert), bucket attribute values by EAV backend_type, and batch-upsert
each of the 5 catalog_product_entity_* value tables -- one explicit
transaction per table, one multi-row `INSERT ... ON DUPLICATE KEY UPDATE`
per batch via SQLAlchemy Core's MySQL-dialect `insert().on_duplicate_key_update()`.
Never a per-row ORM model save.

Usage:
    python import_products.py products.csv --batch-size 500
"""
import argparse
import csv
import time

from sqlalchemy import create_engine, select, text
from sqlalchemy.dialects.mysql import insert as mysql_insert

from utils.database import db_connection

VALUE_TABLES = {
    "varchar": "catalog_product_entity_varchar",
    "int": "catalog_product_entity_int",
    "decimal": "catalog_product_entity_decimal",
    "text": "catalog_product_entity_text",
    "datetime": "catalog_product_entity_datetime",
}


def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def load_attributes(conn, metadata):
    """attribute_code -> {"id": attribute_id, "type": backend_type}, scoped to
    entity_type_id=4 (catalog_product) and the 5 recognized backend types."""
    eav_attribute = metadata.tables["eav_attribute"]
    rows = conn.execute(
        select(eav_attribute.c.attribute_id, eav_attribute.c.attribute_code, eav_attribute.c.backend_type)
        .where(eav_attribute.c.entity_type_id == 4)
        .where(eav_attribute.c.backend_type.in_(VALUE_TABLES.keys()))
    ).fetchall()
    return {row.attribute_code: {"id": row.attribute_id, "type": row.backend_type} for row in rows}


def lookup_existing_skus(conn, entity_table, skus, batch_size):
    """sku -> entity_id, for whichever of `skus` already exist."""
    sku_to_id = {}
    for chunk in chunked(skus, batch_size):
        rows = conn.execute(
            select(entity_table.c.entity_id, entity_table.c.sku).where(entity_table.c.sku.in_(chunk))
        ).fetchall()
        for row in rows:
            sku_to_id[row.sku] = row.entity_id
    return sku_to_id


def insert_new_products(conn, entity_table, entries, attribute_set_id, batch_size):
    """Bulk-inserts new entities, relying on MySQL/InnoDB's consecutive-
    auto-increment-lock guarantee for a multi-row insert -- the same trick
    every other importer in this project's benchmark family uses.

    entries: list of (sku, type_id) tuples.
    Returns sku -> entity_id for the newly created rows.
    """
    sku_to_id = {}
    for chunk in chunked(entries, batch_size):
        rows = [{"attribute_set_id": attribute_set_id, "type_id": type_id, "sku": sku} for sku, type_id in chunk]
        result = conn.execute(entity_table.insert(), rows)
        first_id = result.lastrowid
        for i, (sku, _type_id) in enumerate(chunk):
            sku_to_id[sku] = first_id + i
    return sku_to_id


def upsert_eav_table(conn, table, rows, batch_size):
    """Batched upsert into one of the 5 EAV value tables: one explicit
    transaction wrapping every chunk (the same fix this project's Go and
    Rust importers both needed for per-chunk-autocommit overhead), one
    multi-row `INSERT ... ON DUPLICATE KEY UPDATE` per chunk via
    SQLAlchemy's MySQL-dialect upsert construct -- not a hand-written SQL
    string, and not a per-row ORM save.
    """
    if not rows:
        return
    with conn.begin():
        for chunk in chunked(rows, batch_size):
            stmt = mysql_insert(table).values(chunk)
            stmt = stmt.on_duplicate_key_update(value=stmt.inserted.value)
            conn.execute(stmt)


def main():
    parser = argparse.ArgumentParser(description="Magmi-style bulk product import from CSV")
    parser.add_argument("file", help="Path to the CSV file to import")
    parser.add_argument("--batch-size", type=int, default=500, help="Rows per batched insert/upsert statement")
    parser.add_argument("--store", type=int, default=0, help="Store ID to write EAV values under")
    parser.add_argument("--attribute-set", type=int, default=4, help="attribute_set_id assigned to newly created products")
    args = parser.parse_args()

    total_start = time.perf_counter()

    with open(args.file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        if header is None or "sku" not in header:
            raise SystemExit("CSV must contain a 'sku' column")
        csv_rows = list(reader)
    total_rows = len(csv_rows)

    engine = create_engine(db_connection.get_connection_string())

    from sqlalchemy import MetaData

    metadata = MetaData()
    metadata.reflect(bind=engine, only=["catalog_product_entity", "eav_attribute", *VALUE_TABLES.values()])
    entity_table = metadata.tables["catalog_product_entity"]

    db_time = 0.0
    process_start = time.perf_counter()

    with engine.connect() as conn:
        t0 = time.perf_counter()
        attrs = load_attributes(conn, metadata)
        db_time += time.perf_counter() - t0

        sku_type = {}
        skus = []
        for row in csv_rows:
            sku = (row.get("sku") or "").strip()
            if not sku:
                continue
            skus.append(sku)
            if sku not in sku_type:
                sku_type[sku] = (row.get("type_id") or "").strip() or "simple"
        skus = list(dict.fromkeys(skus))  # de-dup, preserve order
        process_time = time.perf_counter() - process_start

        t0 = time.perf_counter()
        sku_to_id = lookup_existing_skus(conn, entity_table, skus, args.batch_size)
        updated_count = sum(1 for sku in sku_type if sku in sku_to_id)

        new_entries = [(sku, type_id) for sku, type_id in sku_type.items() if sku not in sku_to_id]
        created_count = len(new_entries)
        if new_entries:
            sku_to_id.update(insert_new_products(conn, entity_table, new_entries, args.attribute_set, args.batch_size))
        db_time += time.perf_counter() - t0

        bucket_start = time.perf_counter()
        buckets = {backend_type: [] for backend_type in VALUE_TABLES}
        for row in csv_rows:
            sku = (row.get("sku") or "").strip()
            if not sku or sku not in sku_to_id:
                continue
            entity_id = sku_to_id[sku]
            for code, value in row.items():
                attr = attrs.get(code)
                if attr is None or not value:
                    continue
                buckets[attr["type"]].append(
                    {"entity_id": entity_id, "attribute_id": attr["id"], "store_id": args.store, "value": value}
                )
        process_time += time.perf_counter() - bucket_start

        t0 = time.perf_counter()
        for backend_type, table_name in VALUE_TABLES.items():
            upsert_eav_table(conn, metadata.tables[table_name], buckets[backend_type], args.batch_size)
        db_time += time.perf_counter() - t0

    total_time = time.perf_counter() - total_start
    eav_total = sum(len(rows) for rows in buckets.values())

    print("=== Python (Magmi-style) Import Performance ===")
    print(f"Rows in CSV:    {total_rows}")
    print(f"Products:       {created_count} created, {updated_count} updated")
    print(
        "EAV rows:       {} (varchar={} int={} decimal={} text={} datetime={})".format(
            eav_total,
            len(buckets["varchar"]),
            len(buckets["int"]),
            len(buckets["decimal"]),
            len(buckets["text"]),
            len(buckets["datetime"]),
        )
    )
    print(f"Total time:     {total_time:.3f}s")
    print(f"  - Processing: {process_time:.3f}s")
    print(f"  - DB time:    {db_time:.3f}s")
    print("=================================================")


if __name__ == "__main__":
    main()
