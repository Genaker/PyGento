# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AdminUser(Base):
    __tablename__ = 'admin_user'
    __table_args__ = {'comment': 'Admin User Table'}

    user_id = Column(INTEGER(10), primary_key=True, comment='User ID')
    firstname = Column(String(32), comment='User First Name')
    lastname = Column(String(32), comment='User Last Name')
    email = Column(String(128), comment='User Email')
    username = Column(String(40), unique=True, comment='User Login')
    password = Column(String(255), nullable=False, comment='User Password')
    created = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='User Created Time')
    modified = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='User Modified Time')
    logdate = Column(TIMESTAMP, comment='User Last Login Time')
    lognum = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='User Login Number')
    reload_acl_flag = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Reload ACL')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='User Is Active')
    extra = Column(Text, comment='User Extra Data')
    rp_token = Column(Text, comment='Reset Password Link Token')
    rp_token_created_at = Column(TIMESTAMP, comment='Reset Password Link Token Creation Date')
    interface_locale = Column(String(16), nullable=False, server_default=text("'en_US'"), comment='Backend interface locale')
    failures_num = Column(SMALLINT(6), server_default=text("0"), comment='Failure Number')
    first_failure = Column(TIMESTAMP, comment='First Failure')
    lock_expires = Column(TIMESTAMP, comment='Expiration Lock Dates')
    refresh_token = Column(Text, comment='Email connector refresh token')


class OauthConsumer(Base):
    __tablename__ = 'oauth_consumer'
    __table_args__ = {'comment': 'OAuth Consumers'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, index=True, server_default=text("'0000-00-00 00:00:00'"))
    name = Column(String(255), nullable=False, comment='Name of consumer')
    key = Column(String(32), nullable=False, unique=True, comment='Key code')
    secret = Column(String(32), nullable=False, unique=True, comment='Secret code')
    callback_url = Column(Text, comment='Callback URL')
    rejected_callback_url = Column(Text, nullable=False, comment='Rejected callback URL')


class OauthTokenRequestLog(Base):
    __tablename__ = 'oauth_token_request_log'
    __table_args__ = (
        Index('OAUTH_TOKEN_REQUEST_LOG_USER_NAME_USER_TYPE', 'user_name', 'user_type', unique=True),
        {'comment': 'Log of token request authentication failures.'}
    )

    log_id = Column(INTEGER(10), primary_key=True, comment='Log ID')
    user_name = Column(String(255), nullable=False, comment='Customer email or admin login')
    user_type = Column(SMALLINT(5), nullable=False, comment='User type (admin or customer)')
    failures_count = Column(SMALLINT(5), server_default=text("0"), comment='Number of failed authentication attempts in a row')
    lock_expires_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Lock expiration time')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


t_oauth_nonce = Table(
    'oauth_nonce', metadata,
    Column('nonce', String(32), nullable=False, comment='Nonce String'),
    Column('timestamp', INTEGER(10), nullable=False, index=True, comment='Nonce Timestamp'),
    Column('consumer_id', ForeignKey('oauth_consumer.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Consumer ID'),
    Index('OAUTH_NONCE_NONCE_CONSUMER_ID', 'nonce', 'consumer_id', unique=True),
    comment='OAuth Nonce'
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


class OauthToken(Base):
    __tablename__ = 'oauth_token'
    __table_args__ = {'comment': 'OAuth Tokens'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    consumer_id = Column(ForeignKey('oauth_consumer.entity_id', ondelete='CASCADE'), index=True, comment='Oauth Consumer ID')
    admin_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), index=True, comment='Admin user ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), index=True, comment='Customer user ID')
    type = Column(String(16), nullable=False, comment='Token Type')
    token = Column(String(32), nullable=False, unique=True, comment='Token')
    secret = Column(String(32), nullable=False, comment='Token Secret')
    verifier = Column(String(32), comment='Token Verifier')
    callback_url = Column(Text, nullable=False, comment='Token Callback URL')
    revoked = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Token revoked')
    authorized = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Token authorized')
    user_type = Column(INTEGER(11), comment='User type')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Token creation timestamp')

    admin = relationship('AdminUser')
    consumer = relationship('OauthConsumer')
    customer = relationship('CustomerEntity')
