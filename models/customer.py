# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomerGridFlat(Base):
    __tablename__ = 'customer_grid_flat'
    __table_args__ = (
        Index('FTI_8746F705702DD5F6D45B8C7CE7FE9F2F', 'name', 'email', 'created_in', 'taxvat', 'shipping_full', 'billing_full', 'billing_firstname', 'billing_lastname', 'billing_telephone', 'billing_postcode', 'billing_region', 'billing_city', 'billing_fax', 'billing_company'),
        {'comment': 'customer_grid_flat'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    name = Column(Text, comment='Name')
    email = Column(String(255), comment='Email')
    group_id = Column(INTEGER(11), index=True, comment='Group_id')
    created_at = Column(TIMESTAMP, index=True, comment='Created_at')
    website_id = Column(INTEGER(11), index=True, comment='Website_id')
    confirmation = Column(String(255), index=True, comment='Confirmation')
    created_in = Column(Text, comment='Created_in')
    dob = Column(Date, index=True, comment='Dob')
    gender = Column(INTEGER(11), index=True, comment='Gender')
    taxvat = Column(String(255), comment='Taxvat')
    lock_expires = Column(TIMESTAMP, comment='Lock_expires')
    shipping_full = Column(Text, comment='Shipping_full')
    billing_full = Column(Text, comment='Billing_full')
    billing_firstname = Column(String(255), comment='Billing_firstname')
    billing_lastname = Column(String(255), comment='Billing_lastname')
    billing_telephone = Column(String(255), comment='Billing_telephone')
    billing_postcode = Column(String(255), comment='Billing_postcode')
    billing_country_id = Column(String(255), index=True, comment='Billing_country_id')
    billing_region = Column(String(255), comment='Billing_region')
    billing_street = Column(String(255), comment='Billing_street')
    billing_city = Column(String(255), comment='Billing_city')
    billing_fax = Column(String(255), comment='Billing_fax')
    billing_vat_id = Column(String(255), comment='Billing_vat_id')
    billing_company = Column(String(255), comment='Billing_company')


class CustomerGroup(Base):
    __tablename__ = 'customer_group'
    __table_args__ = {'comment': 'Customer Group'}

    customer_group_id = Column(INTEGER(10), primary_key=True)
    customer_group_code = Column(String(32), nullable=False, comment='Customer Group Code')
    tax_class_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Tax Class ID')


class CustomerLog(Base):
    __tablename__ = 'customer_log'
    __table_args__ = {'comment': 'Customer Log Table'}

    log_id = Column(INTEGER(11), primary_key=True, comment='Log ID')
    customer_id = Column(INTEGER(11), nullable=False, unique=True, comment='Customer ID')
    last_login_at = Column(TIMESTAMP, comment='Last Login Time')
    last_logout_at = Column(TIMESTAMP, comment='Last Logout Time')


class CustomerVisitor(Base):
    __tablename__ = 'customer_visitor'
    __table_args__ = {'comment': 'Visitor Table'}

    visitor_id = Column(BIGINT(20), primary_key=True, comment='Visitor ID')
    customer_id = Column(INTEGER(11), index=True, comment='Customer ID')
    session_id = Column(String(64), comment='Session ID')
    last_visit_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Last Visit Time')


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


class CustomerEavAttribute(EavAttribute):
    __tablename__ = 'customer_eav_attribute'
    __table_args__ = {'comment': 'Customer Eav Attribute'}

    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), primary_key=True, comment='Attribute ID')
    is_visible = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Visible')
    input_filter = Column(String(255), comment='Input Filter')
    multiline_count = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Multiline Count')
    validate_rules = Column(Text, comment='Validate Rules')
    is_system = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is System')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    data_model = Column(String(255), comment='Data Model')
    is_used_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Used in Grid')
    is_visible_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible in Grid')
    is_filterable_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Filterable in Grid')
    is_searchable_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Searchable in Grid')


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


class CustomerEavAttributeWebsite(Base):
    __tablename__ = 'customer_eav_attribute_website'
    __table_args__ = {'comment': 'Customer Eav Attribute Website'}

    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Attribute ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID')
    is_visible = Column(SMALLINT(5), comment='Is Visible')
    is_required = Column(SMALLINT(5), comment='Is Required')
    default_value = Column(Text, comment='Default Value')
    multiline_count = Column(SMALLINT(5), comment='Multiline Count')

    attribute = relationship('EavAttribute')
    website = relationship('StoreWebsite')


class CustomerFormAttribute(Base):
    __tablename__ = 'customer_form_attribute'
    __table_args__ = {'comment': 'Customer Form Attribute'}

    form_code = Column(String(32), primary_key=True, nullable=False, comment='Form Code')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Attribute ID')

    attribute = relationship('EavAttribute')


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


class CustomerAddressEntity(Base):
    __tablename__ = 'customer_address_entity'
    __table_args__ = {'comment': 'Customer Address Entity'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    increment_id = Column(String(50), comment='Increment ID')
    parent_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), index=True, comment='Parent ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Active')
    city = Column(String(255), nullable=False, comment='City')
    company = Column(String(255), comment='Company')
    country_id = Column(String(255), nullable=False, comment='Country')
    fax = Column(String(255), comment='Fax')
    firstname = Column(String(255), nullable=False, comment='First Name')
    lastname = Column(String(255), nullable=False, comment='Last Name')
    middlename = Column(String(255), comment='Middle Name')
    postcode = Column(String(255), comment='Zip/Postal Code')
    prefix = Column(String(40), comment='Name Prefix')
    region = Column(String(255), comment='State/Province')
    region_id = Column(INTEGER(10), comment='State/Province')
    street = Column(Text, nullable=False, comment='Street Address')
    suffix = Column(String(40), comment='Name Suffix')
    telephone = Column(String(255), nullable=False, comment='Phone Number')
    vat_id = Column(String(255), comment='VAT number')
    vat_is_valid = Column(INTEGER(10), comment='VAT number validity')
    vat_request_date = Column(String(255), comment='VAT number validation request date')
    vat_request_id = Column(String(255), comment='VAT number validation request ID')
    vat_request_success = Column(INTEGER(10), comment='VAT number validation request success')

    parent = relationship('CustomerEntity')


class CustomerEntityDatetime(Base):
    __tablename__ = 'customer_entity_datetime'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        Index('CUSTOMER_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Entity Datetime'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DateTime, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerEntity')


class CustomerEntityDecimal(Base):
    __tablename__ = 'customer_entity_decimal'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        Index('CUSTOMER_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        {'comment': 'Customer Entity Decimal'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerEntity')


class CustomerEntityInt(Base):
    __tablename__ = 'customer_entity_int'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        Index('CUSTOMER_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Entity Int'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerEntity')


class CustomerEntityText(Base):
    __tablename__ = 'customer_entity_text'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_TEXT_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Entity Text'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(Text, nullable=False, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerEntity')


class CustomerEntityVarchar(Base):
    __tablename__ = 'customer_entity_varchar'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        Index('CUSTOMER_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Entity Varchar'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(String(255), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerEntity')


class CustomerAddressEntityDatetime(Base):
    __tablename__ = 'customer_address_entity_datetime'
    __table_args__ = (
        Index('CUSTOMER_ADDRESS_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        Index('CUSTOMER_ADDRESS_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        {'comment': 'Customer Address Entity Datetime'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_address_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DateTime, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerAddressEntity')


class CustomerAddressEntityDecimal(Base):
    __tablename__ = 'customer_address_entity_decimal'
    __table_args__ = (
        Index('CUSTOMER_ADDRESS_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        Index('CUSTOMER_ADDRESS_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Address Entity Decimal'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_address_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerAddressEntity')


class CustomerAddressEntityInt(Base):
    __tablename__ = 'customer_address_entity_int'
    __table_args__ = (
        Index('CUSTOMER_ADDRESS_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        Index('CUSTOMER_ADDRESS_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        {'comment': 'Customer Address Entity Int'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_address_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerAddressEntity')


class CustomerAddressEntityText(Base):
    __tablename__ = 'customer_address_entity_text'
    __table_args__ = (
        Index('CUSTOMER_ADDRESS_ENTITY_TEXT_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Address Entity Text'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_address_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(Text, nullable=False, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerAddressEntity')


class CustomerAddressEntityVarchar(Base):
    __tablename__ = 'customer_address_entity_varchar'
    __table_args__ = (
        Index('CUSTOMER_ADDRESS_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID_VALUE', 'entity_id', 'attribute_id', 'value'),
        Index('CUSTOMER_ADDRESS_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID', 'entity_id', 'attribute_id', unique=True),
        {'comment': 'Customer Address Entity Varchar'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    entity_id = Column(ForeignKey('customer_address_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(String(255), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CustomerAddressEntity')
