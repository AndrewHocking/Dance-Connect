from ... import db
from sqlalchemy import Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from .event_tag import EventTag
from .event_occurrence import EventOccurrence

class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    organizer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    organizer: Mapped["User"] = relationship("User", back_populates="events_organized")
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    tags: Mapped[List['EventTag']] = relationship('EventTag', secondary="event_tag_relationships", back_populates='events')
    venue_name: Mapped[str]
    venue_address: Mapped[str]
    venue_is_wheelchair_accessible: Mapped[bool] = mapped_column(Boolean)
    show_is_photosensitivity_friendly: Mapped[bool] = mapped_column(Boolean)
    accessibility_notes: Mapped[str]
    min_ticket_price: Mapped[Optional[float]]
    max_ticket_price: Mapped[Optional[float]]
    occurrences: Mapped[List['EventOccurrence']] = relationship('EventOccurrence', back_populates='event')
    participants = relationship('User', secondary='event_participants', back_populates='events_participated')
    request_notifications: Mapped[List['EventRequestNotification']] = relationship('EventRequestNotification', back_populates="event")
    #TODO: add media gallery

class EventParticipant(db.Model):
    __tablename__ = "event_participants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
