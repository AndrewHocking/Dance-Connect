from sqlalchemy import event
from sqlalchemy.orm import joinedload
from ...models.event.event_tag import EventTag, EventTagRelationship
from ... import db, json_response
from ...models.event import Event


def create_event_tag(name: str, event: Event, commit_db_after_creation: bool = True):
    """Creates a new EventTag object, or finds one that already exists on the database with the same name"""
    name = name.lower()
    new_tag = db.session.query(EventTag).filter_by(name=name).first()
    if new_tag is not None:
        new_tag.events.append(event)
    else:
        new_tag = EventTag(name=name, events=[event])

    db.session.add(new_tag)

    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event tag created successfully.", new_tag)


def read_event_tag():
    # TODO: Add filters
    event_tags = db.session.query(EventTag).all()
    return json_response(200, f"{len(event_tags)} event tags found.", event_tags)


@event.listens_for(EventTagRelationship, 'before_delete')
def delete_orphan_tags(target):
    """Event listener to delete EventTags if they have no associated Events"""
    tag = db.session.query(EventTag).options(
        joinedload(EventTag.events)).get(target.tag_id)
    if not tag.events:
        db.session.delete(tag)
