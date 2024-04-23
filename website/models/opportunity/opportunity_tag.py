from website import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class OpportunityTag(db.Model):
    __tablename__ = "opportunity_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    opportunities: Mapped[List['Opportunity']] = relationship(
        'Opportunity', secondary="opportunity_tag_relationships", back_populates='tags')


class OpportunityTagRelationship(db.Model):
    __tablename__ = 'opportunity_tag_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('opportunity.id'))
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('opportunity_tags.id'))
