# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AmazonPendingAuthorization(Base):
    __tablename__ = 'amazon_pending_authorization'
    __table_args__ = (
        Index('UNQ_E6CCA08713FB32BB136A56837009C371', 'order_id', 'payment_id', 'authorization_id', unique=True),
        {'comment': 'amazon_pending_authorization'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity_id')
    order_id = Column(INTEGER(10), nullable=False, comment='Order_id')
    payment_id = Column(INTEGER(10), nullable=False, comment='Payment_id')
    authorization_id = Column(String(255), comment='Authorization_id')
    created_at = Column(DateTime, nullable=False, comment='Created_at')
    updated_at = Column(DateTime, comment='Updated_at')
    processed = Column(SMALLINT(5), server_default=text("0"), comment='Initial authorization processed')
    capture = Column(SMALLINT(5), server_default=text("0"), comment='Initial authorization has capture')
    capture_id = Column(String(255), comment='Initial authorization capture id')


class AmazonPendingCapture(Base):
    __tablename__ = 'amazon_pending_capture'
    __table_args__ = (
        Index('AMAZON_PENDING_CAPTURE_ORDER_ID_PAYMENT_ID_CAPTURE_ID', 'order_id', 'payment_id', 'capture_id', unique=True),
        {'comment': 'amazon_pending_capture'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity_id')
    capture_id = Column(String(255), nullable=False, comment='Capture_id')
    created_at = Column(DateTime, nullable=False, comment='Created_at')
    order_id = Column(INTEGER(10), nullable=False, comment='order id')
    payment_id = Column(INTEGER(10), nullable=False, comment='payment id')


class AmazonPendingRefund(Base):
    __tablename__ = 'amazon_pending_refund'
    __table_args__ = (
        Index('AMAZON_PENDING_REFUND_ORDER_ID_PAYMENT_ID_REFUND_ID', 'order_id', 'payment_id', 'refund_id', unique=True),
        {'comment': 'amazon_pending_refund'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity_id')
    refund_id = Column(String(255), nullable=False, comment='Refund_id')
    created_at = Column(DateTime, nullable=False, comment='Created_at')
    order_id = Column(INTEGER(10), nullable=False, comment='Order_id')
    payment_id = Column(INTEGER(10), nullable=False, comment='Payment_id')


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


class Quote(Base):
    __tablename__ = 'quote'
    __table_args__ = (
        Index('QUOTE_CUSTOMER_ID_STORE_ID_IS_ACTIVE', 'customer_id', 'store_id', 'is_active'),
        {'comment': 'Sales Flat Quote'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    converted_at = Column(TIMESTAMP, comment='Converted At')
    is_active = Column(SMALLINT(5), server_default=text("1"), comment='Is Active')
    is_virtual = Column(SMALLINT(5), server_default=text("0"), comment='Is Virtual')
    is_multi_shipping = Column(SMALLINT(5), server_default=text("0"), comment='Is Multi Shipping')
    items_count = Column(INTEGER(10), server_default=text("0"), comment='Items Count')
    items_qty = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Items Qty')
    orig_order_id = Column(INTEGER(10), server_default=text("0"), comment='Orig Order ID')
    store_to_base_rate = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Store To Base Rate')
    store_to_quote_rate = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Store To Quote Rate')
    base_currency_code = Column(String(255), comment='Base Currency Code')
    store_currency_code = Column(String(255), comment='Store Currency Code')
    quote_currency_code = Column(String(255), comment='Quote Currency Code')
    grand_total = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Grand Total')
    base_grand_total = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Grand Total')
    checkout_method = Column(String(255), comment='Checkout Method')
    customer_id = Column(INTEGER(10), comment='Customer ID')
    customer_tax_class_id = Column(INTEGER(10), comment='Customer Tax Class ID')
    customer_group_id = Column(INTEGER(10), server_default=text("0"), comment='Customer Group ID')
    customer_email = Column(String(255), comment='Customer Email')
    customer_prefix = Column(String(40), comment='Customer Prefix')
    customer_firstname = Column(String(255), comment='Customer Firstname')
    customer_middlename = Column(String(40), comment='Customer Middlename')
    customer_lastname = Column(String(255), comment='Customer Lastname')
    customer_suffix = Column(String(40), comment='Customer Suffix')
    customer_dob = Column(DateTime, comment='Customer Dob')
    customer_note = Column(String(255), comment='Customer Note')
    customer_note_notify = Column(SMALLINT(5), server_default=text("1"), comment='Customer Note Notify')
    customer_is_guest = Column(SMALLINT(5), server_default=text("0"), comment='Customer Is Guest')
    remote_ip = Column(String(45), comment='Remote Ip')
    applied_rule_ids = Column(String(255), comment='Applied Rule Ids')
    reserved_order_id = Column(String(64), comment='Reserved Order ID')
    password_hash = Column(String(255), comment='Password Hash')
    coupon_code = Column(String(255), comment='Coupon Code')
    global_currency_code = Column(String(255), comment='Global Currency Code')
    base_to_global_rate = Column(DECIMAL(20, 4), comment='Base To Global Rate')
    base_to_quote_rate = Column(DECIMAL(20, 4), comment='Base To Quote Rate')
    customer_taxvat = Column(String(255), comment='Customer Taxvat')
    customer_gender = Column(String(255), comment='Customer Gender')
    subtotal = Column(DECIMAL(20, 4), comment='Subtotal')
    base_subtotal = Column(DECIMAL(20, 4), comment='Base Subtotal')
    subtotal_with_discount = Column(DECIMAL(20, 4), comment='Subtotal With Discount')
    base_subtotal_with_discount = Column(DECIMAL(20, 4), comment='Base Subtotal With Discount')
    is_changed = Column(INTEGER(10), comment='Is Changed')
    trigger_recollect = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Trigger Recollect')
    ext_shipping_info = Column(Text, comment='Ext Shipping Info')
    gift_message_id = Column(INTEGER(11), comment='Gift Message ID')
    is_persistent = Column(SMALLINT(5), server_default=text("0"), comment='Is Quote Persistent')

    store = relationship('Store')


class AmazonCustomer(Base):
    __tablename__ = 'amazon_customer'
    __table_args__ = (
        Index('AMAZON_CUSTOMER_CUSTOMER_ID_AMAZON_ID', 'customer_id', 'amazon_id', unique=True),
        {'comment': 'amazon_customer'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity_id')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, unique=True, comment='Customer_id')
    amazon_id = Column(String(255), nullable=False, comment='Amazon_id')

    customer = relationship('CustomerEntity')


class AmazonQuote(Base):
    __tablename__ = 'amazon_quote'
    __table_args__ = {'comment': 'amazon_quote'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    quote_id = Column(ForeignKey('quote.entity_id', ondelete='CASCADE'), nullable=False, unique=True, comment='Quote ID')
    amazon_order_reference_id = Column(String(255), nullable=False, comment='Amazon Order Reference ID')
    sandbox_simulation_reference = Column(String(255), comment='Sandbox simulation reference')
    confirmed = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Quote confirmed with Amazon')

    quote = relationship('Quote')


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


class AmazonSalesOrder(Base):
    __tablename__ = 'amazon_sales_order'
    __table_args__ = {'comment': 'amazon_sales_order'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, unique=True, comment='Order ID')
    amazon_order_reference_id = Column(String(255), nullable=False, comment='Amazon Order Reference ID')

    order = relationship('SalesOrder')
