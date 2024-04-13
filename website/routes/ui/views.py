from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route("/people/dummy/", methods=["GET", "POST"])
def dummy_user():
    return render_template("dummy-user.html", user=current_user)


@views.route("/events/dummy/", methods=["GET", "POST"])
def dummy_event():
    return render_template("dummy-event.html", user=current_user)


@views.route("/events/dummy-list/", methods=["GET", "POST"])
def dummy_event_list():
    return render_template("dummy-event-list.html", user=current_user)


@views.route("/people/dummy-list/", methods=["GET", "POST"])
def dummy_people_list():
    return render_template("dummy-people-list.html", user=current_user)
