from flask import Blueprint, render_template
from flask_login import current_user
from ..orm.user import read_users

people = Blueprint('people', __name__)


@people.route('/people', methods=['GET', 'POST'])
def people_list():
    response = read_users()
    people = response["data"]
    return render_template("people.html", user=current_user, people=people)
