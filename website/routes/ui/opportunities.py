from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from ... import sanitize_html
from ...forms.opportunity_filter import OpportunityFilter, fill_post_type_data, fill_term_type_data, fill_location_type_data, fill_compensation_type_data
from ...forms.opportunity import CreateOpportunityForm
from ...orm.opportunity.opportunity import get_opportunity_posts, get_opportunity_by_organizer_and_title, create_opportunity_post, update_opportunity_post, delete_opportunity_post
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


@opportunities.route('/create/', methods=['GET', 'POST'])
@login_required
def create_opportunity():
    form = CreateOpportunityForm()

    if request.method == "POST":
        if request.form.get("submit") is None:
            return render_template("create-opportunity.html", user=current_user, form=form)

        post_type = request.form.get(form.type.name)
        for e in PostType:
            if e.name == post_type:
                post_type = e

        deadline = datetime.strptime(
            request.form.get(form.close_date.name), "%Y-%m-%d")
        title = request.form.get(form.title.name)
        organization = request.form.get(form.organizer.name)

        display_desc = request.form.get(form.display_description.name)
        is_paid = True if request.form.get(form.is_paid.name) == 'y' else False
        pay = request.form.get(form.pay.name, "")
        number_positions = request.form.get(form.number_positions.name)
        location = request.form.get(form.location.name)
        duration_type = request.form.get(form.duration_type.name)
        start_date = datetime.strptime(
            request.form.get(form.start_date.name), "%Y-%m-%d")
        end_date = request.form.get(form.end_date.name)
        if end_date == "":
            end_date = None

        tags = request.form.get(form.tags.name, "").split(",")
        tags = [tag.strip() for tag in tags if tag.strip() != ""]

        term = request.form.get(form.term.name)
        for e in TermType:
            term = e if term == e.name else term

        location_type = request.form.get(form.location_type.name)
        location_type = [e for e in LocationType if e.name == location_type][0]

        if is_paid and pay.strip() == "":
            flash("Must specify pay estimate if pay/benefits are offered.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form)

        if duration_type == 'finite' and end_date is None:
            flash("End date must be specified if duration is finite.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form)

        if duration_type == 'finite':
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if end_date < start_date:
                flash("End Date must be after the Start Date.",
                      category='error')
                return render_template("create-opportunity.html", user=current_user, form=form)

        if deadline <= datetime.now() - timedelta(days=1):
            flash("The deadline must not have already passed.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form)

        if start_date <= datetime.now() - timedelta(days=1):
            flash("The start date must not have already passed.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form)

        description = sanitize_html(request.form.get(form.description.name))
        responsibilities = sanitize_html(
            request.form.get(form.responsibilities.name))
        requirements = sanitize_html(request.form.get(form.requirements.name))
        compensation = sanitize_html(request.form.get(form.compensation.name))
        additional = sanitize_html(request.form.get(form.additional.name))
        application = sanitize_html(request.form.get(form.application.name))

        application_link = request.form.get(form.application_link.name)
        application_url = urlparse(application_link)
        if application_link != '' and application_url.scheme != 'https':
            flash("Application link must use HTTPS.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form)

        resp = create_opportunity_post(
            type=post_type,
            title=title,
            organizer=organization,
            poster_id=current_user.id,
            closing_date=deadline,
            location_type=location_type,
            location=location,
            start_date=start_date,
            is_paid=is_paid,
            display_description=display_desc,
            description=description,
            requirements=requirements,
            compensation=compensation,
            application_details=application,
            tags=tags,
            end_date=end_date,
            pay=pay,
            term_type=term,
            number_positions=number_positions,
            responsibilities=responsibilities,
            additional_info=additional,
            application_link=application_link,
        )

        if resp["status_code"] != 201:
            flash(resp["message"],
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form)
        else:
            flash("Opportunity Post Successfully Created",
                  category='success')
            return redirect(url_for('opportunities.opportunity', organizer=organization, title=title))

    return render_template("create-opportunity.html", user=current_user, form=form)


@opportunities.route('/edit/<organizer>/<title>/', methods=['GET', 'POST'])
@login_required
def edit_opportunity(organizer: str, title: str):
    form = CreateOpportunityForm()

    resp = get_opportunity_by_organizer_and_title(
        organizer=organizer, title=title)

    opportunity: Opportunity = resp.get("data", None)
    if opportunity is None:
        flash('No such opportunity post exists.', category='error')
        return redirect(url_for('opportunities.opportunities_list'))

    if opportunity.poster_id != current_user.id:
        flash('You are not the poster of this opportunity.')
        return redirect(url_for('opportunities.opportunity', organizer=organizer, title=title))

    if request.method == "POST":
        if request.form.get("submit") is None:
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        post_type = request.form.get(form.type.name)
        for e in PostType:
            if e.name == post_type:
                post_type = e

        deadline = datetime.strptime(
            request.form.get(form.close_date.name), "%Y-%m-%d")
        title = request.form.get(form.title.name)
        organization = request.form.get(form.organizer.name)

        display_desc = request.form.get(form.display_description.name)
        is_paid = True if request.form.get(form.is_paid.name) == 'y' else False
        pay = request.form.get(form.pay.name, "")
        number_positions = request.form.get(form.number_positions.name)
        location = request.form.get(form.location.name)
        duration_type = request.form.get(form.duration_type.name)
        start_date = datetime.strptime(
            request.form.get(form.start_date.name), "%Y-%m-%d")
        end_date = request.form.get(form.end_date.name)
        if end_date == "":
            end_date = None

        tags = request.form.get(form.tags.name, "").split(",")
        tags = [tag.strip() for tag in tags if tag.strip() != ""]

        term = request.form.get(form.term.name)
        for e in TermType:
            term = e if term == e.name else term

        location_type = request.form.get(form.location_type.name)
        location_type = [e for e in LocationType if e.name == location_type][0]

        if is_paid and pay.strip() == "":
            flash("Must specify pay estimate if pay/benefits are offered.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        if duration_type == 'finite' and end_date is None:
            flash("End date must be specified if duration is finite.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        if duration_type == 'finite':
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if end_date < start_date:
                flash("End Date must be after the Start Date.",
                      category='error')
                return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        if deadline <= datetime.now() - timedelta(days=1):
            flash("The deadline must not have already passed.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        if start_date <= datetime.now() - timedelta(days=1):
            flash("The start date must not have already passed.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        description = sanitize_html(request.form.get(form.description.name))
        responsibilities = sanitize_html(
            request.form.get(form.responsibilities.name))
        requirements = sanitize_html(request.form.get(form.requirements.name))
        compensation = sanitize_html(request.form.get(form.compensation.name))
        additional = sanitize_html(request.form.get(form.additional.name))
        application = sanitize_html(request.form.get(form.application.name))

        application_link = request.form.get(form.application_link.name)
        application_url = urlparse(application_link)
        if application_link != '' and application_url.scheme != 'https':
            flash("Application link must use HTTPS.",
                  category='error')
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

        update_resp = update_opportunity_post(
            id=opportunity.id,
            type=post_type,
            title=title,
            organizer=organization,
            closing_date=deadline,
            location_type=location_type,
            location=location,
            start_date=start_date,
            is_paid=is_paid,
            display_description=display_desc,
            description=description,
            requirements=requirements,
            compensation=compensation,
            application_details=application,
            tags=tags,
            end_date=end_date,
            pay=pay,
            term_type=term,
            number_positions=number_positions,
            responsibilities=responsibilities,
            additional_info=additional,
            application_link=application_link,
        )

        if (update_resp["status_code"] == 200):
            opportunity: Opportunity = update_resp["data"]
            flash('Opportunity Post updated!', category='success')
            return redirect(url_for('opportunities.opportunity', organizer=opportunity.organizer, title=opportunity.title))
        else:
            flash(update_resp["message"],
                  category=update_resp["response_type"])
            return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)

    form.title.data = opportunity.title
    form.organizer.data = opportunity.organizer
    form.type.data = opportunity.type.name
    form.close_date.data = opportunity.closing_date

    form.display_description.data = opportunity.display_description
    form.tags.data = ', '.join([tag.name for tag in opportunity.tags])
    form.is_paid.data = opportunity.is_paid
    if opportunity.pay is not None:
        form.pay.data = opportunity.pay
    if opportunity.term is not None:
        form.term.data = opportunity.term.name
    if opportunity.number_positions is not None:
        form.number_positions.data = opportunity.number_positions
    form.location_type.data = opportunity.location_type.name
    form.location.data = opportunity.location
    form.start_date.data = opportunity.start_date
    if opportunity.end_date is not None:
        form.end_date.data = opportunity.end_date
        form.duration_type.data = 'finite'
    else:
        form.duration_type.data = 'indefinite'

    form.description.data = opportunity.description
    if opportunity.responsibilities is not None:
        form.responsibilities.data = opportunity.responsibilities
    form.requirements.data = opportunity.requirements
    form.compensation.data = opportunity.compensation
    if opportunity.additional_info is not None:
        form.additional.data = opportunity.additional_info
    form.application.data = opportunity.application_details

    if opportunity.application_link is not None:
        form.application_link.data = opportunity.application_link

    return render_template("create-opportunity.html", user=current_user, form=form, edit=True, opportunity=opportunity)


@opportunities.route('/delete/<organizer>/<title>/', methods=['GET', 'POST'])
@login_required
def delete_opportunity(organizer: str, title: str):
    resp = get_opportunity_by_organizer_and_title(
        organizer=organizer, title=title)

    opportunity: Opportunity = resp.get("data", None)
    if opportunity is None:
        flash('No such opportunity post exists.', category='error')
        return redirect(url_for('opportunities.opportunities_list'))

    if opportunity.poster_id != current_user.id:
        flash('You are not the poster of this opportunity.')
        return redirect(url_for('opportunities.opportunity', organizer=organizer, title=title))

    delete_opportunity_post(opportunity.id)
    flash('Opportunity Post deleted!', category='success')
    return redirect(url_for('opportunities.opportunities_list'))
