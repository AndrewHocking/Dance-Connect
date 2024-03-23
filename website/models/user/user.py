from typing import List
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin # adds login_manager required methods
from ... import db, login_manager

Base = declarative_base()

@login_manager.user_loader  # login_managers needs to know how to load a user
def load_user(user_id):
    return User.query.get(int(user_id))

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
    tags: Mapped[List['UserTag']] = relationship('UserTag', secondary="user_tag_relationships", back_populates='users')
    events_organized: Mapped[List['Event']] = relationship('Event', back_populates='organizer')
    events_participated: Mapped[List['Event']] = relationship('Event', secondary='event_participants', back_populates='participants')
    #TODO: add profile_picture: Mapped[str] = mapped_column(String, nullable=False, default="default.jpg")

class UserTagRelationship(db.Model):
    __tablename__ = 'user_tag_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_tags.id'))


class ORG_TYPES:
    INDIVIDUAL: str = "Individual"
    GROUP: str = "Group"
    ORGANIZATION: str = "Organization"

    LIST: list[str] = [INDIVIDUAL, GROUP, ORGANIZATION]

class ROLES:
    CHOREOGRAPHER: str = "Choreographer"
    DESIGNER: str = "Designer"
    WRITER: str = "Writer"
    PRODUCER: str = "Producer"
    STAGEMANAGER: str = "Stage Manager"
    OTHER: str = "Other"

    LIST: list[str] = [CHOREOGRAPHER, DESIGNER, WRITER, PRODUCER, STAGEMANAGER, OTHER]



