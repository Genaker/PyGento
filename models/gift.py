# coding: utf-8
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GiftMessage(Base):
    __tablename__ = 'gift_message'
    __table_args__ = {'comment': 'Gift Message'}

    gift_message_id = Column(INTEGER(10), primary_key=True, comment='GiftMessage ID')
    customer_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Customer ID')
    sender = Column(String(255), comment='Sender')
    recipient = Column(String(255), comment='Registrant')
    message = Column(Text, comment='Message')
