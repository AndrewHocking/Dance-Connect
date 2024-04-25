from flask import render_template
from flask_login import current_user

from ...forms.reports import BugReportForm


# 404 Handling
def not_found_handler(e):
    return render_template("error-404.html", user=current_user), 404


def internal_server_error_handler(e):
    form = BugReportForm()
    return render_template("error-500.html", user=current_user, form=form), 500
