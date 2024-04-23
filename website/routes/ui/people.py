from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app
from flask_login import current_user

from ...orm.event.event_contributor import get_affilliations
from ...orm.user.user import read_users, read_single_user, update_user, User, UserType, create_socials_link, update_socials_link, check_user_exists, check_email_exists
from ...forms.people_filter import (
    PeopleFilter,
    Roles,
    fill_organization_data,
    fill_filter_data,
)
from flask import flash
import os

from werkzeug.utils import secure_filename

from ...cloud.cdn import CDN, ALLOWED_EXTENSIONS

MAX_FILE_SIZE = 1024 * 1024 * 10  # 10MB

people = Blueprint("people", __name__)


@people.route(
    "/people/",
    defaults={"search": "_", "sort": "_", "filters": "_"},
    methods=["GET", "POST"],
)
@people.route("/people/<search>/<sort>/<filters>/", methods=["GET", "POST"])
def people_list(search, sort, filters):
    form = PeopleFilter()

    if request.method == "POST":
        # print(request.form)
        if request.form.get("search_button") is not None:
            search_input = request.form.get("search", "")
            if search_input == "":
                search_input = "_"

            return redirect(
                url_for(
                    "people.people_list",
                    search=search_input,
                    sort=sort,
                    filters=filters,
                )
            )

        elif request.form.get("apply_filters") is not None:
            sort_method = request.form.get("sort", "")
            if sort_method == "":
                sort_method = "_"

            filters = []
            for key in request.form:
                if request.form[key] == "y":
                    filters.append(key)

            other_tags = request.form.get("other_tags", "")
            tag_list = [tag.strip() for tag in other_tags.split(",")]
            for tag in tag_list:
                if tag != "":
                    filters.append("others-" + tag)

            if len(filters) == 0:
                filter_str = "_"
            else:
                filter_str = "+".join(filters)

            return redirect(
                url_for(
                    "people.people_list",
                    search=search,
                    sort=sort_method,
                    filters=filter_str,
                )
            )

        elif request.form.get("clear_filters") is not None:
            return redirect(
                url_for("people.people_list", search=search,
                        sort="_", filters="_")
            )

    if search != "_":
        form.search.data = search
    if sort != "_":
        form.sort_option.data = sort
    if filters != "_":
        filter_arr = filters.split("+")
        other_tags = [
            filter.split("-")[1]
            for filter in filter_arr
            if filter.split("-")[0] == "others"
        ]
        filter_arr = [filter.split("-")[1] for filter in filter_arr]

        fill_organization_data(form.user_type.form, filter_arr)
        fill_filter_data(form.filters.form, filter_arr)
        form.other_tags.data = ", ".join(other_tags)

    query_params = dict()
    if search != "_":
        query_params["search_name"] = search
    if sort != "_":
        query_params["sort_option"] = sort
    if filters != "_":
        all_filters = filters.split("+")
        user_types, filter_tags = [], []

        for filter in all_filters:
            filter = filter.split("-")
            if filter[0] == "user_type":
                user_types.append(filter[1])
            elif filter[0] != "filters" or filter[1] != Roles.OTHER.value:
                filter_tags.append(filter[1])

        query_params["user_types"] = user_types
        query_params["filter_tags"] = filter_tags

    response = read_users(**query_params)
    people = response["data"]

    return render_template(
        "people.html",
        user=current_user,
        people=people,
        filters=form,
        orgType=UserType,
        roles=Roles,
    )


@people.route("/people/<username>/", methods=["GET"])
def person(username):
    person: User = read_single_user(username=username)["data"]
    events_contributed = person.contributor_association

    socialMediaDic = {}
    for social in person.socials:
        socialMediaDic[social.social_media] = social.handle

    # print(socialMediaDic)

    edit = False

    bio = None
    if person.bio != "":
        bio = person.bio

    # affiliations = get_affilliations(person.id)["data"]
    affiliations: list[User] = read_users()["data"]
    if person in affiliations:
        affiliations.remove(person)

    return render_template(
        "person.html",
        user=current_user,
        person=person,
        bio=bio,
        events_contributed=events_contributed,
        affiliations=affiliations,
        edit=edit,
        socials=socialMediaDic,
    )


@people.route("/people/<username>/edit/", methods=["GET", "POST"])
def edit_person(username):
    person: User = read_single_user(username=username)["data"]
    events = list(person.events_organized)
    events.extend(list(person.events_contributed))
    # form = PeopleFilter()

    socialMediaDic = {}
    for social in person.socials:
        socialMediaDic[social.social_media] = social.handle

    edit = True

    bio = None
    if person.bio != "":
        bio = person.bio

    tag_name_list = [tag.name for tag in person.tags]
    tag_name_list = [
        " " + tag for tag in tag_name_list
    ]  # add space to make tags look better

    affiliations: list[User] = read_users()["data"]
    if person in affiliations:
        affiliations.remove(person)
    if request.method == "POST" and request.form["submit"] == "Save":
        newBio = request.form.get("bioTextArea", "")
        display_name = request.form.get("display_name", "")
        pronouns = request.form.get("pronouns", "")
        uniqueUsername = request.form.get("uniqueUsername", "")

        website = request.form.get("website", "")
        if website.startswith("http://") or website.startswith("https://"):
            website = website[website.find("://") + 3:]

        instagram = request.form.get("instagram", "")

        if instagram.startswith("@"):  # url works without @
            instagram = instagram[1:]

        email = request.form.get("email", "")

        threads = request.form.get("threads", "")  # url works with @
        if threads.startswith("@"):
            threads = threads[1:]

        if threads.find("@") != -1:
            threads = threads[0:threads.find("@")]

        tiktok = request.form.get("tiktok", "")

        if tiktok.startswith("@"):  # url works with @
            tiktok = tiktok[1:]

        twitter = request.form.get("twitter", "")  # url works without @
        if twitter.startswith("@"):
            twitter = twitter[1:]

        facebook = request.form.get("facebook", "")

        current_pass = request.form.get("current_password", "")
        new_pass = request.form.get("new_password", "")
        confirm_pass = request.form.get("confirm_new_password", "")

        current_login_email = request.form.get("current_login_email", "")
        new_email = request.form.get("new_login_email", "")
        confirm_email = request.form.get("confirm_new_login_email", "")

        tags = request.form.get("tags", "")
        tag_list = tags.split(",")
        tag_list = [tag.strip() for tag in tag_list]
        tag_list = [tag for tag in tag_list if tag != ""]

        # list of handle and social media types
        socialListofList = [[website, "website"], [instagram, "instagram"], [email, "email"], [
            threads, "threads"], [tiktok, "tiktok"], [twitter, "twitter"], [facebook, "facebook"], ]

        for social in socialListofList:
            if update_socials_link(person.id, social[1], social[0])["status_code"] == 404 and social[0] != "":
                create_socials_link(person.id, social[1], social[0])

        file = request.files['profilePicture']
        # handle file upload
        if file.filename != "" and 'profilePicture' in request.files:
            temp_error_flag = False

            current_app.config['UPLOAD_FOLDER'] = './website/cloud/temp'
            # app.config['UPLOAD_FOLDER'] = '/cloud/temp/'

            # according to co-pilot, this is a secure way to handle file uploads
            # this uses the werkzeug.utils library
            filename = secure_filename(file.filename)

            # Check if file was uploaded and that the type and size is correct
            if not file:
                flash("No file uploaded", "error")
                temp_error_flag = True

            if not allowed_file(file.filename):
                flash("File type not allowed", "error")
                temp_error_flag = True

            if file.content_length > MAX_FILE_SIZE:
                flash("File size too large", "error")
                temp_error_flag = True

            if temp_error_flag:
                return render_template(
                    "edit_person.html",
                    user=current_user,
                    person=person,
                    bio=newBio,
                    events=events,
                    affiliations=affiliations,
                    edit=edit,
                    tag_name_list=tag_name_list,
                    socials=socialMediaDic,
                )
            else:
                # save file to temp folder
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename))
                # upload file to cloudflare
                cdn = CDN()
                output = cdn.upload(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename))

                if len(output["errors"]) > 0:
                    flash("Error uploading file to cloudflare", "error")
                    return render_template(
                        "edit_person.html",
                        user=current_user,
                        person=person,
                        bio=newBio,
                        events=events,
                        affiliations=affiliations,
                        edit=edit,
                        tag_name_list=tag_name_list,
                        socials=socialMediaDic,
                    )

                # if user has profile picture in cloud then delete it!
                if person.profile_picture_id != "":
                    delete_output = cdn.delete(person.profile_picture_id)
                # TODO CHECK IF DELETE WORKED!!!

                # TODO allow for selection of which variant to use instead of always the first one
                update_user(
                    user_id=person.id,
                    profile_picture_url=output["result"]["variants"][0],
                    profile_picture_id=output["result"]["id"]
                )

                # purge temp folder
                cdn.empty_temp_folder()

                # TODO ideally desroy cdn object since it won't be used again...

        # check password and update if all good
        # did user want to change password?
        if (current_pass != "" or new_pass != "" or confirm_pass != ""):
            # check if current password is correct and new password matches
            if (person.password != current_pass or new_pass != confirm_pass):
                flash(
                    "Password did not match or current password is incorrect", "error"
                )
                return render_template(
                    "edit_person.html",
                    user=current_user,
                    person=person,
                    bio=newBio,
                    events=events,
                    affiliations=affiliations,
                    edit=edit,
                    tag_name_list=tag_name_list,
                    socials=socialMediaDic,
                )
            else:
                update_user(
                    user_id=person.id,
                    password=new_pass,
                )

        # check if person wanted to change login email
        if (current_login_email != "" or new_email != "" or confirm_email != ""):
            # check if current email is correct and new email matches and new email is unique
            if (person.email != current_login_email or new_email != confirm_email) and (check_email_exists(email=new_email)["status_code"] == 404):
                flash(
                    "Emails did not match or current email verification is incorrect", "error"
                )
                return render_template(
                    "edit_person.html",
                    user=current_user,
                    person=person,
                    bio=newBio,
                    events=events,
                    affiliations=affiliations,
                    edit=edit,
                    tag_name_list=tag_name_list,
                    socials=socialMediaDic,
                )
            else:
                update_user(
                    user_id=person.id,
                    email=new_email,
                )

        # Check for unique username
        if check_user_exists(username=username)["status_code"] == 404:
            flash("Username already taken", "error")
            return render_template(
                "edit_person.html",
                user=current_user,
                person=person,
                bio=newBio,
                events=events,
                affiliations=affiliations,
                edit=edit,
                tag_name_list=tag_name_list,
                socials=socialMediaDic,
            )

        # TODO add error message for when the password is of invalid format

        # if all okay, then update everyone
        update_user(
            user_id=person.id,
            display_name=display_name,
            pronouns=pronouns,
            bio=request.form.get("bioTextArea", ""),
            tags=tag_list,
        )
        # person.bio = request.form.get("bioTextArea", "")
        # person.save()
        return redirect(url_for("people.person", username=person.username))

    return render_template(
        "edit_person.html",
        user=current_user,
        person=person,
        bio=bio,
        events=events,
        affiliations=affiliations,
        edit=edit,
        tag_name_list=tag_name_list,
        socials=socialMediaDic,
    )


def allowed_file(filename) -> bool:
    """
    Check if the file is allowed to be uploaded

    Args:
        filename (str): the name of the file

    Returns: 
        bool: True if the file is allowed to be uploaded, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_person_fields(person: User, request: dict):
    """
    TODO this is to clean up the people.py file for editing a person
    Update the fields of a person object with the fields in the request

    Args:
        person (User): the person object to update
        request (dict): the request object

    Returns:
        None
    """
    pass
