# PyGento
Python module to work with Magneto Database directly without using broken Magento 2 core

<img src="https://github.com/Genaker/PyGento/blob/main/PyGento.PNG?raw=true" alt="PyGento" width="250"/>

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

# Performace
Acording the performace test PyGento returns 1-20 order data in 1ms when Magento requires 200+ ms
