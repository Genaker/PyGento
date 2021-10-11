# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MediaGalleryAsset(Base):
    __tablename__ = 'media_gallery_asset'
    __table_args__ = {'comment': 'Media Gallery Asset'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='Entity ID')
    path = Column(String(255), unique=True, comment='Path')
    title = Column(String(255), comment='Title')
    source = Column(String(255), comment='Source')
    content_type = Column(String(255), comment='Content Type')
    width = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Width')
    height = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Height')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')

    keywords = relationship('MediaGalleryKeyword', secondary='media_gallery_asset_keyword')


class MediaGalleryKeyword(Base):
    __tablename__ = 'media_gallery_keyword'
    __table_args__ = {'comment': 'Media Gallery Keyword'}

    id = Column(INTEGER(10), primary_key=True, index=True, comment='Keyword ID')
    keyword = Column(String(255), nullable=False, unique=True, comment='Keyword')


t_media_gallery_asset_keyword = Table(
    'media_gallery_asset_keyword', metadata,
    Column('keyword_id', ForeignKey('media_gallery_keyword.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Keyword Id'),
    Column('asset_id', ForeignKey('media_gallery_asset.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Asset ID'),
    comment='Media Gallery Asset Keyword'
)
