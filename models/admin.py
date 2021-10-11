# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AdminAnalyticsUsageVersionLog(Base):
    __tablename__ = 'admin_analytics_usage_version_log'
    __table_args__ = {'comment': 'Admin Notification Viewer Log Table'}

    id = Column(INTEGER(10), primary_key=True, comment='Log ID')
    last_viewed_in_version = Column(String(50), nullable=False, unique=True, comment='Viewer last viewed on product version')


class AdminSystemMessage(Base):
    __tablename__ = 'admin_system_messages'
    __table_args__ = {'comment': 'Admin System Messages'}

    identity = Column(String(100), primary_key=True, comment='Message ID')
    severity = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Problem type')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Create date')


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


class AdminnotificationInbox(Base):
    __tablename__ = 'adminnotification_inbox'
    __table_args__ = {'comment': 'Adminnotification Inbox'}

    notification_id = Column(INTEGER(10), primary_key=True, comment='Notification ID')
    severity = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Problem type')
    date_added = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Create date')
    title = Column(String(255), nullable=False, comment='Title')
    description = Column(Text, comment='Description')
    url = Column(String(255), comment='Url')
    is_read = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Flag if notification read')
    is_remove = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Flag if notification might be removed')


class AdminPassword(Base):
    __tablename__ = 'admin_passwords'
    __table_args__ = {'comment': 'Admin Passwords'}

    password_id = Column(INTEGER(10), primary_key=True, comment='Password ID')
    user_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='User ID')
    password_hash = Column(String(100), comment='Password Hash')
    expires = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Deprecated')
    last_updated = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Last Updated')

    user = relationship('AdminUser')


class AdminUserSession(Base):
    __tablename__ = 'admin_user_session'
    __table_args__ = {'comment': 'Admin User sessions table'}

    id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    session_id = Column(String(128), nullable=False, index=True, comment='Session ID value')
    user_id = Column(ForeignKey('admin_user.user_id', ondelete='CASCADE'), index=True, comment='Admin User ID')
    status = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Current Session status')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created Time')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Update Time')
    ip = Column(String(15), nullable=False, comment='Remote user IP')

    user = relationship('AdminUser')
