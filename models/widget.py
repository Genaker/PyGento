# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
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

    pages = relationship('WidgetInstancePage', secondary='widget_instance_page_layout')


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


class Widget(Base):
    __tablename__ = 'widget'
    __table_args__ = {'comment': 'Preconfigured Widgets'}

    widget_id = Column(INTEGER(10), primary_key=True, comment='Widget ID')
    widget_code = Column(String(255), index=True, comment='Widget code for template directive')
    widget_type = Column(String(255), comment='Widget Type')
    parameters = Column(Text, comment='Parameters')


class WidgetInstance(Base):
    __tablename__ = 'widget_instance'
    __table_args__ = {'comment': 'Instances of Widget for Package Theme'}

    instance_id = Column(INTEGER(10), primary_key=True, comment='Instance ID')
    instance_type = Column(String(255), comment='Instance Type')
    theme_id = Column(ForeignKey('theme.theme_id', ondelete='CASCADE'), nullable=False, index=True, comment='Theme ID')
    title = Column(String(255), comment='Widget Title')
    store_ids = Column(String(255), nullable=False, server_default=text("'0'"), comment='Store ids')
    widget_parameters = Column(Text, comment='Widget parameters')
    sort_order = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Sort order')

    theme = relationship('Theme')


class WidgetInstancePage(Base):
    __tablename__ = 'widget_instance_page'
    __table_args__ = {'comment': 'Instance of Widget on Page'}

    page_id = Column(INTEGER(10), primary_key=True, comment='Page ID')
    instance_id = Column(ForeignKey('widget_instance.instance_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Instance ID')
    page_group = Column(String(25), comment='Block Group Type')
    layout_handle = Column(String(255), comment='Layout Handle')
    block_reference = Column(String(255), comment='Container')
    page_for = Column(String(25), comment='For instance entities')
    entities = Column(Text, comment='Catalog entities (comma separated)')
    page_template = Column(String(255), comment='Path to widget template')

    instance = relationship('WidgetInstance')


t_widget_instance_page_layout = Table(
    'widget_instance_page_layout', metadata,
    Column('page_id', ForeignKey('widget_instance_page.page_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Page ID'),
    Column('layout_update_id', ForeignKey('layout_update.layout_update_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Layout Update ID'),
    Index('WIDGET_INSTANCE_PAGE_LAYOUT_LAYOUT_UPDATE_ID_PAGE_ID', 'layout_update_id', 'page_id', unique=True),
    comment='Layout updates'
)
