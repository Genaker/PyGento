"""Tests for import_products.py -- the Magmi-style bulk importer."""
import os
import subprocess
import sys

from sqlalchemy import select

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.conftest import skip_unless_db_reachable  # noqa: E402

SKU_PREFIX = "PYGENTO-TEST-"
FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "synthetic_products.csv")
IMPORTER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "import_products.py")


def _delete_fixture_products(engine, metadata):
    product_table = metadata.tables["catalog_product_entity"]
    with engine.connect() as conn:
        ids = [row.entity_id for row in conn.execute(select(product_table.c.entity_id).where(product_table.c.sku.like(f"{SKU_PREFIX}%")))]
        if not ids:
            return
        with conn.begin():
            for table_name in ["catalog_product_entity_varchar", "catalog_product_entity_int", "catalog_product_entity_decimal", "catalog_product_entity_text", "catalog_product_entity_datetime"]:
                table = metadata.tables[table_name]
                conn.execute(table.delete().where(table.c.entity_id.in_(ids)))
            conn.execute(product_table.delete().where(product_table.c.entity_id.in_(ids)))


def _run_importer(*args):
    return subprocess.run(
        [sys.executable, IMPORTER, *args],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )


def test_import_creates_products_and_eav_values(engine, metadata):
    skip_unless_db_reachable(engine)
    _delete_fixture_products(engine, metadata)
    try:
        result = _run_importer(FIXTURE, "--batch-size", "500")
        assert result.returncode == 0, result.stderr
        assert "20 created, 0 updated" in result.stdout

        product_table = metadata.tables["catalog_product_entity"]
        with engine.connect() as conn:
            count = conn.execute(select(product_table.c.entity_id).where(product_table.c.sku.like(f"{SKU_PREFIX}%"))).rowcount
        assert count == 20
    finally:
        _delete_fixture_products(engine, metadata)


def test_reimport_updates_in_place_instead_of_duplicating(engine, metadata):
    skip_unless_db_reachable(engine)
    _delete_fixture_products(engine, metadata)
    try:
        _run_importer(FIXTURE, "--batch-size", "500")
        second = _run_importer(FIXTURE, "--batch-size", "500")
        assert second.returncode == 0, second.stderr
        assert "0 created, 20 updated" in second.stdout

        product_table = metadata.tables["catalog_product_entity"]
        varchar_table = metadata.tables["catalog_product_entity_varchar"]
        with engine.connect() as conn:
            product_count = conn.execute(select(product_table.c.entity_id).where(product_table.c.sku.like(f"{SKU_PREFIX}%"))).rowcount
            ids = [row.entity_id for row in conn.execute(select(product_table.c.entity_id).where(product_table.c.sku.like(f"{SKU_PREFIX}%")))]
            varchar_count = conn.execute(select(varchar_table.c.value_id).where(varchar_table.c.entity_id.in_(ids))).rowcount

        assert product_count == 20, "second import must not create duplicate entities"
        assert varchar_count == 60, "upsert must update rows in place, not insert duplicates (3 varchar attrs x 20 products)"
    finally:
        _delete_fixture_products(engine, metadata)


def test_missing_file_fails_cleanly(engine):
    skip_unless_db_reachable(engine)
    result = _run_importer("/nonexistent/path.csv")
    assert result.returncode != 0
