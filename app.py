"""
PyGento storefront: a small FastAPI app rendering home/category/product
pages straight off a real Magento database via SQLAlchemy -- the same
three routes the Go, Rust, and Laravel reimplementations in this benchmark
family each have.

Deliberately separate from test_fastapi.py (an earlier ad-hoc JSON-API +
demo script, not this project's real storefront entrypoint).

Run with:
    uvicorn app:app --reload
"""
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import MetaData, create_engine, func, select

from utils import eav
from utils.database import db_connection

app = FastAPI(title="PyGento Storefront")
templates = Jinja2Templates(directory="templates")

engine = create_engine(db_connection.get_connection_string())
metadata = MetaData()
metadata.reflect(
    bind=engine,
    only=[
        "catalog_product_entity",
        "catalog_category_entity",
        "catalog_category_product",
        "eav_attribute",
        *eav.PRODUCT_VALUE_TABLES.values(),
        *eav.CATEGORY_VALUE_TABLES.values(),
    ],
)

PRODUCT_GRID_ATTRIBUTES = ["name", "price"]
PRODUCT_DETAIL_ATTRIBUTES = ["name", "description", "short_description", "price", "weight"]
CATEGORY_NAME_ATTRIBUTE = ["name"]

# Root categories every product implicitly belongs to that aren't
# meaningful storefront navigation on their own -- mirrors the same
# exclusion set the Go, Rust, and Laravel storefronts all hardcode for
# breadcrumbs.
BREADCRUMB_EXCLUDED_IDS = {1, 2}

PER_PAGE = 12


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    product_table = metadata.tables["catalog_product_entity"]
    category_table = metadata.tables["catalog_category_entity"]
    category_product_table = metadata.tables["catalog_category_product"]

    with engine.connect() as conn:
        product_count = conn.execute(select(func.count()).select_from(product_table)).scalar()
        category_count = conn.execute(select(func.count()).select_from(category_table)).scalar()
        featured_category_id = conn.execute(
            select(category_product_table.c.category_id)
            .group_by(category_product_table.c.category_id)
            .order_by(func.count().desc())
            .limit(1)
        ).scalar()

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "product_count": product_count,
            "category_count": category_count,
            "featured_category_id": featured_category_id,
        },
    )


@app.get("/category/{category_id}", response_class=HTMLResponse)
def category(request: Request, category_id: int, page: int = 1):
    category_table = metadata.tables["catalog_category_entity"]
    category_product_table = metadata.tables["catalog_category_product"]

    with engine.connect() as conn:
        exists = conn.execute(select(category_table.c.entity_id).where(category_table.c.entity_id == category_id)).first()
        if exists is None:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")

        category_attrs = eav.flatten_category(conn, metadata, category_id, CATEGORY_NAME_ATTRIBUTE)

        total_products = conn.execute(
            select(func.count()).select_from(category_product_table).where(category_product_table.c.category_id == category_id)
        ).scalar()
        total_pages = max(1, -(-total_products // PER_PAGE))  # ceil division
        page = min(total_pages, max(1, page))

        # Real DB-level LIMIT/OFFSET, not "pull every product_id in the
        # category into memory and slice it in Python" -- this is exactly
        # the N+1-adjacent bug laragento's CategoryController originally
        # had, avoided here from the start.
        page_ids = [
            row.product_id
            for row in conn.execute(
                select(category_product_table.c.product_id)
                .where(category_product_table.c.category_id == category_id)
                .order_by(category_product_table.c.position)
                .offset((page - 1) * PER_PAGE)
                .limit(PER_PAGE)
            )
        ]

        # One query per EAV value table for every product on this page,
        # not one query per table *per product*.
        attrs_by_product = eav.flatten_products(conn, metadata, page_ids, PRODUCT_GRID_ATTRIBUTES)

    products = [
        {
            "entity_id": product_id,
            "name": attrs_by_product.get(product_id, {}).get("name") or f"Product {product_id}",
            "price": attrs_by_product.get(product_id, {}).get("price"),
        }
        for product_id in page_ids
    ]

    return templates.TemplateResponse(
        request,
        "category.html",
        {
            "category_id": category_id,
            "category_name": category_attrs.get("name") or f"Category {category_id}",
            "products": products,
            "page": page,
            "total_pages": total_pages,
        },
    )


@app.get("/product/{product_id}", response_class=HTMLResponse)
def product(request: Request, product_id: int):
    product_table = metadata.tables["catalog_product_entity"]
    category_product_table = metadata.tables["catalog_category_product"]
    category_table = metadata.tables["catalog_category_entity"]

    with engine.connect() as conn:
        row = conn.execute(
            select(product_table.c.entity_id, product_table.c.sku).where(product_table.c.entity_id == product_id)
        ).first()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        attrs = eav.flatten_product(conn, metadata, product_id, PRODUCT_DETAIL_ATTRIBUTES)

        last_category_id = conn.execute(
            select(category_product_table.c.category_id)
            .where(category_product_table.c.product_id == product_id)
            .order_by(category_product_table.c.category_id.desc())
        ).scalar()

        breadcrumbs = []
        if last_category_id is not None:
            cat_row = conn.execute(
                select(category_table.c.path).where(category_table.c.entity_id == last_category_id)
            ).first()
            if cat_row is not None:
                ids = [
                    int(part)
                    for part in cat_row.path.split("/")
                    if part.isdigit() and int(part) not in BREADCRUMB_EXCLUDED_IDS
                ]
                for cat_id in ids:
                    cat_attrs = eav.flatten_category(conn, metadata, cat_id, CATEGORY_NAME_ATTRIBUTE)
                    breadcrumbs.append({"id": cat_id, "name": cat_attrs.get("name") or f"Category {cat_id}"})

    name: Optional[str] = attrs.get("name") or row.sku
    return templates.TemplateResponse(
        request,
        "product.html",
        {
            "entity_id": product_id,
            "sku": row.sku,
            "name": name,
            "description": attrs.get("description") or "",
            "short_description": attrs.get("short_description") or "",
            "price": attrs.get("price"),
            "weight": attrs.get("weight"),
            "breadcrumbs": breadcrumbs,
        },
    )
