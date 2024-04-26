from typing import List
from sqlalchemy import and_, distinct, func, not_, or_
from flask_login import current_user
from datetime import datetime

from ... import db, json_response
from ...models.event import Event, EventOccurrence
from ...models.user import User
from .event_contributor import connect_user_to_event, remove_user_from_event
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
    venue_is_mobility_aid_accessible: bool = False,
    accessibility_notes: str = "",
    min_ticket_price: float = None,
    max_ticket_price: float = None,
    occurrences: List[dict] = list(),
    contributors: List[User] = list(),
    commit_db_after_creation: bool = True,
    image_picture_url="",
    image_picture_id="",
):
    new_event = Event(
        organizer_id=organizer.id,
        organizer=organizer,
        title=title,
        description=description,
        url=url,
        tags=list(),
        venue_name=venue_name,
        venue_address=venue_address,
        venue_is_mobility_aid_accessible=venue_is_mobility_aid_accessible,
        accessibility_notes=accessibility_notes,
        min_ticket_price=min_ticket_price,
        max_ticket_price=max_ticket_price,
        occurrences=list(),
        contributors=contributors,
        request_notifications=list(),
        image_picture_url=image_picture_url,
        image_picture_id=image_picture_id,
    )

    db.session.add(new_event)
    db.session.commit()

    connect_user_to_event(user=organizer, event=new_event, role="Organizer")

    for tag in tags:
        create_event_tag(tag, new_event, False)

    for occurrence in occurrences:
        create_event_occurrence(
            event=new_event,
            start_time=occurrence.start_time,
            end_time=occurrence.end_time,
            is_relaxed_performance=bool(
                occurrence.is_relaxed_performance or False),
            is_photosensitivity_friendly=bool(
                occurrence.is_photosensitivity_friendly or False),
            is_hearing_accessible=bool(
                occurrence.is_hearing_accessible or False),
            is_visually_accessible=bool(
                occurrence.is_visually_accessible or False),
        )

    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event created successfully.", new_event)


def get_event(id: int):
    event = db.session.query(Event).get(id)
    if event is None:
        return json_response(404, "Event not found.", None)
    return json_response(200, "Event found.", event)


def search_events(
    id: int = None,
    search: str = "",
    sort: str = "upcoming",
    venue_is_mobility_aid_accessible: bool = False,
    is_relaxed_performance: bool = False,
    is_photosensitivity_friendly: bool = False,
    is_hearing_accessible: bool = False,
    is_visually_accessible: bool = False,
    min_ticket_price: float = None,
    max_ticket_price: float = None,
    start_date: datetime = datetime.now(),
    end_date: datetime = None,
    tags: List[str] = list(),
    match_all_tags: str = "any",
    limit: int = None,
    offset: int = None,
):
    filtered_events = db.session.query(Event, func.count(distinct(EventOccurrence.id))).join(Event.occurrences).filter(
        (Event.title.ilike(f"%{search}%") |
         Event.description.ilike(f"%{search}%")),
        or_(Event.venue_is_mobility_aid_accessible ==
            venue_is_mobility_aid_accessible, not venue_is_mobility_aid_accessible),
        or_(EventOccurrence.is_relaxed_performance ==
            is_relaxed_performance, not is_relaxed_performance),
        or_(EventOccurrence.is_photosensitivity_friendly ==
            is_photosensitivity_friendly, not is_photosensitivity_friendly),
        or_(EventOccurrence.is_hearing_accessible ==
            is_hearing_accessible, not is_hearing_accessible),
        or_(EventOccurrence.is_visually_accessible ==
            is_visually_accessible, not is_visually_accessible),
    )

    if id is not None:
        filtered_events = filtered_events.filter(Event.id == id)

    if len(tags) > 0:
        if match_all_tags == "all":
            filtered_events = filtered_events.filter(
                and_(*[Event.tags.any(name=name) for name in tags])
            )
        elif match_all_tags == "any":
            filtered_events = filtered_events.filter(
                or_(*[Event.tags.any(name=name) for name in tags])
            )
        elif match_all_tags == "none":
            filtered_events = filtered_events.filter(
                not_(or_(*[Event.tags.any(name=name) for name in tags]))
            )
        else:
            return json_response(400, "Invalid value for 'match_all_tags'.", None)

    if min_ticket_price is not None:
        filtered_events = filtered_events.filter(
            Event.min_ticket_price >= min_ticket_price)
    if max_ticket_price is not None:
        filtered_events = filtered_events.filter(
            Event.max_ticket_price <= max_ticket_price)
    if start_date is not None:
        filtered_events = filtered_events.filter(
            EventOccurrence.start_time >= start_date)
    if end_date is not None:
        filtered_events = filtered_events.filter(
            EventOccurrence.start_time <= end_date)

    if sort == "alpha-desc":
        filtered_events = filtered_events.order_by(Event.title.desc())
    elif sort == "upcoming":
        filtered_events = filtered_events.order_by(EventOccurrence.start_time)
    else:
        filtered_events = filtered_events.order_by(Event.title)

    filtered_events = filtered_events.group_by(Event)

    if limit is not None:
        filtered_events = filtered_events.limit(limit)
    if offset is not None:
        filtered_events = filtered_events.offset(offset)

    results = filtered_events.all()
    if results is None or len(results) == 0:
        return json_response(404, "No events found that match the given search criteria.", results)

    return json_response(200, f"{len(results)} events found.", results)


def update_event(
    event: Event,
    organizer: User = None,
    title: str = None,
    description: str = None,
    url: str = None,
    tags: List[str] = None,
    venue_name: str = None,
    venue_address: str = None,
    venue_is_mobility_aid_accessible: bool = None,
    accessibility_notes: str = None,
    min_ticket_price: float = None,
    max_ticket_price: float = None,
    occurrences: List[dict] = None,
    contributors: List[User] = None,
    commit_db_after_update: bool = True,
    image_picture_url=None,
    image_picture_id=None,
):

    if organizer is not None:
        remove_user_from_event(event.organizer, event)
        connect_user_to_event(user=organizer, event=event, role="Organizer")
        event.organizer = organizer
        event.organizer_id = organizer.id
    if title is not None:
        event.title = title
    if description is not None:
        event.description = description
    if url is not None:
        event.url = url
    if tags is not None:
        event.tags = list()
        for tag in tags:
            create_event_tag(tag, event, False)
    if venue_name is not None:
        event.venue_name = venue_name
    if venue_address is not None:
        event.venue_address = venue_address
    if venue_is_mobility_aid_accessible is not None:
        event.venue_is_mobility_aid_accessible = venue_is_mobility_aid_accessible
    if accessibility_notes is not None:
        event.accessibility_notes = accessibility_notes
    if min_ticket_price is not None:
        event.min_ticket_price = min_ticket_price
    if max_ticket_price is not None:
        event.max_ticket_price = max_ticket_price
    if occurrences is not None:
        event.occurrences = list()
        for occurrence in occurrences:
            create_event_occurrence(
                event=event,
                start_time=occurrence.start_time,
                end_time=occurrence.end_time,
                is_relaxed_performance=bool(
                    occurrence.is_relaxed_performance or False),
                is_photosensitivity_friendly=bool(
                    occurrence.is_photosensitivity_friendly or False),
                is_hearing_accessible=bool(
                    occurrence.is_hearing_accessible or False),
                is_visually_accessible=bool(
                    occurrence.is_visually_accessible or False),
            )
    if contributors is not None:
        event.contributors = list()
        for contributor in contributors:
            connect_user_to_event(
                user=contributor, event=event, role="Contributor")

    if image_picture_url is not None:
        event.image_picture_url = image_picture_url

    if image_picture_id is not None:
        event.image_picture_id = image_picture_id

    db.session.add(event)
    if commit_db_after_update:
        db.session.commit()

    return json_response(200, "Event updated successfully.", event)


def delete_event(event: Event, commit_db_after_deletion: bool = True):
    db.session.delete(event)
    if commit_db_after_deletion:
        db.session.commit()

    return json_response(200, "Event deleted successfully.")
