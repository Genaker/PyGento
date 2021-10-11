# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, TIMESTAMP, Text, text
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


class MspTfaCountryCode(Base):
    __tablename__ = 'msp_tfa_country_codes'
    __table_args__ = {'comment': 'msp_tfa_country_codes'}

    msp_tfa_country_codes_id = Column(INTEGER(10), primary_key=True, comment='TFA admin user ID')
    code = Column(Text, nullable=False, index=True, comment='Country code')
    name = Column(Text, nullable=False, comment='Country name')
    dial_code = Column(Text, nullable=False, comment='Prefix')


class MspTfaTrusted(Base):
    __tablename__ = 'msp_tfa_trusted'
    __table_args__ = {'comment': 'msp_tfa_trusted'}

    msp_tfa_trusted_id = Column(INTEGER(10), primary_key=True, comment='Trusted device ID')
    date_time = Column(DateTime, nullable=False, comment='Date and time')
    user_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')
    device_name = Column(Text, nullable=False, comment='Device name')
    token = Column(Text, nullable=False, comment='Token')
    last_ip = Column(Text, nullable=False, comment='Last IP')

    user = relationship('AdminUser')


class MspTfaUserConfig(Base):
    __tablename__ = 'msp_tfa_user_config'
    __table_args__ = {'comment': 'msp_tfa_user_config'}

    msp_tfa_user_config_id = Column(INTEGER(10), primary_key=True, comment='TFA admin user ID')
    user_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')
    encoded_providers = Column(Text, comment='Encoded providers list')
    encoded_config = Column(Text, comment='Encoded providers configuration')
    default_provider = Column(Text, comment='Default provider')

    user = relationship('AdminUser')
