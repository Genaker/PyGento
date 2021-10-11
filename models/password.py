# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PasswordResetRequestEvent(Base):
    __tablename__ = 'password_reset_request_event'
    __table_args__ = {'comment': 'Password Reset Request Event under a security control'}

    id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    request_type = Column(SMALLINT(5), nullable=False, comment='Type of the event under a security control')
    account_reference = Column(String(255), index=True, comment='An identifier for existing account or another target')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Timestamp when the event occurs')
    ip = Column(String(15), nullable=False, comment='Remote user IP')
