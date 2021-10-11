# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthorizationRole(Base):
    __tablename__ = 'authorization_role'
    __table_args__ = (
        Index('AUTHORIZATION_ROLE_PARENT_ID_SORT_ORDER', 'parent_id', 'sort_order'),
        {'comment': 'Admin Role Table'}
    )

    role_id = Column(INTEGER(10), primary_key=True, comment='Role ID')
    parent_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Parent Role ID')
    tree_level = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Role Tree Level')
    sort_order = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Role Sort Order')
    role_type = Column(String(1), nullable=False, server_default=text("'0'"), comment='Role Type')
    user_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='User ID')
    user_type = Column(String(16), comment='User Type')
    role_name = Column(String(50), comment='Role Name')


class AuthorizationRule(Base):
    __tablename__ = 'authorization_rule'
    __table_args__ = (
        Index('AUTHORIZATION_RULE_RESOURCE_ID_ROLE_ID', 'resource_id', 'role_id'),
        Index('AUTHORIZATION_RULE_ROLE_ID_RESOURCE_ID', 'role_id', 'resource_id'),
        {'comment': 'Admin Rule Table'}
    )

    rule_id = Column(INTEGER(10), primary_key=True, comment='Rule ID')
    role_id = Column(ForeignKey('authorization_role.role_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Role ID')
    resource_id = Column(String(255), comment='Resource ID')
    privileges = Column(String(20), comment='Privileges')
    permission = Column(String(10), comment='Permission')

    role = relationship('AuthorizationRole')
