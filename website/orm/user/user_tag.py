from ...models.user.user_tag import UserTag
from ... import db, json_response
from ...models.user import User

# Creates a new UserTag object, or finds one that already exists on the database with the same name
def create_user_tag(name: str, user: User, commit_db_after_creation: bool = True):
    name = name.lower()
    new_tag = db.session.query(UserTag).filter_by(name = name).first()
    if new_tag is not None:
        new_tag.users.append(user)
    else:
        new_tag = UserTag(name = name, users = [user])

    db.session.add(new_tag)

    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "User tag created successfully.", new_tag)

def read_user_tag():
    #TODO: Add filters
    user_tags = db.session.query(UserTag).all()
    return json_response(200, f"{len(user_tags)} user tags found.", user_tags)
