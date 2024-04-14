from collections import defaultdict
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from random import randrange

from ...models.notification.notification import EventRequestNotification

from ...orm.notification.notifications import accept_event_request_notification, deny_event_request_notification
from ...models.user import User
from ...models.event import Event

notifications = Blueprint('notifications', __name__)


class EventNotification:
    event: Event
    notification_list: list[EventRequestNotification]

    def __init__(self, event, notifications):
        self.event = event
        self.notification_list = notifications


@notifications.route('/notifications', methods=['GET', 'POST'])
@login_required
def notification_list():
    show_recv_notifications = True

    if request.method == "POST":
        if request.form.get("accept") is not None:
            notification_id = int(request.form["accept"].split("accept-")[1])
            print('id', notification_id)
            resp = accept_event_request_notification(notification_id)

        elif request.form.get("decline") is not None:
            notification_id = int(request.form["decline"].split("decline-")[1])
            resp = deny_event_request_notification(notification_id)

        elif request.form.get("cancel") is not None:
            notification_id = int(request.form["cancel"].split("cancel-")[1])
            resp = deny_event_request_notification(notification_id)
            show_recv_notifications = False

        elif request.form.get("recv-button") is not None:
            show_recv_notifications = True

        elif request.form.get("sent-button") is not None:
            show_recv_notifications = False

    '''
    for i in range(3):
        users = read_users()["data"]
        user: User = users[randrange(len(users))]

        events = list(read_event()["data"])
        events = [
            event for event in events if event not in current_user.events_organized]
        event = events[randrange(len(events))]

        my_events = current_user.events_organized
        my_event = my_events[randrange(len(my_events))]

        if i % 3 == 0:
            new_notif = add_event_request_notification(
                current_user, event.id, "dancer")
            print(new_notif["message"])
        elif i % 3 == 1:
            new_notif = add_event_request_notification(
                user, my_event.id, "choreographer")
            print(new_notif["message"])
        else:
            new_notif = add_event_request_notification(
                user, my_event.id, "Writer")
            print(new_notif["message"])
    '''

    notifications = []
    if show_recv_notifications:
        notifications = load_recv_notifications(current_user)
    else:
        notifications = load_sent_notifications(current_user)

    print(notifications)

    return render_template('notification_view.html', user=current_user, recv_req=show_recv_notifications, notifications=notifications)


def load_recv_notifications(user: User) -> list:
    notifications = defaultdict(list[EventRequestNotification])

    recv_notifications: list[EventRequestNotification] = user.received_notifications

    for notification in recv_notifications:
        notifications[notification.event_id].append((notification))

    notifications = [EventNotification(
        notifications[event_id][0].event, notifications[event_id]) for event_id in notifications]

    notifications.sort(key=lambda x: x.event.title)
    for event in notifications:
        event.notification_list.sort(key=lambda x: x.sender.display_name)

    return notifications


def load_sent_notifications(user: User) -> list:
    notifications: list[EventRequestNotification] = user.sent_notifications

    notifications.sort(key=lambda x: x.recipient.display_name)
    notifications.sort(key=lambda x: x.event.title)

    return notifications
