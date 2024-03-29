from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ...models.event.event import Event
from ...models.event.event_contributor import EventContributor
from ...models.user.user import EventRequestNotification
from ...orm.event.event import all_events, get_event, create_event, search_events
from ...orm.event.event_contributor import get_event_contributors, remove_user_from_event
from ...orm.user.notifications import get_event_request_notification, add_event_request_notification, delete_notification
from ...forms.events import CreateEventForm
from ...forms.event_filter import EventFilterForm


events = Blueprint('events', __name__)


@events.route('/events', methods=['GET', 'POST'])
def events_list():
    filters = EventFilterForm()
    if request.method == "POST":
        filters.search.default = request.form.get("search") or ""
        if request.form.get("clear_filters") is None:
            filters.sort.default = request.form.get("sort") or "upcoming"
            if request.form.get("accessible_venue") is not None:
                filters.accessible_venue.default = request.form.get(
                    "accessible_venue")
            if request.form.get("asl_interpreter") is not None:
                filters.asl_interpreter.default = request.form.get(
                    "asl_interpreter")
            if request.form.get("relaxed_performance") is not None:
                filters.relaxed_performance.default = request.form.get(
                    "relaxed_performance")
            filters.min_ticket_price.default = request.form.get(
                "min_ticket_price")
            filters.max_ticket_price.default = request.form.get(
                "max_ticket_price")
            filters.start_date.default = request.form.get("start_date")
            filters.end_date.default = request.form.get("end_date")
            filters.tags.default = request.form.get("tags")
            filters.match_all_tags.default = request.form.get("match_all_tags")

            search = request.form.get("search") or ""
            sort = request.form.get("sort") or "upcoming"
            accessible_venue = bool(
                request.form.get('accessible_venue') or False)
            asl_interpreter = bool(
                request.form.get('asl_interpreter') or False)
            relaxed_performance = bool(
                request.form.get('relaxed_performance') or False)
            try:
                min_ticket_price = float(request.form.get('min_ticket_price'))
            except Exception:
                min_ticket_price = None
            try:
                max_ticket_price = float(request.form.get('max_ticket_price'))
            except Exception:
                max_ticket_price = None
            try:
                start_time = datetime.strptime(
                    f"{request.form.get("start_date")} 00:00:00", "%Y-%m-%d %H:%M:%S")
            except Exception:
                start_time = datetime.now()
            try:
                end_time = datetime.strptime(
                    f"{request.form.get("end_date")} 23:59:59", "%Y-%m-%d %H:%M:%S")
            except Exception:
                end_time = None
            tags = request.form.get("tags")
            tag_list = list()
            if tags is not None and tags != "":
                for tag in tags.split(","):
                    tag_list.append(tag.strip())
            match_all_tags = request.form.get('match_all_tags') == 'True'
            print(match_all_tags)

            response = search_events(
                search=search,
                sort=sort,
                accessible_venue=accessible_venue,
                asl_interpreter=asl_interpreter,
                relaxed_performance=relaxed_performance,
                min_ticket_price=min_ticket_price,
                max_ticket_price=max_ticket_price,
                start_date=start_time,
                end_date=end_time,
                tags=tag_list,
                match_all_tags=match_all_tags
            )
        else:
            return redirect(url_for("events.events_list"))
    else:
        response = all_events()

    events = response.get("data") or []
    return render_template("events.html", user=current_user, events=events, filters=filters)


@events.route('/events/create', methods=['GET', 'POST'])
@login_required
def event_create():
    occurrences = []
    for i in range(0, 50):
        occurrences.append({"name": f"occurrence_{i}"})
    event_form = CreateEventForm(occurrences=occurrences)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        url = request.form.get('url')
        tags = request.form.get('tags')
        venue_name = request.form.get('venue_name')
        venue_address = request.form.get('venue_address')
        venue_is_physically_accessible = request.form.get(
            'venue_is_physically_accessible')
        accessibility_notes = request.form.get('accessibility_notes')
        show_is_photosensitivity_friendly = request.form.get(
            "show_is_photosensitivity_friendly")
        occurrences = []
        for i in range(0, int(request.form.get("num_occurrences"))):
            occurrences.append({
                "date": request.form.get(f"occurrences-{i}-date"),
                "start_time": request.form.get(f"occurrences-{i}-start_time"),
                "end_time": request.form.get(f"occurrences-{i}-end_time"),
                "is_relaxed_performance": request.form.get(f"occurrences-{i}-is_relaxed_performance"),
                "has_asl_interpreter": request.form.get(f"occurrences-{i}-has_asl_interpreter")
            })

        try:
            min_ticket_price = float(request.form.get('min_ticket_price'))
        except Exception:
            min_ticket_price = None
        try:
            max_ticket_price = float(request.form.get('max_ticket_price'))
        except Exception:
            max_ticket_price = None

        tag_list = list()
        for tag in tags.split(","):
            tag_list.append(tag.strip())

        response = create_event(
            title=title,
            description=description,
            url=url,
            tags=tag_list,
            venue_name=venue_name,
            venue_address=venue_address,
            venue_is_physically_accessible=bool(
                venue_is_physically_accessible),
            show_is_photosensitivity_friendly=bool(
                show_is_photosensitivity_friendly),
            accessibility_notes=accessibility_notes,
            min_ticket_price=min_ticket_price,
            max_ticket_price=max_ticket_price,
            occurrences=occurrences
        )

        if (response["status_code"] == 201):
            flash('Event created!', category='success')
            return redirect(url_for('events.events_list'))
        else:
            flash(response["message"], category=response["response_type"])

    return render_template("create-event.html", user=current_user, event_form=event_form)


@events.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id: int):
    event: Event = get_event(event_id).get("data")
    contributors: EventContributor = get_event_contributors(
        event_id).get("data")
    event_request_notification: EventRequestNotification = get_event_request_notification(
        event_id=event_id, sender_id=current_user.id).get("data") if current_user.is_authenticated else None
    return render_template("event-details.html", user=current_user, event=event, contributors=contributors, event_request_notification=event_request_notification)


@events.route('/events/<int:event_id>/join', methods=['POST'])
@login_required
def join_event(event_id: int):
    add_event_request_notification(
        sender=current_user, event_id=event_id, role=request.form.get("role", ""))["data"]
    flash('Request sent!', category='success')
    return redirect(url_for('events.event_details', event_id=event_id))


@events.route('/events/<int:event_id>/cancel-join-request', methods=['POST'])
@login_required
def cancel_event_join_request(event_id: int):
    notification = get_event_request_notification(
        event_id=event_id, sender_id=current_user.id).get("data")
    delete_notification(notification.id)
    flash('Request cancelled!', category='success')
    return redirect(url_for('events.event_details', event_id=event_id))


@events.route('/events/<int:event_id>/leave', methods=['POST'])
@login_required
def leave_event(event_id: int):
    event: Event = get_event(event_id).get("data")
    remove_user_from_event(event=event, user=current_user)
    flash('You have left the event.', category='success')
    return redirect(url_for('events.event_details', event_id=event_id))


@events.route('/events/<int:event_id>/contributors', methods=['POST'])
def event_contributors(event_id: int):
    contributors: EventContributor = get_event_contributors(
        event_id).get("data")

    if contributors is None:
        return {"message": "No contributors found for the event."}, 404

    return render_template("event-contributors.html", user=current_user, contributors=contributors)
