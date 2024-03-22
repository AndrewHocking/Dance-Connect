from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ...orm.event.event import read_event, create_event
from ...forms.events import CreateEventForm

events = Blueprint('events', __name__)

@events.route('/events', methods=['GET', 'POST'])
def events_list():
    response = read_event()
    events = response["data"]
    return render_template("events.html", user=current_user, events=events)

@events.route('/events/create', methods=['GET', 'POST'])
@login_required
def event_create():
    occurrences = []
    for i in range(0,50):
        occurrences.append({"name" : f"occurrence_{i}"})
    event_form = CreateEventForm(occurrences=occurrences)
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        url = request.form.get('url')
        tags = request.form.get('tags')
        venue_name = request.form.get('venue_name')
        venue_address = request.form.get('venue_address')
        venue_is_wheelchair_accessible = request.form.get('venue_is_wheelchair_accessible')
        accessibility_notes = request.form.get('accessibility_notes')
        show_is_photosensitivity_friendly = request.form.get("show_is_photosensitivity_friendly")
        occurrences = []
        for i in range(0, int(request.form.get("num_occurrences"))):
            occurrences.append({
                "date" : request.form.get(f"occurrences-{i}-date"),
                "start_time" : request.form.get(f"occurrences-{i}-start_time"),
                "end_time" : request.form.get(f"occurrences-{i}-end_time"),
                "is_relaxed_performance" : request.form.get(f"occurrences-{i}-is_relaxed_performance"),
                "has_asl_interpreter" : request.form.get(f"occurrences-{i}-has_asl_interpreter")
            })

        try:
            min_ticket_price = float(request.form.get('min_ticket_price'))
        except:
            min_ticket_price = None
        try:
            max_ticket_price = float(request.form.get('max_ticket_price'))
        except:
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
            venue_is_wheelchair_accessible=bool(venue_is_wheelchair_accessible),
            show_is_photosensitivity_friendly=bool(show_is_photosensitivity_friendly),
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

#TODO: rework this to use the orm methods
@events.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id: int):
    from ... import db
    from ...models.event import Event
    event: Event = db.session.query(Event).get(event_id)
    return render_template("event-details.html", user=current_user, event=event)