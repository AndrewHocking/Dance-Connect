import os
from typing import Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import bleach
from bleach.linkifier import LinkifyFilter

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # passed in function name of the route
login_manager.login_message_category = "info"


def json_response(status_code: int, message: str, data: Any = None):
    """
    Generate a JSON response object with the specified status code, message, and optional data.

    Args:
        status_code (int): The HTTP status code of the response.
        message (str): The message associated with the response.
        data (Any, optional): Additional data to include in the response. Defaults to None.

    Returns:
        dict: A dictionary representing the JSON response object. Use 'jsonify' to convert to JSON.

    """
    if status_code < 200:
        response_type = "information"
    elif status_code < 300:
        response_type = "success"
    elif status_code < 400:
        response_type = "redirect"
    else:
        response_type = "error"

    output = {
        "response_type": response_type,
        "status_code": status_code,
        "message": message,
        "data": data
    }
    return output


def sanitize_html(html_text, additional_tags: list[str] = []):
    allowed_tags = list(bleach.ALLOWED_TAGS)
    allowed_tags.extend(['p', 'h2', 'h3', 'h4'] + additional_tags)
    cleaner = bleach.Cleaner(
        tags=allowed_tags, filters=[LinkifyFilter])
    return cleaner.clean(html_text)


def create_app():
    app = Flask(__name__)

    # config_type = 'DevelopmentConfig'
    config_type = 'ProductionConfig'
    app.config.from_object(f'instance.config.{config_type}')
    db.init_app(app)

    from .routes.ui.views import views
    from .routes.ui.auth import auth
    from .routes.ui.people import people
    from .routes.ui.events import events
    from .routes.ui.debug import debug_route
    from .routes.ui.notifications import notifications
    from .routes.ui.opportunities import opportunities
    from .routes.ui.errors import not_found_handler, internal_server_error_handler
    from .routes.ui.reports import reports

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(people, url_prefix='/people')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(debug_route, url_prefix='/')
    app.register_blueprint(notifications, url_prefix='/')
    app.register_blueprint(opportunities, url_prefix='/opportunities')
    app.register_blueprint(reports, url_prefix='/reports')
    app.register_error_handler(404, not_found_handler)
    app.register_error_handler(500, internal_server_error_handler)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .models.user import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # create the directory if it doesn't yet exist
    # This is the cloud temp folder and to make sure that it exists
    tempFolder = os.path.join(os.path.dirname(
        __file__)) + "/cloud/temp"
    if not os.path.isdir(tempFolder):
        os.mkdir(tempFolder)

    # This is the instance folder and to make sure that it exists
    instanceFolder = os.path.join(os.path.split(os.path.dirname(
        __file__))[0]) + "/instance"
    if not os.path.isdir(instanceFolder):
        os.mkdir(instanceFolder)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
