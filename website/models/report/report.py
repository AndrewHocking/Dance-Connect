from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from ... import db
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


class BugReport(Report):
    __tablename__ = "bug_reports"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("reports.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "bug_reports",
    }
