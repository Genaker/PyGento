# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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
