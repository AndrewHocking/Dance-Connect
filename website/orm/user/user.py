import string
from typing import List

from .user_tag import create_user_tag
from ... import db, json_response
from ...models.user import User, UserType, UserTag, SocialMedia
from sqlalchemy import asc, desc, or_, and_, func

# Creates a new User object


def create_user(
    email: str,
    password: str,
    display_name: str,
    username: str = "",
    pronouns: str = "",
    bio: str = "",
    tags: List[str] = list(),
):
    if len(email) < 5:
        return json_response(400, "Email must be greater than 5 characters.")
    elif len(display_name) < 1:
        return json_response(400, "Display name must be at least 1 character.")
    elif len(password) < 8:
        return json_response(400, "Password must be at least 7 characters.")

    conflict = db.session.query(User).filter_by(email=email).first()
    if conflict is not None:
        return json_response(
            409, "A user with this email address already exists.", conflict.email
        )

    if username == "":
        username = "".join(
            i for i in display_name if i in string.ascii_letters + "0123456789-_"
        ).lower()
        conflicts = db.session.query(User).filter_by(username=username).all()
        if conflicts is not None and len(conflicts) > 0:
            username = f"{username}_{len(conflicts)}"

    new_user = User(
        username=username,
        email=email,
        password=password,
        is_admin=False,
        display_name=display_name,
        user_type=UserType.INDIVIDUAL,
        pronouns=pronouns,
        bio=bio,
        tags=list(),
        socials=list(),
        received_notifications=list(),
        sent_notifications=list(),
        events_organized=list(),
        events_participated=list(),
    )
    db.session.add(new_user)

    for tag in tags:
        create_user_tag(tag, new_user, False)

    db.session.commit()

    return json_response(201, "User created successfully.", new_user)


# Returns List[User] that pass the filter parameters
def read_users(
    search_name: str = None, sort_option: str = "alpha-asc", user_types: list[str] = [], filter_tags: list[str] = []
):
    users = db.session.query(User)

    if search_name is not None:
        users = users.filter(User.display_name.icontains(search_name.lower()))

    if sort_option == "alpha-asc":
        users = users.order_by(asc(User.display_name))
    elif sort_option == "alpha-desc":
        users = users.order_by(desc(User.display_name))

    if len(user_types) > 0:
        queries = []
        for type in UserType:
            if type.value in user_types:
                queries.append(User.user_type == type)

        users = users.filter(or_(*queries))

    if len(filter_tags) > 0:
        queries = []
        for tag in filter_tags:
            queries.append(func.lower(UserTag.name) == func.lower(tag))

        users = users.join(User.tags).filter(or_(*queries))

    # TODO: Add support for filtering by user tags
    users = users.all()

    return json_response(200, f"{len(users)} users found.", users)


# Returns a single User by their id. Returns null if no such user exists.
def read_single_user(user_id: int):
    user = db.session.query(User).filter_by(id=user_id).first()

    if user is None:
        return json_response(404, "No user found")

    return json_response(200, f"User {user.display_name} found.", user)


# Updates a user with the given variables. Pass None to leave a variable unchanged.
def update_user(
    user_id: int,
    username: str = None,
    email: str = None,
    password: str = None,
    is_admin: bool = None,
    display_name: str = None,
    pronouns: str = None,
    bio: str = None,
    socials: List[SocialMedia] = None,
    user_type: UserType = None,
    tags: List[str] = None,
):
    user: User = db.session.query(User).get(user_id)
    if user is None:
        return json_response(404, "User not found.", user_id)

    if username is not None:
        user.username = username

    if email is not None:
        user.email = email

    if password is not None:
        user.password = password

    if is_admin is not None:
        user.is_admin = is_admin

    if display_name is not None:
        user.display_name = display_name

    if pronouns is not None:
        user.pronouns = pronouns

    if bio is not None:
        user.bio = bio

    if user_type is not None:
        user.user_type = user_type

    if socials is not None:
        user.socials.clear()
        for social_link in socials:
            create_socials_link(
                user.id, social_link.social_media, social_link.handle)

    if tags is not None:
        user.tags.clear()
        for tag in tags:
            create_user_tag(tag, User, False)

    db.session.add(user)
    db.session.commit()

    return json_response(200, "User updated successfully.", user)


# Adds a new social media handle to the given user
def create_socials_link(user_id: int, type: str, handle: str):
    conflict = db.session.query(SocialMedia) \
        .filter(and_(
            SocialMedia.user == user_id,
            func.lower(SocialMedia.social_media) == func.lower(type)
        )) \
        .first()

    if conflict is not None:
        return json_response(400, f"User aleady has an existing social media handle <{conflict.handle}> for this platform.")

    new_socials = SocialMedia(
        user=user_id,
        social_media=type,
        handle=handle
    )

    db.session.add(new_socials)
    db.session.commit()

    return json_response(200, f"New social media handle {handle} added for user on platform {type}", new_socials)


def update_socials_link(user_id: int, type: str, handle: str):
    socials_link = db.session.query(SocialMedia) \
        .filter(and_(
            SocialMedia.user == user_id,
            func.lower(SocialMedia.social_media) == func.lower(type)
        )) \

    if socials_link.first() is None:
        return json_response(200, f"User {user_id} does not have an existing handle on platform {type}")

    socials_link.update({"handle": handle})
    db.session.commit()

    return json_response(200, f"User {user_id}'s {type} handle has been updated to {handle}", socials_link.first())
