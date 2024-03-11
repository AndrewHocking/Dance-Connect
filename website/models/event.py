from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Set, Optional
from .. import db

Base = declarative_base()

class EventTag(db.Model):
    __tablename__ = "event_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    events: Mapped[Set['Event']] = relationship('Event', secondary="event_tag_relationships", back_populates='tags')

class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    organizer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    organizer: Mapped["User"] = relationship("User", back_populates="events_organized")
    description: Mapped[str]
    url: Mapped[str]
    tags: Mapped[Set['EventTag']] = relationship('EventTag', secondary="event_tag_relationships", back_populates='events')
    venue_name: Mapped[str]
    venue_address: Mapped[str]
    venue_is_wheelchair_accessible: Mapped[bool] = mapped_column(Boolean)
    accessibility_notes: Mapped[str]
    min_ticket_price: Mapped[Optional[float]]
    max_ticket_price: Mapped[Optional[float]]
    occurrences: Mapped[Set['EventOccurrence']] = relationship('EventOccurrence', back_populates='event')
    participants = relationship('User', secondary='event_participants', back_populates='events_participated')
    #TODO: add media gallery

class EventOccurrence(db.Model):
    __tablename__ = "event_occurrences"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    event: Mapped['Event'] = relationship('Event', back_populates='occurrences')
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_relaxed_performance: Mapped[bool]
    has_asl_interpreter: Mapped[bool]

class EventParticipant(db.Model):
    __tablename__ = "event_participants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

class EventTagRelationship(db.Model):
    __tablename__ = 'event_tag_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('event_tags.id'))

