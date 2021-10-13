# PyGento
Python module to work with Magneto Database directly without using broken Magento 2 core

<img src="https://github.com/Genaker/PyGento/blob/main/PyGento.PNG?raw=true" alt="PyGento" width="600"/>

PyGento is built on top of the SQL Alchemy

SQLAlchemy is a library that facilitates the communication between Python programs and Magento databases. This library  acts as an Object Relational Mapper (ORM) tool that translates Python classes to Magento tables and automatically converts function calls to SQL statements. 

SQLAlchemy allow developers to create and ship enterprise-grade, production-ready Magento 2 applications easily and lets developers focus on business logic.

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

# Models Structure 

Python abstaraction over magento database has multiple Models per file vs Magento one file per Class 

Python is not exclusively class-based - the natural unit of code decomposition in Python is the module. Modules are just as likely to contain functions (which are first-class objects in Python) as classes. In PHP Magento, the unit of decomposition is the class. PyGento hes several models per file. each model represent DB table. One PyGento model file contains all the classes for e-Commerce function (Catalog, Sales, Customer, Quote, Inventory).

Python is much more expressive than Magento, and if you restrict yourself to one class per file (which Python does not prevent you from doing) you will end up with lots of very small files - more to keep track of with very little benefit.

# Database Connection 

```
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:******@127.0.0.1/magento2')
engine.connect()
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
Acording the performace test PyGento returns 1-20 order data in 1ms when Magento requires 200+ ms
Return 100 product with all data: Execution Time 0.07084512710571289 seconds in the debug mode and 0.05914497375488281 seconds in production mode
Array Generate and Json Execution Time 0.008681297302246094 seconds

# Debug 
```
engine = create_engine('mysql+pymysql://root:******@127.0.0.1/magento2', echo=True)
```
if True, the Engine will log all statements as well as a repr() of their parameter lists to the default log handler, which defaults to sys.stdout for output. If set to the string "debug", result rows will be printed to the standard output as well.
