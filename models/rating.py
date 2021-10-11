# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RatingEntity(Base):
    __tablename__ = 'rating_entity'
    __table_args__ = {'comment': 'Rating entities'}

    entity_id = Column(SMALLINT(5), primary_key=True, comment='Entity ID')
    entity_code = Column(String(64), nullable=False, unique=True, comment='Entity Code')


class ReviewEntity(Base):
    __tablename__ = 'review_entity'
    __table_args__ = {'comment': 'Review entities'}

    entity_id = Column(SMALLINT(5), primary_key=True, comment='Review entity ID')
    entity_code = Column(String(32), nullable=False, comment='Review entity code')


class ReviewStatu(Base):
    __tablename__ = 'review_status'
    __table_args__ = {'comment': 'Review statuses'}

    status_id = Column(SMALLINT(5), primary_key=True, comment='Status ID')
    status_code = Column(String(32), nullable=False, comment='Status code')


class StoreWebsite(Base):
    __tablename__ = 'store_website'
    __table_args__ = {'comment': 'Websites'}

    website_id = Column(SMALLINT(5), primary_key=True, comment='Website ID')
    code = Column(String(32), unique=True, comment='Code')
    name = Column(String(64), comment='Website Name')
    sort_order = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Sort Order')
    default_group_id = Column(SMALLINT(5), nullable=False, index=True, server_default=text("0"), comment='Default Group ID')
    is_default = Column(SMALLINT(5), server_default=text("0"), comment='Defines Is Website Default')


class Rating(Base):
    __tablename__ = 'rating'
    __table_args__ = {'comment': 'Ratings'}

    rating_id = Column(SMALLINT(5), primary_key=True, comment='Rating ID')
    entity_id = Column(ForeignKey('rating_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    rating_code = Column(String(64), nullable=False, unique=True, comment='Rating Code')
    position = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Position On Storefront')
    is_active = Column(SMALLINT(6), nullable=False, server_default=text("1"), comment='Rating is active.')

    entity = relationship('RatingEntity')
    stores = relationship('Store', secondary='rating_store')


class Review(Base):
    __tablename__ = 'review'
    __table_args__ = {'comment': 'Review base information'}

    review_id = Column(BIGINT(20), primary_key=True, comment='Review ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), comment='Review create date')
    entity_id = Column(ForeignKey('review_entity.entity_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Entity ID')
    entity_pk_value = Column(INTEGER(10), nullable=False, index=True, server_default=text("0"), comment='Product ID')
    status_id = Column(ForeignKey('review_status.status_id'), nullable=False, index=True, server_default=text("0"), comment='Status code')

    entity = relationship('ReviewEntity')
    status = relationship('ReviewStatu')


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


class RatingOption(Base):
    __tablename__ = 'rating_option'
    __table_args__ = {'comment': 'Rating options'}

    option_id = Column(INTEGER(10), primary_key=True, comment='Rating Option ID')
    rating_id = Column(ForeignKey('rating.rating_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Rating ID')
    code = Column(String(32), nullable=False, comment='Rating Option Code')
    value = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating Option Value')
    position = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Ration option position on Storefront')

    rating = relationship('Rating')


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


class RatingOptionVote(Base):
    __tablename__ = 'rating_option_vote'
    __table_args__ = {'comment': 'Rating option values'}

    vote_id = Column(BIGINT(20), primary_key=True, comment='Vote ID')
    option_id = Column(ForeignKey('rating_option.option_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Vote option ID')
    remote_ip = Column(String(16), nullable=False, comment='Customer IP')
    remote_ip_long = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='Customer IP converted to long integer format')
    customer_id = Column(INTEGER(10), server_default=text("0"), comment='Customer ID')
    entity_pk_value = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='Product ID')
    rating_id = Column(SMALLINT(5), nullable=False, server_default=text("0"), comment='Rating ID')
    review_id = Column(ForeignKey('review.review_id', ondelete='CASCADE'), index=True, comment='Review ID')
    percent = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Percent amount')
    value = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Vote option value')

    option = relationship('RatingOption')
    review = relationship('Review')


class RatingOptionVoteAggregated(Base):
    __tablename__ = 'rating_option_vote_aggregated'
    __table_args__ = {'comment': 'Rating vote aggregated'}

    primary_id = Column(INTEGER(11), primary_key=True, comment='Vote aggregation ID')
    rating_id = Column(ForeignKey('rating.rating_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Rating ID')
    entity_pk_value = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='Product ID')
    vote_count = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='Vote dty')
    vote_value_sum = Column(INTEGER(10), nullable=False, server_default=text("0"), comment='General vote sum')
    percent = Column(SMALLINT(6), nullable=False, server_default=text("0"), comment='Vote percent')
    percent_approved = Column(SMALLINT(6), server_default=text("0"), comment='Vote percent approved by admin')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Store ID')

    rating = relationship('Rating')
    store = relationship('Store')


t_rating_store = Table(
    'rating_store', metadata,
    Column('rating_id', ForeignKey('rating.rating_id', ondelete='CASCADE'), primary_key=True, nullable=False, server_default=text("0"), comment='Rating ID'),
    Column('store_id', ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Store ID'),
    comment='Rating Store'
)


class RatingTitle(Base):
    __tablename__ = 'rating_title'
    __table_args__ = {'comment': 'Rating Title'}

    rating_id = Column(ForeignKey('rating.rating_id', ondelete='CASCADE'), primary_key=True, nullable=False, server_default=text("0"), comment='Rating ID')
    store_id = Column(ForeignKey('store.store_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("0"), comment='Store ID')
    value = Column(String(255), nullable=False, comment='Rating Label')

    rating = relationship('Rating')
    store = relationship('Store')
