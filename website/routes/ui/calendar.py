from flask import Blueprint, render_template
from website.forms.event_filter import EventFilterForm
from website.models.event.event import Event
from ..api.calendars import Calendar, CalendarEvent
from datetime import datetime, timedelta
from flask_login import current_user
from flask import redirect, url_for

calendar_blueprint = Blueprint('calendar', __name__)

@calendar_blueprint.route('/calendar')
def show_calendar():
    # Usage example:
    calendar = Calendar(year=2024)

    # Add events
    event1 = CalendarEvent("Event 1", datetime(2024, 4, 15),"akhdasfa","images/placeholder.jpg")
    event2 = CalendarEvent("Event 2", datetime(2024, 4, 20),"akhdasfa","images/placeholder.jpg")
    calendar.add_event(event1)
    calendar.add_event(event2)

    # Get events for April
    april_events = calendar.get_events(month=4)
    print("April Events:", april_events)
    # Render the calendar template with events
    return render_template('calendar.html', events=april_events, user=current_user)

@calendar_blueprint.route('/create-event', methods=['GET', 'POST'])
def create_event():
    # Assume event_form is your form for creating an event
    event_form = EventFilterForm()

    if event_form.validate_on_submit():
        # Assume Event is your data model for an event
        event = Event(
            title=event_form.title.data,
            description=event_form.description.data,
            # Add all other fields
        )
        from ... import db
        # Assume db is your SQLAlchemy database instance
        db.session.add(event)
        db.session.commit()

        # Redirect to the event calendar page after an event is created
        return redirect(url_for('calendar.show_calendar'))

    # Render the create event page if the form is not submitted or not valid
    return render_template('create-event.html', form=event_form, user=current_user)
