from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..orm.event import read_event, create_event
from ...forms.events import CreateEventForm

events = Blueprint('events', __name__)

@events.route('/events', methods=['GET', 'POST'])
def events_list():
    response = read_event()
    events = response["data"]
    return render_template("events.html", user=current_user, events=events)

@events.route('/create-event', methods=['GET', 'POST'])
@login_required
def event_create():
    occurrences = []
    for i in range(0,50):
        occurrences.append({"name" : f"occurrence_{i}"})
    event_form = CreateEventForm(occurrences=occurrences)
        
    if request.method == 'POST':
        print(request.form)
        title = request.form.get('title')
        description = request.form.get('description')
        url = request.form.get('url')
        tags = request.form.get('tags')
        venue_name = request.form.get('venue_name')
        venue_address = request.form.get('venue_address')
        venue_is_wheelchair_accessible = request.form.get('venue_is_wheelchair_accessible')
        accessibility_notes = request.form.get('accessibility_notes')
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
            accessibility_notes=accessibility_notes,
            min_ticket_price=min_ticket_price,
            max_ticket_price=max_ticket_price
        )

        if (response["status_code"] == 201):
            flash('Event created!', category='success')
            return redirect(url_for('events.events_list'))
        else:
            flash(response["message"], category=response["response_type"])

    return render_template("create-event.html", user=current_user, event_form=event_form)
