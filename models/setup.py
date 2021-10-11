# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SetupModule(Base):
    __tablename__ = 'setup_module'
    __table_args__ = {'comment': 'Module versions registry'}

    module = Column(String(50), primary_key=True, comment='Module')
    schema_version = Column(String(50), comment='Schema Version')
    data_version = Column(String(50), comment='Data Version')
