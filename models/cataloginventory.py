# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CatalogProductEntity(Base):
    __tablename__ = 'catalog_product_entity'
    __table_args__ = {'comment': 'Catalog Product Table'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    attribute_set_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Attribute Set ID')
    type_id = Column(String(32), nullable=False, server_default=text("'simple'"), comment='Type ID')
    sku = Column(String(64), index=True, comment='SKU')
    has_options = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Has Options')
    required_options = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Required Options')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Creation Time')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Update Time')


class CataloginventoryStock(Base):
    __tablename__ = 'cataloginventory_stock'
    __table_args__ = {'comment': 'Cataloginventory Stock'}

    stock_id = Column(SMALLINT(5), primary_key=True, comment='Stock ID')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')
    stock_name = Column(String(255), comment='Stock Name')


class CataloginventoryStockStatu(Base):
    __tablename__ = 'cataloginventory_stock_status'
    __table_args__ = {'comment': 'Cataloginventory Stock Status'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, index=True, comment='Stock Status')


class CataloginventoryStockStatusIdx(Base):
    __tablename__ = 'cataloginventory_stock_status_idx'
    __table_args__ = {'comment': 'Cataloginventory Stock Status Indexer Idx'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, comment='Stock Status')


class CataloginventoryStockStatusReplica(Base):
    __tablename__ = 'cataloginventory_stock_status_replica'
    __table_args__ = {'comment': 'Cataloginventory Stock Status'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, index=True, comment='Stock Status')


class CataloginventoryStockStatusTmp(Base):
    __tablename__ = 'cataloginventory_stock_status_tmp'
    __table_args__ = {'comment': 'Cataloginventory Stock Status Indexer Tmp'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, comment='Stock Status')


class CataloginventoryStockItem(Base):
    __tablename__ = 'cataloginventory_stock_item'
    __table_args__ = (
        Index('CATALOGINVENTORY_STOCK_ITEM_PRODUCT_ID_STOCK_ID', 'product_id', 'stock_id', unique=True),
        {'comment': 'Cataloginventory Stock Item'}
    )

    item_id = Column(INTEGER(10), primary_key=True, comment='Item ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product ID')
    stock_id = Column(ForeignKey('cataloginventory_stock.stock_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Stock ID')
    qty = Column(DECIMAL(12, 4), comment='Qty')
    min_qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Min Qty')
    use_config_min_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Min Qty')
    is_qty_decimal = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Qty Decimal')
    backorders = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Backorders')
    use_config_backorders = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Backorders')
    min_sale_qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("1.0000"), comment='Min Sale Qty')
    use_config_min_sale_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Min Sale Qty')
    max_sale_qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Max Sale Qty')
    use_config_max_sale_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Max Sale Qty')
    is_in_stock = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is In Stock')
    low_stock_date = Column(TIMESTAMP, comment='Low Stock Date')
    notify_stock_qty = Column(DECIMAL(12, 4), comment='Notify Stock Qty')
    use_config_notify_stock_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Notify Stock Qty')
    manage_stock = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Manage Stock')
    use_config_manage_stock = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Manage Stock')
    stock_status_changed_auto = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Stock Status Changed Automatically')
    use_config_qty_increments = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Qty Increments')
    qty_increments = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty Increments')
    use_config_enable_qty_inc = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Enable Qty Increments')
    enable_qty_increments = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Enable Qty Increments')
    is_decimal_divided = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Divided into Multiple Boxes for Shipping')
    website_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Website ID')

    product = relationship('CatalogProductEntity')
    stock = relationship('CataloginventoryStock')
