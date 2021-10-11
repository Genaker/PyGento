# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class LayoutUpdate(Base):
    __tablename__ = 'layout_update'
    __table_args__ = {'comment': 'Layout Updates'}

    layout_update_id = Column(INTEGER(10), primary_key=True, comment='Layout Update ID')
    handle = Column(String(255), index=True, comment='Handle')
    xml = Column(Text, comment='Xml')
    sort_order = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Sort Order')
    updated_at = Column(TIMESTAMP, server_default=text("'0000-00-00 00:00:00'"))


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class Theme(Base):
    __tablename__ = 'theme'
    __table_args__ = {'comment': 'Core theme'}

    theme_id = Column(INTEGER(10), primary_key=True, comment='Theme identifier')
    parent_id = Column(INTEGER(11), comment='Parent ID')
    theme_path = Column(String(255), comment='Theme Path')
    theme_title = Column(String(255), nullable=False, comment='Theme Title')
    preview_image = Column(String(255), comment='Preview Image')
    is_featured = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Is Theme Featured')
    area = Column(String(255), nullable=False, comment='Theme Area')
    type = Column(SMALLINT(6), nullable=False, comment='Theme type: 0:physical, 1:virtual, 2:staging')
    code = Column(Text, comment='Full theme code, including package')


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


class LayoutLink(Base):
    __tablename__ = 'layout_link'
    __table_args__ = (
        Index('LAYOUT_LINK_STORE_ID_THEME_ID_LAYOUT_UPDATE_ID_IS_TEMPORARY', 'store_id', 'theme_id', 'layout_update_id', 'is_temporary'),
        {'comment': 'Layout Link'}
    )

    layout_link_id = Column(INTEGER(10), primary_key=True, comment='Link ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Store ID')
    theme_id = Column(ForeignKey('theme.theme_id', ondelete='CASCADE'), nullable=False, index=True, comment='Theme ID')
    layout_update_id = Column(ForeignKey('layout_update.layout_update_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Layout Update ID')
    is_temporary = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Defines whether Layout Update is Temporary')

    layout_update = relationship('LayoutUpdate')
    store = relationship('Store')
    theme = relationship('Theme')
