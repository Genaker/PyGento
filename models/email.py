# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, LargeBinary, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB, SMALLINT, TINYINT
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


class EmailAbandonedCart(Base):
    __tablename__ = 'email_abandoned_cart'
    __table_args__ = {'comment': 'Abandoned Carts Table'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    quote_id = Column(INTEGER(10), index=True, comment='Quote Id')
    store_id = Column(SMALLINT(5), index=True, comment='Store Id')
    customer_id = Column(INTEGER(10), index=True, comment='Customer ID')
    email = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Email')
    status = Column(String(255), nullable=False, server_default=text("''"), comment='Contact Status')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Quote Active')
    quote_updated_at = Column(TIMESTAMP, comment='Quote updated at')
    abandoned_cart_number = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Abandoned Cart number')
    items_count = Column(SMALLINT(5), server_default=text("0"), comment='Quote items count')
    items_ids = Column(String(255), comment='Quote item ids')
    created_at = Column(TIMESTAMP, comment='Created At')
    updated_at = Column(TIMESTAMP, comment='Updated at')


class EmailAutomation(Base):
    __tablename__ = 'email_automation'
    __table_args__ = {'comment': 'Automation Status'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    automation_type = Column(String(255), index=True, comment='Automation Type')
    store_name = Column(String(255), comment='Automation Type')
    enrolment_status = Column(String(255), nullable=False, index=True, comment='Enrolment Status')
    email = Column(String(255), index=True, comment='Email')
    type_id = Column(String(255), index=True, comment='Type ID')
    program_id = Column(String(255), index=True, comment='Program ID')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website Id')
    message = Column(String(255), nullable=False, comment='Message')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')


class EmailFailedAuth(Base):
    __tablename__ = 'email_failed_auth'
    __table_args__ = {'comment': 'Email Failed Auth Table.'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    failures_num = Column(INTEGER(10), comment='Number of fails')
    first_attempt_date = Column(DateTime, comment='First attempt date')
    last_attempt_date = Column(DateTime, comment='Last attempt date')
    url = Column(String(255), comment='URL')
    store_id = Column(INTEGER(10), index=True, comment='Store Id')


class EmailImporter(Base):
    __tablename__ = 'email_importer'
    __table_args__ = {'comment': 'Email Importer'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    import_type = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Import Type')
    website_id = Column(SMALLINT(6), nullable=False, index=True, server_default=text("0"), comment='Website Id')
    import_status = Column(SMALLINT(6), nullable=False, index=True, server_default=text("0"), comment='Import Status')
    import_id = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Import Id')
    import_data = Column(MEDIUMBLOB, nullable=False, server_default=text("''"), comment='Import Data')
    import_mode = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Import Mode')
    import_file = Column(Text, nullable=False, server_default=text("''"), comment='Import File')
    message = Column(String(255), nullable=False, server_default=text("''"), comment='Error Message')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')
    import_started = Column(TIMESTAMP, index=True, comment='Import Started')
    import_finished = Column(TIMESTAMP, index=True, comment='Import Finished')


class EmailReview(Base):
    __tablename__ = 'email_review'
    __table_args__ = {'comment': 'Connector Reviews'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    review_id = Column(INTEGER(10), nullable=False, index=True, comment='Review Id')
    customer_id = Column(INTEGER(10), nullable=False, index=True, comment='Customer ID')
    store_id = Column(SMALLINT(5), nullable=False, index=True, comment='Store Id')
    review_imported = Column(SMALLINT(5), index=True, comment='Review Imported')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')


class EmailRule(Base):
    __tablename__ = 'email_rules'
    __table_args__ = {'comment': 'Connector Rules'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    name = Column(String(255), nullable=False, server_default=text("''"), comment='Rule Name')
    website_ids = Column(String(255), nullable=False, server_default=text("'0'"), comment='Website Id')
    type = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Rule Type')
    status = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Status')
    combination = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Rule Condition')
    conditions = Column(LargeBinary, nullable=False, comment='Rule Conditions')
    created_at = Column(TIMESTAMP, comment='Creation Time')
    updated_at = Column(TIMESTAMP, comment='Update Time')


class EmailTemplate(Base):
    __tablename__ = 'email_template'
    __table_args__ = {'comment': 'Email Templates'}

    template_id = Column(INTEGER(10), primary_key=True, comment='Template ID')
    template_code = Column(String(150), nullable=False, unique=True, comment='Template Name')
    template_text = Column(Text, nullable=False, comment='Template Content')
    template_styles = Column(Text, comment='Templste Styles')
    template_type = Column(INTEGER(10), comment='Template Type')
    template_subject = Column(String(200), nullable=False, comment='Template Subject')
    template_sender_name = Column(String(200), comment='Template Sender Name')
    template_sender_email = Column(String(200), comment='Template Sender Email')
    added_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Date of Template Creation')
    modified_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Date of Template Modification')
    orig_template_code = Column(String(200), comment='Original Template Code')
    orig_template_variables = Column(Text, comment='Original Template Variables')
    is_legacy = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Should the template render in legacy mode')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class EmailCatalog(Base):
    __tablename__ = 'email_catalog'
    __table_args__ = {'comment': 'Connector Catalog'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product Id')
    imported = Column(SMALLINT(5), comment='Product imported [deprecated]')
    modified = Column(SMALLINT(5), comment='Product modified [deprecated]')
    processed = Column(SMALLINT(5), nullable=False, index=True, comment='Product processed')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')
    last_imported_at = Column(TIMESTAMP, index=True, comment='Last imported date')

    product = relationship('CatalogProductEntity')


class EmailContact(Base):
    __tablename__ = 'email_contact'
    __table_args__ = {'comment': 'Connector Contacts'}

    email_contact_id = Column(INTEGER(10), primary_key=True, index=True, comment='Primary Key')
    is_guest = Column(SMALLINT(5), index=True, comment='Is Guest')
    contact_id = Column(String(15), index=True, comment='Connector Contact ID')
    customer_id = Column(INTEGER(10), nullable=False, index=True, comment='Customer ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    store_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store ID')
    email = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Customer Email')
    is_subscriber = Column(SMALLINT(5), index=True, comment='Is Subscriber')
    subscriber_status = Column(SMALLINT(5), index=True, comment='Subscriber status')
    email_imported = Column(SMALLINT(5), index=True, comment='Is Imported')
    subscriber_imported = Column(SMALLINT(5), index=True, comment='Subscriber Imported')
    suppressed = Column(SMALLINT(5), index=True, comment='Is Suppressed')
    last_subscribed_at = Column(TIMESTAMP, comment='Last time user subscribed')

    website = relationship('StoreWebsite')


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


class EmailContactConsent(Base):
    __tablename__ = 'email_contact_consent'
    __table_args__ = {'comment': 'Email contact consent table.'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    email_contact_id = Column(ForeignKey('email_contact.email_contact_id', ondelete='CASCADE'), index=True, comment='Email Contact Id')
    consent_url = Column(String(255), comment='Contact consent url')
    consent_datetime = Column(DateTime, comment='Contact consent datetime')
    consent_ip = Column(String(255), comment='Contact consent ip')
    consent_user_agent = Column(String(255), comment='Contact consent user agent')

    email_contact = relationship('EmailContact')


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


class EmailCampaign(Base):
    __tablename__ = 'email_campaign'
    __table_args__ = {'comment': 'Connector Campaigns'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    campaign_id = Column(INTEGER(10), nullable=False, index=True, comment='Campaign ID')
    email = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Contact Email')
    customer_id = Column(INTEGER(10), nullable=False, index=True, comment='Customer ID')
    sent_at = Column(TIMESTAMP, index=True, comment='Send Date')
    order_increment_id = Column(String(50), nullable=False, comment='Order Increment ID')
    quote_id = Column(INTEGER(10), nullable=False, index=True, comment='Sales Quote ID')
    message = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Error Message')
    checkout_method = Column(String(255), nullable=False, server_default=text("''"), comment='Checkout Method Used')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    event_name = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Event Name')
    send_id = Column(String(255), nullable=False, index=True, server_default=text("''"), comment='Send Id')
    send_status = Column(SMALLINT(6), nullable=False, index=True, server_default=text("0"), comment='Campaign send status')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')

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


class Wishlist(Base):
    __tablename__ = 'wishlist'
    __table_args__ = {'comment': 'Wishlist main Table'}

    wishlist_id = Column(INTEGER(10), primary_key=True, comment='Wishlist ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, unique=True, server_default=text("0"), comment='Customer ID')
    shared = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sharing flag (0 or 1)')
    sharing_code = Column(String(32), comment='Sharing encrypted code')
    updated_at = Column(TIMESTAMP, comment='Last updated date')

    customer = relationship('CustomerEntity')


class EmailOrder(Base):
    __tablename__ = 'email_order'
    __table_args__ = {'comment': 'Transactional Order Data'}

    email_order_id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    order_id = Column(ForeignKey('sales_order.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Order ID')
    order_status = Column(String(255), nullable=False, index=True, comment='Order Status')
    quote_id = Column(INTEGER(10), nullable=False, index=True, comment='Sales Quote ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    email_imported = Column(SMALLINT(5), index=True, comment='Is Order Imported')
    modified = Column(SMALLINT(5), index=True, comment='Is Order Modified')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')

    order = relationship('SalesOrder')
    store = relationship('Store')


class EmailWishlist(Base):
    __tablename__ = 'email_wishlist'
    __table_args__ = {'comment': 'Connector Wishlist'}

    id = Column(INTEGER(10), primary_key=True, comment='Primary Key')
    wishlist_id = Column(ForeignKey('wishlist.wishlist_id', ondelete='CASCADE'), nullable=False, index=True, comment='Wishlist Id')
    item_count = Column(INTEGER(10), nullable=False, index=True, comment='Item Count')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), index=True, comment='Customer ID')
    store_id = Column(SMALLINT(5), nullable=False, index=True, comment='Store Id')
    wishlist_imported = Column(SMALLINT(5), index=True, comment='Wishlist Imported')
    wishlist_modified = Column(SMALLINT(5), index=True, comment='Wishlist Modified')
    created_at = Column(TIMESTAMP, index=True, comment='Creation Time')
    updated_at = Column(TIMESTAMP, index=True, comment='Update Time')

    customer = relationship('CustomerEntity')
    wishlist = relationship('Wishlist')
