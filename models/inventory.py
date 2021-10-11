# coding: utf-8
from sqlalchemy import Column, DECIMAL, Float, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_inventory_geoname = Table(
    'inventory_geoname', metadata,
    Column('country_code', String(64), nullable=False),
    Column('postcode', String(64), nullable=False),
    Column('city', String(180), nullable=False),
    Column('region', String(100), nullable=False),
    Column('province', String(64), nullable=False),
    Column('latitude', Float(asdecimal=True), nullable=False),
    Column('longitude', Float(asdecimal=True), nullable=False)
)


class InventoryLowStockNotificationConfiguration(Base):
    __tablename__ = 'inventory_low_stock_notification_configuration'

    source_code = Column(String(255), primary_key=True, nullable=False)
    sku = Column(String(64), primary_key=True, nullable=False)
    notify_stock_qty = Column(DECIMAL(12, 4))


class InventoryReservation(Base):
    __tablename__ = 'inventory_reservation'
    __table_args__ = (
        Index('INVENTORY_RESERVATION_STOCK_ID_SKU_QUANTITY', 'stock_id', 'sku', 'quantity'),
    )

    reservation_id = Column(INTEGER(10), primary_key=True)
    stock_id = Column(INTEGER(10), nullable=False)
    sku = Column(String(64), nullable=False)
    quantity = Column(DECIMAL(10, 4), nullable=False, server_default=text("0.0000"))
    metadata_ = Column('metadata', String(255))


class InventoryShipmentSource(Base):
    __tablename__ = 'inventory_shipment_source'

    shipment_id = Column(INTEGER(10), primary_key=True)
    source_code = Column(String(255), nullable=False)


class InventorySource(Base):
    __tablename__ = 'inventory_source'

    source_code = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    enabled = Column(SMALLINT(5), nullable=False, server_default=text("1"))
    description = Column(Text)
    latitude = Column(DECIMAL(8, 6))
    longitude = Column(DECIMAL(9, 6))
    country_id = Column(String(2), nullable=False)
    region_id = Column(INTEGER(10))
    region = Column(String(255))
    city = Column(String(255))
    street = Column(String(255))
    postcode = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    fax = Column(String(255))
    use_default_carrier_config = Column(SMALLINT(5), nullable=False, server_default=text("1"))


class InventoryStock(Base):
    __tablename__ = 'inventory_stock'

    stock_id = Column(INTEGER(10), primary_key=True)
    name = Column(String(255), nullable=False)


class InventorySourceCarrierLink(Base):
    __tablename__ = 'inventory_source_carrier_link'

    link_id = Column(INTEGER(10), primary_key=True)
    source_code = Column(ForeignKey('inventory_source.source_code', ondelete='CASCADE'), nullable=False, index=True)
    carrier_code = Column(String(255), nullable=False)
    position = Column(SMALLINT(5))

    inventory_source = relationship('InventorySource')


class InventorySourceItem(Base):
    __tablename__ = 'inventory_source_item'
    __table_args__ = (
        Index('INVENTORY_SOURCE_ITEM_SKU_SOURCE_CODE_QUANTITY', 'sku', 'source_code', 'quantity'),
        Index('INVENTORY_SOURCE_ITEM_SOURCE_CODE_SKU', 'source_code', 'sku', unique=True)
    )

    source_item_id = Column(INTEGER(10), primary_key=True)
    source_code = Column(ForeignKey('inventory_source.source_code', ondelete='CASCADE'), nullable=False)
    sku = Column(String(64), nullable=False)
    quantity = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"))
    status = Column(SMALLINT(5), nullable=False, server_default=text("0"))

    inventory_source = relationship('InventorySource')


class InventorySourceStockLink(Base):
    __tablename__ = 'inventory_source_stock_link'
    __table_args__ = (
        Index('INVENTORY_SOURCE_STOCK_LINK_STOCK_ID_SOURCE_CODE', 'stock_id', 'source_code', unique=True),
        Index('INVENTORY_SOURCE_STOCK_LINK_STOCK_ID_PRIORITY', 'stock_id', 'priority')
    )

    link_id = Column(INTEGER(10), primary_key=True)
    stock_id = Column(ForeignKey('inventory_stock.stock_id', ondelete='CASCADE'), nullable=False)
    source_code = Column(ForeignKey('inventory_source.source_code', ondelete='CASCADE'), nullable=False, index=True)
    priority = Column(SMALLINT(5), nullable=False)

    inventory_source = relationship('InventorySource')
    stock = relationship('InventoryStock')


class InventoryStockSalesChannel(Base):
    __tablename__ = 'inventory_stock_sales_channel'

    type = Column(String(64), primary_key=True, nullable=False)
    code = Column(String(64), primary_key=True, nullable=False)
    stock_id = Column(ForeignKey('inventory_stock.stock_id', ondelete='CASCADE'), nullable=False, index=True)

    stock = relationship('InventoryStock')
