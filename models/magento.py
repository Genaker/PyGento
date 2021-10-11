# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, LargeBinary, String, TIMESTAMP, VARBINARY, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MagentoBulk(Base):
    __tablename__ = 'magento_bulk'
    __table_args__ = {'comment': 'Bulk entity that represents set of related asynchronous operations'}

    id = Column(INTEGER(10), primary_key=True, comment='Bulk Internal ID (must not be exposed)')
    uuid = Column(VARBINARY(39), unique=True, comment='Bulk UUID (can be exposed to reference bulk entity)')
    user_id = Column(INTEGER(10), index=True, comment='ID of the WebAPI user that performed an action')
    user_type = Column(INTEGER(11), comment='Which type of user')
    description = Column(String(255), comment='Bulk Description')
    operation_count = Column(INTEGER(10), nullable=False, comment='Total number of operations scheduled within this bulk')
    start_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Bulk start time')


class MagentoAcknowledgedBulk(Base):
    __tablename__ = 'magento_acknowledged_bulk'
    __table_args__ = {'comment': 'Bulk that was viewed by user from notification area'}

    id = Column(INTEGER(10), primary_key=True, comment='Internal ID')
    bulk_uuid = Column(ForeignKey('magento_bulk.uuid', ondelete='CASCADE'), unique=True, comment='Related Bulk UUID')

    magento_bulk = relationship('MagentoBulk')


class MagentoOperation(Base):
    __tablename__ = 'magento_operation'
    __table_args__ = (
        Index('MAGENTO_OPERATION_BULK_UUID_ERROR_CODE', 'bulk_uuid', 'error_code'),
        {'comment': 'Operation entity'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='Operation ID')
    bulk_uuid = Column(ForeignKey('magento_bulk.uuid', ondelete='CASCADE'), comment='Related Bulk UUID')
    topic_name = Column(String(255), comment='Name of the related message queue topic')
    serialized_data = Column(LargeBinary, comment='Data (serialized) required to perform an operation')
    result_serialized_data = Column(LargeBinary, comment='Result data (serialized) after perform an operation')
    status = Column(SMALLINT(6), server_default=text("0"), comment='Operation status (OPEN | COMPLETE | RETRIABLY_FAILED | NOT_RETRIABLY_FAILED)')
    error_code = Column(SMALLINT(6), comment='Code of the error that appeared during operation execution (used to aggregate related failed operations)')
    result_message = Column(String(255), comment='Operation result message')

    magento_bulk = relationship('MagentoBulk')
