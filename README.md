# PyGento

## FastAPI HTTP API Usage

PyGento provides a FastAPI-based HTTP API for product and attribute queries (see `test_fastapi.py`).

### Installation: Fixing `bash: uvicorn: command not found`

If you see this error when starting the server:

```
bash: uvicorn: command not found
```

You need to install `uvicorn`:

```bash
pip install uvicorn
```

Or, if you use Python 3:

```bash
pip3 install uvicorn
```

### Running the FastAPI Server (Development)

Start the server with:

```bash
uvicorn test_fastapi:app --reload
```

- The `--reload` flag enables auto-reload on code changes (development only).
- By default, the server runs on `http://127.0.0.1:8000`.

### Accessing the API

Visit:
- [http://127.0.0.1:8000/products](http://127.0.0.1:8000/products) for product listing
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive Swagger UI

#### Example Query:
```
curl 'http://127.0.0.1:8000/products?limit=1&with_attributes=true&store_id=0'
```

---

## FastAPI Production Settings

For production deployments:

- **Never use `--reload` in production.**
- Use a process manager (e.g., `systemd`, `supervisord`, or Docker).
- Run with multiple workers for concurrency:

```bash
uvicorn test_fastapi:app --host 0.0.0.0 --port 8000 --workers 4
```

- Consider using a reverse proxy (e.g., Nginx) in front of Uvicorn for SSL, compression, and security.
- Set environment variables for DB and app secrets securely.
- Monitor logs and set up error reporting for production stability.

See [FastAPI deployment docs](https://fastapi.tiangolo.com/deployment/) for more details.
Python module to work with Magento Database directly without using the Magento 2 core

<img src="https://github.com/Genaker/PyGento/blob/main/PyGento.PNG?raw=true" alt="PyGento" width="600"/>

PyGento is built on top of SQLAlchemy, providing a clean, Pythonic interface to Magento's database.

## Features

- **Unified Interface**: Works with both Magento Community and Enterprise editions
- **Type Annotations**: Full type hints for better IDE support and code reliability
- **Modern Python**: Built with Python 3.8+ and SQLAlchemy 1.4+
- **Enterprise Support**: Handles the differences between Community and Enterprise editions transparently

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PyGento.git
   cd PyGento
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your database connection by copying `.env.example` to `.env`
   and pointing it at a real Magento 2 database:
   ```ini
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=magento
   DB_USER=magento
   DB_PASSWORD=magento
   DB_CHARSET=utf8mb4
   MAGENTO_EDITION=community
   ```
   `.env` itself is gitignored -- it used to be committed with real-looking
   (if only ever locally-used) credentials in it, which is exactly the
   kind of thing `.gitignore` exists to prevent regardless of whether the
   specific values were ever actually sensitive.

## Magmi-Style Bulk Import

```bash
python import_products.py path/to/products.csv --batch-size 500
```

`import_products.py`: the same shape (and the same fix) as every other
importer in this benchmark family (GoGento, gogento-rust, laragento) --
parse a CSV, resolve SKUs, bulk-insert new entities (relying on
MySQL/InnoDB's consecutive-auto-increment-lock guarantee for a multi-row
insert), bucket attribute values by EAV backend_type, and batch-upsert
each of the 5 `catalog_product_entity_*` value tables via SQLAlchemy's
MySQL-dialect `insert().on_duplicate_key_update()` -- one explicit
transaction per table, never a per-row ORM model save.

**Benchmark** (`/usr/bin/time -l`, same 1000-row/13-attribute CSV
gogento-rust's own Go-vs-Rust benchmark uses, same real Magento database
laragento's and the plain-PDO/Magento-bootstrap PHP scripts in
gogento-rust's `bench/` run against):

| | Import time | Max RSS |
|---|---|---|
| PHP, plain PDO + Magento bootstrap (no ORM) | 2.90s | 35.2 MB |
| Laravel, Eloquent `upsert()` | ~4.4s | 50.5 MB |
| **PyGento, SQLAlchemy Core `upsert`** | **~4.5s** | **42.4 MB** |
| PHP, Magento's own `Model::save()` per row | 120.6s | 66.7 MB |

Properly batched (unlike `Model::save()`), so it avoids that 41x-scale
penalty almost entirely, and lands within noise of Laravel's Eloquent
`upsert()` on the identical statement shape against the identical
database (three back-to-back runs of each: 4.29s/4.55s median, ~6% apart)
-- checked directly, not assumed: a `general_log` capture of the actual
SQL confirmed `insert(table).values(chunk).on_duplicate_key_update(...)`
compiles to one genuine multi-row `INSERT ... ON DUPLICATE KEY UPDATE`
per chunk, not N separate statements, so there was no batching bug to
find. An *earlier* version of this number (8.68s) was a measurement
artifact, not a real result -- it compared runs from separate sessions
against a shared, actively-used database whose load varies a lot run to
run; left as a note in gogento-rust's README as a reminder that only
back-to-back, same-session runs are actually comparable on a shared DB.
See the top-level `gogento-rust` repo's README for the full
Go/Rust/PHP/Laravel/Python comparison this benchmark is part of.

## Storefront

```bash
uvicorn app:app --reload
```

`app.py`: a small FastAPI app with the same three routes the Go, Rust, and
Laravel reimplementations in this benchmark family each have --
`/` (catalog stats), `/category/{id}` (paginated product grid), and
`/product/{id}` (detail page with breadcrumbs) -- rendered via Jinja2
templates in `templates/`. Backed by `utils/eav.py`, a small "flatten this
entity's EAV attributes into a dict" helper with a batch-first API
(`flatten_products()` fetches N entities in one query per value table,
not one query per table *per* entity) -- written batch-first deliberately,
after the sibling laragento project's `CategoryController` was found to
have exactly that N+1 bug in its per-product `flattenProduct()` loop; see
"Bugs Found and Fixed" below for what was actually wrong in *this*
codebase.

This is a separate, real entrypoint from `test_fastapi.py` (an earlier
ad-hoc JSON-API + demo script despite the filename, not this project's
storefront).

## Quick Start

```python
from models import init_db, Session
from utils.database import DatabaseConnection

# Initialize database connection
db_conn = DatabaseConnection()
engine, Session = init_db(db_conn.get_connection_string())

# Create a session
session = Session()

# Example query (once models are defined)
# products = session.query(CatalogProductEntity).limit(10).all()
# for product in products:
#     print(product.sku)

# Close the session
session.close()
```

## Testing

```bash
pip install -r requirements.txt   # includes pytest and httpx now
pytest
```

17 tests in `tests/`, against the real database, skipping gracefully
(`pytest.skip`, not a failure) if it isn't reachable -- the same
convention GoGento's, gogento-rust's, and laragento's own DB-touching
tests use, since there's no disposable schema here to spin up in CI.
Coverage: the storefront's three routes (happy path, 404s, a 422 for a
malformed path param), the import command's create/reimport/failure
paths, `utils/eav.py`'s batching, and `tests/test_models.py`, which is
specifically regression coverage for the bugs below -- every one of them
would have been caught by these tests before they ever reached a real
Community Edition install.

`test.py`, `test_cli.py`, `test_db.py`, and `test_fastapi.py` at the repo
root predate this suite and aren't pytest tests despite the name --
they're ad-hoc scripts you run directly with `python <name>.py` to poke
at the database or the old JSON API by hand. Left as-is; `tests/` is the
real, automated suite.

## Bugs Found and Fixed

- **`.env` was committed to git.** Removed from tracking, added a real
  `.gitignore`, and a committed `.env.example` with the same placeholder
  values takes its place. The values themselves were only ever local
  defaults (`magento`/`magento`), but tracking `.env` at all is exactly
  the habit that leaks real credentials the day someone reuses this
  pattern with a real password.
- **Three hardcoded `'row_id'` literals in `models/catalog.py` broke
  Community Edition entirely.** This file has a real, working
  `MAGENTO_EDITION` toggle (`_prd_entity_col`/`_cat_entity_col`,
  resolved per-column via `locals()[...]`) meant to switch every
  attribute-table's entity column between `entity_id` (CE) and `row_id`
  (EE) -- but three places short-circuited it: the top-level
  `catalog_product_entity_media_gallery_value_to_entity` table (both its
  `Column` and its `Index` hardcoded `'row_id'`), and the `Index`
  definitions on `CatalogProductEntityGallery` and
  `CatalogProductEntityMediaGalleryValue`. Importing `models.catalog` at
  all raised `KeyError: 'row_id'` under `MAGENTO_EDITION=community`,
  against a real CE database where that column is named `entity_id`.
- **A copy-paste bug in `CatalogProductEntity.text` and `.intager`.**
  Both properties branch on `is_enterprise` to pick the right join column
  for their relationship to `CatalogProductEntityText`/`Int` -- but in
  both properties, the `else` (Community) branch was copy-pasted from the
  `if` (Enterprise) branch and still said `row_id` instead of `entity_id`.
  Every other attribute-table relationship on the same class (`varchar`,
  `decimal`, `datetime`) has the correct `else` branch; only these two
  didn't. Surfaced as `AttributeError: ... does not have a mapped column
  named 'row_id'` the moment SQLAlchemy tried to configure the mapper --
  not at import time, which is presumably why it went unnoticed.

None of these are found in `models/eav.py`, `models/store.py`, etc.
directly -- `models/catalog.py` keeps its own self-contained copies of
`EavAttribute` and `Store` rather than importing them (each of this
project's 77 model files creates its own independent
`declarative_base()`, so cross-file `relationship("ClassName")` string
lookups wouldn't resolve; every file is written to be self-sufficient
instead). That's an unusual choice worth knowing about if you ever add a
model that needs to reference a class defined in a different file, but it
isn't itself a bug -- `test_every_model_module_is_importable` in
`tests/test_models.py` confirms all 77 files still load cleanly on their
own.

## Models

PyGento organizes models by functionality, with each module containing related models:

- `models/catalog.py`: Product and category models
- `models/sales.py`: Order and invoice models
- `models/customer.py`: Customer and address models
- `models/checkout.py`: Cart and quote models

## License

MIT

# Models Structure 

Python abstraction over magento database has multiple Models per file vs Magento one file per Class 

Python is not exclusively class-based - the natural unit of code decomposition in Python is the module. Modules are just as likely to contain functions (which are first-class objects in Python) as classes. In PHP Magento, the unit of decomposition is the class. PyGento hes several models per file. each model represent DB table. One PyGento model file contains all the classes for e-Commerce function (Catalog, Sales, Customer, Quote, Inventory).

Python is much more expressive than Magento, and if you restrict yourself to one class per file (which Python does not prevent you from doing) you will end up with lots of very small files - more to keep track of with very little benefit.

# Database Connection 

```
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:******@127.0.0.1/magento2')
engine.connect()
```

To make it simple, we configure it to JSON and use it, and read config.json or YML from the original config

```
php -r '$x = include("app/etc/env.php"); echo json_encode($x);' > config.json
```

# Load Magento Model 

```
from models.catalog import CatalogProductEntity as Product

products = db.query(Product).all()

for product in products:
    print ("Product:", product.__dict__) 
    print ("Product Sku:", product.sku) 
```
## Magento/Adobe Commerce edition PyGento(Pythone) Support 
If you have any issues or requires Magento Enterprise (Adobe Commerce/MSI) Version package, please, create a ticket or drop me email at: yegorshytikov@gmail.com

# Tables relations 

## Many To One
Many to one places a foreign key in the parent table referencing the child. relationship() is declared on the parent, where a new scalar-holding attribute will be created:
```
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
```
Bidirectional behavior is achieved by adding a second relationship() and applying the relationship.back_populates parameter in both directions:

```
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", back_populates="parents")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parents = relationship("Parent", back_populates="child")
```
Alternatively, the relationship.backref parameter may be applied to a single relationship(), such as Parent.child:
```
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref="parents")
```

## Selectin Relations Load
The most useful loader in modern SQLAlchemy is the selectinload() loader option. This option solves the most common form of the “N plus one” problem which is that of a set of objects that refer to related collections. selectinload() will ensure that a particular collection for a full series of objects are loaded up front using a single query. It does this using a SELECT form that in most cases can be emitted against the related table alone, without the introduction of JOINs or subqueries, and only queries for those parent objects for which the collection isn’t already loaded. Below we illustrate selectinload() by loading all of the User objects and all of their related Address objects; while we invoke Session.execute() only once, given a select() construct, when the database is accessed, there are in fact two SELECT statements emitted, the second one being to fetch the related Address objects:

```
from sqlalchemy.orm import selectinload
stmt = (
  select(User).options(selectinload(User.addresses)).order_by(User.id)
```

# Async engine 
Initialize the new SQLAlchemy engine with create_async_engine() and create an async session maker by passing it the new AsyncSession class:
```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy"


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

# Performace
According to the performace test, PyGento returns 1-20 order data in 1ms when Magento requires 200+ ms
Return 100 products with all data: Execution Time 0.07084512710571289 seconds in the debug mode and 0.05914497375488281 seconds in production mode
Array Generate and Json Execution Time 0.008681297302246094 seconds
```
Select Execution Time 0.05763673782348633 seconds
Transponder Execution Time 0.0041141510009765625 seconds
Json Execution Time 0.004602909088134766 seconds
Request Execution Time 0.0689239501953125 seconds
```
for 10 product this results is:
```
Select Execution Time 0.013299703598022461 seconds
Transponder Execution Time 0.0005435943603515625 seconds
Json Execution Time 0.0006403923034667969 seconds
Request Execution Time 0.016859769821166992 seconds
```
For 1000 products result is: 
```
Select Execution Time 0.8228793144226074 seconds
Transponder Execution Time 0.049771785736083984 seconds
Json Execution Time 0.051209449768066406 seconds
Request Execution Time 0.9310669898986816 seconds
```

In the future, these results can be improved using Async SQL requests and proper NoSQL product indexer...

# Debug 
```
engine = create_engine('mysql+pymysql://root:******@127.0.0.1/magento2', echo=True)
```
If True, the Engine will log all statements and a repr() of their parameter lists to the default log handler, which defaults to sys.stdout for output. If set to the string "debug," result rows will also be printed to the standard output.

# "Introduction to SQLAlchemy 2020 (Tutorial)" by: Mike Bayer

https://www.youtube.com/watch?v=sO7FFPNvX2s

In this tutorial, we present a "from the ground up" tour of SQLAlchemy, what
the general idea of it is how it's organized and what it looks like to use
it.   This is the latest version of the "classic" SQLAlchemy tutorial  which
has been presented on many occasions since 2008, reworked for the current
recommended SQLAlchemy usage patterns with an emphasis on previewing the upcoming 1.4 and 2.0 releases of SQLAlchemy, which are poised to make major changes to many of SQLAlchemy's central paradigms and capabilities.
SQLAlchemy is presented in terms of a four-layered model, which include "Engine and Connection Basics", "Table Metadata", "SQL Expression Language", and "ORM Usage" which is broken into two sections and API use is presented in terms of a console runner application which participants can install locally and follow along.  The tutorial will also present some of the newest in-development features of SQLAlchemy 1.4 which have only just merged.
