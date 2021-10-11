# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DirectoryCountry(Base):
    __tablename__ = 'directory_country'
    __table_args__ = {'comment': 'Directory Country'}

    country_id = Column(String(2), primary_key=True, comment='Country ID in ISO-2')
    iso2_code = Column(String(2), comment='Country ISO-2 format')
    iso3_code = Column(String(3), comment='Country ISO-3')


class DirectoryCountryFormat(Base):
    __tablename__ = 'directory_country_format'
    __table_args__ = (
        Index('DIRECTORY_COUNTRY_FORMAT_COUNTRY_ID_TYPE', 'country_id', 'type', unique=True),
        {'comment': 'Directory Country Format'}
    )

    country_format_id = Column(INTEGER(10), primary_key=True, comment='Country Format ID')
    country_id = Column(String(2), comment='Country ID in ISO-2')
    type = Column(String(30), comment='Country Format Type')
    format = Column(Text, nullable=False, comment='Country Format')


class DirectoryCountryRegion(Base):
    __tablename__ = 'directory_country_region'
    __table_args__ = {'comment': 'Directory Country Region'}

    region_id = Column(INTEGER(10), primary_key=True, comment='Region ID')
    country_id = Column(String(4), nullable=False, index=True, server_default=text("'0'"), comment='Country ID in ISO-2')
    code = Column(String(32), comment='Region code')
    default_name = Column(String(255), comment='Region Name')


class DirectoryCurrencyRate(Base):
    __tablename__ = 'directory_currency_rate'
    __table_args__ = {'comment': 'Directory Currency Rate'}

    currency_from = Column(String(3), primary_key=True, nullable=False, comment='Currency Code Convert From')
    currency_to = Column(String(3), primary_key=True, nullable=False, index=True, comment='Currency Code Convert To')
    rate = Column(DECIMAL(24, 12), nullable=False, server_default=text("0.000000000000"), comment='Currency Conversion Rate')


class DirectoryCountryRegionName(Base):
    __tablename__ = 'directory_country_region_name'
    __table_args__ = {'comment': 'Directory Country Region Name'}

    locale = Column(String(8), primary_key=True, nullable=False, comment='Locale')
    region_id = Column(ForeignKey('directory_country_region.region_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Region ID')
    name = Column(String(255), comment='Region Name')

    region = relationship('DirectoryCountryRegion')
