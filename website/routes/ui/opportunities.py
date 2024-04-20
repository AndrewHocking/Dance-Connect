from flask import Blueprint, render_template
from flask_login import current_user

opportunities = Blueprint('opportunities', __name__)


@opportunities.route('/', methods=['GET', 'POST'])
def opportunities_list():
    return render_template("opportunities.html", user=current_user)
