from ... import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class UserTag(db.Model):
    __tablename__ = "user_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    users: Mapped[List['User']] = relationship('User', secondary="user_tag_relationships", back_populates='tags')


class UserTagRelationship(db.Model):
    __tablename__ = 'user_tag_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_tags.id'))