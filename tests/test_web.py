"""Feature tests for the FastAPI storefront (app.py) against the real
Magento database."""
import os
import sys

from fastapi.testclient import TestClient
from sqlalchemy import func, select

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.conftest import skip_unless_db_reachable  # noqa: E402


def _client(engine):
    skip_unless_db_reachable(engine)
    import app as app_module

    return TestClient(app_module.app)


def test_home_page_renders_with_catalog_stats(engine):
    client = _client(engine)
    response = client.get("/")
    assert response.status_code == 200
    assert "Products" in response.text
    assert "Categories" in response.text


def test_known_category_renders_a_product_grid(engine, metadata):
    client = _client(engine)
    category_product = metadata.tables["catalog_category_product"]
    with engine.connect() as conn:
        category_id = conn.execute(
            select(category_product.c.category_id)
            .group_by(category_product.c.category_id)
            .order_by(func.count().desc())
            .limit(1)
        ).scalar()
    if category_id is None:
        import pytest

        pytest.skip("No category has any products assigned in this database.")

    response = client.get(f"/category/{category_id}")
    assert response.status_code == 200


def test_unknown_category_is_404(engine):
    client = _client(engine)
    response = client.get("/category/999999999")
    assert response.status_code == 404


def test_non_numeric_category_id_is_422(engine):
    # FastAPI's path-param type coercion rejects non-int values with a 422
    # before the handler even runs -- not a 404 (that's only for a
    # well-formed but nonexistent id), and not a 500.
    client = _client(engine)
    response = client.get("/category/not-a-number")
    assert response.status_code == 422


def test_known_product_renders_its_details(engine, metadata):
    client = _client(engine)
    product_table = metadata.tables["catalog_product_entity"]
    with engine.connect() as conn:
        row = conn.execute(select(product_table.c.entity_id, product_table.c.sku).order_by(product_table.c.entity_id)).first()
    if row is None:
        import pytest

        pytest.skip("No products exist in this database.")

    response = client.get(f"/product/{row.entity_id}")
    assert response.status_code == 200
    assert row.sku in response.text


def test_unknown_product_is_404(engine):
    client = _client(engine)
    response = client.get("/product/999999999")
    assert response.status_code == 404
