# coding: utf-8
from sqlalchemy import Column, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class VertexCustomOptionFlexField(Base):
    __tablename__ = 'vertex_custom_option_flex_field'
    __table_args__ = (
        Index('VERTEX_CUSTOM_OPTION_FLEX_FIELD_OPTION_ID_WEBSITE_ID', 'option_id', 'website_id', unique=True),
        {'comment': 'Customizable Option to Flex Field Map'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Map Entity ID')
    option_id = Column(INTEGER(10), nullable=False, comment='Customizable Option ID')
    website_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Website ID')
    flex_field = Column(Text, comment='Flexible Field ID')


class VertexCustomerCode(Base):
    __tablename__ = 'vertex_customer_code'
    __table_args__ = {'comment': 'vertex_customer_code'}

    customer_id = Column(INTEGER(10), primary_key=True, comment='Customer ID')
    customer_code = Column(Text, comment='Customer Code for Vertex')


class VertexInvoiceSent(Base):
    __tablename__ = 'vertex_invoice_sent'
    __table_args__ = {'comment': 'vertex_invoice_sent'}

    invoice_id = Column(INTEGER(10), primary_key=True, comment='Invoice ID')
    sent_to_vertex = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Invoice has been logged in Vertex')


class VertexOrderInvoiceStatu(Base):
    __tablename__ = 'vertex_order_invoice_status'
    __table_args__ = {'comment': 'vertex_order_invoice_status'}

    order_id = Column(INTEGER(10), primary_key=True, comment='Order ID')
    sent_to_vertex = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Invoice has been logged in Vertex')


t_vertex_sales_creditmemo_item_invoice_text_code = Table(
    'vertex_sales_creditmemo_item_invoice_text_code', metadata,
    Column('item_id', INTEGER(10), nullable=False, comment='Creditmemo Item ID'),
    Column('invoice_text_code', String(100), nullable=False, comment='Invoice text code from Vertex'),
    Index('UNQ_4BC40DA748D7713ADA661D2DE1BCF161', 'item_id', 'invoice_text_code', unique=True),
    comment='vertex_sales_creditmemo_item_invoice_text_code'
)


t_vertex_sales_creditmemo_item_tax_code = Table(
    'vertex_sales_creditmemo_item_tax_code', metadata,
    Column('item_id', INTEGER(10), nullable=False, comment='Creditmemo Item ID'),
    Column('tax_code', String(100), nullable=False, comment='Invoice text code from Vertex'),
    Index('VERTEX_SALES_CREDITMEMO_ITEM_TAX_CODE_ITEM_ID_TAX_CODE', 'item_id', 'tax_code', unique=True),
    comment='vertex_sales_creditmemo_item_tax_code'
)


t_vertex_sales_creditmemo_item_vertex_tax_code = Table(
    'vertex_sales_creditmemo_item_vertex_tax_code', metadata,
    Column('item_id', INTEGER(10), nullable=False, comment='Creditmemo Item ID'),
    Column('vertex_tax_code', String(100), nullable=False, comment='Text code from Vertex'),
    Index('UNQ_31D7AADB3412BC7E7C1C98D5CC3A5D46', 'item_id', 'vertex_tax_code', unique=True),
    comment='vertex_sales_creditmemo_item_vertex_tax_code'
)


t_vertex_sales_order_item_invoice_text_code = Table(
    'vertex_sales_order_item_invoice_text_code', metadata,
    Column('item_id', INTEGER(10), nullable=False, comment='Order Item ID'),
    Column('invoice_text_code', String(100), nullable=False, comment='Invoice text code from Vertex'),
    Index('UNQ_96F6BE3160A4185CEA4D866018EAF6DC', 'item_id', 'invoice_text_code', unique=True),
    comment='vertex_sales_order_item_invoice_text_code'
)


t_vertex_sales_order_item_tax_code = Table(
    'vertex_sales_order_item_tax_code', metadata,
    Column('item_id', INTEGER(10), nullable=False, comment='Order Item ID'),
    Column('tax_code', String(100), nullable=False, comment='Invoice text code from Vertex'),
    Index('VERTEX_SALES_ORDER_ITEM_TAX_CODE_ITEM_ID_TAX_CODE', 'item_id', 'tax_code', unique=True),
    comment='vertex_sales_order_item_tax_code'
)


t_vertex_sales_order_item_vertex_tax_code = Table(
    'vertex_sales_order_item_vertex_tax_code', metadata,
    Column('item_id', INTEGER(10), nullable=False, comment='Order Item ID'),
    Column('vertex_tax_code', String(100), nullable=False, comment='Text code from Vertex'),
    Index('VERTEX_SALES_ORDER_ITEM_VERTEX_TAX_CODE_ITEM_ID_VERTEX_TAX_CODE', 'item_id', 'vertex_tax_code', unique=True),
    comment='vertex_sales_order_item_vertex_tax_code'
)


class VertexTaxrequest(Base):
    __tablename__ = 'vertex_taxrequest'
    __table_args__ = {'comment': 'Log of requests to Vertex'}

    request_id = Column(BIGINT(20), primary_key=True, unique=True)
    request_type = Column(String(255), nullable=False, index=True, comment='Request Type')
    response_time = Column(INTEGER(10), comment='Milliseconds taken for Vertex API call to complete')
    quote_id = Column(BIGINT(20))
    order_id = Column(BIGINT(20), index=True)
    total_tax = Column(String(255), nullable=False, comment='Total Tax Amount')
    source_path = Column(String(255), nullable=False, comment='Source path controller_module_action')
    tax_area_id = Column(String(255), nullable=False, comment='Tax Jurisdictions Id')
    sub_total = Column(String(255), nullable=False, comment='Response Subtotal Amount')
    total = Column(String(255), nullable=False, comment='Response Total Amount')
    lookup_result = Column(String(255), nullable=False, comment='Tax Area Response Lookup Result')
    request_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Request create date')
    request_xml = Column(Text, nullable=False, comment='Request XML')
    response_xml = Column(Text, nullable=False, comment='Response XML')
