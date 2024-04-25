from flask import Blueprint, render_template
from flask_login import current_user
from ...orm.event.event import search_events

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    events = search_events().get("data", list())
    return render_template("home.html", user=current_user, events=events[:2], events_count=len(events))


@views.route("/people/demo/", methods=["GET", "POST"])
def demo_user():
    return render_template("demo-user.html", user=current_user)


@views.route("/events/demo/", methods=["GET", "POST"])
def demo_event():
    return render_template("demo-event.html", user=current_user)


@views.route("/events/demo-list/", methods=["GET", "POST"])
def demo_event_list():
    return render_template("demo-event-list.html", user=current_user)


@views.route("/people/demo-list/", methods=["GET", "POST"])
def demo_people_list():
    return render_template("demo-people-list.html", user=current_user)
