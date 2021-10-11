# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class YotpoRichSnippet(Base):
    __tablename__ = 'yotpo_rich_snippets'
    __table_args__ = {'comment': 'yotpo_rich_snippets'}

    rich_snippet_id = Column(INTEGER(11), primary_key=True, comment='Id')
    product_id = Column(INTEGER(11), nullable=False, comment='Product Id')
    store_id = Column(INTEGER(11), nullable=False, comment='Store Id')
    average_score = Column(Float(10), nullable=False, comment='Average Score')
    reviews_count = Column(Float(10), nullable=False, comment='Reviews Count')
    expiration_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Expiry Time')


class YotpoSync(Base):
    __tablename__ = 'yotpo_sync'
    __table_args__ = (
        Index('YOTPO_SYNC_STORE_ID_ENTITY_TYPE_ENTITY_ID', 'store_id', 'entity_type', 'entity_id', unique=True),
        {'comment': 'yotpo_sync'}
    )

    sync_id = Column(INTEGER(10), primary_key=True, comment='Id')
    store_id = Column(INTEGER(10), comment='Store ID')
    entity_type = Column(String(50), comment='Entity Type')
    entity_id = Column(INTEGER(10), comment='Entity ID')
    sync_flag = Column(SMALLINT(6), server_default=text("0"), comment='Sync Flag')
    sync_date = Column(DateTime, nullable=False, comment='Sync Date')
