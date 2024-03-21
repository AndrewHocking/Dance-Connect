from ...models.user.user_tag import UserTag
from ... import db, json_response
from ...models.user import User
from sqlalchemy import asc, desc;

# Creates a new User object
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

# Returns List[User] that pass the filter parameters
def read_users(searchName: str = None, sortOption: str = 'alpha-asc', filterTags: list[str] = []):
    print('params', searchName, sortOption, filterTags)
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

    return json_response(200, "No user found" if user == None else f"User {user.name} found.", user)
