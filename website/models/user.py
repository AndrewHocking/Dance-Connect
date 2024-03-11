from typing import Set
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin  # adds login_manager required methods
from .event import Event
from .. import db, login_manager

Base = declarative_base()

@login_manager.user_loader  # login_managers needs to know how to load a user
def load_user(user_id):
    return User.query.get(int(user_id))

class UserTag(db.Model):
    __tablename__ = "user_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    users: Mapped[Set['User']] = relationship('User', secondary="user_tag_relationships", back_populates='tags')

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str]
    pronouns: Mapped[str]
    tags: Mapped[Set['UserTag']] = relationship('UserTag', secondary="user_tag_relationships", back_populates='users')
    events_organized: Mapped[Set['Event']] = relationship('Event', back_populates='organizer')
    events_participated: Mapped[Set['Event']] = relationship('Event', secondary='event_participants', back_populates='participants')
    #TODO: add profile_picture: Mapped[str] = mapped_column(String, nullable=False, default="default.jpg")

class UserTagRelationship(db.Model):
    __tablename__ = 'user_tag_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_tags.id'))
