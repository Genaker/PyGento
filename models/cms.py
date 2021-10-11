# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CmsBlock(Base):
    __tablename__ = 'cms_block'
    __table_args__ = (
        Index('CMS_BLOCK_TITLE_IDENTIFIER_CONTENT', 'title', 'identifier', 'content'),
        {'comment': 'CMS Block Table'}
    )

    block_id = Column(SMALLINT(6), primary_key=True, comment='Entity ID')
    title = Column(String(255), nullable=False, comment='Block Title')
    identifier = Column(String(255), nullable=False, comment='Block String Identifier')
    content = Column(MEDIUMTEXT, comment='Block Content')
    creation_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Block Creation Time')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Block Modification Time')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Is Block Active')

    stores = relationship('Store', secondary='cms_block_store')


class CmsPage(Base):
    __tablename__ = 'cms_page'
    __table_args__ = (
        Index('CMS_PAGE_TITLE_META_KEYWORDS_META_DESCRIPTION_IDENTIFIER_CONTENT', 'title', 'meta_keywords', 'meta_description', 'identifier', 'content'),
        {'comment': 'CMS Page Table'}
    )

    page_id = Column(SMALLINT(6), primary_key=True, comment='Entity ID')
    title = Column(String(255), comment='Page Title')
    page_layout = Column(String(255), comment='Page Layout')
    meta_keywords = Column(Text, comment='Page Meta Keywords')
    meta_description = Column(Text, comment='Page Meta Description')
    identifier = Column(String(100), index=True, comment='Page String Identifier')
    content_heading = Column(String(255), comment='Page Content Heading')
    content = Column(MEDIUMTEXT, comment='Page Content')
    creation_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Page Creation Time')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Page Modification Time')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Is Page Active')
    sort_order = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Page Sort Order')
    layout_update_xml = Column(Text, comment='Page Layout Update Content')
    custom_theme = Column(String(100), comment='Page Custom Theme')
    custom_root_template = Column(String(255), comment='Page Custom Template')
    custom_layout_update_xml = Column(Text, comment='Page Custom Layout Update Content')
    layout_update_selected = Column(String(128), comment='Page Custom Layout File')
    custom_theme_from = Column(Date, comment='Page Custom Theme Active From Date')
    custom_theme_to = Column(Date, comment='Page Custom Theme Active To Date')
    meta_title = Column(String(255), comment='Page Meta Title')

    stores = relationship('Store', secondary='cms_page_store')


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


t_cms_block_store = Table(
    'cms_block_store', metadata,
    Column('block_id', ForeignKey('cms_block.block_id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('store_id', ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Store ID'),
    comment='CMS Block To Store Linkage Table'
)


t_cms_page_store = Table(
    'cms_page_store', metadata,
    Column('page_id', ForeignKey('cms_page.page_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Entity ID'),
    Column('store_id', ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Store ID'),
    comment='CMS Page To Store Linkage Table'
)
