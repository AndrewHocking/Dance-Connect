from flask import Blueprint, render_template, request
from flask_login import current_user

from datetime import datetime, timedelta, timezone

from ...forms.opportunity_filter import OpportunityFilter, fill_post_type_data, fill_term_type_data, fill_location_type_data, fill_compensation_type_data
from ...orm.opportunity.opportunity import get_opportunity_posts, get_opportunity_by_organizer_and_title
from ...models.opportunity import PostType, TermType, LocationType, Opportunity

opportunities = Blueprint('opportunities', __name__)

colors = ['primary', 'success', 'danger', 'warning']
post_types = dict()
types = [e for e in PostType]
for i in range(len(types)):
    post_types[types[i].name] = colors[i % len(colors)]


@opportunities.route('/', methods=['GET', 'POST'])
def opportunities_list():
    form = OpportunityFilter()

    search = None
    sort_method = None
    type_filters = []
    location_filters = []
    term_filters = []
    only_paid = False
    tag_filters = []
    tag_match_method = None

    print(request.form)

    if request.method == "POST":
        # print(request.form)
        if request.form.get("clear_filters") is None:

            search = request.form.get("search", None)
            if search == '':
                search = None

            sort_method = request.form.get("sort", None)

            filters = []
            for key in request.form:
                if request.form[key] != "y":
                    continue

                filter_type, *filter_name = key.split("-")
                filter_name = '-'.join(filter_name)
                if filter_type == form.opportunity_type.name:
                    type_filters.append(filter_name)
                elif filter_type == form.term_type.name:
                    term_filters.append(filter_name)
                elif filter_type == form.location_type.name:
                    location_filters.append(filter_name)
                elif filter_type == form.compensation_type.name:
                    only_paid = True

            tag_match_method = request.form.get(form.match_all_tags.name, None)
            tag_list = request.form.get(form.tags.name, '').split(',')
            tag_filters = [tag.strip()
                           for tag in tag_list if tag.strip() != '']

    if search is not None:
        form.search.data = search
    if sort_method is not None:
        form.sort_option.data = sort_method

    fill_post_type_data(form.opportunity_type, type_filters)
    fill_compensation_type_data(form.compensation_type, only_paid)
    fill_term_type_data(form.term_type, term_filters)
    fill_location_type_data(form.location_type, location_filters)

    form.match_all_tags.data = tag_match_method
    form.tags.data = ', '.join(tag_filters)

    resp = get_opportunity_posts(
        search_name=search,
        sort_method=sort_method,
        type_filters=type_filters,
        location_filters=location_filters,
        term_filters=term_filters,
        pay_only=only_paid,
        tags=tag_filters,
        tag_match_method=tag_match_method,
    )
    opportunities: list[Opportunity] = resp.get('data', [])

    return render_template("opportunities.html", user=current_user, filters=form, post_type=post_types, term_type=TermType, location_type=LocationType, opportunities=opportunities)


@opportunities.route('/<organizer>/<title>/', methods=['GET', 'POST'])
def opportunity(organizer: str, title: str):
    resp = get_opportunity_by_organizer_and_title(
        organizer=organizer, title=title)

    opportunity: Opportunity = resp.get("data", None)
    if opportunity is None:
        return render_template("opportunity-details.html", user=current_user, opportunity=opportunity)

    is_editable = current_user == opportunity.poster
    return render_template("opportunity-details.html", user=current_user, opportunity=opportunity, edit=is_editable, post_type=post_types)
