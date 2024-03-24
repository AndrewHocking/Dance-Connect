from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ...orm.user.user import read_users, read_single_user,  update_user, User, UserType
from ...forms.people_filter import PeopleFilter, Roles, fillOrganizationData, fillFilterData

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
        if request.form.get("search_button") != None:
            searchInput = request.form.get("search", "")
            if searchInput == "":
                searchInput = "_"

            return redirect(
                url_for(
                    "people.people_list", search=searchInput, sort=sort, filters=filters
                )
            )
        
        elif request.form.get("apply_filters") != None:
            sortMethod = request.form.get("sort", "")
            if sortMethod == "":
                sortMethod = "_"

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

        elif request.form.get("clear_filters") != None:
            return redirect(
                url_for("people.people_list", search=search, sort="_", filters="_")
            )

    if search != "_":
        form.search.data = search
    if sort != "_":
        form.sortOption.data = sort
    if filters != "_":
        filterArr = filters.split("+")
        other_tags = [filter.split("-")[1] for filter in filterArr if filter.split("-")[0] == "others"]
        filterArr = [filter.split("-")[1] for filter in filterArr]

        fillOrganizationData(form.userType.form, filterArr)
        fillFilterData(form.filters.form, filterArr)
        form.other_tags.data = ', '.join(other_tags)

    query_params = dict()
    if search != "_":
        query_params["searchName"] = search
    if sort != "_":
        query_params["sortOption"] = sort
    if filters != "_":
        all_filters = filters.split("+")
        user_types, filter_tags = [], []

        for filter in all_filters:
            filter = filter.split("-")
            if filter[0] == "userType":
                user_types.append(filter[1])
            elif filter[0] != "filters" or filter[1] != Roles.OTHER.value:
                filter_tags.append(filter[1])

        query_params["userTypes"] = user_types
        query_params["filterTags"] = filter_tags

    response = read_users(**query_params)
    people = response["data"]

    return render_template(
        "people.html", user=current_user, people=people, filters=form, orgType=UserType, roles=Roles
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
