# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = {'comment': 'Database Sessions Storage'}

    session_id = Column(String(255), primary_key=True, comment='Session Id')
    session_expires = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Date of Session Expiration')
    session_data = Column(MEDIUMBLOB, nullable=False, comment='Session Data')
