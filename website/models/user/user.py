import enum
from typing import List
from flask import url_for
from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin  # adds login_manager required methods
from .user_tag import UserTag
from ..event import Event, EventContributor
from ... import db, login_manager

Base = declarative_base()


@login_manager.user_loader  # login_managers needs to know how to load a user
def load_user(user_id):
    return User.query.get(int(user_id))


class UserType(enum.Enum):
    INDIVIDUAL: str = "Individual"
    GROUP: str = "Group"
    ORGANIZATION: str = "Organization"


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


class SocialMedia(db.Model):
    __tablename__ = "social_media"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    social_media: Mapped[str]
    handle: Mapped[str]


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


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    display_name: Mapped[str]
    pronouns: Mapped[str]
    bio: Mapped[str]
    user_type: Mapped['UserType']
    profile_picture_url: Mapped[str]
    profile_picture_id: Mapped[str]
    tags: Mapped[List['UserTag']] = relationship(
        'UserTag', secondary="user_tag_relationships", back_populates='users')
    socials: Mapped[List['SocialMedia']] = relationship('SocialMedia')
    events_organized: Mapped[List['Event']] = relationship(
        'Event', back_populates='organizer')
    events_contributed: Mapped[List['Event']] = relationship(
        'Event', secondary="event_contributors", back_populates="contributors", viewonly=True)
    contributor_association: Mapped[List['EventContributor']] = relationship(
        'EventContributor', back_populates='user')
    # TODO: add profile_picture: Mapped[str] = mapped_column(String, nullable=False, default="default.jpg")

    # @hybrid_property
    def get_profile_pic_url(self):
        if self.profile_picture_url == "":
            return url_for("static", filename="images/placeholder.jpg")
        return self.profile_picture_url
        # <img src="{{person.get_profile_pic_url}}">
