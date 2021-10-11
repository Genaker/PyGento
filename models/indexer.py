# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class IndexerState(Base):
    __tablename__ = 'indexer_state'
    __table_args__ = {'comment': 'Indexer State'}

    state_id = Column(INTEGER(10), primary_key=True, comment='Indexer State ID')
    indexer_id = Column(String(255), index=True, comment='Indexer ID')
    status = Column(String(16), server_default=text("'invalid'"), comment='Indexer Status')
    updated = Column(DateTime, comment='Indexer Status')
    hash_config = Column(String(32), nullable=False, comment='Hash of indexer config')
