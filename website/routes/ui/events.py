from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from ...models.event.event import Event
from ...models.event.event_contributor import EventContributor
from ...models.user.user import EventRequestNotification
from ...orm.event.event import all_events, get_event, create_event, search_events
from ...orm.event.event_contributor import get_event_contributors, remove_user_from_event
from ...orm.user.notifications import get_event_request_notification, add_event_request_notification, delete_notification
from ...forms.events import CreateEventForm, CreateEventOccurrenceForm
from ...forms.event_filter import EventFilterForm


events = Blueprint('events', __name__)


@events.route('/', methods=['GET', 'POST'])
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


@events.route('/create/', methods=['GET', 'POST'])
@login_required
def event_create():
    event_form = CreateEventForm()

    occurrences = []
    if request.method == 'POST':
        if session['form_data'] is not None:
            form = session['form_data']
        else:
            form = request.form

        event_form.title.data = form.get('title', "")
        event_form.description.data = form.get('description', "")
        event_form.url.data = form.get('url', "")
        event_form.tags.data = form.get('tags', "")
        event_form.venue_name.data = form.get('venue_name', "")
        event_form.venue_address.data = form.get('venue_address', "")
        event_form.venue_is_mobility_aid_accessible.data = form.get(
            'venue_is_mobility_aid_accessible', False)
        event_form.accessibility_notes.data = form.get(
            'accessibility_notes', "")
        event_form.min_ticket_price.data = form.get('min_ticket_price', "")
        event_form.max_ticket_price.data = form.get('max_ticket_price', "")
        event_form.num_occurrences.data = form.get('num_occurrences', 1)
        for i in range(0, int(form.get("num_occurrences"))):
            occurrence = CreateEventOccurrenceForm()
            occurrence.date.data = form.get(f"occurrence-{i}-date", "")
            occurrence.start_time.data = form.get(
                f"occurrence-{i}-start-time", "")
            occurrence.end_time.data = form.get(
                f"occurrence-{i}-end-time", "")
            occurrence.is_relaxed_performance.data = form.get(
                f"occurrence-{i}-is-relaxed-performance", False)
            occurrence.is_photosensitivity_friendly.data = form.get(
                f"occurrence-{i}-is-photosensitivity-friendly", False)
            occurrence.is_hearing_accessible.data = form.get(
                f"occurrence-{i}-is-hearing-accessible", False)
            occurrence.is_visually_accessible.data = form.get(
                f"occurrence-{i}-is-visually-accessible", False)
            occurrences.append(occurrence)
        session['form_data'] = None
    else:
        occurrences.append(CreateEventOccurrenceForm())
    return render_template("create-event.html", user=current_user, event_form=event_form, occurrences=occurrences)


@events.route('/create/submit/', methods=['POST'])
def create_event_submit():
    print(request.form)
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    tags = request.form.get('tags')
    venue_name = request.form.get('venue_name')
    venue_address = request.form.get('venue_address')
    venue_is_mobility_aid_accessible = request.form.get(
        'venue_is_mobility_aid_accessible')
    accessibility_notes = request.form.get('accessibility_notes')
    occurrences = []
    for i in range(0, int(request.form.get("num_occurrences"))):
        occurrences.append({
            "start_time": datetime.strptime(f"{request.form.get(f"occurrence-{i}-date")} {
                request.form.get(f"occurrence-{i}-start-time")}", "%Y-%m-%d %H:%M"),
            "end_time": datetime.strptime(f"{request.form.get(f"occurrence-{i}-date")} {
                request.form.get(f"occurrence-{i}-end-time")}", "%Y-%m-%d %H:%M"),
            "is_relaxed_performance": request.form.get(f"occurrence-{i}-is-relaxed-performance"),
            "is_photosensitivity_friendly": request.form.get(f"occurrence-{i}-is-photosensitivity-friendly"),
            "is_hearing_accessible": request.form.get(f"occurrence-{i}-is-hearing-accessible"),
            "is_visually_accessible": request.form.get(f"occurrence-{i}-is-visually-accessible"),
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
        venue_is_mobility_aid_accessible=bool(
            venue_is_mobility_aid_accessible),
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
        session['form_data'] = request.form
        return redirect(url_for('events.event_create', _method='POST'))


@events.route('/create/create-event-occurrence/', methods=['POST'])
def create_event_occurrence():
    print(request.form)
    occurrence = CreateEventOccurrenceForm()
    return render_template("create-event-occurrence.html", occurrence=occurrence, occurrence_number=int(request.form.get("occurrence_number")))


@events.route('/<int:event_id>/', methods=['GET'])
def event_details(event_id: int):
    event: Event = get_event(event_id).get("data")
    contributors: EventContributor = get_event_contributors(
        event_id).get("data")
    event_request_notification: EventRequestNotification = get_event_request_notification(
        event_id=event_id, sender_id=current_user.id).get("data") if current_user.is_authenticated else None

    occurrences = {}
    for occurrence in event.occurrences:
        date = occurrence.start_time.strftime("%A, %B %d")
        if date not in occurrences:
            occurrences[date] = []
        occurrences[date].append(occurrence)

    return render_template("event-details.html", user=current_user, event=event, occurrences=occurrences, contributors=contributors, event_request_notification=event_request_notification)


@events.route('/<int:event_id>/join/', methods=['POST'])
@login_required
def join_event(event_id: int):
    add_event_request_notification(
        sender=current_user, event_id=event_id, role=request.form.get("role", ""))["data"]
    flash('Request sent!', category='success')
    return redirect(url_for('events.event_details', event_id=event_id))


@events.route('/<int:event_id>/cancel-join-request/', methods=['POST'])
@login_required
def cancel_event_join_request(event_id: int):
    notification = get_event_request_notification(
        event_id=event_id, sender_id=current_user.id).get("data")
    delete_notification(notification.id)
    flash('Request cancelled!', category='success')
    return redirect(url_for('events.event_details', event_id=event_id))


@events.route('/<int:event_id>/leave/', methods=['POST'])
@login_required
def leave_event(event_id: int):
    event: Event = get_event(event_id).get("data")
    remove_user_from_event(event=event, user=current_user)
    flash('You are no longer listed as a contributor for this event.',
          category='success')
    return redirect(url_for('events.event_details', event_id=event_id))


@events.route('/<int:event_id>/contributors/', methods=['POST'])
def event_contributors(event_id: int):
    contributors: EventContributor = get_event_contributors(
        event_id).get("data")

    if contributors is None:
        return {"message": "No contributors found for the event."}, 404

    return render_template("event-contributors.html", user=current_user, contributors=contributors)
