from website import db
from website.models.event import Event
from website.models.user.user import User


from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Notification(db.Model):
    __tablename__ = "notification"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str]
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    recipient: Mapped['User'] = relationship(
        'User', foreign_keys=[recipient_id], backref="received_notifications")
    sender: Mapped['User'] = relationship(
        'User', foreign_keys=[sender_id], backref="sent_notifications")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "notification"
    }


class EventRequestNotification(Notification):
    __tablename__ = "event_request_notification"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("notification.id"), primary_key=True)
    event: Mapped['Event'] = relationship(
        'Event', back_populates="request_notifications")
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"))
    role: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "event_request_notification",
    }
