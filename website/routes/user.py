from typing import Set
from .. import db, json_response
from ..models import User
import json
import requests
from flask import Blueprint, request, url_for, jsonify

user_route = Blueprint('user_route', __name__)
   


@user_route.route("user/create", methods=["POST"])
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
        tags=set(),
        events_organized=set(),
        events_participated=set()
    )
    db.session.add(new_user)
    db.session.flush()
    new_user.username = f"user{new_user.id}"
    db.session.commit()

    return json_response(201, "User created successfully.", new_user)

@user_route.route("api/user/create", methods=["POST"])
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