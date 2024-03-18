from typing import List

from ... import db, json_response
from ...models import Event, User, EventTag, EventOccurrence
from flask import Blueprint
from flask_login import current_user
from datetime import datetime

event_orm = Blueprint('event_route', __name__)

#TODO: Make API endpoint for all of these methods

# Creates a new Event object
@event_orm.route("event/create", methods=["POST"])
def create_event(
    organizer: User = current_user,
    title: str = "Untitled Event",
    description: str = "",
    url: str = "",
    tags: List[str] = list(),
    venue_name: str = "",
    venue_address: str = "",
    venue_is_wheelchair_accessible: bool = False,
    show_is_photosensitivity_friendly: bool = False,
    accessibility_notes: str = "",
    min_ticket_price: float = None,
    max_ticket_price: float = None,
    occurrences: List[dict] = list(),
    participants: List[User] = list(),
    commit_db_after_creation: bool = True
):
    new_event = Event(
        organizer_id = organizer.id,
        organizer = organizer,
        title = title,
        description = description,
        url = url,
        tags = list(),
        venue_name = venue_name,
        venue_address = venue_address,
        venue_is_wheelchair_accessible = venue_is_wheelchair_accessible,
        show_is_photosensitivity_friendly = show_is_photosensitivity_friendly,
        accessibility_notes = accessibility_notes,
        min_ticket_price = min_ticket_price,
        max_ticket_price = max_ticket_price,
        occurrences = list(),
        participants = participants
    )

    db.session.add(new_event)
    for tag in tags:
        create_event_tag(tag, new_event, False)
        
    for occurrence in occurrences:
        start_time = datetime.strptime(f"{occurrence.get("date")} {occurrence.get("start_time")}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{occurrence.get("date")} {occurrence.get("end_time")}", "%Y-%m-%d %H:%M")
        create_event_occurrence(event=new_event, start_time=start_time, end_time=end_time, is_relaxed_performance=bool(occurrence.get("is_relaxed_performance")) or False, has_asl_interpreter=bool(occurrence.get("has_asl_interpreter")) or False)
    
    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event created successfully.", new_event)

# Creates a new EventTag object, or finds one that already exists on the database with the same name
@event_orm.route("event/tag/create", methods=["POST"])
def create_event_tag(name: str, event: Event, commit_db_after_creation: bool = True):
    name = name.lower()
    new_tag = db.session.query(EventTag).filter_by(name = name).first()
    if new_tag is not None:
        new_tag.events.append(event)
    else:
        new_tag = EventTag(name = name, events = [event])

    db.session.add(new_tag)

    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event tag created successfully.", new_tag)

@event_orm.route("event/occurrence/create", methods=["POST"])
def create_event_occurrence(
    event: Event,
    start_time: datetime,
    end_time: datetime,
    is_relaxed_performance: bool,
    has_asl_interpreter: bool,
    commit_db_after_creation: bool = True
):
    new_occurrence = EventOccurrence(
        event_id = event.id,
        event = event,
        start_time = start_time,
        end_time = end_time,
        is_relaxed_performance = is_relaxed_performance,
        has_asl_interpreter = has_asl_interpreter
    )

    db.session.add(new_occurrence)
    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event occurrence created successfully.", new_occurrence)


#######

@event_orm.route("event/read", methods=["POST"])
def read_event():
    #TODO: Add filters
    events = db.session.query(Event).all()
    return json_response(200, f"{len(events)} events found.", events)

@event_orm.route("event/tag/read", methods=["POST"])
def read_event_tag():
    #TODO: Add filters
    event_tags = db.session.query(EventTag).all()
    return json_response(200, f"{len(event_tags)} event tags found.", event_tags)

@event_orm.route("event/occurrence/read", methods=["POST"])
def read_event_occurrence():
    #TODO: Add filters
    event_occurrences = db.session.query(EventOccurrence).all()
    return json_response(200, f"{len(event_occurrences)} event occurrences found.", event_occurrences)
