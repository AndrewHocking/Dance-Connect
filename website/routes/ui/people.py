from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ...orm.user.user import read_users, read_single_user, User
from ...forms.people_filter import PeopleFilter, fillOrganizationData, fillFilterData

people = Blueprint('people', __name__)

@people.route('/people', defaults={'search': '_', 'sort': '_', 'filters': '_'}, methods=['GET', 'POST'])
@people.route('/people/<search>/<sort>/<filters>', methods=['GET', 'POST'])
def people_list(search, sort, filters):
    form = PeopleFilter()
    print()
    print('Arg', search, sort, filters)

    if request.method == 'POST':
        print(request.form)
        if request.form['submit'] == 'Search':
            print("Search Request")
            searchInput = request.form.get('search', '')
            if searchInput == '':
                searchInput = '_'

            return redirect(url_for('people.people_list', search=searchInput, sort=sort, filters=filters))
        
        elif request.form['submit'] == 'Apply Filters':
            print("Filter Request")
            sortMethod = request.form.get('sort', '')
            if sortMethod == '':
                sortMethod = '_'

            filters = []
            for key in request.form:
                if request.form[key] == 'y':
                    filters.append(key)
            
            if len(filters) == 0:
                filterStr = '_'
            else:
                filterStr = '+'.join(filters)

            return redirect(url_for('people.people_list', search=search, sort=sortMethod, filters=filterStr))

        elif request.form['submit'] == 'Clear Filters':
            print("Clear Filter Request")
            return redirect(url_for('people.people_list', search=search, sort='_', filters='_'))

    if search != '_':
        form.searchName.data = search
    if sort != '_':
        form.sortOption.data = sort
    if filters != '_':
        filterArr = filters.split('+')
        filterArr = [filter.split('-')[1] for filter in filterArr]

        fillOrganizationData(form.organizationType.form, filterArr)
        fillFilterData(form.filters.form, filterArr)

    query_params = dict()
    if search != '_':
        query_params["searchName"] = search 
    if sort != '_':
        query_params["sortOption"] = sort
    if filters != '_':
        query_params["filterTags"] = filters.split('+')

    response = read_users(**query_params)
    people = response["data"]

    return render_template("people.html", user=current_user, people=people, form=form)


@people.route('/people/<id>', methods=['GET'])
def person(id):
    person: User = read_single_user(user_id = id)["data"]
    events = list(person.events_organized)
    events.extend(list(person.events_participated))
    print(events)

    bio = None
    if person.bio != '':
        bio = person.bio

    affiliations: list[User] = read_users()["data"]
    if person in affiliations:
        affiliations.remove(person)
    
    print('occ', events[0].occurrences)
    return render_template("person.html", user=current_user, person=person, bio=bio, events=events, affiliations=affiliations)

