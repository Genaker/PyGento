"""
Flattens a product or category entity's EAV attribute values into a plain
dict -- the same "join five value tables into one flat map" concept every
other reimplementation in this benchmark family (GoGento, gogento-rust,
laragento) builds its repository layer around.

Scoped to a fixed set of attribute codes per entity type rather than
joining "every attribute this entity has" -- fetching every EAV value a
real Magento product carries (which can be 50+) for a storefront page that
only ever displays a handful of them would be pure waste.

Batch-first: flatten_products() fetches N entities in one query per value
table, not one query per table *per entity* -- looping flatten_product()
over a product grid is an N+1 query bug, not a style choice (this is the
exact bug found and fixed in laragento's CategoryController; this module
is written to make that mistake harder to reach for, not just possible to
avoid).
"""
from sqlalchemy import select

PRODUCT_ENTITY_TYPE_ID = 4
CATEGORY_ENTITY_TYPE_ID = 3

PRODUCT_VALUE_TABLES = {
    "varchar": "catalog_product_entity_varchar",
    "int": "catalog_product_entity_int",
    "decimal": "catalog_product_entity_decimal",
    "text": "catalog_product_entity_text",
    "datetime": "catalog_product_entity_datetime",
}

CATEGORY_VALUE_TABLES = {
    "varchar": "catalog_category_entity_varchar",
    "int": "catalog_category_entity_int",
    "decimal": "catalog_category_entity_decimal",
    "text": "catalog_category_entity_text",
    "datetime": "catalog_category_entity_datetime",
}

_attribute_id_cache = {}


def _attribute_ids(conn, metadata, entity_type_id, codes):
    """attribute_code -> attribute_id, cached per process (attribute IDs
    are effectively static for a running install)."""
    key = (entity_type_id, tuple(sorted(codes)))
    if key in _attribute_id_cache:
        return _attribute_id_cache[key]

    eav_attribute = metadata.tables["eav_attribute"]
    rows = conn.execute(
        select(eav_attribute.c.attribute_id, eav_attribute.c.attribute_code)
        .where(eav_attribute.c.entity_type_id == entity_type_id)
        .where(eav_attribute.c.attribute_code.in_(codes))
    ).fetchall()
    result = {row.attribute_code: row.attribute_id for row in rows}
    _attribute_id_cache[key] = result
    return result


def _flatten(conn, metadata, entity_type_id, tables, entity_ids, codes, store_id):
    """entity_id -> {attribute_code: value}, for every id in entity_ids."""
    result = {entity_id: {} for entity_id in entity_ids}
    if not entity_ids:
        return result

    attribute_ids = _attribute_ids(conn, metadata, entity_type_id, codes)
    if not attribute_ids:
        return result
    id_to_code = {v: k for k, v in attribute_ids.items()}

    for table_name in tables.values():
        table = metadata.tables[table_name]
        rows = conn.execute(
            select(table.c.entity_id, table.c.attribute_id, table.c.store_id, table.c.value)
            .where(table.c.entity_id.in_(entity_ids))
            .where(table.c.attribute_id.in_(id_to_code.keys()))
            .where(table.c.store_id.in_({0, store_id}))
            .order_by(table.c.store_id)
        ).fetchall()

        # Store 0 (default) first, then the requested store overlays it --
        # last-writer-wins on a store-specific override, same precedence
        # Magento's own EAV read path uses.
        for row in rows:
            code = id_to_code.get(row.attribute_id)
            if code is not None:
                result[row.entity_id][code] = row.value

    return result


def flatten_products(conn, metadata, entity_ids, codes, store_id=0):
    """Batch variant: one query per value table for the whole entity_ids
    set. Use this for anything rendering more than one product."""
    return _flatten(conn, metadata, PRODUCT_ENTITY_TYPE_ID, PRODUCT_VALUE_TABLES, entity_ids, codes, store_id)


def flatten_product(conn, metadata, entity_id, codes, store_id=0):
    return flatten_products(conn, metadata, [entity_id], codes, store_id).get(entity_id, {})


def flatten_category(conn, metadata, entity_id, codes, store_id=0):
    return _flatten(conn, metadata, CATEGORY_ENTITY_TYPE_ID, CATEGORY_VALUE_TABLES, [entity_id], codes, store_id).get(
        entity_id, {}
    )
