# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, LargeBinary, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB, MEDIUMTEXT, SMALLINT, TINYINT
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


class SalesCreditmemoGrid(Base):
    __tablename__ = 'sales_creditmemo_grid'
    __table_args__ = (
        Index('SALES_CREDITMEMO_GRID_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        Index('FTI_32B7BA885941A8254EE84AE650ABDC86', 'increment_id', 'order_increment_id', 'billing_name', 'billing_address', 'shipping_address', 'customer_name', 'customer_email'),
        {'comment': 'Sales Flat Creditmemo Grid'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    increment_id = Column(String(50), comment='Increment ID')
    created_at = Column(TIMESTAMP, index=True, comment='Created At')
    updated_at = Column(TIMESTAMP, index=True, comment='Updated At')
    order_id = Column(INTEGER(10), nullable=False, index=True, comment='Order ID')
    order_increment_id = Column(String(50), index=True, comment='Order Increment ID')
    order_created_at = Column(TIMESTAMP, index=True, comment='Order Created At')
    billing_name = Column(String(255), index=True, comment='Billing Name')
    state = Column(INTEGER(11), index=True, comment='Status')
    base_grand_total = Column(DECIMAL(20, 4), index=True, comment='Base Grand Total')
    order_status = Column(String(32), index=True, comment='Order Status')
    store_id = Column(SMALLINT(5), index=True, comment='Store ID')
    billing_address = Column(String(255), comment='Billing Address')
    shipping_address = Column(String(255), comment='Shipping Address')
    customer_name = Column(String(128), nullable=False, comment='Customer Name')
    customer_email = Column(String(128), comment='Customer Email')
    customer_group_id = Column(SMALLINT(6), comment='Customer Group ID')
    payment_method = Column(String(32), comment='Payment Method')
    shipping_information = Column(String(255), comment='Shipping Method Name')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    shipping_and_handling = Column(DECIMAL(20, 4), comment='Shipping and handling amount')
    adjustment_positive = Column(DECIMAL(20, 4), comment='Adjustment Positive')
    adjustment_negative = Column(DECIMAL(20, 4), comment='Adjustment Negative')
    order_base_grand_total = Column(DECIMAL(20, 4), index=True, comment='Order Grand Total')


class SalesInvoiceGrid(Base):
    __tablename__ = 'sales_invoice_grid'
    __table_args__ = (
        Index('FTI_95D9C924DD6A8734EB8B5D01D60F90DE', 'increment_id', 'order_increment_id', 'billing_name', 'billing_address', 'shipping_address', 'customer_name', 'customer_email'),
        Index('SALES_INVOICE_GRID_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        {'comment': 'Sales Flat Invoice Grid'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    increment_id = Column(String(50), comment='Increment ID')
    state = Column(INTEGER(11), index=True, comment='State')
    store_id = Column(SMALLINT(5), index=True, comment='Store ID')
    store_name = Column(String(255), comment='Store Name')
    order_id = Column(INTEGER(10), nullable=False, index=True, comment='Order ID')
    order_increment_id = Column(String(50), index=True, comment='Order Increment ID')
    order_created_at = Column(TIMESTAMP, index=True, comment='Order Created At')
    customer_name = Column(String(255), comment='Customer Name')
    customer_email = Column(String(255), comment='Customer Email')
    customer_group_id = Column(INTEGER(11))
    payment_method = Column(String(128), comment='Payment Method')
    store_currency_code = Column(String(3), comment='Store Currency Code')
    order_currency_code = Column(String(3), comment='Order Currency Code')
    base_currency_code = Column(String(3), comment='Base Currency Code')
    global_currency_code = Column(String(3), comment='Global Currency Code')
    billing_name = Column(String(255), index=True, comment='Billing Name')
    billing_address = Column(String(255), comment='Billing Address')
    shipping_address = Column(String(255), comment='Shipping Address')
    shipping_information = Column(String(255), comment='Shipping Method Name')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    shipping_and_handling = Column(DECIMAL(20, 4), comment='Shipping and handling amount')
    grand_total = Column(DECIMAL(20, 4), index=True, comment='Grand Total')
    created_at = Column(TIMESTAMP, index=True, comment='Created At')
    updated_at = Column(TIMESTAMP, index=True, comment='Updated At')
    base_grand_total = Column(DECIMAL(20, 4), index=True, comment='Base Grand Total')


class SalesOrderGrid(Base):
    __tablename__ = 'sales_order_grid'
    __table_args__ = (
        Index('SALES_ORDER_GRID_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        Index('FTI_65B9E9925EC58F0C7C2E2F6379C233E7', 'increment_id', 'billing_name', 'shipping_name', 'shipping_address', 'billing_address', 'customer_name', 'customer_email'),
        {'comment': 'Sales Flat Order Grid'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    status = Column(String(32), index=True, comment='Status')
    store_id = Column(SMALLINT(5), index=True, comment='Store ID')
    store_name = Column(String(255), comment='Store Name')
    customer_id = Column(INTEGER(10), index=True, comment='Customer ID')
    base_grand_total = Column(DECIMAL(20, 4), index=True, comment='Base Grand Total')
    base_total_paid = Column(DECIMAL(20, 4), index=True, comment='Base Total Paid')
    grand_total = Column(DECIMAL(20, 4), index=True, comment='Grand Total')
    total_paid = Column(DECIMAL(20, 4), index=True, comment='Total Paid')
    increment_id = Column(String(50), comment='Increment ID')
    base_currency_code = Column(String(3), comment='Base Currency Code')
    order_currency_code = Column(String(255), comment='Order Currency Code')
    shipping_name = Column(String(255), index=True, comment='Shipping Name')
    billing_name = Column(String(255), index=True, comment='Billing Name')
    created_at = Column(TIMESTAMP, index=True, comment='Created At')
    updated_at = Column(TIMESTAMP, index=True, comment='Updated At')
    billing_address = Column(String(255), comment='Billing Address')
    shipping_address = Column(String(255), comment='Shipping Address')
    shipping_information = Column(String(255), comment='Shipping Method Name')
    customer_email = Column(String(255), comment='Customer Email')
    customer_group = Column(String(255), comment='Customer Group')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    shipping_and_handling = Column(DECIMAL(20, 4), comment='Shipping and handling amount')
    customer_name = Column(String(255), comment='Customer Name')
    payment_method = Column(String(255), comment='Payment Method')
    total_refunded = Column(DECIMAL(20, 4), comment='Total Refunded')
    signifyd_guarantee_status = Column(String(32), comment='Signifyd Guarantee Disposition Status')


class SalesOrderStatu(Base):
    __tablename__ = 'sales_order_status'
    __table_args__ = {'comment': 'Sales Order Status Table'}

    status = Column(String(32), primary_key=True, comment='Status')
    label = Column(String(128), nullable=False, comment='Label')


class SalesOrderTax(Base):
    __tablename__ = 'sales_order_tax'
    __table_args__ = (
        Index('SALES_ORDER_TAX_ORDER_ID_PRIORITY_POSITION', 'order_id', 'priority', 'position'),
        {'comment': 'Sales Order Tax Table'}
    )

    tax_id = Column(INTEGER(10), primary_key=True, comment='Tax ID')
    order_id = Column(INTEGER(10), nullable=False, comment='Order ID')
    code = Column(String(255), comment='Code')
    title = Column(String(255), comment='Title')
    percent = Column(DECIMAL(12, 4), comment='Percent')
    amount = Column(DECIMAL(20, 4), comment='Amount')
    priority = Column(INTEGER(11), nullable=False, comment='Priority')
    position = Column(INTEGER(11), nullable=False, comment='Position')
    base_amount = Column(DECIMAL(20, 4), comment='Base Amount')
    process = Column(SMALLINT(6), nullable=False, comment='Process')
    base_real_amount = Column(DECIMAL(20, 4), comment='Base Real Amount')


class SalesSequenceMeta(Base):
    __tablename__ = 'sales_sequence_meta'
    __table_args__ = (
        Index('SALES_SEQUENCE_META_ENTITY_TYPE_STORE_ID', 'entity_type', 'store_id', unique=True),
        {'comment': 'sales_sequence_meta'}
    )

    meta_id = Column(INTEGER(10), primary_key=True, comment='ID')
    entity_type = Column(String(32), nullable=False, comment='Prefix')
    store_id = Column(SMALLINT(5), nullable=False, comment='Store ID')
    sequence_table = Column(String(64), nullable=False, comment='table for sequence')


class SalesShipmentGrid(Base):
    __tablename__ = 'sales_shipment_grid'
    __table_args__ = (
        Index('FTI_086B40C8955F167B8EA76653437879B4', 'increment_id', 'order_increment_id', 'shipping_name', 'customer_name', 'customer_email', 'billing_address', 'shipping_address'),
        Index('SALES_SHIPMENT_GRID_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        {'comment': 'Sales Flat Shipment Grid'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    increment_id = Column(String(50), comment='Increment ID')
    store_id = Column(SMALLINT(5), index=True, comment='Store ID')
    order_increment_id = Column(String(32), nullable=False, index=True, comment='Order Increment ID')
    order_id = Column(INTEGER(10), nullable=False, comment='Order ID')
    order_created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Order Increment ID')
    customer_name = Column(String(128), nullable=False, comment='Customer Name')
    total_qty = Column(DECIMAL(12, 4), index=True, comment='Total Qty')
    shipment_status = Column(INTEGER(11), index=True, comment='Shipment Status')
    order_status = Column(String(32), index=True, comment='Order')
    billing_address = Column(String(255), comment='Billing Address')
    shipping_address = Column(String(255), comment='Shipping Address')
    billing_name = Column(String(128), index=True, comment='Billing Name')
    shipping_name = Column(String(128), index=True, comment='Shipping Name')
    customer_email = Column(String(128), comment='Customer Email')
    customer_group_id = Column(INTEGER(11))
    payment_method = Column(String(32), comment='Payment Method')
    shipping_information = Column(String(255), comment='Shipping Method Name')
    created_at = Column(TIMESTAMP, index=True, comment='Created At')
    updated_at = Column(TIMESTAMP, index=True, comment='Updated At')


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


class SalesOrderStatusState(Base):
    __tablename__ = 'sales_order_status_state'
    __table_args__ = {'comment': 'Sales Order Status Table'}

    status = Column(ForeignKey('sales_order_status.status', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Status')
    state = Column(String(32), primary_key=True, nullable=False, comment='Label')
    is_default = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Default')
    visible_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Visible on front')

    sales_order_statu = relationship('SalesOrderStatu')


class SalesSequenceProfile(Base):
    __tablename__ = 'sales_sequence_profile'
    __table_args__ = (
        Index('SALES_SEQUENCE_PROFILE_META_ID_PREFIX_SUFFIX', 'meta_id', 'prefix', 'suffix', unique=True),
        {'comment': 'sales_sequence_profile'}
    )

    profile_id = Column(INTEGER(10), primary_key=True, comment='ID')
    meta_id = Column(ForeignKey('sales_sequence_meta.meta_id', ondelete='CASCADE'), nullable=False, comment='Meta_id')
    prefix = Column(String(32), comment='Prefix')
    suffix = Column(String(32), comment='Suffix')
    start_value = Column(INTEGER(10), nullable=False, server_default=text("1"), comment='Start value for sequence')
    step = Column(INTEGER(10), nullable=False, server_default=text("1"), comment='Step for sequence')
    max_value = Column(INTEGER(10), nullable=False, comment='MaxValue for sequence')
    warning_value = Column(INTEGER(10), nullable=False, comment='WarningValue for sequence')
    is_active = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='isActive flag')

    meta = relationship('SalesSequenceMeta')


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


class SalesBestsellersAggregatedDaily(Base):
    __tablename__ = 'sales_bestsellers_aggregated_daily'
    __table_args__ = (
        Index('SALES_BESTSELLERS_AGGREGATED_DAILY_PERIOD_STORE_ID_PRODUCT_ID', 'period', 'store_id', 'product_id', unique=True),
        {'comment': 'Sales Bestsellers Aggregated Daily'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    product_id = Column(INTEGER(10), index=True, comment='Product ID')
    product_name = Column(String(255), comment='Product Name')
    product_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Product Price')
    qty_ordered = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty Ordered')
    rating_pos = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Pos')

    store = relationship('Store')


class SalesBestsellersAggregatedMonthly(Base):
    __tablename__ = 'sales_bestsellers_aggregated_monthly'
    __table_args__ = (
        Index('SALES_BESTSELLERS_AGGREGATED_MONTHLY_PERIOD_STORE_ID_PRODUCT_ID', 'period', 'store_id', 'product_id', unique=True),
        {'comment': 'Sales Bestsellers Aggregated Monthly'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    product_id = Column(INTEGER(10), index=True, comment='Product ID')
    product_name = Column(String(255), comment='Product Name')
    product_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Product Price')
    qty_ordered = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty Ordered')
    rating_pos = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Pos')

    store = relationship('Store')


class SalesBestsellersAggregatedYearly(Base):
    __tablename__ = 'sales_bestsellers_aggregated_yearly'
    __table_args__ = (
        Index('SALES_BESTSELLERS_AGGREGATED_YEARLY_PERIOD_STORE_ID_PRODUCT_ID', 'period', 'store_id', 'product_id', unique=True),
        {'comment': 'Sales Bestsellers Aggregated Yearly'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), index=True, comment='Store ID')
    product_id = Column(INTEGER(10), index=True, comment='Product ID')
    product_name = Column(String(255), comment='Product Name')
    product_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Product Price')
    qty_ordered = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty Ordered')
    rating_pos = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Pos')

    store = relationship('Store')


class SalesInvoicedAggregated(Base):
    __tablename__ = 'sales_invoiced_aggregated'
    __table_args__ = (
        Index('SALES_INVOICED_AGGREGATED_PERIOD_STORE_ID_ORDER_STATUS', 'period', 'store_id', 'order_status', unique=True),
        {'comment': 'Sales Invoiced Aggregated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    orders_invoiced = Column(DECIMAL(12, 4), comment='Orders Invoiced')
    invoiced = Column(DECIMAL(12, 4), comment='Invoiced')
    invoiced_captured = Column(DECIMAL(12, 4), comment='Invoiced Captured')
    invoiced_not_captured = Column(DECIMAL(12, 4), comment='Invoiced Not Captured')

    store = relationship('Store')


class SalesInvoicedAggregatedOrder(Base):
    __tablename__ = 'sales_invoiced_aggregated_order'
    __table_args__ = (
        Index('SALES_INVOICED_AGGREGATED_ORDER_PERIOD_STORE_ID_ORDER_STATUS', 'period', 'store_id', 'order_status', unique=True),
        {'comment': 'Sales Invoiced Aggregated Order'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), nullable=False, comment='Order Status')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    orders_invoiced = Column(DECIMAL(12, 4), comment='Orders Invoiced')
    invoiced = Column(DECIMAL(12, 4), comment='Invoiced')
    invoiced_captured = Column(DECIMAL(12, 4), comment='Invoiced Captured')
    invoiced_not_captured = Column(DECIMAL(12, 4), comment='Invoiced Not Captured')

    store = relationship('Store')


class SalesOrderAggregatedCreated(Base):
    __tablename__ = 'sales_order_aggregated_created'
    __table_args__ = (
        Index('SALES_ORDER_AGGREGATED_CREATED_PERIOD_STORE_ID_ORDER_STATUS', 'period', 'store_id', 'order_status', unique=True),
        {'comment': 'Sales Order Aggregated Created'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), nullable=False, comment='Order Status')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    total_qty_ordered = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Total Qty Ordered')
    total_qty_invoiced = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Total Qty Invoiced')
    total_income_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Income Amount')
    total_revenue_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Revenue Amount')
    total_profit_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Profit Amount')
    total_invoiced_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Invoiced Amount')
    total_canceled_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Canceled Amount')
    total_paid_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Paid Amount')
    total_refunded_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Refunded Amount')
    total_tax_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Tax Amount')
    total_tax_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Tax Amount Actual')
    total_shipping_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Shipping Amount')
    total_shipping_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Shipping Amount Actual')
    total_discount_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Discount Amount')
    total_discount_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Discount Amount Actual')

    store = relationship('Store')


class SalesOrderAggregatedUpdated(Base):
    __tablename__ = 'sales_order_aggregated_updated'
    __table_args__ = (
        Index('SALES_ORDER_AGGREGATED_UPDATED_PERIOD_STORE_ID_ORDER_STATUS', 'period', 'store_id', 'order_status', unique=True),
        {'comment': 'Sales Order Aggregated Updated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), nullable=False, comment='Order Status')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    total_qty_ordered = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Total Qty Ordered')
    total_qty_invoiced = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Total Qty Invoiced')
    total_income_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Income Amount')
    total_revenue_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Revenue Amount')
    total_profit_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Profit Amount')
    total_invoiced_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Invoiced Amount')
    total_canceled_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Canceled Amount')
    total_paid_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Paid Amount')
    total_refunded_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Refunded Amount')
    total_tax_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Tax Amount')
    total_tax_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Tax Amount Actual')
    total_shipping_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Shipping Amount')
    total_shipping_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Shipping Amount Actual')
    total_discount_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Discount Amount')
    total_discount_amount_actual = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Total Discount Amount Actual')

    store = relationship('Store')


class SalesOrderStatusLabel(Base):
    __tablename__ = 'sales_order_status_label'
    __table_args__ = {'comment': 'Sales Order Status Label Table'}

    status = Column(ForeignKey('sales_order_status.status', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Status')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Store ID')
    label = Column(String(128), nullable=False, comment='Label')

    sales_order_statu = relationship('SalesOrderStatu')
    store = relationship('Store')


class SalesRefundedAggregated(Base):
    __tablename__ = 'sales_refunded_aggregated'
    __table_args__ = (
        Index('SALES_REFUNDED_AGGREGATED_PERIOD_STORE_ID_ORDER_STATUS', 'period', 'store_id', 'order_status', unique=True),
        {'comment': 'Sales Refunded Aggregated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), nullable=False, comment='Order Status')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    refunded = Column(DECIMAL(20, 4), comment='Refunded')
    online_refunded = Column(DECIMAL(20, 4), comment='Online Refunded')
    offline_refunded = Column(DECIMAL(20, 4), comment='Offline Refunded')

    store = relationship('Store')


class SalesRefundedAggregatedOrder(Base):
    __tablename__ = 'sales_refunded_aggregated_order'
    __table_args__ = (
        Index('SALES_REFUNDED_AGGREGATED_ORDER_PERIOD_STORE_ID_ORDER_STATUS', 'period', 'store_id', 'order_status', unique=True),
        {'comment': 'Sales Refunded Aggregated Order'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    refunded = Column(DECIMAL(20, 4), comment='Refunded')
    online_refunded = Column(DECIMAL(20, 4), comment='Online Refunded')
    offline_refunded = Column(DECIMAL(20, 4), comment='Offline Refunded')

    store = relationship('Store')


class SalesShippingAggregated(Base):
    __tablename__ = 'sales_shipping_aggregated'
    __table_args__ = (
        Index('SALES_SHPP_AGGRED_PERIOD_STORE_ID_ORDER_STS_SHPP_DESCRIPTION', 'period', 'store_id', 'order_status', 'shipping_description', unique=True),
        {'comment': 'Sales Shipping Aggregated'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    shipping_description = Column(String(255), comment='Shipping Description')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    total_shipping = Column(DECIMAL(20, 4), comment='Total Shipping')
    total_shipping_actual = Column(DECIMAL(20, 4), comment='Total Shipping Actual')

    store = relationship('Store')


class SalesShippingAggregatedOrder(Base):
    __tablename__ = 'sales_shipping_aggregated_order'
    __table_args__ = (
        Index('UNQ_C05FAE47282EEA68654D0924E946761F', 'period', 'store_id', 'order_status', 'shipping_description', unique=True),
        {'comment': 'Sales Shipping Aggregated Order'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    period = Column(Date, comment='Period')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    order_status = Column(String(50), comment='Order Status')
    shipping_description = Column(String(255), comment='Shipping Description')
    orders_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Orders Count')
    total_shipping = Column(DECIMAL(20, 4), comment='Total Shipping')
    total_shipping_actual = Column(DECIMAL(20, 4), comment='Total Shipping Actual')

    store = relationship('Store')


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


class SalesOrder(Base):
    __tablename__ = 'sales_order'
    __table_args__ = (
        Index('SALES_ORDER_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        {'comment': 'Sales Flat Order'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    state = Column(String(32), index=True, comment='State')
    status = Column(String(32), index=True, comment='Status')
    coupon_code = Column(String(255), comment='Coupon Code')
    protect_code = Column(String(255), comment='Protect Code')
    shipping_description = Column(String(255), comment='Shipping Description')
    is_virtual = Column(SMALLINT(5), comment='Is Virtual')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='SET NULL'), index=True, comment='Customer ID')
    base_discount_amount = Column(DECIMAL(20, 4), comment='Base Discount Amount')
    base_discount_canceled = Column(DECIMAL(20, 4), comment='Base Discount Canceled')
    base_discount_invoiced = Column(DECIMAL(20, 4), comment='Base Discount Invoiced')
    base_discount_refunded = Column(DECIMAL(20, 4), comment='Base Discount Refunded')
    base_grand_total = Column(DECIMAL(20, 4), comment='Base Grand Total')
    base_shipping_amount = Column(DECIMAL(20, 4), comment='Base Shipping Amount')
    base_shipping_canceled = Column(DECIMAL(20, 4), comment='Base Shipping Canceled')
    base_shipping_invoiced = Column(DECIMAL(20, 4), comment='Base Shipping Invoiced')
    base_shipping_refunded = Column(DECIMAL(20, 4), comment='Base Shipping Refunded')
    base_shipping_tax_amount = Column(DECIMAL(20, 4), comment='Base Shipping Tax Amount')
    base_shipping_tax_refunded = Column(DECIMAL(20, 4), comment='Base Shipping Tax Refunded')
    base_subtotal = Column(DECIMAL(20, 4), comment='Base Subtotal')
    base_subtotal_canceled = Column(DECIMAL(20, 4), comment='Base Subtotal Canceled')
    base_subtotal_invoiced = Column(DECIMAL(20, 4), comment='Base Subtotal Invoiced')
    base_subtotal_refunded = Column(DECIMAL(20, 4), comment='Base Subtotal Refunded')
    base_tax_amount = Column(DECIMAL(20, 4), comment='Base Tax Amount')
    base_tax_canceled = Column(DECIMAL(20, 4), comment='Base Tax Canceled')
    base_tax_invoiced = Column(DECIMAL(20, 4), comment='Base Tax Invoiced')
    base_tax_refunded = Column(DECIMAL(20, 4), comment='Base Tax Refunded')
    base_to_global_rate = Column(DECIMAL(20, 4), comment='Base To Global Rate')
    base_to_order_rate = Column(DECIMAL(20, 4), comment='Base To Order Rate')
    base_total_canceled = Column(DECIMAL(20, 4), comment='Base Total Canceled')
    base_total_invoiced = Column(DECIMAL(20, 4), comment='Base Total Invoiced')
    base_total_invoiced_cost = Column(DECIMAL(20, 4), comment='Base Total Invoiced Cost')
    base_total_offline_refunded = Column(DECIMAL(20, 4), comment='Base Total Offline Refunded')
    base_total_online_refunded = Column(DECIMAL(20, 4), comment='Base Total Online Refunded')
    base_total_paid = Column(DECIMAL(20, 4), comment='Base Total Paid')
    base_total_qty_ordered = Column(DECIMAL(12, 4), comment='Base Total Qty Ordered')
    base_total_refunded = Column(DECIMAL(20, 4), comment='Base Total Refunded')
    discount_amount = Column(DECIMAL(20, 4), comment='Discount Amount')
    discount_canceled = Column(DECIMAL(20, 4), comment='Discount Canceled')
    discount_invoiced = Column(DECIMAL(20, 4), comment='Discount Invoiced')
    discount_refunded = Column(DECIMAL(20, 4), comment='Discount Refunded')
    grand_total = Column(DECIMAL(20, 4), comment='Grand Total')
    shipping_amount = Column(DECIMAL(20, 4), comment='Shipping Amount')
    shipping_canceled = Column(DECIMAL(20, 4), comment='Shipping Canceled')
    shipping_invoiced = Column(DECIMAL(20, 4), comment='Shipping Invoiced')
    shipping_refunded = Column(DECIMAL(20, 4), comment='Shipping Refunded')
    shipping_tax_amount = Column(DECIMAL(20, 4), comment='Shipping Tax Amount')
    shipping_tax_refunded = Column(DECIMAL(20, 4), comment='Shipping Tax Refunded')
    store_to_base_rate = Column(DECIMAL(12, 4), comment='Store To Base Rate')
    store_to_order_rate = Column(DECIMAL(12, 4), comment='Store To Order Rate')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    subtotal_canceled = Column(DECIMAL(20, 4), comment='Subtotal Canceled')
    subtotal_invoiced = Column(DECIMAL(20, 4), comment='Subtotal Invoiced')
    subtotal_refunded = Column(DECIMAL(20, 4), comment='Subtotal Refunded')
    tax_amount = Column(DECIMAL(20, 4), comment='Tax Amount')
    tax_canceled = Column(DECIMAL(20, 4), comment='Tax Canceled')
    tax_invoiced = Column(DECIMAL(20, 4), comment='Tax Invoiced')
    tax_refunded = Column(DECIMAL(20, 4), comment='Tax Refunded')
    total_canceled = Column(DECIMAL(20, 4), comment='Total Canceled')
    total_invoiced = Column(DECIMAL(20, 4), comment='Total Invoiced')
    total_offline_refunded = Column(DECIMAL(20, 4), comment='Total Offline Refunded')
    total_online_refunded = Column(DECIMAL(20, 4), comment='Total Online Refunded')
    total_paid = Column(DECIMAL(20, 4), comment='Total Paid')
    total_qty_ordered = Column(DECIMAL(12, 4), comment='Total Qty Ordered')
    total_refunded = Column(DECIMAL(20, 4), comment='Total Refunded')
    can_ship_partially = Column(SMALLINT(5), comment='Can Ship Partially')
    can_ship_partially_item = Column(SMALLINT(5), comment='Can Ship Partially Item')
    customer_is_guest = Column(SMALLINT(5), comment='Customer Is Guest')
    customer_note_notify = Column(SMALLINT(5), comment='Customer Note Notify')
    billing_address_id = Column(INTEGER(11), comment='Billing Address ID')
    customer_group_id = Column(INTEGER(11))
    edit_increment = Column(INTEGER(11), comment='Edit Increment')
    email_sent = Column(SMALLINT(5), index=True, comment='Email Sent')
    send_email = Column(SMALLINT(5), index=True, comment='Send Email')
    forced_shipment_with_invoice = Column(SMALLINT(5), comment='Forced Do Shipment With Invoice')
    payment_auth_expiration = Column(INTEGER(11), comment='Payment Authorization Expiration')
    quote_address_id = Column(INTEGER(11), comment='Quote Address ID')
    quote_id = Column(INTEGER(11), index=True, comment='Quote ID')
    shipping_address_id = Column(INTEGER(11), comment='Shipping Address ID')
    adjustment_negative = Column(DECIMAL(20, 4), comment='Adjustment Negative')
    adjustment_positive = Column(DECIMAL(20, 4), comment='Adjustment Positive')
    base_adjustment_negative = Column(DECIMAL(20, 4), comment='Base Adjustment Negative')
    base_adjustment_positive = Column(DECIMAL(20, 4), comment='Base Adjustment Positive')
    base_shipping_discount_amount = Column(DECIMAL(20, 4), comment='Base Shipping Discount Amount')
    base_subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Base Subtotal Incl Tax')
    base_total_due = Column(DECIMAL(20, 4), comment='Base Total Due')
    payment_authorization_amount = Column(DECIMAL(20, 4), comment='Payment Authorization Amount')
    shipping_discount_amount = Column(DECIMAL(20, 4), comment='Shipping Discount Amount')
    subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Subtotal Incl Tax')
    total_due = Column(DECIMAL(20, 4), comment='Total Due')
    weight = Column(DECIMAL(12, 4), comment='Weight')
    customer_dob = Column(DateTime, comment='Customer Dob')
    increment_id = Column(String(32), comment='Increment ID')
    applied_rule_ids = Column(String(128), comment='Applied Rule Ids')
    base_currency_code = Column(String(3), comment='Base Currency Code')
    customer_email = Column(String(128), comment='Customer Email')
    customer_firstname = Column(String(128), comment='Customer Firstname')
    customer_lastname = Column(String(128), comment='Customer Lastname')
    customer_middlename = Column(String(128), comment='Customer Middlename')
    customer_prefix = Column(String(32), comment='Customer Prefix')
    customer_suffix = Column(String(32), comment='Customer Suffix')
    customer_taxvat = Column(String(32), comment='Customer Taxvat')
    discount_description = Column(String(255), comment='Discount Description')
    ext_customer_id = Column(String(32), comment='Ext Customer ID')
    ext_order_id = Column(String(32), index=True, comment='Ext Order ID')
    global_currency_code = Column(String(3), comment='Global Currency Code')
    hold_before_state = Column(String(32), comment='Hold Before State')
    hold_before_status = Column(String(32), comment='Hold Before Status')
    order_currency_code = Column(String(3), comment='Order Currency Code')
    original_increment_id = Column(String(32), comment='Original Increment ID')
    relation_child_id = Column(String(32), comment='Relation Child ID')
    relation_child_real_id = Column(String(32), comment='Relation Child Real ID')
    relation_parent_id = Column(String(32), comment='Relation Parent ID')
    relation_parent_real_id = Column(String(32), comment='Relation Parent Real ID')
    remote_ip = Column(String(45), comment='Remote Ip')
    shipping_method = Column(String(120))
    store_currency_code = Column(String(3), comment='Store Currency Code')
    store_name = Column(String(255), comment='Store Name')
    x_forwarded_for = Column(String(32), comment='X Forwarded For')
    customer_note = Column(Text, comment='Customer Note')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    total_item_count = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Total Item Count')
    customer_gender = Column(INTEGER(11), comment='Customer Gender')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    shipping_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Shipping Discount Tax Compensation Amount')
    base_shipping_discount_tax_compensation_amnt = Column(DECIMAL(20, 4), comment='Base Shipping Discount Tax Compensation Amount')
    discount_tax_compensation_invoiced = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Invoiced')
    base_discount_tax_compensation_invoiced = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Invoiced')
    discount_tax_compensation_refunded = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Refunded')
    base_discount_tax_compensation_refunded = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Refunded')
    shipping_incl_tax = Column(DECIMAL(20, 4), comment='Shipping Incl Tax')
    base_shipping_incl_tax = Column(DECIMAL(20, 4), comment='Base Shipping Incl Tax')
    coupon_rule_name = Column(String(255), comment='Coupon Sales Rule Name')
    gift_message_id = Column(INTEGER(11), comment='Gift Message ID')
    paypal_ipn_customer_notified = Column(INTEGER(11), server_default=text("0"), comment='Paypal Ipn Customer Notified')

    customer = relationship('CustomerEntity')
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
        Index('SALESRULE_CUSTOMER_CUSTOMER_ID_RULE_ID', 'customer_id', 'rule_id'),
        Index('SALESRULE_CUSTOMER_RULE_ID_CUSTOMER_ID', 'rule_id', 'customer_id'),
        {'comment': 'Salesrule Customer'}
    )

    rule_customer_id = Column(INTEGER(10), primary_key=True, comment='Rule Customer ID')
    rule_id = Column(ForeignKey('salesrule.rule_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Rule ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Customer ID')
    times_used = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Times Used')

    customer = relationship('CustomerEntity')
    rule = relationship('Salesrule')


class SalesCreditmemo(Base):
    __tablename__ = 'sales_creditmemo'
    __table_args__ = (
        Index('SALES_CREDITMEMO_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        {'comment': 'Sales Flat Creditmemo'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    adjustment_positive = Column(DECIMAL(20, 4), comment='Adjustment Positive')
    base_shipping_tax_amount = Column(DECIMAL(20, 4), comment='Base Shipping Tax Amount')
    store_to_order_rate = Column(DECIMAL(20, 4), comment='Store To Order Rate')
    base_discount_amount = Column(DECIMAL(20, 4), comment='Base Discount Amount')
    base_to_order_rate = Column(DECIMAL(20, 4), comment='Base To Order Rate')
    grand_total = Column(DECIMAL(20, 4), comment='Grand Total')
    base_adjustment_negative = Column(DECIMAL(20, 4), comment='Base Adjustment Negative')
    base_subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Base Subtotal Incl Tax')
    shipping_amount = Column(DECIMAL(20, 4), comment='Shipping Amount')
    subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Subtotal Incl Tax')
    adjustment_negative = Column(DECIMAL(20, 4), comment='Adjustment Negative')
    base_shipping_amount = Column(DECIMAL(20, 4), comment='Base Shipping Amount')
    store_to_base_rate = Column(DECIMAL(20, 4), comment='Store To Base Rate')
    base_to_global_rate = Column(DECIMAL(20, 4), comment='Base To Global Rate')
    base_adjustment = Column(DECIMAL(20, 4), comment='Base Adjustment')
    base_subtotal = Column(DECIMAL(20, 4), comment='Base Subtotal')
    discount_amount = Column(DECIMAL(20, 4), comment='Discount Amount')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    adjustment = Column(DECIMAL(20, 4), comment='Adjustment')
    base_grand_total = Column(DECIMAL(20, 4), comment='Base Grand Total')
    base_adjustment_positive = Column(DECIMAL(20, 4), comment='Base Adjustment Positive')
    base_tax_amount = Column(DECIMAL(20, 4), comment='Base Tax Amount')
    shipping_tax_amount = Column(DECIMAL(20, 4), comment='Shipping Tax Amount')
    tax_amount = Column(DECIMAL(20, 4), comment='Tax Amount')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Order ID')
    email_sent = Column(SMALLINT(5), index=True, comment='Email Sent')
    send_email = Column(SMALLINT(5), index=True, comment='Send Email')
    creditmemo_status = Column(INTEGER(11), index=True, comment='Creditmemo Status')
    state = Column(INTEGER(11), index=True, comment='State')
    shipping_address_id = Column(INTEGER(11), comment='Shipping Address ID')
    billing_address_id = Column(INTEGER(11), comment='Billing Address ID')
    invoice_id = Column(INTEGER(11), comment='Invoice ID')
    store_currency_code = Column(String(3), comment='Store Currency Code')
    order_currency_code = Column(String(3), comment='Order Currency Code')
    base_currency_code = Column(String(3), comment='Base Currency Code')
    global_currency_code = Column(String(3), comment='Global Currency Code')
    transaction_id = Column(String(255), comment='Transaction ID')
    increment_id = Column(String(50), comment='Increment ID')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    shipping_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Shipping Discount Tax Compensation Amount')
    base_shipping_discount_tax_compensation_amnt = Column(DECIMAL(20, 4), comment='Base Shipping Discount Tax Compensation Amount')
    shipping_incl_tax = Column(DECIMAL(20, 4), comment='Shipping Incl Tax')
    base_shipping_incl_tax = Column(DECIMAL(20, 4), comment='Base Shipping Incl Tax')
    discount_description = Column(String(255), comment='Discount Description')
    customer_note = Column(Text, comment='Customer Note')
    customer_note_notify = Column(SMALLINT(5), comment='Customer Note Notify')

    order = relationship('SalesOrder')
    store = relationship('Store')


class SalesInvoice(Base):
    __tablename__ = 'sales_invoice'
    __table_args__ = (
        Index('SALES_INVOICE_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        {'comment': 'Sales Flat Invoice'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    base_grand_total = Column(DECIMAL(20, 4), comment='Base Grand Total')
    shipping_tax_amount = Column(DECIMAL(20, 4), comment='Shipping Tax Amount')
    tax_amount = Column(DECIMAL(20, 4), comment='Tax Amount')
    base_tax_amount = Column(DECIMAL(20, 4), comment='Base Tax Amount')
    store_to_order_rate = Column(DECIMAL(20, 4), comment='Store To Order Rate')
    base_shipping_tax_amount = Column(DECIMAL(20, 4), comment='Base Shipping Tax Amount')
    base_discount_amount = Column(DECIMAL(20, 4), comment='Base Discount Amount')
    base_to_order_rate = Column(DECIMAL(20, 4), comment='Base To Order Rate')
    grand_total = Column(DECIMAL(20, 4), index=True, comment='Grand Total')
    shipping_amount = Column(DECIMAL(20, 4), comment='Shipping Amount')
    subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Subtotal Incl Tax')
    base_subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Base Subtotal Incl Tax')
    store_to_base_rate = Column(DECIMAL(20, 4), comment='Store To Base Rate')
    base_shipping_amount = Column(DECIMAL(20, 4), comment='Base Shipping Amount')
    total_qty = Column(DECIMAL(12, 4), comment='Total Qty')
    base_to_global_rate = Column(DECIMAL(20, 4), comment='Base To Global Rate')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    base_subtotal = Column(DECIMAL(20, 4), comment='Base Subtotal')
    discount_amount = Column(DECIMAL(20, 4), comment='Discount Amount')
    billing_address_id = Column(INTEGER(11), comment='Billing Address ID')
    is_used_for_refund = Column(SMALLINT(5), comment='Is Used For Refund')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Order ID')
    email_sent = Column(SMALLINT(5), index=True, comment='Email Sent')
    send_email = Column(SMALLINT(5), index=True, comment='Send Email')
    can_void_flag = Column(SMALLINT(5), comment='Can Void Flag')
    state = Column(INTEGER(11), index=True, comment='State')
    shipping_address_id = Column(INTEGER(11), comment='Shipping Address ID')
    store_currency_code = Column(String(3), comment='Store Currency Code')
    transaction_id = Column(String(255), comment='Transaction ID')
    order_currency_code = Column(String(3), comment='Order Currency Code')
    base_currency_code = Column(String(3), comment='Base Currency Code')
    global_currency_code = Column(String(3), comment='Global Currency Code')
    increment_id = Column(String(50), comment='Increment ID')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    shipping_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Shipping Discount Tax Compensation Amount')
    base_shipping_discount_tax_compensation_amnt = Column(DECIMAL(20, 4), comment='Base Shipping Discount Tax Compensation Amount')
    shipping_incl_tax = Column(DECIMAL(20, 4), comment='Shipping Incl Tax')
    base_shipping_incl_tax = Column(DECIMAL(20, 4), comment='Base Shipping Incl Tax')
    base_total_refunded = Column(DECIMAL(20, 4), comment='Base Total Refunded')
    discount_description = Column(String(255), comment='Discount Description')
    customer_note = Column(Text, comment='Customer Note')
    customer_note_notify = Column(SMALLINT(5), comment='Customer Note Notify')

    order = relationship('SalesOrder')
    store = relationship('Store')


class SalesOrderAddres(Base):
    __tablename__ = 'sales_order_address'
    __table_args__ = {'comment': 'Sales Flat Order Address'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), index=True, comment='Parent ID')
    customer_address_id = Column(INTEGER(11), comment='Customer Address ID')
    quote_address_id = Column(INTEGER(11), comment='Quote Address ID')
    region_id = Column(INTEGER(11), comment='Region ID')
    customer_id = Column(INTEGER(11), comment='Customer ID')
    fax = Column(String(255), comment='Fax')
    region = Column(String(255), comment='Region')
    postcode = Column(String(255), comment='Postcode')
    lastname = Column(String(255), comment='Lastname')
    street = Column(String(255), comment='Street')
    city = Column(String(255), comment='City')
    email = Column(String(255), comment='Email')
    telephone = Column(String(255), comment='Phone Number')
    country_id = Column(String(2), comment='Country ID')
    firstname = Column(String(255), comment='Firstname')
    address_type = Column(String(255), comment='Address Type')
    prefix = Column(String(255), comment='Prefix')
    middlename = Column(String(255), comment='Middlename')
    suffix = Column(String(255), comment='Suffix')
    company = Column(String(255), comment='Company')
    vat_id = Column(Text, comment='Vat ID')
    vat_is_valid = Column(SMALLINT(6), comment='Vat Is Valid')
    vat_request_id = Column(Text, comment='Vat Request ID')
    vat_request_date = Column(Text, comment='Vat Request Date')
    vat_request_success = Column(SMALLINT(6), comment='Vat Request Success')

    parent = relationship('SalesOrder')


class SalesOrderItem(Base):
    __tablename__ = 'sales_order_item'
    __table_args__ = {'comment': 'Sales Flat Order Item'}

    item_id = Column(INTEGER(10), primary_key=True, comment='Item ID')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Order ID')
    parent_item_id = Column(INTEGER(10), comment='Parent Item ID')
    quote_item_id = Column(INTEGER(10), comment='Quote Item ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    product_id = Column(INTEGER(10), comment='Product ID')
    product_type = Column(String(255), comment='Product Type')
    product_options = Column(Text, comment='Product Options')
    weight = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Weight')
    is_virtual = Column(SMALLINT(5), comment='Is Virtual')
    sku = Column(String(255), comment='Sku')
    name = Column(String(255), comment='Name')
    description = Column(Text, comment='Description')
    applied_rule_ids = Column(Text, comment='Applied Rule Ids')
    additional_data = Column(Text, comment='Additional Data')
    is_qty_decimal = Column(SMALLINT(5), comment='Is Qty Decimal')
    no_discount = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='No Discount')
    qty_backordered = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Qty Backordered')
    qty_canceled = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Qty Canceled')
    qty_invoiced = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Qty Invoiced')
    qty_ordered = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Qty Ordered')
    qty_refunded = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Qty Refunded')
    qty_shipped = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Qty Shipped')
    base_cost = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Base Cost')
    price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Price')
    base_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Base Price')
    original_price = Column(DECIMAL(12, 4), comment='Original Price')
    base_original_price = Column(DECIMAL(12, 4), comment='Base Original Price')
    tax_percent = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Tax Percent')
    tax_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Tax Amount')
    base_tax_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Tax Amount')
    tax_invoiced = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Tax Invoiced')
    base_tax_invoiced = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Tax Invoiced')
    discount_percent = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Discount Percent')
    discount_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Discount Amount')
    base_discount_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Discount Amount')
    discount_invoiced = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Discount Invoiced')
    base_discount_invoiced = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Discount Invoiced')
    amount_refunded = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Amount Refunded')
    base_amount_refunded = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Amount Refunded')
    row_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Row Total')
    base_row_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Row Total')
    row_invoiced = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Row Invoiced')
    base_row_invoiced = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Row Invoiced')
    row_weight = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Row Weight')
    base_tax_before_discount = Column(DECIMAL(20, 4), comment='Base Tax Before Discount')
    tax_before_discount = Column(DECIMAL(20, 4), comment='Tax Before Discount')
    ext_order_item_id = Column(String(255), comment='Ext Order Item ID')
    locked_do_invoice = Column(SMALLINT(5), comment='Locked Do Invoice')
    locked_do_ship = Column(SMALLINT(5), comment='Locked Do Ship')
    price_incl_tax = Column(DECIMAL(20, 4), comment='Price Incl Tax')
    base_price_incl_tax = Column(DECIMAL(20, 4), comment='Base Price Incl Tax')
    row_total_incl_tax = Column(DECIMAL(20, 4), comment='Row Total Incl Tax')
    base_row_total_incl_tax = Column(DECIMAL(20, 4), comment='Base Row Total Incl Tax')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    discount_tax_compensation_invoiced = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Invoiced')
    base_discount_tax_compensation_invoiced = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Invoiced')
    discount_tax_compensation_refunded = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Refunded')
    base_discount_tax_compensation_refunded = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Refunded')
    tax_canceled = Column(DECIMAL(12, 4), comment='Tax Canceled')
    discount_tax_compensation_canceled = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Canceled')
    tax_refunded = Column(DECIMAL(20, 4), comment='Tax Refunded')
    base_tax_refunded = Column(DECIMAL(20, 4), comment='Base Tax Refunded')
    discount_refunded = Column(DECIMAL(20, 4), comment='Discount Refunded')
    base_discount_refunded = Column(DECIMAL(20, 4), comment='Base Discount Refunded')
    gift_message_id = Column(INTEGER(11), comment='Gift Message ID')
    gift_message_available = Column(INTEGER(11), comment='Gift Message Available')
    free_shipping = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Free Shipping')
    weee_tax_applied = Column(Text, comment='Weee Tax Applied')
    weee_tax_applied_amount = Column(DECIMAL(12, 4), comment='Weee Tax Applied Amount')
    weee_tax_applied_row_amount = Column(DECIMAL(12, 4), comment='Weee Tax Applied Row Amount')
    weee_tax_disposition = Column(DECIMAL(12, 4), comment='Weee Tax Disposition')
    weee_tax_row_disposition = Column(DECIMAL(12, 4), comment='Weee Tax Row Disposition')
    base_weee_tax_applied_amount = Column(DECIMAL(12, 4), comment='Base Weee Tax Applied Amount')
    base_weee_tax_applied_row_amnt = Column(DECIMAL(12, 4), comment='Base Weee Tax Applied Row Amnt')
    base_weee_tax_disposition = Column(DECIMAL(12, 4), comment='Base Weee Tax Disposition')
    base_weee_tax_row_disposition = Column(DECIMAL(12, 4), comment='Base Weee Tax Row Disposition')

    order = relationship('SalesOrder')
    store = relationship('Store')


class SalesOrderPayment(Base):
    __tablename__ = 'sales_order_payment'
    __table_args__ = {'comment': 'Sales Flat Order Payment'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    base_shipping_captured = Column(DECIMAL(20, 4), comment='Base Shipping Captured')
    shipping_captured = Column(DECIMAL(20, 4), comment='Shipping Captured')
    amount_refunded = Column(DECIMAL(20, 4), comment='Amount Refunded')
    base_amount_paid = Column(DECIMAL(20, 4), comment='Base Amount Paid')
    amount_canceled = Column(DECIMAL(20, 4), comment='Amount Canceled')
    base_amount_authorized = Column(DECIMAL(20, 4), comment='Base Amount Authorized')
    base_amount_paid_online = Column(DECIMAL(20, 4), comment='Base Amount Paid Online')
    base_amount_refunded_online = Column(DECIMAL(20, 4), comment='Base Amount Refunded Online')
    base_shipping_amount = Column(DECIMAL(20, 4), comment='Base Shipping Amount')
    shipping_amount = Column(DECIMAL(20, 4), comment='Shipping Amount')
    amount_paid = Column(DECIMAL(20, 4), comment='Amount Paid')
    amount_authorized = Column(DECIMAL(20, 4), comment='Amount Authorized')
    base_amount_ordered = Column(DECIMAL(20, 4), comment='Base Amount Ordered')
    base_shipping_refunded = Column(DECIMAL(20, 4), comment='Base Shipping Refunded')
    shipping_refunded = Column(DECIMAL(20, 4), comment='Shipping Refunded')
    base_amount_refunded = Column(DECIMAL(20, 4), comment='Base Amount Refunded')
    amount_ordered = Column(DECIMAL(20, 4), comment='Amount Ordered')
    base_amount_canceled = Column(DECIMAL(20, 4), comment='Base Amount Canceled')
    quote_payment_id = Column(INTEGER(11), comment='Quote Payment ID')
    additional_data = Column(Text, comment='Additional Data')
    cc_exp_month = Column(String(12), comment='Cc Exp Month')
    cc_ss_start_year = Column(String(12), comment='Cc Ss Start Year')
    echeck_bank_name = Column(String(128), comment='Echeck Bank Name')
    method = Column(String(128), comment='Method')
    cc_debug_request_body = Column(String(32), comment='Cc Debug Request Body')
    cc_secure_verify = Column(String(32), comment='Cc Secure Verify')
    protection_eligibility = Column(String(32), comment='Protection Eligibility')
    cc_approval = Column(String(32), comment='Cc Approval')
    cc_last_4 = Column(String(100), comment='Cc Last 4')
    cc_status_description = Column(String(32), comment='Cc Status Description')
    echeck_type = Column(String(32), comment='Echeck Type')
    cc_debug_response_serialized = Column(String(32), comment='Cc Debug Response Serialized')
    cc_ss_start_month = Column(String(128), comment='Cc Ss Start Month')
    echeck_account_type = Column(String(255), comment='Echeck Account Type')
    last_trans_id = Column(String(255), comment='Last Trans ID')
    cc_cid_status = Column(String(32), comment='Cc Cid Status')
    cc_owner = Column(String(128), comment='Cc Owner')
    cc_type = Column(String(32), comment='Cc Type')
    po_number = Column(String(32), comment='Po Number')
    cc_exp_year = Column(String(4), comment='Cc Exp Year')
    cc_status = Column(String(4), comment='Cc Status')
    echeck_routing_number = Column(String(32), comment='Echeck Routing Number')
    account_status = Column(String(32), comment='Account Status')
    anet_trans_method = Column(String(32), comment='Anet Trans Method')
    cc_debug_response_body = Column(String(32), comment='Cc Debug Response Body')
    cc_ss_issue = Column(String(32), comment='Cc Ss Issue')
    echeck_account_name = Column(String(32), comment='Echeck Account Name')
    cc_avs_status = Column(String(32), comment='Cc Avs Status')
    cc_number_enc = Column(String(128))
    cc_trans_id = Column(String(32), comment='Cc Trans ID')
    address_status = Column(String(32), comment='Address Status')
    additional_information = Column(Text, comment='Additional Information')

    parent = relationship('SalesOrder')


class SalesOrderStatusHistory(Base):
    __tablename__ = 'sales_order_status_history'
    __table_args__ = {'comment': 'Sales Flat Order Status History'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    is_customer_notified = Column(INTEGER(11), comment='Is Customer Notified')
    is_visible_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible On Front')
    comment = Column(Text, comment='Comment')
    status = Column(String(32), comment='Status')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    entity_name = Column(String(32), comment='Shows what entity history is bind to.')

    parent = relationship('SalesOrder')


class SalesShipment(Base):
    __tablename__ = 'sales_shipment'
    __table_args__ = (
        Index('SALES_SHIPMENT_INCREMENT_ID_STORE_ID', 'increment_id', 'store_id', unique=True),
        {'comment': 'Sales Flat Shipment'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    total_weight = Column(DECIMAL(12, 4), comment='Total Weight')
    total_qty = Column(DECIMAL(12, 4), index=True, comment='Total Qty')
    email_sent = Column(SMALLINT(5), index=True, comment='Email Sent')
    send_email = Column(SMALLINT(5), index=True, comment='Send Email')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Order ID')
    customer_id = Column(INTEGER(11), comment='Customer ID')
    shipping_address_id = Column(INTEGER(11), comment='Shipping Address ID')
    billing_address_id = Column(INTEGER(11), comment='Billing Address ID')
    shipment_status = Column(INTEGER(11), comment='Shipment Status')
    increment_id = Column(String(50), comment='Increment ID')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    packages = Column(Text, comment='Packed Products in Packages')
    shipping_label = Column(MEDIUMBLOB, comment='Shipping Label Content')
    customer_note = Column(Text, comment='Customer Note')
    customer_note_notify = Column(SMALLINT(5), comment='Customer Note Notify')

    order = relationship('SalesOrder')
    store = relationship('Store')


class SalesCreditmemoComment(Base):
    __tablename__ = 'sales_creditmemo_comment'
    __table_args__ = {'comment': 'Sales Flat Creditmemo Comment'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_creditmemo.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    is_customer_notified = Column(INTEGER(11), comment='Is Customer Notified')
    is_visible_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible On Front')
    comment = Column(Text, comment='Comment')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')

    parent = relationship('SalesCreditmemo')


class SalesCreditmemoItem(Base):
    __tablename__ = 'sales_creditmemo_item'
    __table_args__ = {'comment': 'Sales Flat Creditmemo Item'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_creditmemo.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    base_price = Column(DECIMAL(12, 4), comment='Base Price')
    tax_amount = Column(DECIMAL(12, 4), comment='Tax Amount')
    base_row_total = Column(DECIMAL(12, 4), comment='Base Row Total')
    discount_amount = Column(DECIMAL(12, 4), comment='Discount Amount')
    row_total = Column(DECIMAL(12, 4), comment='Row Total')
    base_discount_amount = Column(DECIMAL(12, 4), comment='Base Discount Amount')
    price_incl_tax = Column(DECIMAL(12, 4), comment='Price Incl Tax')
    base_tax_amount = Column(DECIMAL(12, 4), comment='Base Tax Amount')
    base_price_incl_tax = Column(DECIMAL(12, 4), comment='Base Price Incl Tax')
    qty = Column(DECIMAL(12, 4), comment='Qty')
    base_cost = Column(DECIMAL(12, 4), comment='Base Cost')
    price = Column(DECIMAL(12, 4), comment='Price')
    base_row_total_incl_tax = Column(DECIMAL(12, 4), comment='Base Row Total Incl Tax')
    row_total_incl_tax = Column(DECIMAL(12, 4), comment='Row Total Incl Tax')
    product_id = Column(INTEGER(11), comment='Product ID')
    order_item_id = Column(INTEGER(11), comment='Order Item ID')
    additional_data = Column(Text, comment='Additional Data')
    description = Column(Text, comment='Description')
    sku = Column(String(255), comment='Sku')
    name = Column(String(255), comment='Name')
    discount_tax_compensation_amount = Column(DECIMAL(12, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(12, 4), comment='Base Discount Tax Compensation Amount')
    tax_ratio = Column(Text, comment='Ratio of tax in the creditmemo item over tax of the order item')
    weee_tax_applied = Column(Text, comment='Weee Tax Applied')
    weee_tax_applied_amount = Column(DECIMAL(12, 4), comment='Weee Tax Applied Amount')
    weee_tax_applied_row_amount = Column(DECIMAL(12, 4), comment='Weee Tax Applied Row Amount')
    weee_tax_disposition = Column(DECIMAL(12, 4), comment='Weee Tax Disposition')
    weee_tax_row_disposition = Column(DECIMAL(12, 4), comment='Weee Tax Row Disposition')
    base_weee_tax_applied_amount = Column(DECIMAL(12, 4), comment='Base Weee Tax Applied Amount')
    base_weee_tax_applied_row_amnt = Column(DECIMAL(12, 4), comment='Base Weee Tax Applied Row Amnt')
    base_weee_tax_disposition = Column(DECIMAL(12, 4), comment='Base Weee Tax Disposition')
    base_weee_tax_row_disposition = Column(DECIMAL(12, 4), comment='Base Weee Tax Row Disposition')

    parent = relationship('SalesCreditmemo')


class SalesInvoiceComment(Base):
    __tablename__ = 'sales_invoice_comment'
    __table_args__ = {'comment': 'Sales Flat Invoice Comment'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_invoice.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    is_customer_notified = Column(SMALLINT(5), comment='Is Customer Notified')
    is_visible_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible On Front')
    comment = Column(Text, comment='Comment')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')

    parent = relationship('SalesInvoice')


class SalesInvoiceItem(Base):
    __tablename__ = 'sales_invoice_item'
    __table_args__ = {'comment': 'Sales Flat Invoice Item'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_invoice.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    base_price = Column(DECIMAL(12, 4), comment='Base Price')
    tax_amount = Column(DECIMAL(12, 4), comment='Tax Amount')
    base_row_total = Column(DECIMAL(20, 4), comment='Base Row Total')
    discount_amount = Column(DECIMAL(12, 4), comment='Discount Amount')
    row_total = Column(DECIMAL(20, 4), comment='Row Total')
    base_discount_amount = Column(DECIMAL(12, 4), comment='Base Discount Amount')
    price_incl_tax = Column(DECIMAL(12, 4), comment='Price Incl Tax')
    base_tax_amount = Column(DECIMAL(12, 4), comment='Base Tax Amount')
    base_price_incl_tax = Column(DECIMAL(12, 4), comment='Base Price Incl Tax')
    qty = Column(DECIMAL(12, 4), comment='Qty')
    base_cost = Column(DECIMAL(12, 4), comment='Base Cost')
    price = Column(DECIMAL(12, 4), comment='Price')
    base_row_total_incl_tax = Column(DECIMAL(12, 4), comment='Base Row Total Incl Tax')
    row_total_incl_tax = Column(DECIMAL(12, 4), comment='Row Total Incl Tax')
    product_id = Column(INTEGER(11), comment='Product ID')
    order_item_id = Column(INTEGER(11), comment='Order Item ID')
    additional_data = Column(Text, comment='Additional Data')
    description = Column(Text, comment='Description')
    sku = Column(String(255), comment='Sku')
    name = Column(String(255), comment='Name')
    discount_tax_compensation_amount = Column(DECIMAL(12, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(12, 4), comment='Base Discount Tax Compensation Amount')
    tax_ratio = Column(Text, comment='Ratio of tax invoiced over tax of the order item')
    weee_tax_applied = Column(Text, comment='Weee Tax Applied')
    weee_tax_applied_amount = Column(DECIMAL(12, 4), comment='Weee Tax Applied Amount')
    weee_tax_applied_row_amount = Column(DECIMAL(12, 4), comment='Weee Tax Applied Row Amount')
    weee_tax_disposition = Column(DECIMAL(12, 4), comment='Weee Tax Disposition')
    weee_tax_row_disposition = Column(DECIMAL(12, 4), comment='Weee Tax Row Disposition')
    base_weee_tax_applied_amount = Column(DECIMAL(12, 4), comment='Base Weee Tax Applied Amount')
    base_weee_tax_applied_row_amnt = Column(DECIMAL(12, 4), comment='Base Weee Tax Applied Row Amnt')
    base_weee_tax_disposition = Column(DECIMAL(12, 4), comment='Base Weee Tax Disposition')
    base_weee_tax_row_disposition = Column(DECIMAL(12, 4), comment='Base Weee Tax Row Disposition')

    parent = relationship('SalesInvoice')


class SalesOrderTaxItem(Base):
    __tablename__ = 'sales_order_tax_item'
    __table_args__ = (
        Index('SALES_ORDER_TAX_ITEM_TAX_ID_ITEM_ID', 'tax_id', 'item_id', unique=True),
        {'comment': 'Sales Order Tax Item'}
    )

    tax_item_id = Column(INTEGER(10), primary_key=True, comment='Tax Item ID')
    tax_id = Column(ForeignKey('sales_order_tax.tax_id', ondelete='CASCADE'), nullable=False, comment='Tax ID')
    item_id = Column(ForeignKey('sales_order_item.item_id', ondelete='CASCADE'), index=True, comment='Item ID')
    tax_percent = Column(DECIMAL(12, 4), nullable=False, comment='Real Tax Percent For Item')
    amount = Column(DECIMAL(20, 4), nullable=False, comment='Tax amount for the item and tax rate')
    base_amount = Column(DECIMAL(20, 4), nullable=False, comment='Base tax amount for the item and tax rate')
    real_amount = Column(DECIMAL(20, 4), nullable=False, comment='Real tax amount for the item and tax rate')
    real_base_amount = Column(DECIMAL(20, 4), nullable=False, comment='Real base tax amount for the item and tax rate')
    associated_item_id = Column(ForeignKey('sales_order_item.item_id', ondelete='CASCADE'), index=True, comment='Id of the associated item')
    taxable_item_type = Column(String(32), nullable=False, comment='Type of the taxable item')

    associated_item = relationship('SalesOrderItem', primaryjoin='SalesOrderTaxItem.associated_item_id == SalesOrderItem.item_id')
    item = relationship('SalesOrderItem', primaryjoin='SalesOrderTaxItem.item_id == SalesOrderItem.item_id')
    tax = relationship('SalesOrderTax')


class SalesPaymentTransaction(Base):
    __tablename__ = 'sales_payment_transaction'
    __table_args__ = (
        Index('SALES_PAYMENT_TRANSACTION_ORDER_ID_PAYMENT_ID_TXN_ID', 'order_id', 'payment_id', 'txn_id', unique=True),
        {'comment': 'Sales Payment Transaction'}
    )

    transaction_id = Column(INTEGER(10), primary_key=True, comment='Transaction ID')
    parent_id = Column(ForeignKey('sales_payment_transaction.transaction_id', ondelete='CASCADE'), index=True, comment='Parent ID')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Order ID')
    payment_id = Column(ForeignKey('sales_order_payment.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Payment ID')
    txn_id = Column(String(100), comment='Txn ID')
    parent_txn_id = Column(String(100), comment='Parent Txn ID')
    txn_type = Column(String(15), comment='Txn Type')
    is_closed = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Closed')
    additional_information = Column(LargeBinary, comment='Additional Information')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')

    order = relationship('SalesOrder')
    parent = relationship('SalesPaymentTransaction', remote_side=[transaction_id])
    payment = relationship('SalesOrderPayment')


class SalesShipmentComment(Base):
    __tablename__ = 'sales_shipment_comment'
    __table_args__ = {'comment': 'Sales Flat Shipment Comment'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_shipment.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    is_customer_notified = Column(INTEGER(11), comment='Is Customer Notified')
    is_visible_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible On Front')
    comment = Column(Text, comment='Comment')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')

    parent = relationship('SalesShipment')


class SalesShipmentItem(Base):
    __tablename__ = 'sales_shipment_item'
    __table_args__ = {'comment': 'Sales Flat Shipment Item'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_shipment.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    row_total = Column(DECIMAL(20, 4), comment='Row Total')
    price = Column(DECIMAL(20, 4), comment='Price')
    weight = Column(DECIMAL(12, 4), comment='Weight')
    qty = Column(DECIMAL(12, 4), comment='Qty')
    product_id = Column(INTEGER(11), comment='Product ID')
    order_item_id = Column(INTEGER(11), comment='Order Item ID')
    additional_data = Column(Text, comment='Additional Data')
    description = Column(Text, comment='Description')
    name = Column(String(255), comment='Name')
    sku = Column(String(255), comment='Sku')

    parent = relationship('SalesShipment')


class SalesShipmentTrack(Base):
    __tablename__ = 'sales_shipment_track'
    __table_args__ = {'comment': 'Sales Flat Shipment Track'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    parent_id = Column(ForeignKey('sales_shipment.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    weight = Column(DECIMAL(12, 4), comment='Weight')
    qty = Column(DECIMAL(12, 4), comment='Qty')
    order_id = Column(INTEGER(10), nullable=False, index=True, comment='Order ID')
    track_number = Column(Text, comment='Number')
    description = Column(Text, comment='Description')
    title = Column(String(255), comment='Title')
    carrier_code = Column(String(32), comment='Carrier Code')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')

    parent = relationship('SalesShipment')
