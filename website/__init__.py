from typing import Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

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


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # TODO: Change this
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes.ui.views import views
    from .routes.ui.auth import auth
    from .routes.ui.people import people
    from .routes.ui.events import events
    from .routes.ui.debug import debug_route
    from .routes.api.user import user_api
    from .routes.api.event import event_api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(people, url_prefix='/')
    app.register_blueprint(events, url_prefix='/')
    app.register_blueprint(debug_route, url_prefix='/')
    app.register_blueprint(user_api, url_prefix='/api/')
    app.register_blueprint(event_api, url_prefix='/api/')

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    from .models.user import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
