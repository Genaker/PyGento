# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Cache(Base):
    __tablename__ = 'cache'
    __table_args__ = {'comment': 'Caches'}

    id = Column(String(200), primary_key=True, comment='Cache Id')
    data = Column(MEDIUMBLOB, comment='Cache Data')
    create_time = Column(INTEGER(11), comment='Cache Creation Time')
    update_time = Column(INTEGER(11), comment='Time of Cache Updating')
    expire_time = Column(INTEGER(11), index=True, comment='Cache Expiration Time')


class CacheTag(Base):
    __tablename__ = 'cache_tag'
    __table_args__ = {'comment': 'Tag Caches'}

    tag = Column(String(100), primary_key=True, nullable=False, comment='Tag')
    cache_id = Column(String(200), primary_key=True, nullable=False, index=True, comment='Cache Id')
