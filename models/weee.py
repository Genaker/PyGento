# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CatalogProductEntity(Base):
    __tablename__ = 'catalog_product_entity'
    __table_args__ = {'comment': 'Catalog Product Table'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    attribute_set_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Attribute Set ID')
    type_id = Column(String(32), nullable=False, server_default=text("'simple'"), comment='Type ID')
    sku = Column(String(64), index=True, comment='SKU')
    has_options = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Has Options')
    required_options = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Required Options')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Creation Time')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Update Time')


class DirectoryCountry(Base):
    __tablename__ = 'directory_country'
    __table_args__ = {'comment': 'Directory Country'}

    country_id = Column(String(2), primary_key=True, comment='Country ID in ISO-2')
    iso2_code = Column(String(2), comment='Country ISO-2 format')
    iso3_code = Column(String(3), comment='Country ISO-3')


class EavEntityType(Base):
    __tablename__ = 'eav_entity_type'
    __table_args__ = {'comment': 'Eav Entity Type'}

    entity_type_id = Column(SMALLINT(5), primary_key=True, comment='Entity Type ID')
    entity_type_code = Column(String(50), nullable=False, index=True, comment='Entity Type Code')
    entity_model = Column(String(255), nullable=False, comment='Entity Model')
    attribute_model = Column(String(255), comment='Attribute Model')
    entity_table = Column(String(255), comment='Entity Table')
    value_table_prefix = Column(String(255), comment='Value Table Prefix')
    entity_id_field = Column(String(255), comment='Entity ID Field')
    is_data_sharing = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Defines Is Data Sharing')
    data_sharing_key = Column(String(100), server_default=text("'default'"), comment='Data Sharing Key')
    default_attribute_set_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Default Attribute Set ID')
    increment_model = Column(String(255), comment='Increment Model')
    increment_per_store = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Increment Per Store')
    increment_pad_length = Column(SMALLINT(5), nullable=False, server_default=text("8"), comment='Increment Pad Length')
    increment_pad_char = Column(String(1), nullable=False, server_default=text("'0'"), comment='Increment Pad Char')
    additional_attribute_table = Column(String(255), comment='Additional Attribute Table')
    entity_attribute_collection = Column(String(255), comment='Entity Attribute Collection')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class EavAttribute(Base):
    __tablename__ = 'eav_attribute'
    __table_args__ = (
        Index('EAV_ATTRIBUTE_ENTITY_TYPE_ID_ATTRIBUTE_CODE', 'entity_type_id', 'attribute_code', unique=True),
        {'comment': 'Eav Attribute'}
    )

    attribute_id = Column(SMALLINT(5), primary_key=True, comment='Attribute ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_code = Column(String(255), nullable=False, comment='Attribute Code')
    attribute_model = Column(String(255), comment='Attribute Model')
    backend_model = Column(String(255), comment='Backend Model')
    backend_type = Column(String(8), nullable=False, server_default=text("'static'"), comment='Backend Type')
    backend_table = Column(String(255), comment='Backend Table')
    frontend_model = Column(String(255), comment='Frontend Model')
    frontend_input = Column(String(50), comment='Frontend Input')
    frontend_label = Column(String(255), comment='Frontend Label')
    frontend_class = Column(String(255), comment='Frontend Class')
    source_model = Column(String(255), comment='Source Model')
    is_required = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Defines Is Required')
    is_user_defined = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Defines Is User Defined')
    default_value = Column(Text, comment='Default Value')
    is_unique = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Defines Is Unique')
    note = Column(String(255), comment='Note')

    entity_type = relationship('EavEntityType')


class WeeeTax(Base):
    __tablename__ = 'weee_tax'
    __table_args__ = {'comment': 'Weee Tax'}

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    country = Column(ForeignKey('directory_country.country_id', ondelete='CASCADE'), index=True, comment='Country')
    value = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Value')
    state = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='State')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, comment='Attribute ID')

    attribute = relationship('EavAttribute')
    directory_country = relationship('DirectoryCountry')
    entity = relationship('CatalogProductEntity')
    website = relationship('StoreWebsite')
