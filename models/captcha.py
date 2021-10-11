# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CaptchaLog(Base):
    __tablename__ = 'captcha_log'
    __table_args__ = {'comment': 'Count Login Attempts'}

    type = Column(String(32), primary_key=True, nullable=False, comment='Type')
    value = Column(String(255), primary_key=True, nullable=False, comment='Value')
    count = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Count')
    updated_at = Column(TIMESTAMP, comment='Update Time')
