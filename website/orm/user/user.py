import string
from typing import List

from .user_tag import create_user_tag
from ... import db, json_response
from ...models.user import User
from sqlalchemy import asc, desc;

# Creates a new User object
def create_user(
    email: str,
    password: str,
    name: str,
    username: str = "",
    pronouns: str = "",
    bio: str = "",
    tags: List[str] = list()
):
    if len(email) < 5:
        return json_response(400, 'Email must be greater than 5 characters.')
    elif len(name) < 1:
        return json_response(400, 'Display name must be at least 1 character.')
    elif len(password) < 8:
        return json_response(400, 'Password must be at least 7 characters.')

    conflict = db.session.query(User).filter_by(email=email).first()
    if (conflict is not None):
        return json_response(409, 'A user with this email address already exists.', conflict.email)

    if username == "":
        username = ''.join(i for i in name if i in string.ascii_letters+'0123456789-_').lower()
        conflicts = db.session.query(User).filter_by(username=username).all()
        if conflicts is not None and len(conflicts) > 0:
            username = f"{username}_{len(conflicts)}"

    new_user = User(
        username=username,
        email=email,
        password=password,
        is_admin=False,
        name=name,
        pronouns=pronouns,
        bio=bio,
        tags=list(),
        events_organized=list(),
        events_participated=list()
    )
    db.session.add(new_user)
    
    for tag in tags:
        create_user_tag(tag, new_user, False)

    db.session.commit()

    return json_response(201, "User created successfully.", new_user)

# Returns List[User] that pass the filter parameters
def read_users(searchName: str = None, sortOption: str = 'alpha-asc', filterTags: list[str] = []):
    users = db.session.query(User)
    if searchName != None:
        users = users.filter(User.name.icontains(searchName.lower()))
    
    if sortOption == 'alpha-asc':
        users = users.order_by(asc(User.name))
    elif sortOption == 'alpha-desc':
        users = users.order_by(desc(User.name))

    #TODO: Add support for filtering by user tags
        
    users = users.all()

    return json_response(200, f"{len(users)} users found.", users)

# Returns a single User by their id. Returns null if no such user exists.
def read_single_user(user_id: int):
    user = db.session.query(User).filter_by(id = user_id).first()

    if user == None:
        return json_response(404, "No user found")
    
    return json_response(200, f"User {user.name} found.", user)
