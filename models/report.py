# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, INTEGER, SMALLINT
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


class ReportEventType(Base):
    __tablename__ = 'report_event_types'
    __table_args__ = {'comment': 'Reports Event Type Table'}

    event_type_id = Column(SMALLINT(5), primary_key=True, comment='Event Type ID')
    event_name = Column(String(64), nullable=False, comment='Event Name')
    customer_login = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Customer Login')


class ReportingCount(Base):
    __tablename__ = 'reporting_counts'
    __table_args__ = {'comment': 'Reporting for all count related events generated via the cron job'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    type = Column(String(255), comment='Item Reported')
    count = Column(INTEGER(10), comment='Count Value')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')


class ReportingModuleStatu(Base):
    __tablename__ = 'reporting_module_status'
    __table_args__ = {'comment': 'Module Status Table'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Module ID')
    name = Column(String(255), comment='Module Name')
    active = Column(String(255), comment='Module Active Status')
    setup_version = Column(String(255), comment='Module Version')
    state = Column(String(255), comment='Module State')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')


class ReportingOrder(Base):
    __tablename__ = 'reporting_orders'
    __table_args__ = {'comment': 'Reporting for all orders'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    customer_id = Column(INTEGER(10), comment='Customer ID')
    total = Column(DECIMAL(20, 4))
    total_base = Column(DECIMAL(20, 4))
    item_count = Column(INTEGER(10), nullable=False, comment='Line Item Count')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Updated At')


class ReportingSystemUpdate(Base):
    __tablename__ = 'reporting_system_updates'
    __table_args__ = {'comment': 'Reporting for system updates'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    type = Column(String(255), comment='Update Type')
    action = Column(String(255), comment='Action Performed')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Updated At')


class ReportingUser(Base):
    __tablename__ = 'reporting_users'
    __table_args__ = {'comment': 'Reporting for user actions'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    type = Column(String(255), comment='User Type')
    action = Column(String(255), comment='Action Performed')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Updated At')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


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


class CustomerEntity(Base):
    __tablename__ = 'customer_entity'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_EMAIL_WEBSITE_ID', 'email', 'website_id', unique=True),
        {'comment': 'Customer Entity'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='SET NULL'), index=True, comment='Website ID')
    email = Column(String(255), comment='Email')
    group_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Group ID')
    increment_id = Column(String(50), comment='Increment ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, server_default=text("0"), comment='Store ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Active')
    disable_auto_group_change = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Disable automatic group change based on VAT ID')
    created_in = Column(String(255), comment='Created From')
    prefix = Column(String(40), comment='Name Prefix')
    firstname = Column(String(255), index=True, comment='First Name')
    middlename = Column(String(255), comment='Middle Name/Initial')
    lastname = Column(String(255), index=True, comment='Last Name')
    suffix = Column(String(40), comment='Name Suffix')
    dob = Column(Date, comment='Date of Birth')
    password_hash = Column(String(128), comment='Password_hash')
    rp_token = Column(String(128), comment='Reset password token')
    rp_token_created_at = Column(DateTime, comment='Reset password token creation time')
    default_billing = Column(INTEGER(10), comment='Default Billing Address')
    default_shipping = Column(INTEGER(10), comment='Default Shipping Address')
    taxvat = Column(String(50), comment='Tax/VAT Number')
    confirmation = Column(String(64), comment='Is Confirmed')
    gender = Column(SMALLINT(5), comment='Gender')
    failures_num = Column(SMALLINT(6), server_default=text("0"), comment='Failure Number')
    first_failure = Column(TIMESTAMP, comment='First Failure')
    lock_expires = Column(TIMESTAMP, comment='Lock Expiration Date')

    store = relationship('Store')
    website = relationship('StoreWebsite')


class ReportEvent(Base):
    __tablename__ = 'report_event'
    __table_args__ = {'comment': 'Reports Event Table'}

    event_id = Column(BIGINT(20), primary_key=True, comment='Event ID')
    logged_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Logged At')
    event_type_id = Column(ForeignKey('report_event_types.event_type_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Event Type ID')
    object_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Object ID')
    subject_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Subject ID')
    subtype = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Subtype')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, comment='Store ID')

    event_type = relationship('ReportEventType')
    store = relationship('Store')


class ReportViewedProductAggregatedDaily(Base):
    __tablename__ = 'report_viewed_product_aggregated_daily'
    __table_args__ = (
        Index('REPORT_VIEWED_PRD_AGGRED_DAILY_PERIOD_STORE_ID_PRD_ID', 'period', 'store_id', 'product_id', unique=True),
        {'comment': 'Most Viewed Products Aggregated Daily'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), index=True, comment='Product ID')
    product_name = Column(String(255), comment='Product Name')
    product_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Product Price')
    views_num = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Number of Views')
    rating_pos = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Pos')

    product = relationship('CatalogProductEntity')
    store = relationship('Store')


class ReportViewedProductAggregatedMonthly(Base):
    __tablename__ = 'report_viewed_product_aggregated_monthly'
    __table_args__ = (
        Index('REPORT_VIEWED_PRD_AGGRED_MONTHLY_PERIOD_STORE_ID_PRD_ID', 'period', 'store_id', 'product_id', unique=True),
        {'comment': 'Most Viewed Products Aggregated Monthly'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), index=True, comment='Product ID')
    product_name = Column(String(255), comment='Product Name')
    product_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Product Price')
    views_num = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Number of Views')
    rating_pos = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Pos')

    product = relationship('CatalogProductEntity')
    store = relationship('Store')


class ReportViewedProductAggregatedYearly(Base):
    __tablename__ = 'report_viewed_product_aggregated_yearly'
    __table_args__ = (
        Index('REPORT_VIEWED_PRD_AGGRED_YEARLY_PERIOD_STORE_ID_PRD_ID', 'period', 'store_id', 'product_id', unique=True),
        {'comment': 'Most Viewed Products Aggregated Yearly'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), index=True, comment='Product ID')
    product_name = Column(String(255), comment='Product Name')
    product_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Product Price')
    views_num = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Number of Views')
    rating_pos = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Pos')

    product = relationship('CatalogProductEntity')
    store = relationship('Store')


class ReportComparedProductIndex(Base):
    __tablename__ = 'report_compared_product_index'
    __table_args__ = (
        Index('REPORT_COMPARED_PRODUCT_INDEX_CUSTOMER_ID_PRODUCT_ID', 'customer_id', 'product_id', unique=True),
        Index('REPORT_COMPARED_PRODUCT_INDEX_VISITOR_ID_PRODUCT_ID', 'visitor_id', 'product_id', unique=True),
        {'comment': 'Reports Compared Product Index Table'}
    )

    index_id = Column(BIGINT(20), primary_key=True, comment='Index ID')
    visitor_id = Column(INTEGER(10), comment='Visitor ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), comment='Customer ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    added_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Added At')

    customer = relationship('CustomerEntity')
    product = relationship('CatalogProductEntity')
    store = relationship('Store')


class ReportViewedProductIndex(Base):
    __tablename__ = 'report_viewed_product_index'
    __table_args__ = (
        Index('REPORT_VIEWED_PRODUCT_INDEX_VISITOR_ID_PRODUCT_ID', 'visitor_id', 'product_id', unique=True),
        Index('REPORT_VIEWED_PRODUCT_INDEX_CUSTOMER_ID_PRODUCT_ID', 'customer_id', 'product_id', unique=True),
        {'comment': 'Reports Viewed Product Index Table'}
    )

    index_id = Column(BIGINT(20), primary_key=True, comment='Index ID')
    visitor_id = Column(INTEGER(10), comment='Visitor ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), comment='Customer ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    added_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Added At')

    customer = relationship('CustomerEntity')
    product = relationship('CatalogProductEntity')
    store = relationship('Store')
