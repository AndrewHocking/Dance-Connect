from flask import render_template
from flask_login import current_user


# 404 Handling
def not_found_handler(e):
    return render_template("error-404.html", user=current_user), 404
