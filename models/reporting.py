# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import DECIMAL, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ReportingCount(Base):
    __tablename__ = 'reporting_counts'
    __table_args__ = {'comment': 'Reporting for all count related events generated via the cron job'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    type = Column(String(255), comment='Item Reported')
    count = Column(INTEGER(10), comment='Count Value')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')


class ReportingModuleStatu(Base):
    __tablename__ = 'reporting_module_status'
    __table_args__ = {'comment': 'Module Status Table'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Module ID')
    name = Column(String(255), comment='Module Name')
    active = Column(String(255), comment='Module Active Status')
    setup_version = Column(String(255), comment='Module Version')
    state = Column(String(255), comment='Module State')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')


class ReportingOrder(Base):
    __tablename__ = 'reporting_orders'
    __table_args__ = {'comment': 'Reporting for all orders'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    customer_id = Column(INTEGER(10), comment='Customer ID')
    total = Column(DECIMAL(20, 4))
    total_base = Column(DECIMAL(20, 4))
    item_count = Column(INTEGER(10), nullable=False, comment='Line Item Count')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Updated At')


class ReportingSystemUpdate(Base):
    __tablename__ = 'reporting_system_updates'
    __table_args__ = {'comment': 'Reporting for system updates'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    type = Column(String(255), comment='Update Type')
    action = Column(String(255), comment='Action Performed')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Updated At')


class ReportingUser(Base):
    __tablename__ = 'reporting_users'
    __table_args__ = {'comment': 'Reporting for user actions'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    type = Column(String(255), comment='User Type')
    action = Column(String(255), comment='Action Performed')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Updated At')
