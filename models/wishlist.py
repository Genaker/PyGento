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


class Wishlist(Base):
    __tablename__ = 'wishlist'
    __table_args__ = {'comment': 'Wishlist main Table'}

    wishlist_id = Column(INTEGER(10), primary_key=True, comment='Wishlist ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), nullable=False, unique=True, server_default=text("0"), comment='Customer ID')
    shared = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sharing flag (0 or 1)')
    sharing_code = Column(String(32), comment='Sharing encrypted code')
    updated_at = Column(TIMESTAMP, comment='Last updated date')

    customer = relationship('CustomerEntity')


class WishlistItem(Base):
    __tablename__ = 'wishlist_item'
    __table_args__ = {'comment': 'Wishlist items'}

    wishlist_item_id = Column(INTEGER(10), primary_key=True, comment='Wishlist item ID')
    wishlist_id = Column(ForeignKey('wishlist.wishlist_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Wishlist ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')
    added_at = Column(TIMESTAMP, comment='Add date and time')
    description = Column(Text, comment='Short description of wish list item')
    qty = Column(DECIMAL(12, 4), nullable=False, comment='Qty')

    product = relationship('CatalogProductEntity')
    store = relationship('Store')
    wishlist = relationship('Wishlist')


class WishlistItemOption(Base):
    __tablename__ = 'wishlist_item_option'
    __table_args__ = {'comment': 'Wishlist Item Option Table'}

    option_id = Column(INTEGER(10), primary_key=True, comment='Option ID')
    wishlist_item_id = Column(ForeignKey('wishlist_item.wishlist_item_id', ondelete='CASCADE'), nullable=False, index=True, comment='Wishlist Item ID')
    product_id = Column(INTEGER(10), nullable=False, comment='Product ID')
    code = Column(String(255), nullable=False, comment='Code')
    value = Column(Text, comment='Value')

    wishlist_item = relationship('WishlistItem')
