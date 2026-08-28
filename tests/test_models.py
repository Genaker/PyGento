"""
Sanity coverage for models/catalog.py against a real Magento database, and
regression tests for the bugs found and fixed in it: hardcoded 'row_id'
literals that broke Community Edition (entity_id-keyed) installs even
though this file has an explicit CE/EE toggle (MAGENTO_EDITION) meant to
handle exactly this. This project runs with MAGENTO_EDITION=community
(see .env.example) since the target database is CE, not EE -- these tests
would have caught every one of those bugs before they reached anyone
actually running this against a CE install.
"""
import os
import sys

import pytest
from sqlalchemy import select
from sqlalchemy.orm import configure_mappers

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.conftest import skip_unless_db_reachable  # noqa: E402


def test_catalog_module_imports_without_error():
    # This alone would have caught the three hardcoded Index/Column
    # 'row_id' literals: SQLAlchemy raises KeyError at class-definition
    # time when an Index references a column name that doesn't exist on
    # the table -- and in community mode, the real column is 'entity_id'.
    import models.catalog  # noqa: F401


def test_mappers_configure_without_error():
    # Would have caught the CatalogProductEntity.text/intager relationship
    # bug: both branches of an if/else meant to pick 'row_id' vs
    # 'entity_id' hardcoded 'row_id' in the community-edition branch too,
    # which only surfaces as an AttributeError when SQLAlchemy actually
    # tries to resolve every pending relationship.
    import models.catalog  # noqa: F401

    configure_mappers()


def test_community_edition_uses_entity_id_column(engine, metadata):
    skip_unless_db_reachable(engine)
    import models.catalog as catalog
    from utils.database import db_connection

    assert db_connection.get_entity_id_column() == "entity_id", (
        "these tests assume MAGENTO_EDITION=community (see .env.example); "
        "the real target database has no row_id column"
    )

    # A KeyError/AttributeError here would mean the dynamic entity_id/row_id
    # column mapping broke again -- this is deliberately a live query
    # against the real column, not just a class-attribute check, so it
    # exercises the same path a real request would. Not raising is the
    # entire assertion.
    with engine.connect() as conn:
        conn.execute(select(catalog.CatalogProductEntityVarchar.__table__.c.entity_id).limit(1)).first()


def test_product_text_and_int_relationships_use_entity_id_in_community_mode(engine, metadata):
    """Direct regression test for the exact copy-paste bug: both branches
    of CatalogProductEntity.text/.intager hardcoded 'row_id', so accessing
    product.text or product.intager against a CE database raised
    AttributeError instead of resolving the relationship."""
    skip_unless_db_reachable(engine)
    import models.catalog as catalog
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    session = Session()

    product = session.query(catalog.CatalogProductEntity).first()
    if product is None:
        pytest.skip("No products in this database.")

    # Must not raise -- these two both had the bug (varchar/decimal/datetime
    # never did, only text and intager).
    list(product.text)
    list(product.intager)

    session.close()


def test_every_model_module_is_importable():
    """The pre-existing library has 77 model files; this doesn't assert
    correctness of each one's schema mapping (that would need a live query
    per file), but it does prove none of them has a class-definition-time
    error like the ones found in catalog.py."""
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    failures = []
    for filename in sorted(os.listdir(models_dir)):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue
        module_name = f"models.{filename[:-3]}"
        try:
            __import__(module_name)
        except Exception as e:  # noqa: BLE001 -- intentionally broad, this is an audit
            failures.append(f"{module_name}: {type(e).__name__}: {e}")

    assert not failures, "some model modules failed to import:\n" + "\n".join(failures)
