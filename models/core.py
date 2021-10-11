# coding: utf-8
from sqlalchemy import Column, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CoreConfigDatum(Base):
    __tablename__ = 'core_config_data'
    __table_args__ = (
        Index('CORE_CONFIG_DATA_SCOPE_SCOPE_ID_PATH', 'scope', 'scope_id', 'path', unique=True),
        {'comment': 'Config Data'}
    )

    config_id = Column(INTEGER(10), primary_key=True, comment='Config ID')
    scope = Column(String(8), nullable=False, server_default=text("'default'"), comment='Config Scope')
    scope_id = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Config Scope ID')
    path = Column(String(255), nullable=False, server_default=text("'general'"), comment='Config Path')
    value = Column(Text, comment='Config Value')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Updated At')
