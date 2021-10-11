# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ShippingTablerate(Base):
    __tablename__ = 'shipping_tablerate'
    __table_args__ = (
        Index('UNQ_D60821CDB2AFACEE1566CFC02D0D4CAA', 'website_id', 'dest_country_id', 'dest_region_id', 'dest_zip', 'condition_name', 'condition_value', unique=True),
        {'comment': 'Shipping Tablerate'}
    )

    pk = Column(INTEGER(10), primary_key=True, comment='Primary key')
    website_id = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Website ID')
    dest_country_id = Column(String(4), nullable=False, server_default=text("'0'"), comment='Destination coutry ISO/2 or ISO/3 code')
    dest_region_id = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Destination Region ID')
    dest_zip = Column(String(10), nullable=False, server_default=text("'*'"), comment='Destination Post Code (Zip)')
    condition_name = Column(String(30), nullable=False, comment='Rate Condition name')
    condition_value = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Rate condition value')
    price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Price')
    cost = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Cost')
