from website.orm.event.event_contributor import connect_user_to_event
from ... import db, json_response
from ...models.user import User, EventRequestNotification, Notification
from ...models.event import Event, EventContributor

from sqlalchemy import and_


def add_event_request_notification(sender: User, event_id: Event, role: str = ""):
    associated_event: Event | None = db.session.query(
        Event).filter_by(id=event_id).first()
    if associated_event is None:
        return json_response(404, f"No event was found for the given event_id: {event_id}")

    if associated_event.organizer_id == sender.id:
        return json_response(404, f"A user can't request to join their own event.")

    for contributor in associated_event.contributor_association:
        if contributor.user_id == sender.id:
            return json_response(404, f"A user can't request to join an event their already a part of.", contributor.role)

    conflict = db.session.query(EventRequestNotification).filter(and_(
        EventRequestNotification.event_id == event_id, EventRequestNotification.sender_id == sender.id)).first()
    if conflict is not None:
        return json_response(400, f"This user has already request to join this event.", conflict.role)

    new_notification = EventRequestNotification(
        recipient_id=associated_event.organizer_id,
        sender_id=sender.id,
        recipient=associated_event.organizer,
        sender=sender,
        event=associated_event,
        event_id=event_id,
        role=role,
    )

    db.session.add(new_notification)
    db.session.commit()

    return json_response(
        200,
        f"New Notification Added: \
            {sender.display_name} requested to be added to {associated_event.organizer.display_name}'s \
            {associated_event.title} event.",
        new_notification
    )


# accepts the request to be added to an event by adding user to the event and deleting the notification
def accept_event_request_notification(notification_id: int):
    notification = db.session.query(
        EventRequestNotification).filter_by(id=notification_id).first()
    if notification is None:
        return json_response(404, f"Found no entry for notification {notification_id}")

    requesting_user = db.session.query(User).filter_by(
        id=notification.sender_id).first()
    if requesting_user is None:
        return json_response(404, "Found no entry for the user requesting to join this event", notification.sender_id)

    event = notification.event
    role = notification.role
    deleted = delete_notification(notification_id)
    if not deleted:
        return json_response(404, f"Found no entry for notification {notification_id}")

    connect_user_to_event(user=requesting_user,
                          event=event, role=role)
    db.session.commit()

    return json_response(
        200,
        f"Successfully accepted user {
            requesting_user.display_name}'s request to be added to event {notification.event.title}",
        notification.event
    )


# declines the request to be added to event by deleting the notification
def deny_event_request_notification(notification_id: int):
    deleted = delete_notification(notification_id)
    if not deleted:
        return json_response(404, f"Found no entry for notification {notification_id}")

    return json_response(200, "Notification request successfully removed")


def delete_notification(notification_id: int) -> int:
    notification = db.session.query(
        EventRequestNotification).filter_by(id=notification_id).first()

    if notification is None:
        return False

    db.session.delete(notification)
    db.session.commit()

    return True


def get_event_request_notification(event_id: int, sender_id: int):
    notification = db.session.query(
        EventRequestNotification).filter_by(event_id=event_id).filter_by(sender_id=sender_id).first()

    if notification is None:
        return json_response(404, "No notification found for the given event_id and sender_id")
    return json_response(200, "Notification found.", notification)
