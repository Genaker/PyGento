"""
Shared pytest fixtures. Every test that touches the database calls
`skip_unless_db_reachable()` first and skips rather than fails if it isn't
reachable -- there's no disposable schema here to spin up in CI, this
project reads a real Magento database, same convention GoGento's,
gogento-rust's, and laragento's own DB-touching tests all use.
"""
import os
import sys

import pytest
from sqlalchemy import MetaData, create_engine, text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import db_connection  # noqa: E402


@pytest.fixture(scope="session")
def engine():
    return create_engine(db_connection.get_connection_string())


@pytest.fixture(scope="session")
def metadata(engine):
    md = MetaData()
    md.reflect(
        bind=engine,
        only=[
            "catalog_product_entity",
            "catalog_category_entity",
            "catalog_category_product",
            "eav_attribute",
            "catalog_product_entity_varchar",
            "catalog_product_entity_int",
            "catalog_product_entity_decimal",
            "catalog_product_entity_text",
            "catalog_product_entity_datetime",
        ],
    )
    return md


def skip_unless_db_reachable(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        pytest.skip(f"Magento database not reachable: {e}")


@pytest.fixture(autouse=False)
def require_db(engine):
    skip_unless_db_reachable(engine)
