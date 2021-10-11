# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text, text
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


class AdobeStockCategory(Base):
    __tablename__ = 'adobe_stock_category'
    __table_args__ = {'comment': 'Adobe Stock Category'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='Entity ID')
    name = Column(String(255), comment='Name')


class AdobeStockCreator(Base):
    __tablename__ = 'adobe_stock_creator'
    __table_args__ = {'comment': 'Adobe Stock Creator'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='ID')
    name = Column(String(255), comment="Asset creator's name")


class MediaGalleryAsset(Base):
    __tablename__ = 'media_gallery_asset'
    __table_args__ = {'comment': 'Media Gallery Asset'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='Entity ID')
    path = Column(String(255), unique=True, comment='Path')
    title = Column(String(255), comment='Title')
    source = Column(String(255), comment='Source')
    content_type = Column(String(255), comment='Content Type')
    width = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Width')
    height = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Height')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')


class AdobeStockAsset(Base):
    __tablename__ = 'adobe_stock_asset'
    __table_args__ = {'comment': 'Adobe Stock Asset'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='Entity ID')
    media_gallery_id = Column(ForeignKey('media_gallery_asset.id', ondelete='CASCADE'), index=True, comment='Media gallery ID')
    category_id = Column(ForeignKey('adobe_stock_category.id', ondelete='SET NULL'), index=True, comment='Category ID')
    creator_id = Column(ForeignKey('adobe_stock_creator.id', ondelete='SET NULL'), index=True, comment='Creator ID')
    is_licensed = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Is Licensed')
    creation_date = Column(String(255), comment='Creation Date')

    category = relationship('AdobeStockCategory')
    creator = relationship('AdobeStockCreator')
    media_gallery = relationship('MediaGalleryAsset')


class AdobeUserProfile(Base):
    __tablename__ = 'adobe_user_profile'
    __table_args__ = {'comment': 'Adobe IMS User Profile'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='Entity ID')
    admin_user_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Admin User Id')
    name = Column(String(255), nullable=False, comment='Display Name')
    email = Column(String(255), nullable=False, comment='user profile email')
    image = Column(String(255), nullable=False, comment='user profile avatar')
    account_type = Column(String(255), comment='Account Type')
    access_token = Column(Text, comment='Access Token')
    refresh_token = Column(Text, comment='Refresh Token')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    access_token_expires_at = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"), comment='Access Token Expires At')

    admin_user = relationship('AdminUser')
