# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ImportHistory(Base):
    __tablename__ = 'import_history'
    __table_args__ = {'comment': 'Import history table'}

    history_id = Column(INTEGER(10), primary_key=True, comment='History record ID')
    started_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Started at')
    user_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='User ID')
    imported_file = Column(String(255), comment='Imported file')
    execution_time = Column(String(255), comment='Execution time')
    summary = Column(String(255), comment='Summary')
    error_file = Column(String(255), nullable=False, comment='Imported file with errors')


class ImportexportImportdatum(Base):
    __tablename__ = 'importexport_importdata'
    __table_args__ = {'comment': 'Import Data Table'}

    id = Column(INTEGER(10), primary_key=True, comment='ID')
    entity = Column(String(50), nullable=False, comment='Entity')
    behavior = Column(String(10), nullable=False, server_default=text("'append'"), comment='Behavior')
    data = Column(LONGTEXT, comment='Data')
