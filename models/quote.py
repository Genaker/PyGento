# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Index, String, TIMESTAMP, Text, text
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


class QuoteAddres(Base):
    __tablename__ = 'quote_address'
    __table_args__ = {'comment': 'Sales Flat Quote Address'}

    address_id = Column(INTEGER(10), primary_key=True, comment='Address ID')
    quote_id = Column(ForeignKey('quote.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Quote ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    customer_id = Column(INTEGER(10), comment='Customer ID')
    save_in_address_book = Column(SMALLINT(6), server_default=text("0"), comment='Save In Address Book')
    customer_address_id = Column(INTEGER(10), comment='Customer Address ID')
    address_type = Column(String(10), comment='Address Type')
    email = Column(String(255), comment='Email')
    prefix = Column(String(40), comment='Prefix')
    firstname = Column(String(255))
    middlename = Column(String(40))
    lastname = Column(String(255))
    suffix = Column(String(40), comment='Suffix')
    company = Column(String(255), comment='Company')
    street = Column(String(255), comment='Street')
    city = Column(String(255))
    region = Column(String(255))
    region_id = Column(INTEGER(10), comment='Region ID')
    postcode = Column(String(20), comment='Postcode')
    country_id = Column(String(30), comment='Country ID')
    telephone = Column(String(255))
    fax = Column(String(255))
    same_as_billing = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Same As Billing')
    collect_shipping_rates = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Collect Shipping Rates')
    shipping_method = Column(String(120))
    shipping_description = Column(String(255), comment='Shipping Description')
    weight = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Weight')
    subtotal = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal')
    base_subtotal = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Subtotal')
    subtotal_with_discount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Subtotal With Discount')
    base_subtotal_with_discount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Subtotal With Discount')
    tax_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Tax Amount')
    base_tax_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Tax Amount')
    shipping_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Shipping Amount')
    base_shipping_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Shipping Amount')
    shipping_tax_amount = Column(DECIMAL(20, 4), comment='Shipping Tax Amount')
    base_shipping_tax_amount = Column(DECIMAL(20, 4), comment='Base Shipping Tax Amount')
    discount_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Discount Amount')
    base_discount_amount = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Discount Amount')
    grand_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Grand Total')
    base_grand_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Grand Total')
    customer_notes = Column(Text, comment='Customer Notes')
    applied_taxes = Column(Text, comment='Applied Taxes')
    discount_description = Column(String(255), comment='Discount Description')
    shipping_discount_amount = Column(DECIMAL(20, 4), comment='Shipping Discount Amount')
    base_shipping_discount_amount = Column(DECIMAL(20, 4), comment='Base Shipping Discount Amount')
    subtotal_incl_tax = Column(DECIMAL(20, 4), comment='Subtotal Incl Tax')
    base_subtotal_total_incl_tax = Column(DECIMAL(20, 4), comment='Base Subtotal Total Incl Tax')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    shipping_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Shipping Discount Tax Compensation Amount')
    base_shipping_discount_tax_compensation_amnt = Column(DECIMAL(20, 4), comment='Base Shipping Discount Tax Compensation Amount')
    shipping_incl_tax = Column(DECIMAL(20, 4), comment='Shipping Incl Tax')
    base_shipping_incl_tax = Column(DECIMAL(20, 4), comment='Base Shipping Incl Tax')
    vat_id = Column(Text, comment='Vat ID')
    vat_is_valid = Column(SMALLINT(6), comment='Vat Is Valid')
    vat_request_id = Column(Text, comment='Vat Request ID')
    vat_request_date = Column(Text, comment='Vat Request Date')
    vat_request_success = Column(SMALLINT(6), comment='Vat Request Success')
    validated_country_code = Column(Text, comment='Validated Country Code')
    validated_vat_number = Column(Text, comment='Validated Vat Number')
    gift_message_id = Column(INTEGER(11), comment='Gift Message ID')
    free_shipping = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Free Shipping')

    quote = relationship('Quote')


class QuoteIdMask(Base):
    __tablename__ = 'quote_id_mask'
    __table_args__ = {'comment': 'Quote ID and masked ID mapping'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    quote_id = Column(ForeignKey('quote.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Quote ID')
    masked_id = Column(String(32), index=True, comment='Masked ID')

    quote = relationship('Quote')


class QuoteItem(Base):
    __tablename__ = 'quote_item'
    __table_args__ = {'comment': 'Sales Flat Quote Item'}

    item_id = Column(INTEGER(10), primary_key=True, comment='Item ID')
    quote_id = Column(ForeignKey('quote.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Quote ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    product_id = Column(INTEGER(10), index=True, comment='Product ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    parent_item_id = Column(ForeignKey('quote_item.item_id', ondelete='CASCADE'), index=True, comment='Parent Item ID')
    is_virtual = Column(SMALLINT(5), comment='Is Virtual')
    sku = Column(String(255), comment='Sku')
    name = Column(String(255), comment='Name')
    description = Column(Text, comment='Description')
    applied_rule_ids = Column(Text, comment='Applied Rule Ids')
    additional_data = Column(Text, comment='Additional Data')
    is_qty_decimal = Column(SMALLINT(5), comment='Is Qty Decimal')
    no_discount = Column(SMALLINT(5), server_default=text("0"), comment='No Discount')
    weight = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Weight')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Price')
    base_price = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Base Price')
    custom_price = Column(DECIMAL(12, 4), comment='Custom Price')
    discount_percent = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Discount Percent')
    discount_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Discount Amount')
    base_discount_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Discount Amount')
    tax_percent = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Tax Percent')
    tax_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Tax Amount')
    base_tax_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Tax Amount')
    row_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Row Total')
    base_row_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Row Total')
    row_total_with_discount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Row Total With Discount')
    row_weight = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Row Weight')
    product_type = Column(String(255), comment='Product Type')
    base_tax_before_discount = Column(DECIMAL(20, 4), comment='Base Tax Before Discount')
    tax_before_discount = Column(DECIMAL(20, 4), comment='Tax Before Discount')
    original_custom_price = Column(DECIMAL(12, 4), comment='Original Custom Price')
    redirect_url = Column(String(255), comment='Redirect Url')
    base_cost = Column(DECIMAL(12, 4), comment='Base Cost')
    price_incl_tax = Column(DECIMAL(20, 4), comment='Price Incl Tax')
    base_price_incl_tax = Column(DECIMAL(20, 4), comment='Base Price Incl Tax')
    row_total_incl_tax = Column(DECIMAL(20, 4), comment='Row Total Incl Tax')
    base_row_total_incl_tax = Column(DECIMAL(20, 4), comment='Base Row Total Incl Tax')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    gift_message_id = Column(INTEGER(11), comment='Gift Message ID')
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

    parent_item = relationship('QuoteItem', remote_side=[item_id])
    quote = relationship('Quote')
    store = relationship('Store')


class QuotePayment(Base):
    __tablename__ = 'quote_payment'
    __table_args__ = {'comment': 'Sales Flat Quote Payment'}

    payment_id = Column(INTEGER(10), primary_key=True, comment='Payment ID')
    quote_id = Column(ForeignKey('quote.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Quote ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    method = Column(String(255), comment='Method')
    cc_type = Column(String(255), comment='Cc Type')
    cc_number_enc = Column(String(255), comment='Cc Number Enc')
    cc_last_4 = Column(String(255), comment='Cc Last 4')
    cc_cid_enc = Column(String(255), comment='Cc Cid Enc')
    cc_owner = Column(String(255), comment='Cc Owner')
    cc_exp_month = Column(String(255), comment='Cc Exp Month')
    cc_exp_year = Column(SMALLINT(5), server_default=text("0"), comment='Cc Exp Year')
    cc_ss_owner = Column(String(255), comment='Cc Ss Owner')
    cc_ss_start_month = Column(SMALLINT(5), server_default=text("0"), comment='Cc Ss Start Month')
    cc_ss_start_year = Column(SMALLINT(5), server_default=text("0"), comment='Cc Ss Start Year')
    po_number = Column(String(255), comment='Po Number')
    additional_data = Column(Text, comment='Additional Data')
    cc_ss_issue = Column(String(255), comment='Cc Ss Issue')
    additional_information = Column(Text, comment='Additional Information')
    paypal_payer_id = Column(String(255), comment='Paypal Payer ID')
    paypal_payer_status = Column(String(255), comment='Paypal Payer Status')
    paypal_correlation_id = Column(String(255), comment='Paypal Correlation ID')

    quote = relationship('Quote')


class QuoteAddressItem(Base):
    __tablename__ = 'quote_address_item'
    __table_args__ = {'comment': 'Sales Flat Quote Address Item'}

    address_item_id = Column(INTEGER(10), primary_key=True, comment='Address Item ID')
    parent_item_id = Column(ForeignKey('quote_address_item.address_item_id', ondelete='CASCADE'), index=True, comment='Parent Item ID')
    quote_address_id = Column(ForeignKey('quote_address.address_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Quote Address ID')
    quote_item_id = Column(ForeignKey('quote_item.item_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Quote Item ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    applied_rule_ids = Column(Text, comment='Applied Rule Ids')
    additional_data = Column(Text, comment='Additional Data')
    weight = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Weight')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    discount_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Discount Amount')
    tax_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Tax Amount')
    row_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Row Total')
    base_row_total = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Base Row Total')
    row_total_with_discount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Row Total With Discount')
    base_discount_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Discount Amount')
    base_tax_amount = Column(DECIMAL(20, 4), server_default=text("0.0000"), comment='Base Tax Amount')
    row_weight = Column(DECIMAL(12, 4), server_default=text("0.0000"), comment='Row Weight')
    product_id = Column(INTEGER(10), comment='Product ID')
    super_product_id = Column(INTEGER(10), comment='Super Product ID')
    parent_product_id = Column(INTEGER(10), comment='Parent Product ID')
    store_id = Column(SMALLINT(5), index=True, comment='Store ID')
    sku = Column(String(255), comment='Sku')
    image = Column(String(255), comment='Image')
    name = Column(String(255), comment='Name')
    description = Column(Text, comment='Description')
    is_qty_decimal = Column(INTEGER(10), comment='Is Qty Decimal')
    price = Column(DECIMAL(12, 4), comment='Price')
    discount_percent = Column(DECIMAL(12, 4), comment='Discount Percent')
    no_discount = Column(INTEGER(10), comment='No Discount')
    tax_percent = Column(DECIMAL(12, 4), comment='Tax Percent')
    base_price = Column(DECIMAL(12, 4), comment='Base Price')
    base_cost = Column(DECIMAL(12, 4), comment='Base Cost')
    price_incl_tax = Column(DECIMAL(20, 4), comment='Price Incl Tax')
    base_price_incl_tax = Column(DECIMAL(20, 4), comment='Base Price Incl Tax')
    row_total_incl_tax = Column(DECIMAL(20, 4), comment='Row Total Incl Tax')
    base_row_total_incl_tax = Column(DECIMAL(20, 4), comment='Base Row Total Incl Tax')
    discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Discount Tax Compensation Amount')
    base_discount_tax_compensation_amount = Column(DECIMAL(20, 4), comment='Base Discount Tax Compensation Amount')
    gift_message_id = Column(INTEGER(11), comment='Gift Message ID')
    free_shipping = Column(INTEGER(10), comment='Free Shipping')

    parent_item = relationship('QuoteAddressItem', remote_side=[address_item_id])
    quote_address = relationship('QuoteAddres')
    quote_item = relationship('QuoteItem')


class QuoteItemOption(Base):
    __tablename__ = 'quote_item_option'
    __table_args__ = {'comment': 'Sales Flat Quote Item Option'}

    option_id = Column(INTEGER(10), primary_key=True, comment='Option ID')
    item_id = Column(ForeignKey('quote_item.item_id', ondelete='CASCADE'), nullable=False, index=True, comment='Item ID')
    product_id = Column(INTEGER(10), nullable=False, comment='Product ID')
    code = Column(String(255), nullable=False, comment='Code')
    value = Column(Text, comment='Value')

    item = relationship('QuoteItem')


class QuoteShippingRate(Base):
    __tablename__ = 'quote_shipping_rate'
    __table_args__ = {'comment': 'Sales Flat Quote Shipping Rate'}

    rate_id = Column(INTEGER(10), primary_key=True, comment='Rate ID')
    address_id = Column(ForeignKey('quote_address.address_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Address ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    carrier = Column(String(255), comment='Carrier')
    carrier_title = Column(String(255), comment='Carrier Title')
    code = Column(String(255), comment='Code')
    method = Column(String(255), comment='Method')
    method_description = Column(Text, comment='Method Description')
    price = Column(DECIMAL(20, 4), nullable=False, server_default=text("0.0000"), comment='Price')
    error_message = Column(Text, comment='Error Message')
    method_title = Column(Text, comment='Method Title')

    address = relationship('QuoteAddres')
