# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Theme(Base):
    __tablename__ = 'theme'
    __table_args__ = {'comment': 'Core theme'}

    theme_id = Column(INTEGER(10), primary_key=True, comment='Theme identifier')
    parent_id = Column(INTEGER(11), comment='Parent ID')
    theme_path = Column(String(255), comment='Theme Path')
    theme_title = Column(String(255), nullable=False, comment='Theme Title')
    preview_image = Column(String(255), comment='Preview Image')
    is_featured = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Is Theme Featured')
    area = Column(String(255), nullable=False, comment='Theme Area')
    type = Column(SMALLINT(6), nullable=False, comment='Theme type: 0:physical, 1:virtual, 2:staging')
    code = Column(Text, comment='Full theme code, including package')


class ThemeFile(Base):
    __tablename__ = 'theme_file'
    __table_args__ = {'comment': 'Core theme files'}

    theme_files_id = Column(INTEGER(10), primary_key=True, comment='Theme files identifier')
    theme_id = Column(ForeignKey('theme.theme_id', ondelete='CASCADE'), nullable=False, index=True, comment='Theme ID')
    file_path = Column(String(255), comment='Relative path to file')
    file_type = Column(String(32), nullable=False, comment='File Type')
    content = Column(LONGTEXT, nullable=False, comment='File Content')
    sort_order = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Sort Order')
    is_temporary = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Is Temporary File')

    theme = relationship('Theme')
