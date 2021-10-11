from models.admin import *
from models.catalog import CatalogProductEntity as Product
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import http.server
from pprint import pprint
import time

engine = create_engine('mysql+pymysql://root:******@127.0.0.1/magento2')
engine.connect()
Session = sessionmaker(bind=engine)
db = Session()

admins = db.query(AdminUser).all()

productNew = Product(
    sku = "Test001"
)

db.add(productNew)
db.commit()

products = db.query(Product).all()

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

db.add(admin)
db.commit()

# Test Simple Server 
class Handler(http.server.SimpleHTTPRequestHandler):
        # A new Handler is created for every incommming request tho do_XYZ
        # methods correspond to different HTTP methods.
        
        def do_GET(self) :
                #print(self)
                start_time = time.time()
                print('-----------------------')
                print("Start Time: " + str(start_time))
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
                    
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>Title goes here.</title></head><body>" + body + "</body></html>","utf-8"))
                print("Execution Time %s seconds" % str(time.time() - start_time))
                
s = http.server.HTTPServer( ('', 8080), Handler )
s.serve_forever()
