#!/usr/bin/env python3
"""
PyGento Test CLI - Command Line Interface for testing database operations
"""
import time
import argparse
import logging
from pprint import pprint
from typing import Dict, List, Any

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.dialects import mysql
# Enable SQLAlchemy logging to stdout
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from models import init_db, Session as DBSession, Base, metadata
from models.admin import AdminUser
from models.catalog import CatalogProductEntity as Product, EavAttribute
from utils.database import DatabaseConnection


class TestCli:
    """Command Line Interface for testing PyGento database operations"""
    
    def __init__(self):
        """Initialize the CLI with database connection"""
        self.db_conn = DatabaseConnection()
        self.engine, self.Session = init_db(self.db_conn.get_connection_string())
        self.session = self.Session()
        
    def test_connection(self) -> bool:
        """Test the database connection"""
        print("Testing database connection...")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                connected = result.scalar() == 1
                status = "✓" if connected else "✗"
                print(f"{status} Connection successful" if connected else f"{status} Connection failed")
                return connected
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def list_admins(self, limit: int = 5) -> None:
        """List admin users"""
        print(f"\nListing first {limit} admin users:")
        print("-" * 80)
        
        try:
            admins = self.session.query(AdminUser).limit(limit).all()
            for i, admin in enumerate(admins, 1):
                print(f"{i}. {admin.firstname} {admin.lastname} ({admin.username})")
                print(f"   Email: {admin.email}")
                print(f"   Created: {admin.created}")
                print("-" * 80)
        except Exception as e:
            print(f"Error fetching admin users: {e}")
    
    def list_products(self, limit: int = 5, with_attributes: bool = False, store_id: int = None) -> None:
        """List products with optional attributes"""
        print(f"\nListing first {limit} products:")
        print("=" * 80)
        
        total_start = time.perf_counter()
        
        try:
            step_start = time.perf_counter()
            query = self.session.query(Product)
            # Eager load attributes if requested
            attribute_code_map = {}
            if with_attributes:
                # Load all attribute IDs and codes before fetching products
                try:
                    from models.eav import EavAttribute
                    attr_load_start = time.perf_counter()
                    attribute_code_map = {a.attribute_id: a.attribute_code for a in self.session.query(EavAttribute).all()}
                    attr_load_end = time.perf_counter()
                    print(f"[DEBUG] Attribute code loading took {attr_load_end - attr_load_start:.4f} seconds")
                except Exception as e:
                    print(f"Warning: Could not load attribute codes: {e}")
                # No eager loading for dynamic attribute relationships (varchar, int, text, decimal, datetime, gallery)
# Only load attribute codes eagerly above; attribute values are accessed via dynamic relationships per product.
            
            query_build_end = time.perf_counter()
            print(f"[DEBUG] Query build took {query_build_end - step_start:.4f} seconds")
            step_start = time.perf_counter()
            final_query = query.limit(limit)
            products = final_query.all()
            query_exec_end = time.perf_counter()
            print(f"[DEBUG] Product query execution took {query_exec_end - step_start:.4f} seconds")
            
            for i, product in enumerate(products, 1):
                prod_start = time.perf_counter()
                print(f"{i}. SKU: {product.sku}")
                print(f"   ID: {product.entity_id}, Type: {product.type_id}")
                print(f"   Created: {product.created_at}, Updated: {product.updated_at}")
                
                # Initialize attributes dict for this product
                if not hasattr(product, 'attributes'):
                    product.attributes = {}
                
                # Show attribute count if loaded
                if with_attributes:
                    for attr_type in ['varchar', 'int', 'text', 'decimal', 'datetime', 'gallery']:
                        attr_type_start = time.perf_counter()
                        if hasattr(product, attr_type) and getattr(product, attr_type) is not None:
                            if attr_type != 'gallery':
                                sid = store_id if store_id is not None else 0
                                attr_query = getattr(product, attr_type).filter_by(store_id=sid)
                                compiled_sql = attr_query.statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
                                print(f"[DEBUG SQL] {compiled_sql}")
                                attr_list = attr_query.all()
                            else:
                                attr_list = list(getattr(product, attr_type))
                            setattr(product, f'{attr_type}_attributes', attr_list)
                            attr_type_end = time.perf_counter()
                            print(f"[DEBUG] {attr_type} attribute loading for product {product.entity_id} took {attr_type_end - attr_type_start:.4f} seconds")
                            if isinstance(attr_list, list):
                                print(f"   {attr_type.capitalize()} attributes: {len(attr_list)}")
                                # Print first few attribute values as example
                                for attr in attr_list[:3]:  # Show first 3 attributes of each type
                                    try:
                                        attr_id = getattr(attr, 'attribute_id', None)
                                        attr_code = attribute_code_map.get(attr_id) if attr_id is not None else None
                                        value = getattr(attr, 'value', 'N/A')
                                        if isinstance(value, str):
                                            if len(value) > 30:
                                                value = value[:30] + '...'
                                            else:
                                                value = value[:30]
                                        print(f"     - {attr_code if attr_code else attr_id}: {value}")
                                        if attr_code:
                                            product.attributes[attr_code] = value
                                    except:
                                        pass
                                    if len(attr_list) > 3:
                                        print(f"     ... and {len(attr_list) - 3} more")
                
                print("-" * 80)
                prod_end = time.perf_counter()
                print(f"[DEBUG] Product {product.entity_id} total attribute loading took {prod_end - prod_start:.4f} seconds")
            
            total_end = time.perf_counter()
            if products:
                print("\n[DEBUG] First product object:")
                import pprint
                pprint.pprint(vars(products[0]))
            print(f"\nFetched {len(products)} products in {total_end - total_start:.2f} seconds")
            
        except Exception as e:
            print(f"Error fetching products: {e}")
    
    def get_table_info(self) -> None:
        """Show database table information"""
        print("\nDatabase Tables Information:")
        print("=" * 80)
        
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            print(f"Total tables: {len(tables)}")
            print("\nSample tables (first 10):")
            for i, table in enumerate(tables[:10], 1):
                print(f"  {i}. {table}")
            
            if len(tables) > 10:
                print(f"  ... and {len(tables) - 10} more tables")
                
        except Exception as e:
            print(f"Error getting table information: {e}")


def main():
    """Main entry point for the test CLI"""
    parser = argparse.ArgumentParser(description='PyGento Test CLI')
    
    # Add command line arguments
    parser.add_argument('--test-connection', action='store_true', 
                       help='Test database connection')
    
    parser.add_argument('--list-admins', type=int, nargs='?', const=5, metavar='LIMIT',
                       help='List admin users (default: 5)')
    
    parser.add_argument('-p', '--list-products', type=int, nargs='?', const=5, metavar='LIMIT',
                       help='List products (default: 5)')
    
    parser.add_argument('-a', '--with-attributes', action='store_true',
                       help='Include attribute data with products (use with --list-products)')
    
    parser.add_argument('--tables', action='store_true',
                       help='Show database tables information')

    parser.add_argument('-s', '--store-id', type=int, nargs='?', const=0, default=None, help='Filter product attributes by store_id (default 0 if no value)')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    try:
        cli = TestCli()
        
        if args.test_connection:
            cli.test_connection()
            
        if args.list_admins is not None:
            cli.list_admins(limit=args.list_admins)
            
        if args.list_products is not None:
            cli.list_products(limit=args.list_products, with_attributes=args.with_attributes, store_id=args.store_id)
            
        if args.tables:
            cli.get_table_info()
            
    except Exception as e:
        print(f"Error: {e}")
        print(e.__traceback__)


if __name__ == "__main__":
    main()
