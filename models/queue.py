# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Queue(Base):
    __tablename__ = 'queue'
    __table_args__ = {'comment': 'Table storing unique queues'}

    id = Column(INTEGER(10), primary_key=True, comment='Queue ID')
    name = Column(String(255), unique=True, comment='Queue name')


class QueueLock(Base):
    __tablename__ = 'queue_lock'
    __table_args__ = {'comment': 'Messages that were processed are inserted here to be locked.'}

    id = Column(INTEGER(10), primary_key=True, comment='Message ID')
    message_code = Column(String(255), nullable=False, unique=True, server_default=text("''"), comment='Message Code')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Created At')


class QueueMessage(Base):
    __tablename__ = 'queue_message'
    __table_args__ = {'comment': 'Queue messages'}

    id = Column(BIGINT(20), primary_key=True, comment='Message ID')
    topic_name = Column(String(255), comment='Message topic')
    body = Column(LONGTEXT, comment='Message body')


t_queue_poison_pill = Table(
    'queue_poison_pill', metadata,
    Column('version', String(255), nullable=False, comment='Poison Pill version.'),
    comment='Sequence table for poison pill versions'
)


class QueueMessageStatu(Base):
    __tablename__ = 'queue_message_status'
    __table_args__ = (
        Index('QUEUE_MESSAGE_STATUS_QUEUE_ID_MESSAGE_ID', 'queue_id', 'message_id', unique=True),
        Index('QUEUE_MESSAGE_STATUS_STATUS_UPDATED_AT', 'status', 'updated_at'),
        {'comment': 'Relation table to keep associations between queues and messages'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='Relation ID')
    queue_id = Column(ForeignKey('queue.id', ondelete='CASCADE'), nullable=False, comment='Queue ID')
    message_id = Column(ForeignKey('queue_message.id', ondelete='CASCADE'), nullable=False, index=True, comment='Message ID')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    status = Column(SMALLINT(5), nullable=False, comment='Message status in particular queue')
    number_of_trials = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Number of trials to processed failed message processing')

    message = relationship('QueueMessage')
    queue = relationship('Queue')
