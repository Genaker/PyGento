# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ImportexportImportdatum(Base):
    __tablename__ = 'importexport_importdata'
    __table_args__ = {'comment': 'Import Data Table'}

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    entity = Column(String(50), nullable=False, comment='Entity')
    behavior = Column(String(10), nullable=False, server_default=text("'append'"), comment='Behavior')
    data = Column(LONGTEXT, comment='Data')
