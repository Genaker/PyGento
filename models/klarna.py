# coding: utf-8
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class KlarnaCoreOrder(Base):
    __tablename__ = 'klarna_core_order'
    __table_args__ = {'comment': 'Klarna Order'}

    id = Column(INTEGER(10), primary_key=True, comment='Entity Id')
    klarna_order_id = Column(String(255), comment='Klarna Order Id')
    session_id = Column(String(255), comment='Session Id')
    reservation_id = Column(String(255), comment='Reservation Id')
    order_id = Column(INTEGER(10), nullable=False, index=True, comment='Order Id')
    is_acknowledged = Column(SMALLINT(6), nullable=False, index=True, server_default=text("0"), comment='Is Acknowledged')


class KlarnaPaymentsQuote(Base):
    __tablename__ = 'klarna_payments_quote'
    __table_args__ = {'comment': 'Klarna Payments Quote'}

    payments_quote_id = Column(INTEGER(10), primary_key=True, comment='Payments Id')
    session_id = Column(String(255), comment='Klarna Session Id')
    client_token = Column(Text, comment='Klarna Client Token')
    authorization_token = Column(String(255), comment='Authorization Token')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Active')
    quote_id = Column(INTEGER(10), nullable=False, index=True, comment='Quote Id')
    payment_methods = Column(String(255), comment='Payment Method Categories')
    payment_method_info = Column(Text, comment='Payment Method Category Info')
