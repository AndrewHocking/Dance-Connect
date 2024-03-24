from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ...orm.user.user import read_users, read_single_user, User, update_user
from ...forms.people_filter import PeopleFilter, fillOrganizationData, fillFilterData
from flask import flash

people = Blueprint("people", __name__)


@people.route(
    "/people",
    defaults={"search": "_", "sort": "_", "filters": "_"},
    methods=["GET", "POST"],
)
@people.route("/people/<search>/<sort>/<filters>", methods=["GET", "POST"])
def people_list(search, sort, filters):
    form = PeopleFilter()

    if request.method == "POST":
        if request.form["submit"] == "Search":
            searchInput = request.form.get("search", "")
            if searchInput == "":
                searchInput = "_"

            return redirect(
                url_for(
                    "people.people_list", search=searchInput, sort=sort, filters=filters
                )
            )

        elif request.form["submit"] == "Apply Filters":
            sortMethod = request.form.get("sort", "")
            if sortMethod == "":
                sortMethod = "_"

            filters = []
            for key in request.form:
                if request.form[key] == "y":
                    filters.append(key)

            if len(filters) == 0:
                filterStr = "_"
            else:
                filterStr = "+".join(filters)

            return redirect(
                url_for(
                    "people.people_list",
                    search=search,
                    sort=sortMethod,
                    filters=filterStr,
                )
            )

        elif request.form["submit"] == "Clear Filters":
            return redirect(
                url_for("people.people_list", search=search, sort="_", filters="_")
            )

    if search != "_":
        form.search.data = search
    if sort != "_":
        form.sortOption.data = sort
    if filters != "_":
        filterArr = filters.split("+")
        filterArr = [filter.split("-")[1] for filter in filterArr]

        fillOrganizationData(form.organizationType.form, filterArr)
        fillFilterData(form.filters.form, filterArr)

    query_params = dict()
    if search != "_":
        query_params["searchName"] = search
    if sort != "_":
        query_params["sortOption"] = sort
    if filters != "_":
        query_params["filterTags"] = filters.split("+")

    response = read_users(**query_params)
    people = response["data"]

    return render_template(
        "people.html", user=current_user, people=people, filters=form
    )


@people.route("/people/<id>", methods=["GET"])
def person(id):
    person: User = read_single_user(user_id=id)["data"]
    events = list(person.events_organized)
    events.extend(list(person.events_participated))

    edit = False

    bio = None
    if person.bio != "":
        bio = person.bio

    affiliations: list[User] = read_users()["data"]
    if person in affiliations:
        affiliations.remove(person)

    return render_template(
        "person.html",
        user=current_user,
        person=person,
        bio=bio,
        events=events,
        affiliations=affiliations,
        edit=edit,
    )


@people.route("/people/<id>/edit", methods=["GET", "POST"])
def edit_person(id):
    person: User = read_single_user(user_id=id)["data"]
    events = list(person.events_organized)
    events.extend(list(person.events_participated))
    # form = PeopleFilter()

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
    if request.method == "POST":
        if request.form["submit"] == "Save":
            display_name = request.form.get("display_name", "")
            pronouns = request.form.get("pronouns", "")
            website = request.form.get("website", "")
            instagram = request.form.get("instagram", "")

            if instagram.startswith("@"):  # url works without @
                instagram = instagram[1:]

            email = request.form.get("email", "")
            threads = request.form.get("threads", "")
            tiktok = request.form.get("tiktok", "")

            if not tiktok.startswith("@"):  # url works with @
                tiktok = "@" + tiktok

            twitter = request.form.get("twitter", "")  # url works without @
            if twitter.startswith("@"):
                twitter = twitter[1:]

            facebook = request.form.get("facebook", "")
            current_pass = request.form.get("current_password", "")
            new_pass = request.form.get("new_password", "")
            confirm_pass = request.form.get("confirm_new_password", "")
            tags = request.form.get("tags", "")
            tag_list = tags.split(",")
            tag_list = [tag.strip() for tag in tag_list]
            tag_list = [tag for tag in tag_list if tag != ""]
            # print(tag_list)
            # print(person.password)
            # print(current_pass[0])
            # print(new_pass[0])
            # print(confirm_pass[0])
            if (person.password != current_pass or new_pass != confirm_pass) and (
                current_pass != "" or new_pass != "" or confirm_pass != ""
            ):
                flash(
                    "Password did not match or current password is incorrect", "error"
                )
                return redirect(url_for("people.edit_person", id=id))
            else:
                update_user(
                    user_id=id,
                    password=new_pass,
                )

            # TODO add error message for when the password is of invalid format

            update_user(
                user_id=id,
                display_name=display_name,
                pronouns=pronouns,
                bio=request.form.get("bioTextArea", ""),
                tags=tag_list,
            )
            person.bio = request.form.get("bioTextArea", "")
            # person.save()
            return redirect(url_for("people.person", id=id))

    return render_template(
        "edit_person.html",
        user=current_user,
        person=person,
        bio=bio,
        events=events,
        affiliations=affiliations,
        edit=edit,
        tag_name_list=tag_name_list,
    )
