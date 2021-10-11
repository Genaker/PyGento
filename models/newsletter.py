# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class NewsletterTemplate(Base):
    __tablename__ = 'newsletter_template'
    __table_args__ = {'comment': 'Newsletter Template'}

    template_id = Column(INTEGER(10), primary_key=True, comment='Template ID')
    template_code = Column(String(150), comment='Template Code')
    template_text = Column(Text, comment='Template Text')
    template_styles = Column(Text, comment='Template Styles')
    template_type = Column(INTEGER(10), comment='Template Type')
    template_subject = Column(String(200), comment='Template Subject')
    template_sender_name = Column(String(200), comment='Template Sender Name')
    template_sender_email = Column(String(200), comment='Template Sender Email')
    template_actual = Column(SMALLINT(5), index=True, server_default=text("1"), comment='Template Actual')
    added_at = Column(TIMESTAMP, index=True, comment='Added At')
    modified_at = Column(TIMESTAMP, index=True, comment='Modified At')
    is_legacy = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='Should the template render in legacy mode')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class NewsletterQueue(Base):
    __tablename__ = 'newsletter_queue'
    __table_args__ = {'comment': 'Newsletter Queue'}

    queue_id = Column(INTEGER(10), primary_key=True, comment='Queue ID')
    template_id = Column(ForeignKey('newsletter_template.template_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Template ID')
    newsletter_type = Column(INTEGER(11), comment='Newsletter Type')
    newsletter_text = Column(Text, comment='Newsletter Text')
    newsletter_styles = Column(Text, comment='Newsletter Styles')
    newsletter_subject = Column(String(200), comment='Newsletter Subject')
    newsletter_sender_name = Column(String(200), comment='Newsletter Sender Name')
    newsletter_sender_email = Column(String(200), comment='Newsletter Sender Email')
    queue_status = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Queue Status')
    queue_start_at = Column(TIMESTAMP, comment='Queue Start At')
    queue_finish_at = Column(TIMESTAMP, comment='Queue Finish At')

    template = relationship('NewsletterTemplate')
    stores = relationship('Store', secondary='newsletter_queue_store_link')


class StoreGroup(Base):
    __tablename__ = 'store_group'
    __table_args__ = {'comment': 'Store Groups'}

    group_id = Column(SMALLINT(5), primary_key=True, comment='Group ID')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    name = Column(String(255), nullable=False, comment='Store Group Name')
    root_category_id = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Root Category ID')
    default_store_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Store ID')
    code = Column(String(32), unique=True, comment='Store group unique code')

    website = relationship('StoreWebsite')


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        Index('STORE_IS_ACTIVE_SORT_ORDER', 'is_active', 'sort_order'),
        {'comment': 'Stores'}
    )

    store_id = Column(SMALLINT(5), primary_key=True, comment='Store ID')
    code = Column(String(32), unique=True, comment='Code')
    website_id = Column(ForeignKey('store_website.website_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Website ID')
    group_id = Column(ForeignKey('store_group.group_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Group ID')
    name = Column(String(255), nullable=False, comment='Store Name')
    sort_order = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store Sort Order')
    is_active = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Store Activity')

    group = relationship('StoreGroup')
    website = relationship('StoreWebsite')


t_newsletter_queue_store_link = Table(
    'newsletter_queue_store_link', metadata,
    Column('queue_id', ForeignKey('newsletter_queue.queue_id', ondelete='CASCADE'), primary_key=True, nullable=False, server_default=text("0"), comment='Queue ID'),
    Column('store_id', ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Store ID'),
    comment='Newsletter Queue Store Link'
)


class NewsletterSubscriber(Base):
    __tablename__ = 'newsletter_subscriber'
    __table_args__ = {'comment': 'Newsletter Subscriber'}

    subscriber_id = Column(INTEGER(10), primary_key=True, comment='Subscriber ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='SET NULL'), index=True, server_default=text("0"), comment='Store ID')
    change_status_at = Column(TIMESTAMP, comment='Change Status At')
    customer_id = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Customer ID')
    subscriber_email = Column(String(150), index=True, comment='Subscriber Email')
    subscriber_status = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Subscriber Status')
    subscriber_confirm_code = Column(String(32), server_default=text("'NULL'"), comment='Subscriber Confirm Code')

    store = relationship('Store')


class NewsletterProblem(Base):
    __tablename__ = 'newsletter_problem'
    __table_args__ = {'comment': 'Newsletter Problems'}

    problem_id = Column(INTEGER(10), primary_key=True, comment='Problem ID')
    subscriber_id = Column(ForeignKey('newsletter_subscriber.subscriber_id', ondelete='CASCADE'), index=True, comment='Subscriber ID')
    queue_id = Column(ForeignKey('newsletter_queue.queue_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Queue ID')
    problem_error_code = Column(INTEGER(10), server_default=text("0"), comment='Problem Error Code')
    problem_error_text = Column(String(200), comment='Problem Error Text')

    queue = relationship('NewsletterQueue')
    subscriber = relationship('NewsletterSubscriber')


class NewsletterQueueLink(Base):
    __tablename__ = 'newsletter_queue_link'
    __table_args__ = (
        Index('NEWSLETTER_QUEUE_LINK_QUEUE_ID_LETTER_SENT_AT', 'queue_id', 'letter_sent_at'),
        {'comment': 'Newsletter Queue Link'}
    )

    queue_link_id = Column(INTEGER(10), primary_key=True, comment='Queue Link ID')
    queue_id = Column(ForeignKey('newsletter_queue.queue_id', ondelete='CASCADE'), nullable=False, server_default=text("0"), comment='Queue ID')
    subscriber_id = Column(ForeignKey('newsletter_subscriber.subscriber_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Subscriber ID')
    letter_sent_at = Column(TIMESTAMP, comment='Letter Sent At')

    queue = relationship('NewsletterQueue')
    subscriber = relationship('NewsletterSubscriber')
