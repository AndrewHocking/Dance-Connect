from flask import Blueprint, render_template
from flask_login import current_user
from ..orm.user import read_user

people = Blueprint('people', __name__)


@people.route('/people', methods=['GET', 'POST'])
def people_list():
    response = read_user()
    people = response["data"]
    return render_template("people.html", user=current_user, people=people)
