from datetime import datetime

from flask import url_for
from ... import db
from sqlalchemy import Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional
from .event_tag import EventTag
from .event_occurrence import EventOccurrence
from .event_contributor import EventContributor


class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    organizer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    organizer: Mapped["User"] = relationship(
        "User", back_populates="events_organized")
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    tags: Mapped[List['EventTag']] = relationship(
        'EventTag', secondary="event_tag_relationships", back_populates='events', cascade="all, delete")
    venue_name: Mapped[str]
    venue_address: Mapped[str]
    venue_is_mobility_aid_accessible: Mapped[bool] = mapped_column(Boolean)
    accessibility_notes: Mapped[str]
    min_ticket_price: Mapped[Optional[float]]
    max_ticket_price: Mapped[Optional[float]]
    image_picture_url: Mapped[str]
    image_picture_id: Mapped[str]
    occurrences: Mapped[List['EventOccurrence']] = relationship(
        'EventOccurrence', back_populates='event', order_by="asc(EventOccurrence.start_time)", cascade="all, delete-orphan")
    contributors: Mapped[List['User']] = relationship(
        'User', secondary="event_contributors", back_populates="events_contributed", viewonly=True)
    contributor_association: Mapped[List['EventContributor']] = relationship(
        'EventContributor', back_populates='event', cascade="all, delete-orphan")
    request_notifications: Mapped[List['EventRequestNotification']] = relationship(
        'EventRequestNotification', back_populates="event", cascade="all, delete-orphan")
    # TODO: add media gallery

    @hybrid_property
    def next_occurrence(self) -> Optional[EventOccurrence]:
        chronological_list = self.occurrences
        chronological_list.sort(
            key=lambda occurrence: occurrence.start_time)
        for occurrence in chronological_list:
            if occurrence.start_time > datetime.now():
                return occurrence
        return None

    def get_image_url(self):
        if self.image_picture_url == "":
            return url_for("static", filename="images/placeholder.jpg")
        return self.image_picture_url
