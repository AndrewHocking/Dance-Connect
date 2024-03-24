from typing import List

from ... import db, json_response
from ...models.event import Event
from ...models.user import User
from flask_login import current_user
from datetime import datetime
from .event_tag import create_event_tag
from .event_occurrence import create_event_occurrence

# Creates a new Event object
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
        participants = participants,
        request_notifications = list(),
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

def read_event():
    #TODO: Add filters
    events = db.session.query(Event).all()
    return json_response(200, f"{len(events)} events found.", events)


