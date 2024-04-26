from datetime import datetime

from ...models.event import Event, EventContributor, EventOccurrence
from ..user.user import User
from ... import db, json_response


def connect_user_to_event(user: User, event: Event, role: str):
    """
    Connects a user to an event with the specified role.

    Args:
        user (User): The User object.
        event (Event): The Event object.
        role (str): The role of the user in the event.

    Returns:
        dict: The JSON response.
    """
    # Check if the user is already connected to the event
    existing_entry = EventContributor.query.filter_by(
        user_id=user.id, event_id=event.id).first()
    if existing_entry:
        return json_response(409, "User is already connected to the event.", existing_entry.role)

    # Create a new EventContributor entry
    event_contributor = EventContributor(
        user_id=user.id, event_id=event.id, role=role)
    db.session.add(event_contributor)
    db.session.commit()

    return json_response(201, "User connected to event successfully.", event_contributor.role)


def remove_user_from_event(user: User, event: Event):
    """
    Removes a user from an event.

    Args:
        user (User): The user to be removed from the event.
        event (Event): The event from which the user will be removed.

    Returns:
        dict: The JSON response.
    """
    # Find the EventContributor entry
    event_contributor = EventContributor.query.filter_by(
        user_id=user.id, event_id=event.id).first()

    if event_contributor:
        # Delete the entry
        db.session.delete(event_contributor)
        db.session.commit()
        return json_response(200, "User removed from event successfully.")
    else:
        # User is not associated with the event
        return json_response(404, "User is not connected to the event.")


def get_event_contributors(event_id: int):
    """
    Get all contributors of an event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        dict: The JSON response.
    """
    contributors = EventContributor.query.filter_by(event_id=event_id).all()
    return json_response(200, f"{len(contributors)} event contributors found.", contributors)


def get_affiliations(user_id: int):
    query = (
        db.session.query(User, Event)
        .join(User.events_contributed)
        .filter(Event.contributors.any(id=user_id))
        .filter(User.id != user_id)
        .order_by(User.id)
    )

    affiliations = {}
    for user, event in query.all():
        if user not in affiliations:
            affiliations[user] = []
        affiliations[user].append(event)

    if not affiliations or len(affiliations) == 0:
        return json_response(404, "No affiliations found.", None)
    return json_response(200, f"{len(affiliations)} affiliations found.", affiliations)


def get_future_contributions(user_id: int):
    query = (
        db.session.query(EventContributor)
        .join(EventOccurrence, EventContributor.event_id == EventOccurrence.event_id)
        .filter(EventContributor.user_id == user_id)
        .filter(EventOccurrence.start_time > datetime.now())
        .order_by(EventOccurrence.start_time.asc())
    )

    future_contributions = query.all()

    if not future_contributions:
        return json_response(404, "No future contributions found.", None)
    return json_response(200, f"{len(future_contributions)} future contributions found.", future_contributions)


def get_past_contributions(user_id: int):
    future_occurrences_subquery = (
        db.session.query(EventContributor.id)
        .join(EventOccurrence, EventContributor.event_id == EventOccurrence.event_id)
        .filter(EventContributor.user_id == user_id)
        .filter(EventOccurrence.start_time > datetime.now())
        .subquery()
    )

    query = (
        db.session.query(EventContributor)
        .filter(EventContributor.user_id == user_id)
        # Exclude contributors with future occurrences
        .filter(~EventContributor.id.in_(future_occurrences_subquery))
        .join(EventOccurrence, EventContributor.event_id == EventOccurrence.event_id)
        .order_by(EventOccurrence.start_time.asc())
    )

    past_contributions = query.all()

    if not past_contributions or len(past_contributions) == 0:
        return json_response(404, "No past contributions found.", None)
    return json_response(200, f"{len(past_contributions)} past contributions found.", past_contributions)
