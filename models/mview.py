# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MviewState(Base):
    __tablename__ = 'mview_state'
    __table_args__ = {'comment': 'View State'}

    state_id = Column(INTEGER(10), primary_key=True, comment='View State ID')
    view_id = Column(String(255), index=True, comment='View ID')
    mode = Column(String(16), index=True, server_default=text("'disabled'"), comment='View Mode')
    status = Column(String(16), server_default=text("'idle'"), comment='View Status')
    updated = Column(DateTime, comment='View updated time')
    version_id = Column(INTEGER(10), comment='View Version ID')
