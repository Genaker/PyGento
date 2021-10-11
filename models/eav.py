# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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

    types = relationship('EavFormType', secondary='eav_form_type_entity')


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


class EavAttributeSet(Base):
    __tablename__ = 'eav_attribute_set'
    __table_args__ = (
        Index('EAV_ATTRIBUTE_SET_ENTITY_TYPE_ID_ATTRIBUTE_SET_NAME', 'entity_type_id', 'attribute_set_name', unique=True),
        Index('EAV_ATTRIBUTE_SET_ENTITY_TYPE_ID_SORT_ORDER', 'entity_type_id', 'sort_order'),
        {'comment': 'Eav Attribute Set'}
    )

    attribute_set_id = Column(SMALLINT(5), primary_key=True, comment='Attribute Set ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_set_name = Column(String(255), comment='Attribute Set Name')
    sort_order = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Sort Order')

    entity_type = relationship('EavEntityType')


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


class EavAttributeGroup(Base):
    __tablename__ = 'eav_attribute_group'
    __table_args__ = (
        Index('EAV_ATTRIBUTE_GROUP_ATTRIBUTE_SET_ID_ATTRIBUTE_GROUP_NAME', 'attribute_set_id', 'attribute_group_name', unique=True),
        Index('EAV_ATTRIBUTE_GROUP_ATTRIBUTE_SET_ID_SORT_ORDER', 'attribute_set_id', 'sort_order'),
        Index('EAV_ATTRIBUTE_GROUP_ATTRIBUTE_SET_ID_ATTRIBUTE_GROUP_CODE', 'attribute_set_id', 'attribute_group_code', unique=True),
        {'comment': 'Eav Attribute Group'}
    )

    attribute_group_id = Column(SMALLINT(5), primary_key=True, comment='Attribute Group ID')
    attribute_set_id = Column(ForeignKey('eav_attribute_set.attribute_set_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Attribute Set ID')
    attribute_group_name = Column(String(255), comment='Attribute Group Name')
    sort_order = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Sort Order')
    default_id = Column(SMALLINT(5), server_default=text("0"), comment='Default ID')
    attribute_group_code = Column(String(255), nullable=False, comment='Attribute Group Code')
    tab_group_code = Column(String(255), comment='Tab Group Code')

    attribute_set = relationship('EavAttributeSet')


class EavAttributeOption(Base):
    __tablename__ = 'eav_attribute_option'
    __table_args__ = {'comment': 'Eav Attribute Option'}

    option_id = Column(INTEGER(10), primary_key=True, comment='Option ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    sort_order = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Sort Order')

    attribute = relationship('EavAttribute')


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


class EavAttributeLabel(Base):
    __tablename__ = 'eav_attribute_label'
    __table_args__ = (
        Index('EAV_ATTRIBUTE_LABEL_ATTRIBUTE_ID_STORE_ID', 'attribute_id', 'store_id'),
        {'comment': 'Eav Attribute Label'}
    )

    attribute_label_id = Column(INTEGER(10), primary_key=True, comment='Attribute Label ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    value = Column(String(255), comment='Value')

    attribute = relationship('EavAttribute')
    store = relationship('Store')


class EavAttributeOptionSwatch(Base):
    __tablename__ = 'eav_attribute_option_swatch'
    __table_args__ = (
        Index('EAV_ATTRIBUTE_OPTION_SWATCH_STORE_ID_OPTION_ID', 'store_id', 'option_id', unique=True),
        {'comment': 'Magento Swatches table'}
    )

    swatch_id = Column(INTEGER(10), primary_key=True, index=True, comment='Swatch ID')
    option_id = Column(ForeignKey('eav_attribute_option.option_id', ondelete='CASCADE'), nullable=False, index=True, comment='Option ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, comment='Store ID')
    type = Column(SMALLINT(5), nullable=False, comment='Swatch type: 0 - text, 1 - visual color, 2 - visual image')
    value = Column(String(255), comment='Swatch Value')

    option = relationship('EavAttributeOption')
    store = relationship('Store')


class EavAttributeOptionValue(Base):
    __tablename__ = 'eav_attribute_option_value'
    __table_args__ = {'comment': 'Eav Attribute Option Value'}

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    option_id = Column(ForeignKey('eav_attribute_option.option_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Option ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    value = Column(String(255), comment='Value')

    option = relationship('EavAttributeOption')
    store = relationship('Store')


class EavEntity(Base):
    __tablename__ = 'eav_entity'
    __table_args__ = {'comment': 'Eav Entity'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity Type ID')
    attribute_set_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute Set ID')
    increment_id = Column(String(50), comment='Increment ID')
    parent_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Parent ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Defines Is Entity Active')

    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavEntityAttribute(Base):
    __tablename__ = 'eav_entity_attribute'
    __table_args__ = (
        Index('EAV_ENTITY_ATTRIBUTE_ATTRIBUTE_SET_ID_SORT_ORDER', 'attribute_set_id', 'sort_order'),
        Index('EAV_ENTITY_ATTRIBUTE_ATTRIBUTE_SET_ID_ATTRIBUTE_ID', 'attribute_set_id', 'attribute_id', unique=True),
        Index('EAV_ENTITY_ATTRIBUTE_ATTRIBUTE_GROUP_ID_ATTRIBUTE_ID', 'attribute_group_id', 'attribute_id', unique=True),
        {'comment': 'Eav Entity Attributes'}
    )

    entity_attribute_id = Column(INTEGER(10), primary_key=True, comment='Entity Attribute ID')
    entity_type_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_set_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute Set ID')
    attribute_group_id = Column(ForeignKey('eav_attribute_group.attribute_group_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Attribute Group ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    sort_order = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Sort Order')

    attribute_group = relationship('EavAttributeGroup')
    attribute = relationship('EavAttribute')


class EavEntityStore(Base):
    __tablename__ = 'eav_entity_store'
    __table_args__ = {'comment': 'Eav Entity Store'}

    entity_store_id = Column(INTEGER(10), primary_key=True, comment='Entity Store ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity Type ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    increment_prefix = Column(String(20), comment='Increment Prefix')
    increment_last_id = Column(String(50), comment='Last Incremented ID')

    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavFormType(Base):
    __tablename__ = 'eav_form_type'
    __table_args__ = (
        Index('EAV_FORM_TYPE_CODE_THEME_STORE_ID', 'code', 'theme', 'store_id', unique=True),
        {'comment': 'Eav Form Type'}
    )

    type_id = Column(SMALLINT(5), primary_key=True, comment='Type ID')
    code = Column(String(64), nullable=False, comment='Code')
    label = Column(String(255), nullable=False, comment='Label')
    is_system = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is System')
    theme = Column(String(64), comment='Theme')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, comment='Store ID')

    store = relationship('Store')


class EavEntityDatetime(Base):
    __tablename__ = 'eav_entity_datetime'
    __table_args__ = (
        Index('EAV_ENTITY_DATETIME_ATTRIBUTE_ID_VALUE', 'attribute_id', 'value'),
        Index('EAV_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        Index('EAV_ENTITY_DATETIME_ENTITY_TYPE_ID_VALUE', 'entity_type_id', 'value'),
        {'comment': 'Eav Entity Value Prefix'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('eav_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DateTime, comment='Attribute Value')

    entity = relationship('EavEntity')
    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavEntityDecimal(Base):
    __tablename__ = 'eav_entity_decimal'
    __table_args__ = (
        Index('EAV_ENTITY_DECIMAL_ENTITY_TYPE_ID_VALUE', 'entity_type_id', 'value'),
        Index('EAV_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        Index('EAV_ENTITY_DECIMAL_ATTRIBUTE_ID_VALUE', 'attribute_id', 'value'),
        {'comment': 'Eav Entity Value Prefix'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('eav_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Attribute Value')

    entity = relationship('EavEntity')
    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavEntityInt(Base):
    __tablename__ = 'eav_entity_int'
    __table_args__ = (
        Index('EAV_ENTITY_INT_ATTRIBUTE_ID_VALUE', 'attribute_id', 'value'),
        Index('EAV_ENTITY_INT_ENTITY_TYPE_ID_VALUE', 'entity_type_id', 'value'),
        Index('EAV_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Eav Entity Value Prefix'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('eav_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Attribute Value')

    entity = relationship('EavEntity')
    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavEntityText(Base):
    __tablename__ = 'eav_entity_text'
    __table_args__ = (
        Index('EAV_ENTITY_TEXT_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Eav Entity Value Prefix'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity Type ID')
    attribute_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('eav_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(Text, nullable=False, comment='Attribute Value')

    entity = relationship('EavEntity')
    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavEntityVarchar(Base):
    __tablename__ = 'eav_entity_varchar'
    __table_args__ = (
        Index('EAV_ENTITY_VARCHAR_ATTRIBUTE_ID_VALUE', 'attribute_id', 'value'),
        Index('EAV_ENTITY_VARCHAR_ENTITY_TYPE_ID_VALUE', 'entity_type_id', 'value'),
        Index('EAV_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Eav Entity Value Prefix'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    entity_type_id = Column(ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity Type ID')
    attribute_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('eav_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(String(255), comment='Attribute Value')

    entity = relationship('EavEntity')
    entity_type = relationship('EavEntityType')
    store = relationship('Store')


class EavFormFieldset(Base):
    __tablename__ = 'eav_form_fieldset'
    __table_args__ = (
        Index('EAV_FORM_FIELDSET_TYPE_ID_CODE', 'type_id', 'code', unique=True),
        {'comment': 'Eav Form Fieldset'}
    )

    fieldset_id = Column(SMALLINT(5), primary_key=True, comment='Fieldset ID')
    type_id = Column(ForeignKey('eav_form_type.type_id', ondelete='CASCADE'), nullable=False, comment='Type ID')
    code = Column(String(64), nullable=False, comment='Code')
    sort_order = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Sort Order')

    type = relationship('EavFormType')


t_eav_form_type_entity = Table(
    'eav_form_type_entity', metadata,
    Column('type_id', ForeignKey('eav_form_type.type_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Type ID'),
    Column('entity_type_id', ForeignKey('eav_entity_type.entity_type_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Entity Type ID'),
    comment='Eav Form Type Entity'
)


class EavFormElement(Base):
    __tablename__ = 'eav_form_element'
    __table_args__ = (
        Index('EAV_FORM_ELEMENT_TYPE_ID_ATTRIBUTE_ID', 'type_id', 'attribute_id', unique=True),
        {'comment': 'Eav Form Element'}
    )

    element_id = Column(INTEGER(10), primary_key=True, comment='Element ID')
    type_id = Column(ForeignKey('eav_form_type.type_id', ondelete='CASCADE'), nullable=False, comment='Type ID')
    fieldset_id = Column(ForeignKey('eav_form_fieldset.fieldset_id', ondelete='SET NULL'), index=True, comment='Fieldset ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, comment='Attribute ID')
    sort_order = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Sort Order')

    attribute = relationship('EavAttribute')
    fieldset = relationship('EavFormFieldset')
    type = relationship('EavFormType')


class EavFormFieldsetLabel(Base):
    __tablename__ = 'eav_form_fieldset_label'
    __table_args__ = {'comment': 'Eav Form Fieldset Label'}

    fieldset_id = Column(ForeignKey('eav_form_fieldset.fieldset_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Fieldset ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Store ID')
    label = Column(String(255), nullable=False, comment='Label')

    fieldset = relationship('EavFormFieldset')
    store = relationship('Store')
