# coding: utf-8
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ScconnectorGoogleFeedCl(Base):
    __tablename__ = 'scconnector_google_feed_cl'
    __table_args__ = {'comment': 'scconnector_google_feed_cl'}

    version_id = Column(INTEGER(10), primary_key=True, comment='Version ID')
    entity_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Entity ID')


class ScconnectorGoogleRemoveCl(Base):
    __tablename__ = 'scconnector_google_remove_cl'
    __table_args__ = {'comment': 'scconnector_google_remove_cl'}

    version_id = Column(INTEGER(10), primary_key=True, comment='Version ID')
    entity_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Entity ID')
