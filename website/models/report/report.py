from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from ... import db
from ..user import User
from ..event import Event
from ..opportunity import Opportunity
# from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Report(db.Model):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "reports"
    }


class BugReport(db.Model):
    __tablename__ = "bug_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]


class ContentReport(db.Model):
    __tablename__ = "content_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str]
    reason: Mapped[str]
    details: Mapped[str]
    reporter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True)
    reporter: Mapped['User'] = relationship('User', foreign_keys=[reporter_id])

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "content_reports"
    }


class UserReport(ContentReport):
    __tablename__ = "user_reports"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("content_reports.id"), primary_key=True)
    reported_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True)
    reported_user: Mapped['User'] = relationship(
        'User', foreign_keys=[reported_user_id])

    __mapper_args__ = {
        "polymorphic_identity": "user_reports",
    }


class EventReport(ContentReport):
    __tablename__ = "event_reports"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("content_reports.id"), primary_key=True)
    reported_event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("events.id"), nullable=True)
    reported_event: Mapped['Event'] = relationship(
        'Event', foreign_keys=[reported_event_id])

    __mapper_args__ = {
        "polymorphic_identity": "event_reports",
    }


class OpportunityReport(ContentReport):
    __tablename__ = "opportunity_reports"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("content_reports.id"), primary_key=True)
    reported_opportunity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("opportunity.id"), nullable=True)
    reported_opportunity: Mapped['Opportunity'] = relationship(
        'Opportunity', foreign_keys=[reported_opportunity_id])

    __mapper_args__ = {
        "polymorphic_identity": "opportunity_reports",
    }
