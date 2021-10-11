# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PatchList(Base):
    __tablename__ = 'patch_list'
    __table_args__ = {'comment': 'List of data/schema patches'}

    patch_id = Column(INTEGER(11), primary_key=True, comment='Patch Auto Increment')
    patch_name = Column(String(1024), nullable=False, comment='Patch Class Name')
