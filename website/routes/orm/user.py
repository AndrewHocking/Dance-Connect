from typing import List
from ... import db, json_response
from ...models import User, UserTag
import json
import requests
from flask import Blueprint, request, url_for, jsonify

user_orm = Blueprint('user_route', __name__)
   
# Creates a new User object
@user_orm.route("user/create", methods=["POST"])
def create_user(email: str, password: str, name: str, username: str = None, pronouns: str = ""):
    if len(email) < 4:
        return json_response(400, 'Email must be greater than 3 characters.')
    elif len(name) < 2:
        return json_response(400, 'First name must be greater than 1 character.')
    elif len(password) < 8:
        return json_response(400, 'Password must be at least 7 characters.')

    conflict = db.session.query(User).filter_by(email=email).first()
    if (conflict is not None):
        return json_response(409, 'A user with this email address already exists.')

    new_user = User(
        username=email,
        email=email,
        password=password,
        is_admin=False,
        name=name,
        pronouns="",
        bio="",
        tags=list(),
        events_organized=list(),
        events_participated=list()
    )
    db.session.add(new_user)
    db.session.flush()
    new_user.username = f"user{new_user.id}"
    db.session.commit()

    return json_response(201, "User created successfully.", new_user)

# API access for the create_user method
@user_orm.route("api/user/create", methods=["POST"])
def create_user_api():
    criteria = json.loads(request.json)
    email = criteria.get('email')
    name = criteria.get('name')
    password = criteria.get('password')

    output = create_user(email=email, password=password, name=name)
    if (output["status_code"] == 201):
        new_user: User = output["data"]
        output["data"] = new_user.id

    return jsonify(output)


# Creates a new UserTag object, or finds one that already exists on the database with the same name
@user_orm.route("user/tag/create", methods=["POST"])
def create_user_tag(name: str, user: User, commit_db_after_creation: bool = True):
    name = name.lower
    existing_tag = db.session.query(UserTag).filter_by(name = name).first()
    if existing_tag is not None:
        existing_tag.users.append(user)
    else:
        new_tag = UserTag(name = name, users = [user])

    db.session.add(new_tag)

    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "User tag created successfully.", new_tag)


#######

#TODO: Make API endpoint for these methods

# Creates a new User object
@user_orm.route("user/read", methods=["POST"])
def read_users():
    #TODO: Add filters
    users = db.session.query(User).all()
    return json_response(200, f"{len(users)} users found.", users)

@user_orm.route("user/tag/read", methods=["POST"])
def read_user_tag():
    #TODO: Add filters
    user_tags = db.session.query(UserTag).all()
    return json_response(200, f"{len(user_tags)} user tags found.", user_tags)
