import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Singleton class to manage database connection parameters"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Load environment variables from .env file
        load_dotenv()
        
        # Database configuration
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = int(os.getenv('DB_PORT', '3306'))
        self.db_name = os.getenv('DB_NAME', 'magento')
        self.db_user = os.getenv('DB_USER', 'magento')
        self.db_password = os.getenv('DB_PASSWORD', 'magento')
        self.db_charset = os.getenv('DB_CHARSET', 'utf8mb4')
        self._is_enterprise = None
        self._entity_id_column = None  # Will be 'entity_id' or 'row_id' based on edition
        
        self._initialized = True
    
    def get_connection_string(self):
        """Get SQLAlchemy connection string"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}"
    
    def is_enterprise_edition(self, engine=None):
        """Check if the Magento installation is Enterprise Edition.
        
        Only checks the MAGENTO_EDITION environment variable.
        Must be set to either 'enterprise'/'ee' or 'community'/'ce'.
        """
        if self._is_enterprise is not None:
            return self._is_enterprise
            
        # Check the environment variable
        edition = os.getenv('MAGENTO_EDITION', '').lower()
        if edition in ('enterprise', 'ee'):
            self._is_enterprise = True
            self._entity_id_column = 'row_id'
            logger.info("Magento Edition: Enterprise (from MAGENTO_EDITION)")
        elif edition in ('community', 'ce'):
            self._is_enterprise = False
            self._entity_id_column = 'entity_id'
            logger.info("Magento Edition: Community (from MAGENTO_EDITION)")
        else:
            raise ValueError(
                "MAGENTO_EDITION must be set to either 'enterprise'/'ee' or 'community'/'ce'. "
                f"Current value: {edition or 'not set'}"
            )
            
        return self._is_enterprise
    
    def get_entity_id_column(self):
        """Get the correct entity ID column name based on Magento edition"""
        if self._entity_id_column is None:
            self.is_enterprise_edition()  # This will set _entity_id_column
        return self._entity_id_column
    
    def test_connection(self, engine=None):
        """Test database connection and detect Magento edition"""
        from sqlalchemy import text, create_engine
        
        # Create engine if not provided
        if engine is None:
            engine = create_engine(self.get_connection_string())
        
        try:
            with engine.connect() as conn:
                # Test basic connection
                result = conn.execute(text("SELECT 1"))
                if result.scalar() != 1:
                    return False
                
                # This will detect and cache the edition if not already done
                self.is_enterprise_edition(engine)
                
                return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            return False

# Create a singleton instance of DatabaseConnection
db_connection = DatabaseConnection()
