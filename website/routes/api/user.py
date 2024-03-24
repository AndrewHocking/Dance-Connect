from ...models.user import User
from ...orm.user.user import create_user
import json
from flask import Blueprint, request, jsonify

user_api = Blueprint('user_route', __name__)

# API access for the create_user method
@user_api.route("user/create", methods=["POST"])
def create_user():
    #TODO: There probably should be some sort of verification of where this API request is coming from, so that not just anyone who discovers the link can just create infinite users.
    criteria = json.loads(request.json)
    email = criteria.get('email')
    display_name = criteria.get('display_name')
    password = criteria.get('password')

    output = create_user(email=email, password=password, display_name=display_name)
    if (output["status_code"] == 201):
        new_user: User = output["data"]
        output["data"] = new_user.id

    return jsonify(output)
