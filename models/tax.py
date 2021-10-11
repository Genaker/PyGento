# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, Float, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class TaxCalculationRate(Base):
    __tablename__ = 'tax_calculation_rate'
    __table_args__ = (
        Index('IDX_CA799F1E2CB843495F601E56C84A626D', 'tax_calculation_rate_id', 'tax_country_id', 'tax_region_id', 'zip_is_range', 'tax_postcode'),
        Index('TAX_CALCULATION_RATE_TAX_COUNTRY_ID_TAX_REGION_ID_TAX_POSTCODE', 'tax_country_id', 'tax_region_id', 'tax_postcode'),
        {'comment': 'Tax Calculation Rate'}
    )

    tax_calculation_rate_id = Column(INTEGER(11), primary_key=True, comment='Tax Calculation Rate ID')
    tax_country_id = Column(String(2), nullable=False, comment='Tax Country ID')
    tax_region_id = Column(INTEGER(11), nullable=False, comment='Tax Region ID')
    tax_postcode = Column(String(21), comment='Tax Postcode')
    code = Column(String(255), nullable=False, index=True, comment='Code')
    rate = Column(DECIMAL(12, 4), nullable=False, comment='Rate')
    zip_is_range = Column(SMALLINT(6), comment='Zip Is Range')
    zip_from = Column(INTEGER(10), comment='Zip From')
    zip_to = Column(INTEGER(10), comment='Zip To')


class TaxCalculationRule(Base):
    __tablename__ = 'tax_calculation_rule'
    __table_args__ = (
        Index('TAX_CALCULATION_RULE_PRIORITY_POSITION', 'priority', 'position'),
        {'comment': 'Tax Calculation Rule'}
    )

    tax_calculation_rule_id = Column(INTEGER(11), primary_key=True, comment='Tax Calculation Rule ID')
    code = Column(String(255), nullable=False, index=True, comment='Code')
    priority = Column(INTEGER(11), nullable=False, comment='Priority')
    position = Column(INTEGER(11), nullable=False, comment='Position')
    calculate_subtotal = Column(INTEGER(11), nullable=False, comment='Calculate off subtotal option')


class TaxClas(Base):
    __tablename__ = 'tax_class'
    __table_args__ = {'comment': 'Tax Class'}

    class_id = Column(SMALLINT(6), primary_key=True, comment='Class ID')
    class_name = Column(String(255), nullable=False, comment='Class Name')
    class_type = Column(String(8), nullable=False, server_default=text("'CUSTOMER'"), comment='Class Type')


class StoreGroup(Base):
    __tablename__ = 'store_group'
    __table_args__ = {'comment': 'Store Groups'}

    group_id = Column(SMALLINT(5), primary_key=True, comment='Group ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    name = Column(String(255), nullable=False, comment='Store Group Name')
    root_category_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Root Category ID')
    default_store_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Store ID')
    code = Column(String(32), unique=True, comment='Store group unique code')

    website = relationship('StoreWebsite')


class TaxCalculation(Base):
    __tablename__ = 'tax_calculation'
    __table_args__ = (
        Index('TAX_CALC_TAX_CALC_RATE_ID_CSTR_TAX_CLASS_ID_PRD_TAX_CLASS_ID', 'tax_calculation_rate_id', 'customer_tax_class_id', 'product_tax_class_id'),
        {'comment': 'Tax Calculation'}
    )

    tax_calculation_id = Column(INTEGER(11), primary_key=True, comment='Tax Calculation ID')
    tax_calculation_rate_id = Column(ForeignKey('tax_calculation_rate.tax_calculation_rate_id', ondelete='CASCADE'), nullable=False, comment='Tax Calculation Rate ID')
    tax_calculation_rule_id = Column(ForeignKey('tax_calculation_rule.tax_calculation_rule_id', ondelete='CASCADE'), nullable=False, index=True, comment='Tax Calculation Rule ID')
    customer_tax_class_id = Column(ForeignKey('tax_class.class_id', ondelete='CASCADE'), nullable=False, index=True, comment='Customer Tax Class ID')
    product_tax_class_id = Column(ForeignKey('tax_class.class_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product Tax Class ID')

    customer_tax_class = relationship('TaxClas', primaryjoin='TaxCalculation.customer_tax_class_id == TaxClas.class_id')
    product_tax_class = relationship('TaxClas', primaryjoin='TaxCalculation.product_tax_class_id == TaxClas.class_id')
    tax_calculation_rate = relationship('TaxCalculationRate')
    tax_calculation_rule = relationship('TaxCalculationRule')


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        Index('STORE_IS_ACTIVE_SORT_ORDER', 'is_active', 'sort_order'),
        {'comment': 'Stores'}
    )

    store_id = Column(SMALLINT(5), primary_key=True, comment='Store ID')
    code = Column(String(32), unique=True, comment='Code')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    group_id = Column(ForeignKey('store_group.group_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Group ID')
    name = Column(String(255), nullable=False, comment='Store Name')
    sort_order = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store Sort Order')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store Activity')

    group = relationship('StoreGroup')
    website = relationship('StoreWebsite')


class TaxCalculationRateTitle(Base):
    __tablename__ = 'tax_calculation_rate_title'
    __table_args__ = (
        Index('TAX_CALCULATION_RATE_TITLE_TAX_CALCULATION_RATE_ID_STORE_ID', 'tax_calculation_rate_id', 'store_id'),
        {'comment': 'Tax Calculation Rate Title'}
    )

    tax_calculation_rate_title_id = Column(INTEGER(11), primary_key=True, comment='Tax Calculation Rate Title ID')
    tax_calculation_rate_id = Column(ForeignKey('tax_calculation_rate.tax_calculation_rate_id', ondelete='CASCADE'), nullable=False, comment='Tax Calculation Rate ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, comment='Store ID')
    value = Column(String(255), nullable=False, comment='Value')

    store = relationship('Store')
    tax_calculation_rate = relationship('TaxCalculationRate')


class TaxOrderAggregatedCreated(Base):
    __tablename__ = 'tax_order_aggregated_created'
    __table_args__ = (
        Index('TAX_ORDER_AGGRED_CREATED_PERIOD_STORE_ID_CODE_PERCENT_ORDER_STS', 'period', 'store_id', 'code', 'percent', 'order_status', unique=True),
        {'comment': 'Tax Order Aggregation'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    code = Column(String(255), nullable=False, comment='Code')
    order_status = Column(String(50), nullable=False, comment='Order Status')
    percent = Column(Float, comment='Percent')
    orders_count = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Orders Count')
    tax_base_amount_sum = Column(Float, comment='Tax Base Amount Sum')

    store = relationship('Store')


class TaxOrderAggregatedUpdated(Base):
    __tablename__ = 'tax_order_aggregated_updated'
    __table_args__ = (
        Index('TAX_ORDER_AGGRED_UPDATED_PERIOD_STORE_ID_CODE_PERCENT_ORDER_STS', 'period', 'store_id', 'code', 'percent', 'order_status', unique=True),
        {'comment': 'Tax Order Aggregated Updated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    code = Column(String(255), nullable=False, comment='Code')
    order_status = Column(String(50), nullable=False, comment='Order Status')
    percent = Column(Float, comment='Percent')
    orders_count = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Orders Count')
    tax_base_amount_sum = Column(Float, comment='Tax Base Amount Sum')

    store = relationship('Store')
