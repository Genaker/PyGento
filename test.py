from models.admin import *
from models.catalog import CatalogProductEntity as Product
from models.catalog import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import lazyload, joinedload,selectinload, aliased
import http.server
from pprint import pprint
import time
import json

engine = create_engine('mysql+pymysql://root:asdfDFhdjtDFGeq4rwrc3IOcvxb4xbfsdf@127.0.0.1/magento2')#, echo=True, echo_pool='debug')
engine.connect()
Session = sessionmaker(bind=engine)
db = Session()

admins = db.query(AdminUser).all()
#products = db.query(Product).options(selectinload("varchar"), selectinload(Product.intager), selectinload(Product.text), selectinload(Product.decimal), selectinload(Product.datetime), selectinload(Product.gallery)).filter(Product.sku != "Test001").limit(1).all()

#productNew = Product(
#    sku = "Test001"
#)

#db.add(productNew)
#db.commit()
#exit()

start_time = time.time()
products = db.query(Product).options(selectinload("varchar"), selectinload(Product.intager), selectinload(Product.text), selectinload(Product.decimal), selectinload(Product.datetime), selectinload(Product.gallery)).filter(Product.sku != "Test001").limit(100).all()
#products = db.query(Product).filter(Product.sku != "Test001").limit(100).all()

##for pr in products:
#pprint(products)

#exit();

print("Execution Time %s seconds" % str(time.time() - start_time))

start_time = time.time()
all_attributes =  db.query(EavAttribute).all();
print("Execution Time %s seconds" % str(time.time() - start_time))

attributes_ids = {}
for a in all_attributes:
    ##pprint(a.__dict__)
    attributes_ids[a.__dict__['attribute_id']] = a.__dict__['attribute_code']

def transpondAttributes(products, attributes=['varchar','intager','datetime','text','decimal', 'gallery', 'wrong_key']):
    result = {}
    n = 1;
    product_id = 0;
    for product in products:
        product_id = product.__dict__['entity_id']
        result[product_id] = {"attributes":[], "gallery":[]}
        for atype in attributes:
            #print(atype)
            if atype in product.__dict__:
                for attr in product.__dict__[atype]:
                    del attr.__dict__['_sa_instance_state']
                    attribute_id = attr.__dict__["attribute_id"]
                    attribute_code = attributes_ids[attribute_id]
                    if atype == "gallery":
                        ## Gallery has only one type of attributes "media_gallery"
                        result[product_id]["gallery"].append(attr.__dict__)
                    else:
                        attr.__dict__["attribute_code"] = attribute_code
                        result[product_id]["attributes"].append({attribute_code: attr.__dict__ })
                            
                    ##print("-->",var.__dict__)
                del product.__dict__[atype]
        del product.__dict__["_sa_instance_state"]
        result[product_id].update({"product":product.__dict__}) 
    return result

start_time = time.time()
products=[]
p = transpondAttributes(products);
j = json.dumps(p, default=str)
##print(j)
print("Transpond Execution Time %s seconds" % str(time.time() - start_time))

print(len(p))

#pprint(p)

for product in products:
    pprint(product.__dict__)


pprint(admins)

def print_admin_list(admins):
    result = []
    for admin in admins:
        print("Admin User:")
        pprint (admin.__dict__)
        print ("Admin Name:", admin.firstname) 
        print ("Admin Created:", admin.created)

print_admin_list(admins)

for product in products:
    print ("Products:", product.__dict__) 
    print ("Product SKU:", product.sku) 

#db.add(admin)
#db.commit()

class Handler(http.server.SimpleHTTPRequestHandler):
        # A new Handler is created for every incommming request tho do_XYZ
        # methods correspond to different HTTP methods.

        def do_GET(self) :
                #print(self)
                start_time_req = time.time()
                print('-----------------------')
                print("Start Time: " + str(start_time_req))
                print('GET %s (from client %s)' % (self.path, self.client_address))
                #print(self.headers)
                
                admins = db.query(AdminUser).all()
               
                body = str("");
                for admin in admins:
                    print("Admin User:")
                    pprint (admin.__dict__)
                    print ("Admin Name:", admin.firstname) 
                    print ("Admin Created:", admin.created)
                    body += str(admin.__dict__)
                
                start_time = time.time()
                products = db.query(Product).options(selectinload(Product.varchar), selectinload(Product.intager), selectinload(Product.text), selectinload(Product.decimal), selectinload(Product.datetime), selectinload(Product.gallery)).filter(Product.sku != "Test001").limit(1000).all()
                print("Selects Execution Time %s seconds" % str(time.time() - start_time))
                
                start_time = time.time()
                p = transpondAttributes(products) 
                print("Transpond Execution Time %s seconds" % str(time.time() - start_time))

                start_time = time.time()
                jsonD = json.dumps(p, default=str)
                print("Json Execution Time %s seconds" % str(time.time() - start_time))
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>Magento Data Provided by Python</title></head><body>" + jsonD + "</body></html>","utf-8"))

                print("Request Execution Time %s seconds" % str(time.time() - start_time_req))
                #self.wfile.close()
                
s = http.server.HTTPServer( ('', 8080), Handler )
s.serve_forever()
