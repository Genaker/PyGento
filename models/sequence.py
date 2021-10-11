# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SequenceCreditmemo0(Base):
    __tablename__ = 'sequence_creditmemo_0'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceCreditmemo1(Base):
    __tablename__ = 'sequence_creditmemo_1'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceInvoice0(Base):
    __tablename__ = 'sequence_invoice_0'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceInvoice1(Base):
    __tablename__ = 'sequence_invoice_1'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceOrder0(Base):
    __tablename__ = 'sequence_order_0'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceOrder1(Base):
    __tablename__ = 'sequence_order_1'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceShipment0(Base):
    __tablename__ = 'sequence_shipment_0'

    sequence_value = Column(INTEGER(10), primary_key=True)


class SequenceShipment1(Base):
    __tablename__ = 'sequence_shipment_1'

    sequence_value = Column(INTEGER(10), primary_key=True)
