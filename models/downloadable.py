# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, String, TIMESTAMP, Text, text
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


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class DownloadableLink(Base):
    __tablename__ = 'downloadable_link'
    __table_args__ = (
        Index('DOWNLOADABLE_LINK_PRODUCT_ID_SORT_ORDER', 'product_id', 'sort_order'),
        {'comment': 'Downloadable Link Table'}
    )

    link_id = Column(INTEGER(10), primary_key=True, comment='Link ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product ID')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort order')
    number_of_downloads = Column(INTEGER(11), comment='Number of downloads')
    is_shareable = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Shareable flag')
    link_url = Column(String(255), comment='Link Url')
    link_file = Column(String(255), comment='Link File')
    link_type = Column(String(20), comment='Link Type')
    sample_url = Column(String(255), comment='Sample Url')
    sample_file = Column(String(255), comment='Sample File')
    sample_type = Column(String(20), comment='Sample Type')

    product = relationship('CatalogProductEntity')


class DownloadableSample(Base):
    __tablename__ = 'downloadable_sample'
    __table_args__ = {'comment': 'Downloadable Sample Table'}

    sample_id = Column(INTEGER(10), primary_key=True, comment='Sample ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    sample_url = Column(String(255), comment='Sample URL')
    sample_file = Column(String(255), comment='Sample file')
    sample_type = Column(String(20), comment='Sample Type')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')

    product = relationship('CatalogProductEntity')


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


class DownloadableLinkPrice(Base):
    __tablename__ = 'downloadable_link_price'
    __table_args__ = {'comment': 'Downloadable Link Price Table'}

    price_id = Column(INTEGER(10), primary_key=True, comment='Price ID')
    link_id = Column(ForeignKey('downloadable_link.link_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Link ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Price')

    link = relationship('DownloadableLink')
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


class DownloadableLinkTitle(Base):
    __tablename__ = 'downloadable_link_title'
    __table_args__ = (
        Index('DOWNLOADABLE_LINK_TITLE_LINK_ID_STORE_ID', 'link_id', 'store_id', unique=True),
        {'comment': 'Link Title Table'}
    )

    title_id = Column(INTEGER(10), primary_key=True, comment='Title ID')
    link_id = Column(ForeignKey('downloadable_link.link_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Link ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    title = Column(String(255), comment='Title')

    link = relationship('DownloadableLink')
    store = relationship('Store')


class DownloadableSampleTitle(Base):
    __tablename__ = 'downloadable_sample_title'
    __table_args__ = (
        Index('DOWNLOADABLE_SAMPLE_TITLE_SAMPLE_ID_STORE_ID', 'sample_id', 'store_id', unique=True),
        {'comment': 'Downloadable Sample Title Table'}
    )

    title_id = Column(INTEGER(10), primary_key=True, comment='Title ID')
    sample_id = Column(ForeignKey('downloadable_sample.sample_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Sample ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    title = Column(String(255), comment='Title')

    sample = relationship('DownloadableSample')
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


class DownloadableLinkPurchased(Base):
    __tablename__ = 'downloadable_link_purchased'
    __table_args__ = {'comment': 'Downloadable Link Purchased Table'}

    purchased_id = Column(INTEGER(10), primary_key=True, comment='Purchased ID')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='SET NULL'), index=True, server_default=text("0"), comment='Order ID')
    order_increment_id = Column(String(50), comment='Order Increment ID')
    order_item_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Order Item ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Date of creation')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Date of modification')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='SET NULL'), index=True, server_default=text("0"), comment='Customer ID')
    product_name = Column(String(255), comment='Product name')
    product_sku = Column(String(255), comment='Product sku')
    link_section_title = Column(String(255), comment='Link_section_title')

    customer = relationship('CustomerEntity')
    order = relationship('SalesOrder')


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


class DownloadableLinkPurchasedItem(Base):
    __tablename__ = 'downloadable_link_purchased_item'
    __table_args__ = {'comment': 'Downloadable Link Purchased Item Table'}

    item_id = Column(INTEGER(10), primary_key=True, comment='Item ID')
    purchased_id = Column(ForeignKey('downloadable_link_purchased.purchased_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Purchased ID')
    order_item_id = Column(ForeignKey('sales_order_item.item_id', ondelete='SET NULL'), index=True, server_default=text("0"), comment='Order Item ID')
    product_id = Column(INTEGER(10), server_default=text("0"), comment='Product ID')
    link_hash = Column(String(255), index=True, comment='Link hash')
    number_of_downloads_bought = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Number of downloads bought')
    number_of_downloads_used = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Number of downloads used')
    link_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Link ID')
    link_title = Column(String(255), comment='Link Title')
    is_shareable = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Shareable Flag')
    link_url = Column(String(255), comment='Link Url')
    link_file = Column(String(255), comment='Link File')
    link_type = Column(String(255), comment='Link Type')
    status = Column(String(50), comment='Status')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Creation Time')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Update Time')

    order_item = relationship('SalesOrderItem')
    purchased = relationship('DownloadableLinkPurchased')
