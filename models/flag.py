# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Flag(Base):
    __tablename__ = 'flag'
    __table_args__ = {'comment': 'Flag'}

    flag_id = Column(INTEGER(10), primary_key=True, comment='Flag Id')
    flag_code = Column(String(255), nullable=False, comment='Flag Code')
    state = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Flag State')
    flag_data = Column(MEDIUMTEXT, comment='Flag Data')
    last_update = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Date of Last Flag Update')
