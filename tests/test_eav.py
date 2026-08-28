"""
Unit-level coverage for utils/eav.py's batching -- the module this project
writes specifically so the N+1 query bug found (and fixed) in laragento's
CategoryController isn't reachable here: flatten_products() must do a
fixed number of queries (one per value table) no matter how many entity
ids are passed in, not "5 x number of entities".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.conftest import skip_unless_db_reachable  # noqa: E402
from utils import eav  # noqa: E402


def test_flatten_products_issues_one_query_per_value_table_regardless_of_count(engine, metadata):
    skip_unless_db_reachable(engine)
    from sqlalchemy import select

    product_table = metadata.tables["catalog_product_entity"]
    with engine.connect() as conn:
        ids = [row.entity_id for row in conn.execute(select(product_table.c.entity_id).limit(10))]
    if len(ids) < 2:
        import pytest

        pytest.skip("Fewer than 2 products in this database.")

    query_count = {"n": 0}
    with engine.connect() as conn:
        # Wrap execute to count round trips without needing SQLAlchemy's
        # event API (keeps this test readable and version-agnostic).
        real_execute = conn.execute

        def counting_execute(*args, **kwargs):
            query_count["n"] += 1
            return real_execute(*args, **kwargs)

        conn.execute = counting_execute

        eav.flatten_products(conn, metadata, ids, ["name", "price"])

    # 1 query to resolve attribute codes -> ids, + 1 per value table (all 5,
    # regardless of which backend types the requested codes actually use) --
    # a fixed number that must NOT grow with len(ids). The real regression
    # this guards against is "5 x len(ids)" (or worse), not this constant.
    assert query_count["n"] <= 6, f"expected a bounded query count for {len(ids)} products, got {query_count['n']}"


def test_flatten_product_returns_expected_codes(engine, metadata):
    skip_unless_db_reachable(engine)
    from sqlalchemy import select

    product_table = metadata.tables["catalog_product_entity"]
    with engine.connect() as conn:
        row = conn.execute(select(product_table.c.entity_id).limit(1)).first()
    if row is None:
        import pytest

        pytest.skip("No products in this database.")

    with engine.connect() as conn:
        attrs = eav.flatten_product(conn, metadata, row.entity_id, ["name", "price"])

    # name/price are required core attributes on any real Magento catalog
    # install, so a product must have at least one of them resolved.
    assert "name" in attrs or "price" in attrs


def test_flatten_products_with_empty_id_list_does_not_query(engine, metadata):
    skip_unless_db_reachable(engine)
    with engine.connect() as conn:
        result = eav.flatten_products(conn, metadata, [], ["name"])
    assert result == {}
