from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index, Table, event, and_
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship, backref, configure_mappers, mapper
from sqlalchemy.sql.expression import text
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()
metadata = Base.metadata

class EntityIdMixin:
    """Mixin class that handles the dynamic entity_id/row_id column for Magento entities.
    
    This mixin automatically handles the differences between Community and Enterprise editions
    by dynamically creating the appropriate column name ('entity_id' or 'row_id').
    It also provides common functionality for attribute backend tables.
    """
    
    @classmethod
    def _get_entity_id_column_name(cls):
        """Get the correct entity ID column name based on Magento edition"""
        from utils.database import db_connection
        try:
            return db_connection.get_entity_id_column()
        except Exception as e:
            # Fallback to 'entity_id' if there's any error getting the column name
            logger.warning(f"Error getting entity_id column name, falling back to 'entity_id': {e}")
            return 'entity_id'
    
    @declared_attr
    def entity_id(cls):
        """Dynamically create the entity_id/row_id column based on Magento edition"""
        column_name = cls._get_entity_id_column_name()
        is_enterprise = column_name == 'row_id'
        
        logger.info(f"Creating {column_name} column for {cls.__name__}")
        
        # For the catalog_product_entity table itself
        if hasattr(cls, '__tablename__') and cls.__tablename__ == 'catalog_product_entity':
            logger.debug(f"Creating primary key column for {cls.__name__}")
            return Column(
                column_name,
                Integer,
                primary_key=True,
                autoincrement=True,
                comment='Entity ID' if not is_enterprise else 'Row ID'
            )
        
        # For attribute backend tables
        if hasattr(cls, '__tablename__') and 'catalog_product_entity_' in cls.__tablename__:
            logger.debug(f"Creating foreign key column for {cls.__name__}")
            col = Column(
                column_name,
                Integer,
                ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'),
                nullable=False,
                index=True,
                server_default=text("0"),
                comment='Entity ID' if not is_enterprise else 'Row ID'
            )
            logger.debug(f"Created column: {col}")
            return col
        
        # For other tables that reference catalog_product_entity
        if hasattr(cls, '__table__') and any(col.foreign_keys for col in cls.__table__.columns):
            for column in cls.__table__.columns:
                if column.foreign_keys and any('catalog_product_entity' in str(fk.column) for fk in column.foreign_keys):
                    logger.debug(f"Creating foreign key column for {cls.__name__} (referencing catalog_product_entity)")
                    col = Column(
                        column_name,
                        Integer,
                        ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'),
                        nullable=False,
                        index=True,
                        server_default=text("0"),
                        comment='Entity ID' if not is_enterprise else 'Row ID'
                    )
                    logger.debug(f"Created column: {col}")
                    return col
        
        # Default case for other tables that need an entity_id
        logger.debug(f"Creating default column for {cls.__name__}")
        col = Column(
            column_name,
            Integer,
            primary_key=not is_enterprise,
            autoincrement=not is_enterprise,
            nullable=False,
            comment='Entity ID' if not is_enterprise else 'Row ID'
        )
        logger.debug(f"Created default column: {col}")
        return col
    
    @declared_attr
    def __table_args__(cls):
        """Dynamically create table arguments including the appropriate index for attribute tables"""
        # Only apply to attribute backend tables
        if not hasattr(cls, '__tablename__') or 'catalog_product_entity_' not in cls.__tablename__:
            return None
            
        # Get the correct column name based on Magento edition
        column_name = cls._get_entity_id_column_name()
        
        # Create the index with the correct column name
        return (
            Index(
                f'IDX_{cls.__tablename__.upper()}_{column_name.upper()}_ATTR_STORE',
                column_name,
                'attribute_id',
                'store_id',
                unique=True
            ),
            {'comment': f'{cls.__name__} Table'}
        )
    
    @declared_attr
    def attribute(cls):
        """Standard relationship to EavAttribute for attribute backend tables"""
        if not hasattr(cls, '__tablename__') or 'catalog_product_entity_' not in cls.__tablename__:
            return None
        return relationship('EavAttribute')
    
    @declared_attr
    def store(cls):
        """Standard relationship to Store for attribute backend tables"""
        if not hasattr(cls, '__tablename__') or 'catalog_product_entity_' not in cls.__tablename__:
            return None
        return relationship('Store')
    
    @declared_attr
    def entity(cls):
        """Standard relationship to CatalogProductEntity for attribute backend tables"""
        if not hasattr(cls, '__tablename__') or 'catalog_product_entity_' not in cls.__tablename__:
            return None
            
        from models.catalog import CatalogProductEntity
        
        # Get the correct column name based on Magento edition
        column_name = cls._get_entity_id_column_name()
        
        # Create a lambda that will be evaluated at runtime to get the correct column
        return relationship(
            "CatalogProductEntity",
            primaryjoin=f"and_({cls.__name__}.{column_name}==CatalogProductEntity.entity_id, {cls.__name__}.store_id==0)",
            foreign_keys=f"[{cls.__name__}.{column_name}]",
            viewonly=True
        )


def check_enterprise(engine=None):
    """Check if we're using the enterprise edition"""
    from utils.database import db_connection
    return db_connection.is_enterprise_edition(engine)
