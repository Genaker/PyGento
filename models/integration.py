# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class OauthConsumer(Base):
    __tablename__ = 'oauth_consumer'
    __table_args__ = {'comment': 'OAuth Consumers'}

    entity_id = Column(INTEGER(10), primary_key=True, comment='Entity ID')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"), comment='Created At')
    updated_at = Column(TIMESTAMP, index=True, server_default=text("'0000-00-00 00:00:00'"))
    name = Column(String(255), nullable=False, comment='Name of consumer')
    key = Column(String(32), nullable=False, unique=True, comment='Key code')
    secret = Column(String(32), nullable=False, unique=True, comment='Secret code')
    callback_url = Column(Text, comment='Callback URL')
    rejected_callback_url = Column(Text, nullable=False, comment='Rejected callback URL')


class Integration(Base):
    __tablename__ = 'integration'
    __table_args__ = {'comment': 'integration'}

    integration_id = Column(INTEGER(10), primary_key=True, comment='Integration ID')
    name = Column(String(255), nullable=False, unique=True, comment='Integration name is displayed in the admin interface')
    email = Column(String(255), nullable=False, comment='Email address of the contact person')
    endpoint = Column(String(255), comment='Endpoint for posting consumer credentials')
    status = Column(SMALLINT(5), nullable=False, comment='Integration status')
    consumer_id = Column(ForeignKey('oauth_consumer.entity_id', ondelete='CASCADE'), unique=True, comment='Oauth consumer')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Creation Time')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment='Update Time')
    setup_type = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Integration type - manual or config file')
    identity_link_url = Column(String(255), comment='Identity linking Url')

    consumer = relationship('OauthConsumer')
