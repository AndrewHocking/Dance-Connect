from flask import Blueprint, request, redirect, url_for, flash

from ...models.user import User
from ...models.event import Event
from ...orm.report.report import add_bug_report

reports = Blueprint('reports', __name__)


@reports.route('/bug/submit', methods=['POST'])
def submit_bug():
    title = request.form.get("title")
    desc = request.form.get("description")

    resp = add_bug_report(title=title, description=desc)

    if resp['status_code'] != 201:
        flash('Unable to report issue.', category='error')
    else:
        flash('Report successfully recieved', category='success')

    return redirect(url_for('views.home'))
