from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ..orm.user import read_users
from ...forms.people_filter import PeopleFilter

people = Blueprint('people', __name__)

@people.route('/people', defaults={'search': ''}, methods=['GET', 'POST'])
@people.route('/people/<search>', methods=['GET', 'POST'])
def people_list(search):
    form = PeopleFilter()
    print('Arg', search)

    if request.method == 'POST':
        print(request.form)
        if request.form['submit'] == 'Search':
            print("Search Request")
            print(request.form.get('search'))
            if request.form.get('search', '') != '':
                redirect(url_for('people.people_list', search=request.form.get('search', '')))
        elif request.form['submit'] == 'Apply Filters':
            print("Filter Request")
        elif request.form['submit'] == 'Clear Filters':
            print("Clear Filter Request")

    response = read_users()
    people = response["data"]

    return render_template("people.html", user=current_user, people=people, form=form)

