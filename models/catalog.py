# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CatalogCategoryEntity(Base):
    __tablename__ = 'catalog_category_entity'
    __table_args__ = {'comment': 'Catalog Category Table'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    attribute_set_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute Set ID')
    parent_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Parent Category ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Creation Time')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Update Time')
    path = Column(String(255), nullable=False, index=True, comment='Tree Path')
    position = Column(INTEGER(11), nullable=False, comment='Position')
    level = Column(INTEGER(11), nullable=False, index=True, server_default=text("0"), comment='Tree Level')
    children_count = Column(INTEGER(11), nullable=False, comment='Child Count')


class CatalogCategoryProductIndex(Base):
    __tablename__ = 'catalog_category_product_index'
    __table_args__ = (
        Index('CAT_CTGR_PRD_IDX_STORE_ID_CTGR_ID_VISIBILITY_IS_PARENT_POSITION', 'store_id', 'category_id', 'visibility', 'is_parent', 'position'),
        Index('CAT_CTGR_PRD_IDX_PRD_ID_STORE_ID_CTGR_ID_VISIBILITY', 'product_id', 'store_id', 'category_id', 'visibility'),
        {'comment': 'Catalog Category Product Index'}
    )

    category_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Category ID')
    product_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Product ID')
    position = Column(INTEGER(11), comment='Position')
    is_parent = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Parent')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, server_default=text("0"), comment='Store ID')
    visibility = Column(SMALLINT(5), nullable=False, comment='Visibility')



class CatalogCategoryProductIndexStore1(Base):
    __tablename__ = 'catalog_category_product_index_store1'
    __table_args__ = (
        Index('CAT_CTGR_PRD_IDX_STORE1_PRD_ID_STORE_ID_CTGR_ID_VISIBILITY', 'product_id', 'store_id', 'category_id', 'visibility'),
        Index('IDX_216E521C8AD125E066D2B0BAB4A08412', 'store_id', 'category_id', 'visibility', 'is_parent', 'position'),
        {'comment': 'Catalog Category Product Index Store1'}
    )

    category_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Category Id')
    product_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Product Id')
    position = Column(INTEGER(11), comment='Position')
    is_parent = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Parent')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, server_default=text("0"), comment='Store Id')
    visibility = Column(SMALLINT(5), nullable=False, comment='Visibility')
    

class CatalogCategoryProductIndexTmp(Base):
    __tablename__ = 'catalog_category_product_index_tmp'
    __table_args__ = (
        Index('CAT_CTGR_PRD_IDX_TMP_PRD_ID_CTGR_ID_STORE_ID', 'product_id', 'category_id', 'store_id'),
        {'comment': 'Catalog Category Product Indexer temporary table'}
    )

    category_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Category ID')
    product_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Product ID')
    position = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Position')
    is_parent = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Parent')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, server_default=text("0"), comment='Store ID')
    visibility = Column(SMALLINT(5), nullable=False, comment='Visibility')


class CatalogProductBundleStockIndex(Base):
    __tablename__ = 'catalog_product_bundle_stock_index'
    __table_args__ = {'comment': 'Catalog Product Bundle Stock Index'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Stock ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    stock_status = Column(SMALLINT(6), server_default=text("0"), comment='Stock Status')


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

    gallery = relationship('CatalogProductEntityMediaGallery', secondary='catalog_product_entity_media_gallery_value_to_entity')
    parents = relationship(
        'CatalogProductEntity',
        secondary='catalog_product_relation',
        primaryjoin='CatalogProductEntity.entity_id == catalog_product_relation.c.child_id',
        secondaryjoin='CatalogProductEntity.entity_id == catalog_product_relation.c.parent_id'
    )
    varchar = relationship("CatalogProductEntityVarchar", back_populates="entity")
    decimal = relationship("CatalogProductEntityDecimal", back_populates="entity")
    datetime = relationship("CatalogProductEntityDatetime", back_populates="entity")
    text = relationship("CatalogProductEntityText", back_populates="entity")
    intager = relationship("CatalogProductEntityInt", back_populates="entity")
    
    websites = relationship('StoreWebsite', secondary='catalog_product_website')


class CatalogProductIndexEav(Base):
    __tablename__ = 'catalog_product_index_eav'
    __table_args__ = {'comment': 'Catalog Product EAV Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavDecimal(Base):
    __tablename__ = 'catalog_product_index_eav_decimal'
    __table_args__ = {'comment': 'Catalog Product EAV Decimal Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(DECIMAL(12, 4), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavDecimalIdx(Base):
    __tablename__ = 'catalog_product_index_eav_decimal_idx'
    __table_args__ = {'comment': 'Catalog Product EAV Decimal Indexer Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(DECIMAL(12, 4), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavDecimalReplica(Base):
    __tablename__ = 'catalog_product_index_eav_decimal_replica'
    __table_args__ = {'comment': 'Catalog Product EAV Decimal Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(DECIMAL(12, 4), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavDecimalTmp(Base):
    __tablename__ = 'catalog_product_index_eav_decimal_tmp'
    __table_args__ = {'comment': 'Catalog Product EAV Decimal Indexer Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(DECIMAL(12, 4), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavIdx(Base):
    __tablename__ = 'catalog_product_index_eav_idx'
    __table_args__ = {'comment': 'Catalog Product EAV Indexer Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavReplica(Base):
    __tablename__ = 'catalog_product_index_eav_replica'
    __table_args__ = {'comment': 'Catalog Product EAV Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexEavTmp(Base):
    __tablename__ = 'catalog_product_index_eav_tmp'
    __table_args__ = {'comment': 'Catalog Product EAV Indexer Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    attribute_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Attribute ID')
    store_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Store ID')
    value = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='Value')
    source_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Original entity ID for attribute value')


class CatalogProductIndexPrice(Base):
    __tablename__ = 'catalog_product_index_price'
    __table_args__ = (
        Index('CAT_PRD_IDX_PRICE_WS_ID_CSTR_GROUP_ID_MIN_PRICE', 'website_id', 'customer_group_id', 'min_price'),
        {'comment': 'Catalog Product Price Index Table'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    price = Column(DECIMAL(20, 6), comment='Price')
    final_price = Column(DECIMAL(20, 6), comment='Final Price')
    min_price = Column(DECIMAL(20, 6), index=True, comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceBundleIdx(Base):
    __tablename__ = 'catalog_product_index_price_bundle_idx'
    __table_args__ = {'comment': 'Catalog Product Index Price Bundle Idx'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    price_type = Column(SMALLINT(5), nullable=False, comment='Price Type')
    special_price = Column(DECIMAL(20, 6), comment='Special Price')
    tier_percent = Column(DECIMAL(20, 6), comment='Tier Percent')
    orig_price = Column(DECIMAL(20, 6), comment='Orig Price')
    price = Column(DECIMAL(20, 6), comment='Price')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')
    base_tier = Column(DECIMAL(20, 6), comment='Base Tier')


class CatalogProductIndexPriceBundleOptIdx(Base):
    __tablename__ = 'catalog_product_index_price_bundle_opt_idx'
    __table_args__ = {'comment': 'Catalog Product Index Price Bundle Opt Idx'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    alt_price = Column(DECIMAL(20, 6), comment='Alt Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')
    alt_tier_price = Column(DECIMAL(20, 6), comment='Alt Tier Price')


class CatalogProductIndexPriceBundleOptTmp(Base):
    __tablename__ = 'catalog_product_index_price_bundle_opt_tmp'
    __table_args__ = {'comment': 'Catalog Product Index Price Bundle Opt Tmp'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    alt_price = Column(DECIMAL(20, 6), comment='Alt Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')
    alt_tier_price = Column(DECIMAL(20, 6), comment='Alt Tier Price')


class CatalogProductIndexPriceBundleSelIdx(Base):
    __tablename__ = 'catalog_product_index_price_bundle_sel_idx'
    __table_args__ = {'comment': 'Catalog Product Index Price Bundle Sel Idx'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    selection_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Selection ID')
    group_type = Column(SMALLINT(5), server_default=text("0"), comment='Group Type')
    is_required = Column(SMALLINT(5), server_default=text("0"), comment='Is Required')
    price = Column(DECIMAL(20, 6), comment='Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceBundleSelTmp(Base):
    __tablename__ = 'catalog_product_index_price_bundle_sel_tmp'
    __table_args__ = {'comment': 'Catalog Product Index Price Bundle Sel Tmp'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    selection_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Selection ID')
    group_type = Column(SMALLINT(5), server_default=text("0"), comment='Group Type')
    is_required = Column(SMALLINT(5), server_default=text("0"), comment='Is Required')
    price = Column(DECIMAL(20, 6), comment='Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceBundleTmp(Base):
    __tablename__ = 'catalog_product_index_price_bundle_tmp'
    __table_args__ = {'comment': 'Catalog Product Index Price Bundle Tmp'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    price_type = Column(SMALLINT(5), nullable=False, comment='Price Type')
    special_price = Column(DECIMAL(20, 6), comment='Special Price')
    tier_percent = Column(DECIMAL(20, 6), comment='Tier Percent')
    orig_price = Column(DECIMAL(20, 6), comment='Orig Price')
    price = Column(DECIMAL(20, 6), comment='Price')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')
    base_tier = Column(DECIMAL(20, 6), comment='Base Tier')


class CatalogProductIndexPriceCfgOptAgrIdx(Base):
    __tablename__ = 'catalog_product_index_price_cfg_opt_agr_idx'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Config Option Aggregate Index Table'}

    parent_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Parent ID')
    child_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Child ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    price = Column(DECIMAL(20, 6), comment='Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceCfgOptAgrTmp(Base):
    __tablename__ = 'catalog_product_index_price_cfg_opt_agr_tmp'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Config Option Aggregate Temp Table'}

    parent_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Parent ID')
    child_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Child ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    price = Column(DECIMAL(20, 6), comment='Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceCfgOptIdx(Base):
    __tablename__ = 'catalog_product_index_price_cfg_opt_idx'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Config Option Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceCfgOptTmp(Base):
    __tablename__ = 'catalog_product_index_price_cfg_opt_tmp'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Config Option Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceDownlodIdx(Base):
    __tablename__ = 'catalog_product_index_price_downlod_idx'
    __table_args__ = {'comment': 'Indexer Table for price of downloadable products'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Minimum price')
    max_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Maximum price')


class CatalogProductIndexPriceDownlodTmp(Base):
    __tablename__ = 'catalog_product_index_price_downlod_tmp'
    __table_args__ = {'comment': 'Temporary Indexer Table for price of downloadable products'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(11), primary_key=True, nullable=False)
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Minimum price')
    max_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Maximum price')


class CatalogProductIndexPriceFinalIdx(Base):
    __tablename__ = 'catalog_product_index_price_final_idx'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Final Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    orig_price = Column(DECIMAL(20, 6), comment='Original Price')
    price = Column(DECIMAL(20, 6), comment='Price')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')
    base_tier = Column(DECIMAL(20, 6), comment='Base Tier')


class CatalogProductIndexPriceFinalTmp(Base):
    __tablename__ = 'catalog_product_index_price_final_tmp'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Final Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    orig_price = Column(DECIMAL(20, 6), comment='Original Price')
    price = Column(DECIMAL(20, 6), comment='Price')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')
    base_tier = Column(DECIMAL(20, 6), comment='Base Tier')


class CatalogProductIndexPriceIdx(Base):
    __tablename__ = 'catalog_product_index_price_idx'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    price = Column(DECIMAL(20, 6), comment='Price')
    final_price = Column(DECIMAL(20, 6), comment='Final Price')
    min_price = Column(DECIMAL(20, 6), index=True, comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceOptAgrIdx(Base):
    __tablename__ = 'catalog_product_index_price_opt_agr_idx'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Option Aggregate Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceOptAgrTmp(Base):
    __tablename__ = 'catalog_product_index_price_opt_agr_tmp'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Option Aggregate Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    option_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Option ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceOptIdx(Base):
    __tablename__ = 'catalog_product_index_price_opt_idx'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Option Index Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceOptTmp(Base):
    __tablename__ = 'catalog_product_index_price_opt_tmp'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Option Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceReplica(Base):
    __tablename__ = 'catalog_product_index_price_replica'
    __table_args__ = (
        Index('CAT_PRD_IDX_PRICE_WS_ID_CSTR_GROUP_ID_MIN_PRICE', 'website_id', 'customer_group_id', 'min_price'),
        {'comment': 'Catalog Product Price Index Table'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    price = Column(DECIMAL(20, 6), comment='Price')
    final_price = Column(DECIMAL(20, 6), comment='Final Price')
    min_price = Column(DECIMAL(20, 6), index=True, comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductIndexPriceTmp(Base):
    __tablename__ = 'catalog_product_index_price_tmp'
    __table_args__ = {'comment': 'Catalog Product Price Indexer Temp Table'}

    entity_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    tax_class_id = Column(SMALLINT(5), server_default=text("0"), comment='Tax Class ID')
    price = Column(DECIMAL(20, 6), comment='Price')
    final_price = Column(DECIMAL(20, 6), comment='Final Price')
    min_price = Column(DECIMAL(20, 6), index=True, comment='Min Price')
    max_price = Column(DECIMAL(20, 6), comment='Max Price')
    tier_price = Column(DECIMAL(20, 6), comment='Tier Price')


class CatalogProductLinkType(Base):
    __tablename__ = 'catalog_product_link_type'
    __table_args__ = {'comment': 'Catalog Product Link Type Table'}

    link_type_id = Column(SMALLINT(5), primary_key=True, comment='Link Type ID')
    code = Column(String(32), comment='Code')


class CataloginventoryStock(Base):
    __tablename__ = 'cataloginventory_stock'
    __table_args__ = {'comment': 'Cataloginventory Stock'}

    stock_id = Column(SMALLINT(5), primary_key=True, comment='Stock ID')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')
    stock_name = Column(String(255), comment='Stock Name')


class CataloginventoryStockStatu(Base):
    __tablename__ = 'cataloginventory_stock_status'
    __table_args__ = {'comment': 'Cataloginventory Stock Status'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, index=True, comment='Stock Status')


class CataloginventoryStockStatusIdx(Base):
    __tablename__ = 'cataloginventory_stock_status_idx'
    __table_args__ = {'comment': 'Cataloginventory Stock Status Indexer Idx'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, comment='Stock Status')


class CataloginventoryStockStatusReplica(Base):
    __tablename__ = 'cataloginventory_stock_status_replica'
    __table_args__ = {'comment': 'Cataloginventory Stock Status'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, index=True, comment='Stock Status')


class CataloginventoryStockStatusTmp(Base):
    __tablename__ = 'cataloginventory_stock_status_tmp'
    __table_args__ = {'comment': 'Cataloginventory Stock Status Indexer Tmp'}

    product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Product ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Website ID')
    stock_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, comment='Stock ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty')
    stock_status = Column(SMALLINT(5), nullable=False, comment='Stock Status')


class Catalogrule(Base):
    __tablename__ = 'catalogrule'
    __table_args__ = (
        Index('CATALOGRULE_IS_ACTIVE_SORT_ORDER_TO_DATE_FROM_DATE', 'is_active', 'sort_order', 'to_date', 'from_date'),
        {'comment': 'CatalogRule'}
    )

    rule_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    name = Column(String(255), comment='Name')
    description = Column(Text, comment='Description')
    from_date = Column(Date, comment='From')
    to_date = Column(Date, comment='To')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Is Active')
    conditions_serialized = Column(MEDIUMTEXT, comment='Conditions Serialized')
    actions_serialized = Column(MEDIUMTEXT, comment='Actions Serialized')
    stop_rules_processing = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Stop Rules Processing')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    simple_action = Column(String(32), comment='Simple Action')
    discount_amount = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Discount Amount')

    websites = relationship('StoreWebsite', secondary='catalogrule_website')


class CatalogruleGroupWebsite(Base):
    __tablename__ = 'catalogrule_group_website'
    __table_args__ = {'comment': 'CatalogRule Group Website'}

    rule_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Rule ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Website ID')


class CatalogruleGroupWebsiteReplica(Base):
    __tablename__ = 'catalogrule_group_website_replica'
    __table_args__ = {'comment': 'CatalogRule Group Website'}

    rule_id = Column(INTEGER(10), primary_key=True, nullable=False, server_default=text("0"), comment='Rule ID')
    customer_group_id = Column(INTEGER(10), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    website_id = Column(SMALLINT(5), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Website ID')


class CatalogruleProduct(Base):
    __tablename__ = 'catalogrule_product'
    __table_args__ = (
        Index('UNQ_EAA51B56FF092A0DCB795D1CEF812B7B', 'rule_id', 'from_time', 'to_time', 'website_id', 'customer_group_id', 'product_id', 'sort_order', unique=True),
        {'comment': 'CatalogRule Product'}
    )

    rule_product_id = Column(INTEGER(10), primary_key=True, comment='Rule Product ID')
    rule_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Rule ID')
    from_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='From Time')
    to_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='To time')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    action_operator = Column(String(10), server_default=text("'to_fixed'"), comment='Action Operator')
    action_amount = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Action Amount')
    action_stop = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Action Stop')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')


class CatalogruleProductPrice(Base):
    __tablename__ = 'catalogrule_product_price'
    __table_args__ = (
        Index('CATRULE_PRD_PRICE_RULE_DATE_WS_ID_CSTR_GROUP_ID_PRD_ID', 'rule_date', 'website_id', 'customer_group_id', 'product_id', unique=True),
        {'comment': 'CatalogRule Product Price'}
    )

    rule_product_price_id = Column(INTEGER(10), primary_key=True, comment='Rule Product PriceId')
    rule_date = Column(Date, nullable=False, comment='Rule Date')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    rule_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Rule Price')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')
    latest_start_date = Column(Date, comment='Latest StartDate')
    earliest_end_date = Column(Date, comment='Earliest EndDate')


class CatalogruleProductPriceReplica(Base):
    __tablename__ = 'catalogrule_product_price_replica'
    __table_args__ = (
        Index('CATRULE_PRD_PRICE_RULE_DATE_WS_ID_CSTR_GROUP_ID_PRD_ID', 'rule_date', 'website_id', 'customer_group_id', 'product_id', unique=True),
        {'comment': 'CatalogRule Product Price'}
    )

    rule_product_price_id = Column(INTEGER(10), primary_key=True, comment='Rule Product PriceId')
    rule_date = Column(Date, nullable=False, comment='Rule Date')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    rule_price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Rule Price')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')
    latest_start_date = Column(Date, comment='Latest StartDate')
    earliest_end_date = Column(Date, comment='Earliest EndDate')


class CatalogruleProductReplica(Base):
    __tablename__ = 'catalogrule_product_replica'
    __table_args__ = (
        Index('UNQ_EAA51B56FF092A0DCB795D1CEF812B7B', 'rule_id', 'from_time', 'to_time', 'website_id', 'customer_group_id', 'product_id', 'sort_order', unique=True),
        {'comment': 'CatalogRule Product'}
    )

    rule_product_id = Column(INTEGER(10), primary_key=True, comment='Rule Product ID')
    rule_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Rule ID')
    from_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='From Time')
    to_time = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='To time')
    customer_group_id = Column(INTEGER(11), index=True)
    product_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    action_operator = Column(String(10), server_default=text("'to_fixed'"), comment='Action Operator')
    action_amount = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Action Amount')
    action_stop = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Action Stop')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')
    website_id = Column(SMALLINT(5), nullable=False, index=True, comment='Website ID')


class CustomerGroup(Base):
    __tablename__ = 'customer_group'
    __table_args__ = {'comment': 'Customer Group'}

    customer_group_id = Column(INTEGER(10), primary_key=True)
    customer_group_code = Column(String(32), nullable=False, comment='Customer Group Code')
    tax_class_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Tax Class ID')

    rules = relationship('Catalogrule', secondary='catalogrule_customer_group')


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


class CatalogProductIndexWebsite(StoreWebsite):
    __tablename__ = 'catalog_product_index_website'
    __table_args__ = {'comment': 'Catalog Product Website Index Table'}

    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, comment='Website ID')
    default_store_id = Column(SMALLINT(5), nullable=False, comment='Default store ID for website')
    website_date = Column(Date, index=True, comment='Website Date')
    rate = Column(Float, server_default=text("1"), comment='Rate')


class UrlRewrite(Base):
    __tablename__ = 'url_rewrite'
    __table_args__ = (
        Index('URL_REWRITE_STORE_ID_ENTITY_ID', 'store_id', 'entity_id'),
        Index('URL_REWRITE_REQUEST_PATH_STORE_ID', 'request_path', 'store_id', unique=True),
        {'comment': 'Url Rewrites'}
    )

    url_rewrite_id = Column(INTEGER(10), primary_key=True, comment='Rewrite ID')
    entity_type = Column(String(32), nullable=False, comment='Entity type code')
    entity_id = Column(INTEGER(10), nullable=False, index=True, comment='Entity ID')
    request_path = Column(String(255), comment='Request Path')
    target_path = Column(String(255), index=True, comment='Target Path')
    redirect_type = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Redirect Type')
    store_id = Column(SMALLINT(5), nullable=False, comment='Store ID')
    description = Column(String(255), comment='Description')
    is_autogenerated = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is rewrite generated automatically flag')
    metadata_ = Column('metadata', String(255), comment='Meta data for url rewrite')


class CatalogCategoryProduct(Base):
    __tablename__ = 'catalog_category_product'
    __table_args__ = (
        Index('CATALOG_CATEGORY_PRODUCT_CATEGORY_ID_PRODUCT_ID', 'category_id', 'product_id', unique=True),
        {'comment': 'Catalog Product To Category Linkage Table'}
    )

    entity_id = Column(INTEGER(11), primary_key=True, nullable=False, comment='Entity ID')
    category_id = Column(ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, server_default=text("0"), comment='Category ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Product ID')
    position = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Position')

    category = relationship('CatalogCategoryEntity')
    product = relationship('CatalogProductEntity')


class CatalogProductBundleOption(Base):
    __tablename__ = 'catalog_product_bundle_option'
    __table_args__ = {'comment': 'Catalog Product Bundle Option'}

    option_id = Column(INTEGER(10), primary_key=True, comment='Option ID')
    parent_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Parent ID')
    required = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Required')
    position = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Position')
    type = Column(String(255), comment='Type')

    parent = relationship('CatalogProductEntity')


class CatalogProductBundlePriceIndex(Base):
    __tablename__ = 'catalog_product_bundle_price_index'
    __table_args__ = {'comment': 'Catalog Product Bundle Price Index'}

    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Entity ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID')
    customer_group_id = Column(ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer Group ID')
    min_price = Column(DECIMAL(20, 6), nullable=False, comment='Min Price')
    max_price = Column(DECIMAL(20, 6), nullable=False, comment='Max Price')

    customer_group = relationship('CustomerGroup')
    entity = relationship('CatalogProductEntity')
    website = relationship('StoreWebsite')


class CatalogProductEntityTierPrice(Base):
    __tablename__ = 'catalog_product_entity_tier_price'
    __table_args__ = (
        Index('UNQ_E8AB433B9ACB00343ABB312AD2FAB087', 'entity_id', 'all_groups', 'customer_group_id', 'qty', 'website_id', unique=True),
        {'comment': 'Catalog Product Tier Price Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    all_groups = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Applicable To All Customer Groups')
    customer_group_id = Column(ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Customer Group ID')
    qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("1.0000"), comment='QTY')
    value = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Value')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, comment='Website ID')
    percentage_value = Column(DECIMAL(5, 2), comment='Percentage value')

    customer_group = relationship('CustomerGroup')
    entity = relationship('CatalogProductEntity')
    website = relationship('StoreWebsite')


class CatalogProductIndexTierPrice(Base):
    __tablename__ = 'catalog_product_index_tier_price'
    __table_args__ = {'comment': 'Catalog Product Tier Price Index Table'}

    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Entity ID')
    customer_group_id = Column(ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer Group ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID')
    min_price = Column(DECIMAL(20, 6), comment='Min Price')

    customer_group = relationship('CustomerGroup')
    entity = relationship('CatalogProductEntity')
    website = relationship('StoreWebsite')


class CatalogProductLink(Base):
    __tablename__ = 'catalog_product_link'
    __table_args__ = (
        Index('CATALOG_PRODUCT_LINK_LINK_TYPE_ID_PRODUCT_ID_LINKED_PRODUCT_ID', 'link_type_id', 'product_id', 'linked_product_id', unique=True),
        {'comment': 'Catalog Product To Product Linkage Table'}
    )

    link_id = Column(INTEGER(10), primary_key=True, comment='Link ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    linked_product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Linked Product ID')
    link_type_id = Column(ForeignKey('catalog_product_link_type.link_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Link Type ID')

    link_type = relationship('CatalogProductLinkType')
    linked_product = relationship('CatalogProductEntity', primaryjoin='CatalogProductLink.linked_product_id == CatalogProductEntity.entity_id')
    product = relationship('CatalogProductEntity', primaryjoin='CatalogProductLink.product_id == CatalogProductEntity.entity_id')


class CatalogProductLinkAttribute(Base):
    __tablename__ = 'catalog_product_link_attribute'
    __table_args__ = {'comment': 'Catalog Product Link Attribute Table'}

    product_link_attribute_id = Column(SMALLINT(5), primary_key=True, comment='Product Link Attribute ID')
    link_type_id = Column(ForeignKey('catalog_product_link_type.link_type_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Link Type ID')
    product_link_attribute_code = Column(String(32), comment='Product Link Attribute Code')
    data_type = Column(String(32), comment='Data Type')

    link_type = relationship('CatalogProductLinkType')


class CatalogProductOption(Base):
    __tablename__ = 'catalog_product_option'
    __table_args__ = {'comment': 'Catalog Product Option Table'}

    option_id = Column(INTEGER(10), primary_key=True, comment='Option ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    type = Column(String(50), comment='Type')
    is_require = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Is Required')
    sku = Column(String(64), comment='SKU')
    max_characters = Column(INTEGER(10), comment='Max Characters')
    file_extension = Column(String(50), comment='File Extension')
    image_size_x = Column(SMALLINT(5), comment='Image Size X')
    image_size_y = Column(SMALLINT(5), comment='Image Size Y')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')

    product = relationship('CatalogProductEntity')


t_catalog_product_relation = Table(
    'catalog_product_relation', metadata,
    Column('parent_id', ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Parent ID'),
    Column('child_id', ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Child ID'),
    comment='Catalog Product Relation Table'
)


class CatalogProductSuperAttribute(Base):
    __tablename__ = 'catalog_product_super_attribute'
    __table_args__ = (
        Index('CATALOG_PRODUCT_SUPER_ATTRIBUTE_PRODUCT_ID_ATTRIBUTE_ID', 'product_id', 'attribute_id', unique=True),
        {'comment': 'Catalog Product Super Attribute Table'}
    )

    product_super_attribute_id = Column(INTEGER(10), primary_key=True, comment='Product Super Attribute ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product ID')
    attribute_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Attribute ID')
    position = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Position')

    product = relationship('CatalogProductEntity')


class CatalogProductSuperLink(Base):
    __tablename__ = 'catalog_product_super_link'
    __table_args__ = (
        Index('CATALOG_PRODUCT_SUPER_LINK_PRODUCT_ID_PARENT_ID', 'product_id', 'parent_id', unique=True),
        {'comment': 'Catalog Product Super Link Table'}
    )

    link_id = Column(INTEGER(10), primary_key=True, comment='Link ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product ID')
    parent_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Parent ID')

    parent = relationship('CatalogProductEntity', primaryjoin='CatalogProductSuperLink.parent_id == CatalogProductEntity.entity_id')
    product = relationship('CatalogProductEntity', primaryjoin='CatalogProductSuperLink.product_id == CatalogProductEntity.entity_id')


t_catalog_product_website = Table(
    'catalog_product_website', metadata,
    Column('product_id', ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Product ID'),
    Column('website_id', ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID'),
    comment='Catalog Product To Website Linkage Table'
)


t_catalog_url_rewrite_product_category = Table(
    'catalog_url_rewrite_product_category', metadata,
    Column('url_rewrite_id', ForeignKey('url_rewrite.url_rewrite_id', ondelete='CASCADE'), nullable=False, index=True, comment='url_rewrite_id'),
    Column('category_id', ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), nullable=False, comment='category_id'),
    Column('product_id', ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='product_id'),
    Index('CATALOG_URL_REWRITE_PRODUCT_CATEGORY_CATEGORY_ID_PRODUCT_ID', 'category_id', 'product_id'),
    comment='url_rewrite_relation'
)


class CataloginventoryStockItem(Base):
    __tablename__ = 'cataloginventory_stock_item'
    __table_args__ = (
        Index('CATALOGINVENTORY_STOCK_ITEM_PRODUCT_ID_STOCK_ID', 'product_id', 'stock_id', unique=True),
        {'comment': 'Cataloginventory Stock Item'}
    )

    item_id = Column(INTEGER(10), primary_key=True, comment='Item ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product ID')
    stock_id = Column(ForeignKey('cataloginventory_stock.stock_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Stock ID')
    qty = Column(DECIMAL(12, 4), comment='Qty')
    min_qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Min Qty')
    use_config_min_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Min Qty')
    is_qty_decimal = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Qty Decimal')
    backorders = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Backorders')
    use_config_backorders = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Backorders')
    min_sale_qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("1.0000"), comment='Min Sale Qty')
    use_config_min_sale_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Min Sale Qty')
    max_sale_qty = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Max Sale Qty')
    use_config_max_sale_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Max Sale Qty')
    is_in_stock = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is In Stock')
    low_stock_date = Column(TIMESTAMP, comment='Low Stock Date')
    notify_stock_qty = Column(DECIMAL(12, 4), comment='Notify Stock Qty')
    use_config_notify_stock_qty = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Notify Stock Qty')
    manage_stock = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Manage Stock')
    use_config_manage_stock = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Manage Stock')
    stock_status_changed_auto = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Stock Status Changed Automatically')
    use_config_qty_increments = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Qty Increments')
    qty_increments = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Qty Increments')
    use_config_enable_qty_inc = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Use Config Enable Qty Increments')
    enable_qty_increments = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Enable Qty Increments')
    is_decimal_divided = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Divided into Multiple Boxes for Shipping')
    website_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Website ID')

    product = relationship('CatalogProductEntity')
    stock = relationship('CataloginventoryStock')


t_catalogrule_customer_group = Table(
    'catalogrule_customer_group', metadata,
    Column('rule_id', ForeignKey('catalogrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID'),
    Column('customer_group_id', ForeignKey('customer_group.customer_group_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Customer Group ID'),
    comment='Catalog Rules To Customer Groups Relations'
)


t_catalogrule_website = Table(
    'catalogrule_website', metadata,
    Column('rule_id', ForeignKey('catalogrule.rule_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Rule ID'),
    Column('website_id', ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID'),
    comment='Catalog Rules To Websites Relations'
)


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


class CatalogEavAttribute(EavAttribute):
    __tablename__ = 'catalog_eav_attribute'
    __table_args__ = {'comment': 'Catalog EAV Attribute Table'}

    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), primary_key=True, comment='Attribute ID')
    frontend_input_renderer = Column(String(255), comment='Frontend Input Renderer')
    is_global = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Global')
    is_visible = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Visible')
    is_searchable = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Searchable')
    is_filterable = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Filterable')
    is_comparable = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Comparable')
    is_visible_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible On Front')
    is_html_allowed_on_front = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is HTML Allowed On Front')
    is_used_for_price_rules = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Used For Price Rules')
    is_filterable_in_search = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Filterable In Search')
    used_in_product_listing = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Is Used In Product Listing')
    used_for_sort_by = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Is Used For Sorting')
    apply_to = Column(String(255), comment='Apply To')
    is_visible_in_advanced_search = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible In Advanced Search')
    position = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Position')
    is_wysiwyg_enabled = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is WYSIWYG Enabled')
    is_used_for_promo_rules = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Used For Promo Rules')
    is_required_in_admin_store = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Required In Admin Store')
    is_used_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Used in Grid')
    is_visible_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Visible in Grid')
    is_filterable_in_grid = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Filterable in Grid')
    search_weight = Column(Float, nullable=False, server_default=text("1"), comment='Search Weight')
    additional_data = Column(Text, comment='Additional swatch attributes data')


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


class CatalogProductBundleOptionValue(Base):
    __tablename__ = 'catalog_product_bundle_option_value'
    __table_args__ = (
        Index('CAT_PRD_BNDL_OPT_VAL_OPT_ID_PARENT_PRD_ID_STORE_ID', 'option_id', 'parent_product_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Bundle Option Value'}
    )

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    option_id = Column(ForeignKey('catalog_product_bundle_option.option_id', ondelete='CASCADE'), nullable=False, comment='Option ID')
    store_id = Column(SMALLINT(5), nullable=False, comment='Store ID')
    title = Column(String(255), comment='Title')
    parent_product_id = Column(INTEGER(10), nullable=False, comment='Parent Product ID')

    option = relationship('CatalogProductBundleOption')


class CatalogProductBundleSelection(Base):
    __tablename__ = 'catalog_product_bundle_selection'
    __table_args__ = {'comment': 'Catalog Product Bundle Selection'}

    selection_id = Column(INTEGER(10), primary_key=True, comment='Selection ID')
    option_id = Column(ForeignKey('catalog_product_bundle_option.option_id', ondelete='CASCADE'), nullable=False, index=True, comment='Option ID')
    parent_product_id = Column(INTEGER(10), nullable=False, comment='Parent Product ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product ID')
    position = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Position')
    is_default = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Default')
    selection_price_type = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Selection Price Type')
    selection_price_value = Column(DECIMAL(12, 4), nullable=False, server_default=text("0.0000"), comment='Selection Price Value')
    selection_qty = Column(DECIMAL(12, 4), comment='Selection Qty')
    selection_can_change_qty = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Selection Can Change Qty')

    option = relationship('CatalogProductBundleOption')
    product = relationship('CatalogProductEntity')


class CatalogProductEntityMediaGallery(Base):
    __tablename__ = 'catalog_product_entity_media_gallery'
    __table_args__ = {'comment': 'Catalog Product Media Gallery Attribute Backend Table'}

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    value = Column(String(255), comment='Value')
    media_type = Column(String(32), nullable=False, server_default=text("'image'"), comment='Media entry type')
    disabled = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Visibility status')

    attribute = relationship('EavAttribute')


class CatalogProductLinkAttributeDecimal(Base):
    __tablename__ = 'catalog_product_link_attribute_decimal'
    __table_args__ = (
        Index('CAT_PRD_LNK_ATTR_DEC_PRD_LNK_ATTR_ID_LNK_ID', 'product_link_attribute_id', 'link_id', unique=True),
        {'comment': 'Catalog Product Link Decimal Attribute Table'}
    )

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    product_link_attribute_id = Column(ForeignKey('catalog_product_link_attribute.product_link_attribute_id', ondelete='CASCADE'), comment='Product Link Attribute ID')
    link_id = Column(ForeignKey('catalog_product_link.link_id', ondelete='CASCADE'), nullable=False, index=True, comment='Link ID')
    value = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Value')

    link = relationship('CatalogProductLink')
    product_link_attribute = relationship('CatalogProductLinkAttribute')


class CatalogProductLinkAttributeInt(Base):
    __tablename__ = 'catalog_product_link_attribute_int'
    __table_args__ = (
        Index('CAT_PRD_LNK_ATTR_INT_PRD_LNK_ATTR_ID_LNK_ID', 'product_link_attribute_id', 'link_id', unique=True),
        {'comment': 'Catalog Product Link Integer Attribute Table'}
    )

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    product_link_attribute_id = Column(ForeignKey('catalog_product_link_attribute.product_link_attribute_id', ondelete='CASCADE'), comment='Product Link Attribute ID')
    link_id = Column(ForeignKey('catalog_product_link.link_id', ondelete='CASCADE'), nullable=False, index=True, comment='Link ID')
    value = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Value')

    link = relationship('CatalogProductLink')
    product_link_attribute = relationship('CatalogProductLinkAttribute')


class CatalogProductLinkAttributeVarchar(Base):
    __tablename__ = 'catalog_product_link_attribute_varchar'
    __table_args__ = (
        Index('CAT_PRD_LNK_ATTR_VCHR_PRD_LNK_ATTR_ID_LNK_ID', 'product_link_attribute_id', 'link_id', unique=True),
        {'comment': 'Catalog Product Link Varchar Attribute Table'}
    )

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    product_link_attribute_id = Column(ForeignKey('catalog_product_link_attribute.product_link_attribute_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product Link Attribute ID')
    link_id = Column(ForeignKey('catalog_product_link.link_id', ondelete='CASCADE'), nullable=False, index=True, comment='Link ID')
    value = Column(String(255), comment='Value')

    link = relationship('CatalogProductLink')
    product_link_attribute = relationship('CatalogProductLinkAttribute')


class CatalogProductOptionTypeValue(Base):
    __tablename__ = 'catalog_product_option_type_value'
    __table_args__ = {'comment': 'Catalog Product Option Type Value Table'}

    option_type_id = Column(INTEGER(10), primary_key=True, comment='Option Type ID')
    option_id = Column(ForeignKey('catalog_product_option.option_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Option ID')
    sku = Column(String(64), comment='SKU')
    sort_order = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Sort Order')

    option = relationship('CatalogProductOption')


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


class CatalogCategoryEntityDatetime(Base):
    __tablename__ = 'catalog_category_entity_datetime'
    __table_args__ = (
        Index('CATALOG_CATEGORY_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Category Datetime Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    value = Column(DateTime, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogCategoryEntity')
    store = relationship('Store')


class CatalogCategoryEntityDecimal(Base):
    __tablename__ = 'catalog_category_entity_decimal'
    __table_args__ = (
        Index('CATALOG_CATEGORY_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Category Decimal Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    value = Column(DECIMAL(20, 6), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogCategoryEntity')
    store = relationship('Store')


class CatalogCategoryEntityInt(Base):
    __tablename__ = 'catalog_category_entity_int'
    __table_args__ = (
        Index('CATALOG_CATEGORY_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Category Integer Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    value = Column(INTEGER(11), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogCategoryEntity')
    store = relationship('Store')


class CatalogCategoryEntityText(Base):
    __tablename__ = 'catalog_category_entity_text'
    __table_args__ = (
        Index('CATALOG_CATEGORY_ENTITY_TEXT_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Category Text Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    value = Column(Text, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogCategoryEntity')
    store = relationship('Store')


class CatalogCategoryEntityVarchar(Base):
    __tablename__ = 'catalog_category_entity_varchar'
    __table_args__ = (
        Index('CATALOG_CATEGORY_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Category Varchar Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_category_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    value = Column(String(255), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogCategoryEntity')
    store = relationship('Store')


class CatalogProductBundleSelectionPrice(Base):
    __tablename__ = 'catalog_product_bundle_selection_price'
    __table_args__ = {'comment': 'Catalog Product Bundle Selection Price'}

    selection_id = Column(ForeignKey('catalog_product_bundle_selection.selection_id', ondelete='CASCADE'), primary_key=True, nullable=False, comment='Selection ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, comment='Website ID')
    selection_price_type = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Selection Price Type')
    selection_price_value = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Selection Price Value')
    parent_product_id = Column(INTEGER(10), primary_key=True, nullable=False, comment='Parent Product ID')

    selection = relationship('CatalogProductBundleSelection')
    website = relationship('StoreWebsite')


class CatalogProductEntityDatetime(Base):
    __tablename__ = 'catalog_product_entity_datetime'
    __table_args__ = (
        Index('CATALOG_PRODUCT_ENTITY_DATETIME_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Datetime Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DateTime, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogProductEntity', back_populates="datetime")
    store = relationship('Store')


class CatalogProductEntityDecimal(Base):
    __tablename__ = 'catalog_product_entity_decimal'
    __table_args__ = (
        Index('CATALOG_PRODUCT_ENTITY_DECIMAL_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Decimal Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(DECIMAL(20, 6), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogProductEntity', back_populates="decimal")
    store = relationship('Store')


class CatalogProductEntityGallery(Base):
    __tablename__ = 'catalog_product_entity_gallery'
    __table_args__ = (
        Index('CATALOG_PRODUCT_ENTITY_GALLERY_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Gallery Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    position = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Position')
    value = Column(String(255), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogProductEntity')
    store = relationship('Store')


class CatalogProductEntityInt(Base):
    __tablename__ = 'catalog_product_entity_int'
    __table_args__ = (
        Index('CATALOG_PRODUCT_ENTITY_INT_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Integer Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(INTEGER(11), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogProductEntity', back_populates="intager")
    store = relationship('Store')


class CatalogProductEntityMediaGalleryValue(Base):
    __tablename__ = 'catalog_product_entity_media_gallery_value'
    __table_args__ = (
        Index('CAT_PRD_ENTT_MDA_GLR_VAL_ENTT_ID_VAL_ID_STORE_ID', 'entity_id', 'value_id', 'store_id'),
        {'comment': 'Catalog Product Media Gallery Attribute Value Table'}
    )

    value_id = Column(ForeignKey('catalog_product_entity_media_gallery.value_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Value ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    label = Column(String(255), comment='Label')
    position = Column(INTEGER(10), comment='Position')
    disabled = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Is Disabled')
    record_id = Column(INTEGER(10), primary_key=True, comment='Record ID')

    entity = relationship('CatalogProductEntity')
    store = relationship('Store')
    value = relationship('CatalogProductEntityMediaGallery')


t_catalog_product_entity_media_gallery_value_to_entity = Table(
    'catalog_product_entity_media_gallery_value_to_entity', metadata,
    Column('value_id', ForeignKey('catalog_product_entity_media_gallery.value_id', ondelete='CASCADE'), nullable=False, comment='Value media Entry ID'),
    Column('entity_id', ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product Entity ID'),
    Index('CAT_PRD_ENTT_MDA_GLR_VAL_TO_ENTT_VAL_ID_ENTT_ID', 'value_id', 'entity_id', unique=True),
    comment='Link Media value to Product entity table'
)


t_catalog_product_entity_media_gallery_value_video = Table(
    'catalog_product_entity_media_gallery_value_video', metadata,
    Column('value_id', ForeignKey('catalog_product_entity_media_gallery.value_id', ondelete='CASCADE'), nullable=False, comment='Media Entity ID'),
    Column('store_id', ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID'),
    Column('provider', String(32), comment='Video provider ID'),
    Column('url', Text, comment='Video URL'),
    Column('title', String(255), comment='Title'),
    Column('description', Text, comment='Page Meta Description'),
    Column('metadata', Text, comment='Video meta data'),
    Index('CAT_PRD_ENTT_MDA_GLR_VAL_VIDEO_VAL_ID_STORE_ID', 'value_id', 'store_id', unique=True),
    comment='Catalog Product Video Table'
)


class CatalogProductEntityText(Base):
    __tablename__ = 'catalog_product_entity_text'
    __table_args__ = (
        Index('CATALOG_PRODUCT_ENTITY_TEXT_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Text Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(Text, comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogProductEntity', back_populates="text")
    store = relationship('Store')


class CatalogProductEntityVarchar(Base):
    __tablename__ = 'catalog_product_entity_varchar'
    __table_args__ = (
        Index('CATALOG_PRODUCT_ENTITY_VARCHAR_ENTITY_ID_ATTRIBUTE_ID_STORE_ID', 'entity_id', 'attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Varchar Attribute Backend Table'}
    )

    value_id = Column(INTEGER(11), primary_key=True, comment='Value ID')
    attribute_id = Column(ForeignKey('eav_attribute.attribute_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    entity_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Entity ID')
    value = Column(String(255), comment='Value')

    attribute = relationship('EavAttribute')
    entity = relationship('CatalogProductEntity', back_populates="varchar")
    store = relationship('Store')


class CatalogProductOptionPrice(Base):
    __tablename__ = 'catalog_product_option_price'
    __table_args__ = (
        Index('CATALOG_PRODUCT_OPTION_PRICE_OPTION_ID_STORE_ID', 'option_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Option Price Table'}
    )

    option_price_id = Column(INTEGER(10), primary_key=True, comment='Option Price ID')
    option_id = Column(ForeignKey('catalog_product_option.option_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Option ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Price')
    price_type = Column(String(7), nullable=False, server_default=text("'fixed'"), comment='Price Type')

    option = relationship('CatalogProductOption')
    store = relationship('Store')


class CatalogProductOptionTitle(Base):
    __tablename__ = 'catalog_product_option_title'
    __table_args__ = (
        Index('CATALOG_PRODUCT_OPTION_TITLE_OPTION_ID_STORE_ID', 'option_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Option Title Table'}
    )

    option_title_id = Column(INTEGER(10), primary_key=True, comment='Option Title ID')
    option_id = Column(ForeignKey('catalog_product_option.option_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Option ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    title = Column(String(255), comment='Title')

    option = relationship('CatalogProductOption')
    store = relationship('Store')


class CatalogProductOptionTypePrice(Base):
    __tablename__ = 'catalog_product_option_type_price'
    __table_args__ = (
        Index('CATALOG_PRODUCT_OPTION_TYPE_PRICE_OPTION_TYPE_ID_STORE_ID', 'option_type_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Option Type Price Table'}
    )

    option_type_price_id = Column(INTEGER(10), primary_key=True, comment='Option Type Price ID')
    option_type_id = Column(ForeignKey('catalog_product_option_type_value.option_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Option Type ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    price = Column(DECIMAL(20, 6), nullable=False, server_default=text("0.000000"), comment='Price')
    price_type = Column(String(7), nullable=False, server_default=text("'fixed'"), comment='Price Type')

    option_type = relationship('CatalogProductOptionTypeValue')
    store = relationship('Store')


class CatalogProductOptionTypeTitle(Base):
    __tablename__ = 'catalog_product_option_type_title'
    __table_args__ = (
        Index('CATALOG_PRODUCT_OPTION_TYPE_TITLE_OPTION_TYPE_ID_STORE_ID', 'option_type_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Option Type Title Table'}
    )

    option_type_title_id = Column(INTEGER(10), primary_key=True, comment='Option Type Title ID')
    option_type_id = Column(ForeignKey('catalog_product_option_type_value.option_type_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Option Type ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    title = Column(String(255), comment='Title')

    option_type = relationship('CatalogProductOptionTypeValue')
    store = relationship('Store')


class CatalogProductSuperAttributeLabel(Base):
    __tablename__ = 'catalog_product_super_attribute_label'
    __table_args__ = (
        Index('CAT_PRD_SPR_ATTR_LBL_PRD_SPR_ATTR_ID_STORE_ID', 'product_super_attribute_id', 'store_id', unique=True),
        {'comment': 'Catalog Product Super Attribute Label Table'}
    )

    value_id = Column(INTEGER(10), primary_key=True, comment='Value ID')
    product_super_attribute_id = Column(ForeignKey('catalog_product_super_attribute.product_super_attribute_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Product Super Attribute ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')
    use_default = Column(SMALLINT(5), server_default=text("0"), comment='Use Default Value')
    value = Column(String(255), comment='Value')

    product_super_attribute = relationship('CatalogProductSuperAttribute')
    store = relationship('Store')


class CustomerEntity(Base):
    __tablename__ = 'customer_entity'
    __table_args__ = (
        Index('CUSTOMER_ENTITY_EMAIL_WEBSITE_ID', 'email', 'website_id', unique=True),
        {'comment': 'Customer Entity'}
    )

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='SET NULL'), index=True, comment='Website ID')
    email = Column(String(255), comment='Email')
    group_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Group ID')
    increment_id = Column(String(50), comment='Increment ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, server_default=text("0"), comment='Store ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("1"), comment='Is Active')
    disable_auto_group_change = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Disable automatic group change based on VAT ID')
    created_in = Column(String(255), comment='Created From')
    prefix = Column(String(40), comment='Name Prefix')
    firstname = Column(String(255), index=True, comment='First Name')
    middlename = Column(String(255), comment='Middle Name/Initial')
    lastname = Column(String(255), index=True, comment='Last Name')
    suffix = Column(String(40), comment='Name Suffix')
    dob = Column(Date, comment='Date of Birth')
    password_hash = Column(String(128), comment='Password_hash')
    rp_token = Column(String(128), comment='Reset password token')
    rp_token_created_at = Column(DateTime, comment='Reset password token creation time')
    default_billing = Column(INTEGER(10), comment='Default Billing Address')
    default_shipping = Column(INTEGER(10), comment='Default Shipping Address')
    taxvat = Column(String(50), comment='Tax/VAT Number')
    confirmation = Column(String(64), comment='Is Confirmed')
    gender = Column(SMALLINT(5), comment='Gender')
    failures_num = Column(SMALLINT(6), server_default=text("0"), comment='Failure Number')
    first_failure = Column(TIMESTAMP, comment='First Failure')
    lock_expires = Column(TIMESTAMP, comment='Lock Expiration Date')

    store = relationship('Store')
    website = relationship('StoreWebsite')


class SearchQuery(Base):
    __tablename__ = 'search_query'
    __table_args__ = (
        Index('SEARCH_QUERY_QUERY_TEXT_STORE_ID', 'query_text', 'store_id', unique=True),
        Index('SEARCH_QUERY_STORE_ID_POPULARITY', 'store_id', 'popularity'),
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


class CatalogCompareItem(Base):
    __tablename__ = 'catalog_compare_item'
    __table_args__ = (
        Index('CATALOG_COMPARE_ITEM_CUSTOMER_ID_PRODUCT_ID', 'customer_id', 'product_id'),
        Index('CATALOG_COMPARE_ITEM_VISITOR_ID_PRODUCT_ID', 'visitor_id', 'product_id'),
        {'comment': 'Catalog Compare Table'}
    )

    catalog_compare_item_id = Column(INTEGER(10), primary_key=True, comment='Compare Item ID')
    visitor_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Visitor ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), comment='Customer ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, comment='Store ID')

    customer = relationship('CustomerEntity')
    product = relationship('CatalogProductEntity')
    store = relationship('Store')


class CatalogProductFrontendAction(Base):
    __tablename__ = 'catalog_product_frontend_action'
    __table_args__ = (
        Index('CATALOG_PRODUCT_FRONTEND_ACTION_CUSTOMER_ID_PRODUCT_ID_TYPE_ID', 'customer_id', 'product_id', 'type_id', unique=True),
        Index('CATALOG_PRODUCT_FRONTEND_ACTION_VISITOR_ID_PRODUCT_ID_TYPE_ID', 'visitor_id', 'product_id', 'type_id', unique=True),
        {'comment': 'Catalog Product Frontend Action Table'}
    )

    action_id = Column(BIGINT(20), primary_key=True, comment='Product Action ID')
    type_id = Column(String(64), nullable=False, comment='Type of product action')
    visitor_id = Column(INTEGER(10), comment='Visitor ID')
    customer_id = Column(ForeignKey('customer_entity.entity_id', ondelete='CASCADE'), comment='Customer ID')
    product_id = Column(ForeignKey('catalog_product_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, comment='Product ID')
    added_at = Column(BIGINT(20), nullable=False, comment='Added At')

    customer = relationship('CustomerEntity')
    product = relationship('CatalogProductEntity')


class CatalogsearchRecommendation(Base):
    __tablename__ = 'catalogsearch_recommendations'
    __table_args__ = {'comment': 'Advanced Search Recommendations'}

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    query_id = Column(ForeignKey('search_query.query_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Query ID')
    relation_id = Column(ForeignKey('search_query.query_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Relation ID')

    query = relationship('SearchQuery', primaryjoin='CatalogsearchRecommendation.query_id == SearchQuery.query_id')
    relation = relationship('SearchQuery', primaryjoin='CatalogsearchRecommendation.relation_id == SearchQuery.query_id')
