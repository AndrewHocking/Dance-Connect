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
login_manager.login_view = "auth.login" # passed in function name of the route
login_manager.login_message_category = "info"

def json_response(status_code: int, message: str, data: Any = None):
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
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes.ui.views import views
    from .routes.ui.auth import auth
    from .routes.ui.people import people
    from .routes.ui.events import events
    from .routes.orm.user import user_orm
    from .routes.orm.event import event_orm

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(people, url_prefix='/')
    app.register_blueprint(events, url_prefix='/')
    app.register_blueprint(user_orm, url_prefix='/')
    app.register_blueprint(event_orm, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
