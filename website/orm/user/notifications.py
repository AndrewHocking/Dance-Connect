import string
from typing import List

from .user_tag import create_user_tag
from ... import db, json_response
from ...models.user import User, OrgType, Roles, UserTag, SocialMedia, EventRequestNotification
from ...models.event import Event
from sqlalchemy import asc, desc, or_, and_, func;

def add_event_request_notification(sender: User, event_id: Event, role: str = ""):
    associated_event: Event | None = db.session.query(Event).filter_by(id=event_id).first()
    if associated_event is None:
        return json_response(400, f"No event was found for the given event_id: {event_id}")
    
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
    notification = db.session.query(EventRequestNotification).filter_by(id=notification_id).first()
    if notification is None:
        return json_response(400, f"Found no entry for notification {notification_id}")
    
    requesting_user = db.session.query(User).filter_by(id=notification.sender_id).first()
    if requesting_user is None:
        return json_response(400, f"Found no entry for the user requesting to join this event", notification.sender_id)
    
    notification.event.participants.append(requesting_user)

    delete_notification(notification_id)
    db.session.commit()
    
    return json_response(
        200, 
        f"Successfully accepted user {requesting_user.display_name}'s request to be added to event {notification.event.title}", 
        notification.event
    )


# declines the request to be added to event by deleting the notification
def deny_event_request_notification(notification_id: int):
    result = delete_notification(notification_id)
    if result == 0:
        return json_response(400, f"Found no entry for notification {notification_id}")
    
    db.session.commit()
    return json_response(200, f"Notification request successfully removed")



def delete_notification(notification_id: int) -> int:
    num_rows_deleted = db.session.query(EventRequestNotification).filter_by(id=notification_id).delete()
    return num_rows_deleted