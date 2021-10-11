# coding: utf-8
from sqlalchemy import Column, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CronSchedule(Base):
    __tablename__ = 'cron_schedule'
    __table_args__ = (
        Index('CRON_SCHEDULE_SCHEDULED_AT_STATUS', 'scheduled_at', 'status'),
        {'comment': 'Cron Schedule'}
    )

    schedule_id = Column(INTEGER(10), primary_key=True, comment='Schedule ID')
    job_code = Column(String(255), nullable=False, index=True, server_default=text("'0'"), comment='Job Code')
    status = Column(String(7), nullable=False, server_default=text("'pending'"), comment='Status')
    messages = Column(Text, comment='Messages')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    scheduled_at = Column(TIMESTAMP, comment='Scheduled At')
    executed_at = Column(TIMESTAMP, comment='Executed At')
    finished_at = Column(TIMESTAMP, comment='Finished At')
