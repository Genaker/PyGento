# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class StoreGroup(Base):
    __tablename__ = 'store_group'
    __table_args__ = {'comment': 'Store Groups'}

    group_id = Column(SMALLINT(5), primary_key=True, comment='Group ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    name = Column(String(255), nullable=False, comment='Store Group Name')
    root_category_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Root Category ID')
    default_store_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Store ID')
    code = Column(String(32), unique=True, comment='Store group unique code')

    website = relationship('StoreWebsite')


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        Index('STORE_IS_ACTIVE_SORT_ORDER', 'is_active', 'sort_order'),
        {'comment': 'Stores'}
    )

    store_id = Column(SMALLINT(5), primary_key=True, comment='Store ID')
    code = Column(String(32), unique=True, comment='Code')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    group_id = Column(ForeignKey('store_group.group_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Group ID')
    name = Column(String(255), nullable=False, comment='Store Name')
    sort_order = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store Sort Order')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store Activity')

    group = relationship('StoreGroup')
    website = relationship('StoreWebsite')


class SearchQuery(Base):
    __tablename__ = 'search_query'
    __table_args__ = (
        Index('SEARCH_QUERY_STORE_ID_POPULARITY', 'store_id', 'popularity'),
        Index('SEARCH_QUERY_QUERY_TEXT_STORE_ID', 'query_text', 'store_id', unique=True),
        Index('SEARCH_QUERY_QUERY_TEXT_STORE_ID_POPULARITY', 'query_text', 'store_id', 'popularity'),
        {'comment': 'Search query table'}
    )

    query_id = Column(INTEGER(10), primary_key=True, comment='Query ID')
    query_text = Column(String(255), comment='Query text')
    num_results = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Num results')
    popularity = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Popularity')
    redirect = Column(String(255), comment='Redirect')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    display_in_terms = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Display in terms')
    is_active = Column(SMALLINT(6), server_default=text("1"), comment='Active status')
    is_processed = Column(SMALLINT(6), index=True, server_default=text("0"), comment='Processed status')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated at')

    store = relationship('Store')


class SearchSynonym(Base):
    __tablename__ = 'search_synonyms'
    __table_args__ = {'comment': 'table storing various synonyms groups'}

    group_id = Column(BIGINT(20), primary_key=True, comment='Synonyms Group ID')
    synonyms = Column(Text, nullable=False, index=True, comment='list of synonyms making up this group')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID - identifies the store view these synonyms belong to')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID - identifies the website ID these synonyms belong to')

    store = relationship('Store')
    website = relationship('StoreWebsite')
