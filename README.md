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

3. Configure your database connection by creating a `.env` file:
   ```ini
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=magento
   DB_USER=magento
   DB_PASSWORD=magento
   DB_CHARSET=utf8mb4
   ```

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

Run the test script to verify your setup:

```bash
python test_db.py
```

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
