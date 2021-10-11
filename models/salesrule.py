# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomerGroup(Base):
    __tablename__ = 'customer_group'
    __table_args__ = {'comment': 'Customer Group'}

    customer_group_id = Column(INTEGER(10), primary_key=True)
    customer_group_code = Column(String(32), nullable=False, comment='Customer Group Code')
    tax_class_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Tax Class ID')

    rules = relationship('Salesrule', secondary='salesrule_customer_group')


class EavEntityType(Base):
    __tablename__ = 'eav_entity_type'
    __table_args__ = {'comment': 'Eav Entity Type'}

    entity_type_id = Column(SMALLINT(5), primary_key=True, comment='Entity Type ID')
    entity_type_code = Column(String(50), nullable=False, index=True, comment='Entity Type Code')
    entity_model = Column(String(255), nullable=False, comment='Entity Model')
    attribute_model = Column(String(255), comment='Attribute Model')
    entity_table = Column(String(255), comment='Entity Table')
    value_table_prefix = Column(String(255), comment='Value Table Prefix')
    entity_id_field = Column(String(255), comment='Entity ID Field')
    is_data_sharing = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Defines Is Data Sharing')
    data_sharing_key = Column(String(100), server_default=text("'default'"), comment='Data Sharing Key')
    default_attribute_set_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Default Attribute Set ID')
    increment_model = Column(String(255), comment='Increment Model')
    increment_per_store = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Increment Per Store')
    increment_pad_length = Column(SMALLINT(5), nullable=False, server_default=text("8"), comment='Increment Pad Length')
    increment_pad_char = Column(String(1), nullable=False, server_default=text("'0'"), comment='Increment Pad Char')
    additional_attribute_table = Column(String(255), comment='Additional Attribute Table')
    entity_attribute_collection = Column(String(255), comment='Entity Attribute Collection')


class Salesrule(Base):
    __tablename__ = 'salesrule'
    __table_args__ = (
        Index('SALESRULE_IS_ACTIVE_SORT_ORDER_TO_DATE_FROM_DATE', 'is_active', 'sort_order', 'to_date', 'from_date'),
        {'comment': 'Salesrule'}
    )

    rule_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    name = Column(String(255), comment='Name')
    description = Column(Text, comment='Description')
    from_date = Column(Date, comment='From')
    to_date = Column(Date, comment='To')
    uses_per_customer = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Uses Per Customer')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Active')
    conditions_serialized = Column(MEDIUMTEXT, comment='Conditions Serialized')
    actions_serialized = Column(MEDIUMTEXT, comment='Actions Serialized')
    stop_rules_processing = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Stop Rules Processing')
    is_advanced = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Advanced')
    product_ids = Column(Text, comment='Product Ids')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    simple_action = Column(String(32), comment='Simple Action')
    discount_amount = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount')
    discount_qty = Column(DECIMAL(12, 4), comment='Discount Qty')
    discount_step = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Discount Step')
    apply_to_shipping = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Apply To Shipping')
    times_used = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Times Used')
    is_rss = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Rss')
    coupon_type = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Coupon Type')
    use_auto_generation = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Use Auto Generation')
    uses_per_coupon = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='User Per Coupon')
    simple_free_shipping = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Simple Free Shipping')

    websites = relationship('StoreWebsite', secondary='salesrule_website')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class EavAttribute(Base):
    __tablename__ = 'eav_attribute'
    __table_args__ = (
        Index('EAV_ATTRIBUTE_ENTITY_TYPE_ID_ATTRIBUTE_CODE', 'entity_type_id', 'attribute_code', unique=True),
        {'comment': 'Eav Attribute'}
    )

    attribute_id = Column(SMALLINT(5), primary_key=True, comment='Attribute ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_code = Column(String(255), nullable=False, comment='Attribute Code')
    attribute_model = Column(String(255), comment='Attribute Model')
    backend_model = Column(String(255), comment='Backend Model')
    backend_type = Column(String(8), nullable=False, server_default=text("'static'"), comment='Backend Type')
    backend_table = Column(String(255), comment='Backend Table')
    frontend_model = Column(String(255), comment='Frontend Model')
    frontend_input = Column(String(50), comment='Frontend Input')
    frontend_label = Column(String(255), comment='Frontend Label')
    frontend_class = Column(String(255), comment='Frontend Class')
    source_model = Column(String(255), comment='Source Model')
    is_required = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Defines Is Required')
    is_user_defined = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Defines Is User Defined')
    default_value = Column(Text, comment='Default Value')
    is_unique = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Defines Is Unique')
    note = Column(String(255), comment='Note')

    entity_type = relationship('EavEntityType')


class SalesruleCoupon(Base):
    __tablename__ = 'salesrule_coupon'
    __table_args__ = (
        Index('SALESRULE_COUPON_RULE_ID_IS_PRIMARY', 'rule_id', 'is_primary', unique=True),
        {'comment': 'Salesrule Coupon'}
    )

    coupon_id = Column(INTEGER(10), primary_key=True, comment='Coupon ID')
    rule_id = Column(ForeignKey('salesrule.rule_id', ondelete='CASCADE'), nullable=False, index=True, comment='Rule ID')
    code = Column(String(255), unique=True, comment='Code')
    usage_limit = Column(INTEGER(10), comment='Usage Limit')
    usage_per_customer = Column(INTEGER(10), comment='Usage Per Customer')
    times_used = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Times Used')
    expiration_date = Column(DateTime, comment='Expiration Date')
    is_primary = Column(SMALLINT(5), comment='Is Primary')
    created_at = Column(TIMESTAMP, comment='Coupon Code Creation Date')
    type = Column(SMALLINT(6), server_default=text("0"), comment='Coupon Code Type')
    generated_by_dotmailer = Column(SMALLINT(6), comment='1 = Generated by dotmailer')

    rule = relationship('Salesrule')


t_salesrule_customer_group = Table(
    'salesrule_customer_group', metadata,
    Column('rule_id', ForeignKey('salesrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID'),
    Column('customer_group_id', ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer Group ID'),
    comment='Sales Rules To Customer Groups Relations'
)


t_salesrule_website = Table(
    'salesrule_website', metadata,
    Column('rule_id', ForeignKey('salesrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID'),
    Column('website_id', ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID'),
    comment='Sales Rules To Websites Relations'
)


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


class SalesruleProductAttribute(Base):
    __tablename__ = 'salesrule_product_attribute'
    __table_args__ = {'comment': 'Salesrule Product Attribute'}

    rule_id = Column(ForeignKey('salesrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID')
    customer_group_id = Column(ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer Group ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Attribute ID')

    attribute = relationship('EavAttribute')
    customer_group = relationship('CustomerGroup')
    rule = relationship('Salesrule')
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


class SalesruleCouponAggregated(Base):
    __tablename__ = 'salesrule_coupon_aggregated'
    __table_args__ = (
        Index('SALESRULE_COUPON_AGGRED_PERIOD_STORE_ID_ORDER_STS_COUPON_CODE', 'period', 'store_id', 'order_status', 'coupon_code', unique=True),
        {'comment': 'Coupon Aggregated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, nullable=False, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    coupon_code = Column(String(50), comment='Coupon Code')
    coupon_uses = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Coupon Uses')
    subtotal_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal Amount')
    discount_amount = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount')
    total_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Amount')
    subtotal_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal Amount Actual')
    discount_amount_actual = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount Actual')
    total_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Amount Actual')
    rule_name = Column(String(255), index=True, comment='Rule Name')

    store = relationship('Store')


class SalesruleCouponAggregatedOrder(Base):
    __tablename__ = 'salesrule_coupon_aggregated_order'
    __table_args__ = (
        Index('UNQ_1094D1FBBCBB11704A29DEF3ACC37D2B', 'period', 'store_id', 'order_status', 'coupon_code', unique=True),
        {'comment': 'Coupon Aggregated Order'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, nullable=False, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    coupon_code = Column(String(50), comment='Coupon Code')
    coupon_uses = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Coupon Uses')
    subtotal_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal Amount')
    discount_amount = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount')
    total_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Amount')
    rule_name = Column(String(255), index=True, comment='Rule Name')

    store = relationship('Store')


class SalesruleCouponAggregatedUpdated(Base):
    __tablename__ = 'salesrule_coupon_aggregated_updated'
    __table_args__ = (
        Index('UNQ_7196FA120A4F0F84E1B66605E87E213E', 'period', 'store_id', 'order_status', 'coupon_code', unique=True),
        {'comment': 'Salesrule Coupon Aggregated Updated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, nullable=False, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    coupon_code = Column(String(50), comment='Coupon Code')
    coupon_uses = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Coupon Uses')
    subtotal_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal Amount')
    discount_amount = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount')
    total_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Amount')
    subtotal_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal Amount Actual')
    discount_amount_actual = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount Actual')
    total_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Amount Actual')
    rule_name = Column(String(255), index=True, comment='Rule Name')

    store = relationship('Store')


class SalesruleLabel(Base):
    __tablename__ = 'salesrule_label'
    __table_args__ = (
        Index('SALESRULE_LABEL_RULE_ID_STORE_ID', 'rule_id', 'store_id', unique=True),
        {'comment': 'Salesrule Label'}
    )

    label_id = Column(INTEGER(10), primary_key=True, comment='Label ID')
    rule_id = Column(ForeignKey('salesrule.rule_id', ondelete='CASCADE'), nullable=False, comment='Rule ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, comment='Store ID')
    label = Column(String(255), comment='Label')

    rule = relationship('Salesrule')
    store = relationship('Store')


class SalesruleCouponUsage(Base):
    __tablename__ = 'salesrule_coupon_usage'
    __table_args__ = {'comment': 'Salesrule Coupon Usage'}

    coupon_id = Column(ForeignKey('salesrule_coupon.coupon_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Coupon ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer ID')
    times_used = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Times Used')

    coupon = relationship('SalesruleCoupon')
    customer = relationship('CustomerEntity')


class SalesruleCustomer(Base):
    __tablename__ = 'salesrule_customer'
    __table_args__ = (
        Index('SALESRULE_CUSTOMER_RULE_ID_CUSTOMER_ID', 'rule_id', 'customer_id'),
        Index('SALESRULE_CUSTOMER_CUSTOMER_ID_RULE_ID', 'customer_id', 'rule_id'),
        {'comment': 'Salesrule Customer'}
    )

    rule_customer_id = Column(INTEGER(10), primary_key=True, comment='Rule Customer ID')
    rule_id = Column(ForeignKey('salesrule.rule_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Rule ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Customer ID')
    times_used = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Times Used')

    customer = relationship('CustomerEntity')
    rule = relationship('Salesrule')
