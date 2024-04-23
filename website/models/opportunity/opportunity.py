import enum
from typing import List, Optional
from datetime import datetime

from website import db

from sqlalchemy import ForeignKey, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .opportunity_tag import OpportunityTag


class PostType(enum.Enum):
    AUDITION: str = "Audition"
    OPEN_CALL: str = "Open Call"
    DANCE_JOB: str = "Dance Job"
    INTENSIVE: str = "Intensive"


class LocationType(enum.Enum):
    IN_PERSON: str = "In-Person"
    REMOTE: str = "Remote"
    HYBRID: str = "Hybrid"


class TermType(enum.Enum):
    CONTRACT: str = "Contract"
    PART_TIME: str = "Part-Time"
    FULL_TIME: str = "Full-Time"


class Opportunity(db.Model):
    __tablename__ = "opportunity"
    # Identifying attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped['PostType']
    title: Mapped[str]
    organizer: Mapped[str]

    # Post Metadata
    poster_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    poster: Mapped['User'] = relationship(
        'User', back_populates='opportunity_posts')
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_modified: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    closing_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Descriptors
    tags: Mapped[List['OpportunityTag']] = relationship(
        'OpportunityTag', secondary="opportunity_tag_relationships", back_populates='opportunities', cascade="all, delete")
    location_type: Mapped['LocationType']
    location: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True))
    is_paid: Mapped[bool]
    pay: Mapped[Optional[str]]
    term: Mapped[Optional['TermType']]
    number_positions: Mapped[Optional[int]]

    # Content
    display_description: Mapped[str]
    description: Mapped[str]
    responsibilities: Mapped[Optional[str]]
    requirements: Mapped[str]
    compensation: Mapped[str]
    additional_info: Mapped[Optional[str]]
    application_details: Mapped[str]
    application_link: Mapped[Optional[str]]

    __table_args__ = (
        UniqueConstraint('title', 'poster_id', name="uix_1"),
    )
