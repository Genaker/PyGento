# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CheckoutAgreement(Base):
    __tablename__ = 'checkout_agreement'
    __table_args__ = {'comment': 'Checkout Agreement'}

    agreement_id = Column(INTEGER(10), primary_key=True, comment='Agreement ID')
    name = Column(String(255), comment='Name')
    content = Column(Text, comment='Content')
    content_height = Column(String(25), comment='Content Height')
    checkbox_text = Column(Text, comment='Checkbox Text')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Active')
    is_html = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Html')
    mode = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Applied mode')

    stores = relationship('Store', secondary='checkout_agreement_store')


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


t_checkout_agreement_store = Table(
    'checkout_agreement_store', metadata,
    Column('agreement_id', ForeignKey('checkout_agreement.agreement_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Agreement ID'),
    Column('store_id', ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Store ID'),
    comment='Checkout Agreement Store'
)
