from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ...orm.user.user import read_users, read_single_user,  update_user, User, UserType
from ...forms.people_filter import PeopleFilter, Roles, fill_organization_data, fill_filter_data

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
        print(request.form)
        if request.form.get("search_button") is not None:
            search_input = request.form.get("search", "")
            if search_input == "":
                search_input = "_"

            return redirect(
                url_for(
                    "people.people_list", search=search_input, sort=sort, filters=filters
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
        other_tags = [filter.split(
            "-")[1] for filter in filter_arr if filter.split("-")[0] == "others"]
        filter_arr = [filter.split("-")[1] for filter in filter_arr]

        fill_organization_data(form.user_type.form, filter_arr)
        fill_filter_data(form.filters.form, filter_arr)
        form.other_tags.data = ', '.join(other_tags)

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
        "people.html", user=current_user, people=people, filters=form, orgType=UserType, roles=Roles
    )


@people.route("/people/<id>", methods=["GET"])
def person(id):
    person: User = read_single_user(user_id=id)["data"]
    events = list(person.events_organized)
    events.extend(list(person.events_contributed))

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
    events.extend(list(person.events_contributed))
    # form = PeopleFilter()

    edit = True

    bio = None
    if person.bio != "":
        bio = person.bio

    affiliations: list[User] = read_users()["data"]
    if person in affiliations:
        affiliations.remove(person)
    if request.method == "POST":
        if request.form["submit"] == "Save":
            update_user(
                user_id=id,
                bio=request.form.get("bioTextArea", ""),
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
    )
