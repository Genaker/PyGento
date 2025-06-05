#!/usr/bin/env python3
"""
Test script to verify database connection and model setup.
"""
import os
import sys
import logging
from sqlalchemy import inspect

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main test function"""
    try:
        # Initialize database connection
        from utils.database import DatabaseConnection
        from models import init_db, check_enterprise, Base, metadata
        
        # Get database connection string
        db_conn = DatabaseConnection()
        connection_string = db_conn.get_connection_string()
        logger.info(f"Connecting to database: {connection_string.split('@')[-1]}")
        
        # Initialize database and get session
        logger.info("Initializing database connection...")
        engine, Session = init_db(connection_string)
        
        # Test the connection
        logger.info("Testing database connection...")
        if not db_conn.test_connection(engine):
            logger.error("Failed to connect to the database")
            return 1
            
        logger.info("Successfully connected to the database")
        
        # Check if we're using enterprise edition
        logger.info("Checking Magento edition...")
        try:
            is_enterprise = check_enterprise(engine)
            logger.info(f"Magento Enterprise Edition: {is_enterprise}")
        except Exception as e:
            logger.error(f"Error checking Magento edition: {e}", exc_info=True)
            return 1
        
        # Inspect the database
        logger.info("Inspecting database...")
        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"Found {len(tables)} tables in the database")
            
            # Show first 10 tables
            if tables:
                logger.info(f"Sample tables: {', '.join(tables[:10])}...")
            else:
                logger.warning("No tables found in the database")
        except Exception as e:
            logger.error(f"Error inspecting database: {e}", exc_info=True)
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
