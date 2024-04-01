from website import db
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class EventContributor(db.Model):
    __tablename__ = "event_contributors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    event = relationship('Event', backref='user_roles')
    user = relationship('User', backref='event_roles')
    role: Mapped[str]
