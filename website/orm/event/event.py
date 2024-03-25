from typing import List

from sqlalchemy import and_, or_

from website.models.event.event_occurrence import EventOccurrence
from website.models.event.event_tag import EventTag

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
    db.session.commit()
    
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

def search_events(
    search: str,
    sort: str,
    accessible_venue: bool,
    asl_interpreter: bool,
    relaxed_performance: bool,
    min_ticket_price: float,
    max_ticket_price: float,
    start_date: datetime,
    end_date: datetime,
    tags: List[str],
    match_all_tags: bool
):    
    filtered_events = db.session.query(Event).join(Event.occurrences).join(Event.tags).filter(
        (Event.title.ilike(f"%{search}%") | Event.description.ilike(f"%{search}%")),
        or_(Event.venue_is_wheelchair_accessible == accessible_venue, accessible_venue == False),
        or_(EventOccurrence.has_asl_interpreter == asl_interpreter, asl_interpreter == False),
        or_(EventOccurrence.is_relaxed_performance == relaxed_performance, relaxed_performance == False)
    )
    
    if len(tags) > 0:
        if match_all_tags:
            filtered_events=filtered_events.filter(
                and_(*[Event.tags.any(name=name) for name in tags])
            )
        else:
            filtered_events=filtered_events.filter(
                or_(*[Event.tags.any(name=name) for name in tags])
            )
    
    if min_ticket_price is not None:
        filtered_events = filtered_events.filter(Event.min_ticket_price >= min_ticket_price)
    if max_ticket_price is not None:
        filtered_events = filtered_events.filter(Event.max_ticket_price <= max_ticket_price)
    if start_date is not None:
        filtered_events = filtered_events.filter(EventOccurrence.start_time >= start_date)
    if end_date is not None:
        filtered_events = filtered_events.filter(EventOccurrence.end_time <= end_date)
            
    if sort == "alpha-desc":
        filtered_events = filtered_events.order_by(Event.title.desc())
    elif sort == "upcoming":
        filtered_events = filtered_events.order_by(EventOccurrence.start_time)
    else:
        filtered_events = filtered_events.order_by(Event.title)
    
    results = filtered_events.all()
    if results is  None or len(results) == 0:
        return json_response(404, "No events found that match the given search criteria.", results)
    
    return json_response(200, f"{len(results)} events found.", results)