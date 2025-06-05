# Import base classes first
from .base import Base, metadata, EntityIdMixin, check_enterprise

# Initialize database connection
engine = None
Session = None

def init_db(connection_string):
    """
    Initialize the database connection and configure models based on the Magento edition.
    
    Args:
        connection_string (str): SQLAlchemy connection string
        
    Returns:
        tuple: (engine, Session) SQLAlchemy engine and session factory
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, configure_mappers
    
    global engine, Session
    
    # Create engine
    engine = create_engine(connection_string)
    
    # Check if we're using enterprise edition
    is_enterprise = check_enterprise(engine)
    
    # Set the enterprise edition flag on the EntityIdMixin
    from .base import EntityIdMixin
    EntityIdMixin._is_enterprise_edition = is_enterprise
    
    # Configure all mappers to ensure relationships are set up correctly
    configure_mappers()
    
    # Create session factory
    Session = sessionmaker(bind=engine)
    
    return engine, Session

# Import all model modules
#from .admin import *
#from .adobe import *
#from .amazon import *
#from .authorization import *
#from .cache import *
#from .captcha import *
#from .catalog import *
#from .checkout import *
#from .cms import *
#from .core import *
#from .cron import *

#from .customer import *
#from .design import *
#from .directory import *
#from .downloadable import *
#from .eav import *
#from .email import *
#from .flag import *
#from .gift import *
#from .googleoptimizer import *
#from .indexer import *
#from .integration import *
#from .inventory import *
#from .klarna import *
#from .layout import *
#from .magento import *
#from .media import *
#from .msp import *
#from .mview import *
#from .newsletter import *
#from .oauth import *
#from .password import *
#from .patch import *
#from .paypal import *
#from .persistent import *
#from .product import *
#from .queue import *
#from .quote import *
#from .rating import *
#from .release import *
#from .report import *
#from .review import *
#from .sales import *
#from .scconnector import *
#from .search import *
#from .sendfriend import *
#from .sequence import *
#from .session import *
#from .setup import *
#from .shipping import *
#from .signifyd import *
#from .sitemap import *
#from .store import *
#from .tax import *
#from .theme import *
#from .translation import *
#from .ui import *
#from .url import *
#from .variable import *
#from .vault import *
#from .vertex import *
#from .weee import *
#from .widget import *
#from .wishlist import *
#from .yotpo import *
