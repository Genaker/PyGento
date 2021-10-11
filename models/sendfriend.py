# coding: utf-8
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SendfriendLog(Base):
    __tablename__ = 'sendfriend_log'
    __table_args__ = {'comment': 'Send to friend function log storage table'}

    log_id = Column(INTEGER(10), primary_key=True, comment='Log ID')
    ip = Column(BIGINT(20), nullable=False, index=True, server_default=text("0"), comment='Customer IP address')
    time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Log time')
    website_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Website ID')
