from sqlalchemy import event
from sqlalchemy.orm import joinedload

from ... import db, json_response
from ...models.opportunity import Opportunity, OpportunityTag, OpportunityTagRelationship


def create_opportunity_tag(name: str, opportunity: Opportunity, commit_db_after_creation: bool = True):
    name = name.lower()
    new_tag = db.session.query(OpportunityTag).filter_by(name=name).first()

    if new_tag is not None:
        new_tag.opportunities.append(opportunity)
    else:
        new_tag = OpportunityTag(name=name, opportunities=[opportunity])

    db.session.add(new_tag)

    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Opportunity tag created successfully.", new_tag)


def read_opportunity_tag():
    tags = db.session.query(OpportunityTag).all()
    return json_response(200, f"{len(tags)} opportunity tags found.", tags)


@event.listens_for(OpportunityTagRelationship, 'before_delete')
def delete_orphan_tags(target: OpportunityTagRelationship):
    """Event listener to delete OpportunityTags if they have no associated Events"""
    tag: OpportunityTag = db.session.query(OpportunityTag).options(
        joinedload(OpportunityTag.opportunities)).get(target.tag_id)
    if not tag.opportunities:
        db.session.delete(tag)
