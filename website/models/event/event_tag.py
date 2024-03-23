from ... import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class EventTag(db.Model):
    __tablename__ = "event_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    events: Mapped[List['Event']] = relationship('Event', secondary="event_tag_relationships", back_populates='tags')


class EventTagRelationship(db.Model):
    __tablename__ = 'event_tag_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('event_tags.id'))