# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT
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


class UiBookmark(Base):
    __tablename__ = 'ui_bookmark'
    __table_args__ = (
        Index('UI_BOOKMARK_USER_ID_NAMESPACE_IDENTIFIER', 'user_id', 'namespace', 'identifier'),
        {'comment': 'Bookmark'}
    )

    bookmark_id = Column(INTEGER(10), primary_key=True, comment='Bookmark identifier')
    user_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), nullable=False, comment='User ID')
    namespace = Column(String(255), nullable=False, comment='Bookmark namespace')
    identifier = Column(String(255), nullable=False, comment='Bookmark Identifier')
    current = Column(SMALLINT(6), nullable=False, comment='Mark current bookmark per user and identifier')
    title = Column(String(255), comment='Bookmark title')
    config = Column(LONGTEXT, comment='Bookmark config')
    created_at = Column(DateTime, nullable=False, server_default=text("current_timestamp()"), comment='Bookmark created at')
    updated_at = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Bookmark updated at')

    user = relationship('AdminUser')
