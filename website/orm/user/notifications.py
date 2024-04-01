from website.orm.event.event_contributor import connect_user_to_event
from ... import db, json_response
from ...models.user import User, EventRequestNotification
from ...models.event import Event


def add_event_request_notification(sender: User, event_id: Event, role: str = ""):
    associated_event: Event | None = db.session.query(
        Event).filter_by(id=event_id).first()
    if associated_event is None:
        return json_response(404, f"No event was found for the given event_id: {event_id}")

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

    connect_user_to_event(user=requesting_user,
                          event=notification.event, role=notification.role)

    delete_notification(notification_id)
    db.session.commit()

    return json_response(
        200,
        f"Successfully accepted user {
            requesting_user.display_name}'s request to be added to event {notification.event.title}",
        notification.event
    )


# declines the request to be added to event by deleting the notification
def deny_event_request_notification(notification_id: int):
    result = delete_notification(notification_id)
    if result == 0:
        return json_response(404, f"Found no entry for notification {notification_id}")

    db.session.commit()
    return json_response(200, "Notification request successfully removed")


def delete_notification(notification_id: int) -> int:
    num_rows_deleted = db.session.query(
        EventRequestNotification).filter_by(id=notification_id).delete()
    db.session.commit()
    return num_rows_deleted


def get_event_request_notification(event_id: int, sender_id: int):
    notification = db.session.query(
        EventRequestNotification).filter_by(event_id=event_id).filter_by(sender_id=sender_id).first()

    if notification is None:
        return json_response(404, "No notification found for the given event_id and sender_id")
    return json_response(200, "Notification found.", notification)
