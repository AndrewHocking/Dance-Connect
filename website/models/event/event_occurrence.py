from ... import db
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class EventOccurrence(db.Model):
    __tablename__ = "event_occurrences"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    event: Mapped['Event'] = relationship('Event', back_populates='occurrences')
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_relaxed_performance: Mapped[bool]
    has_asl_interpreter: Mapped[bool]