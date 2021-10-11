# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Catalogrule(Base):
    __tablename__ = 'catalogrule'
    __table_args__ = (
        Index('CATALOGRULE_IS_ACTIVE_SORT_ORDER_TO_DATE_FROM_DATE', 'is_active', 'sort_order', 'to_date', 'from_date'),
        {'comment': 'CatalogRule'}
    )

    rule_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    name = Column(String(255), comment='Name')
    description = Column(Text, comment='Description')
    from_date = Column(Date, comment='From')
    to_date = Column(Date, comment='To')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Active')
    conditions_serialized = Column(MEDIUMTEXT, comment='Conditions Serialized')
    actions_serialized = Column(MEDIUMTEXT, comment='Actions Serialized')
    stop_rules_processing = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Stop Rules Processing')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    simple_action = Column(String(32), comment='Simple Action')
    discount_amount = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Discount Amount')

    websites = relationship('StoreWebsite', secondary='catalogrule_website')


class CatalogruleGroupWebsite(Base):
    __tablename__ = 'catalogrule_group_website'
    __table_args__ = {'comment': 'CatalogRule Group Website'}

    rule_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Rule ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Website ID')


class CatalogruleGroupWebsiteReplica(Base):
    __tablename__ = 'catalogrule_group_website_replica'
    __table_args__ = {'comment': 'CatalogRule Group Website'}

    rule_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Rule ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Website ID')


class CatalogruleProduct(Base):
    __tablename__ = 'catalogrule_product'
    __table_args__ = (
        Index('UNQ_EAA51B56FF092A0DCB795D1CEF812B7B', 'rule_id', 'from_time', 'to_time', 'website_id', 'customer_group_id', 'product_id', 'sort_order', unique=True),
        {'comment': 'CatalogRule Product'}
    )

    rule_product_id = Column(INTEGER(10), primary_key=True, comment='Rule Product ID')
    rule_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Rule ID')
    from_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='From Time')
    to_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='To time')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    action_operator = Column(String(10), server_default=text("'to_fixed'"), comment='Action Operator')
    action_amount = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Action Amount')
    action_stop = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Action Stop')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')


class CatalogruleProductPrice(Base):
    __tablename__ = 'catalogrule_product_price'
    __table_args__ = (
        Index('CATRULE_PRD_PRICE_RULE_DATE_WS_ID_CSTR_GROUP_ID_PRD_ID', 'rule_date', 'website_id', 'customer_group_id', 'product_id', unique=True),
        {'comment': 'CatalogRule Product Price'}
    )

    rule_product_price_id = Column(INTEGER(10), primary_key=True, comment='Rule Product PriceId')
    rule_date = Column(Date, nullable=False, comment='Rule Date')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    rule_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Rule Price')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')
    latest_start_date = Column(Date, comment='Latest StartDate')
    earliest_end_date = Column(Date, comment='Earliest EndDate')


class CatalogruleProductPriceReplica(Base):
    __tablename__ = 'catalogrule_product_price_replica'
    __table_args__ = (
        Index('CATRULE_PRD_PRICE_RULE_DATE_WS_ID_CSTR_GROUP_ID_PRD_ID', 'rule_date', 'website_id', 'customer_group_id', 'product_id', unique=True),
        {'comment': 'CatalogRule Product Price'}
    )

    rule_product_price_id = Column(INTEGER(10), primary_key=True, comment='Rule Product PriceId')
    rule_date = Column(Date, nullable=False, comment='Rule Date')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    rule_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Rule Price')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')
    latest_start_date = Column(Date, comment='Latest StartDate')
    earliest_end_date = Column(Date, comment='Earliest EndDate')


class CatalogruleProductReplica(Base):
    __tablename__ = 'catalogrule_product_replica'
    __table_args__ = (
        Index('UNQ_EAA51B56FF092A0DCB795D1CEF812B7B', 'rule_id', 'from_time', 'to_time', 'website_id', 'customer_group_id', 'product_id', 'sort_order', unique=True),
        {'comment': 'CatalogRule Product'}
    )

    rule_product_id = Column(INTEGER(10), primary_key=True, comment='Rule Product ID')
    rule_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Rule ID')
    from_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='From Time')
    to_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='To time')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    action_operator = Column(String(10), server_default=text("'to_fixed'"), comment='Action Operator')
    action_amount = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Action Amount')
    action_stop = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Action Stop')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')


class CustomerGroup(Base):
    __tablename__ = 'customer_group'
    __table_args__ = {'comment': 'Customer Group'}

    customer_group_id = Column(INTEGER(10), primary_key=True)
    customer_group_code = Column(String(32), nullable=False, comment='Customer Group Code')
    tax_class_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Tax Class ID')

    rules = relationship('Catalogrule', secondary='catalogrule_customer_group')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


t_catalogrule_customer_group = Table(
    'catalogrule_customer_group', metadata,
    Column('rule_id', ForeignKey('catalogrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID'),
    Column('customer_group_id', ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer Group ID'),
    comment='Catalog Rules To Customer Groups Relations'
)


t_catalogrule_website = Table(
    'catalogrule_website', metadata,
    Column('rule_id', ForeignKey('catalogrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID'),
    Column('website_id', ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID'),
    comment='Catalog Rules To Websites Relations'
)
