from datetime import datetime, timezone
from typing import List
from sqlalchemy import func, and_, or_, not_

from ... import db, json_response
from ...models.opportunity import Opportunity, PostType, LocationType, TermType, OpportunityTag
from ...models.user import User
from .opportunity_tag import create_opportunity_tag


def create_opportunity_post(
        type: PostType,
        title: str,
        organizer: str,

        poster_id: int,
        closing_date: datetime,

        location_type: LocationType,
        location: str,
        start_date: datetime,
        is_paid: bool,

        display_description: str,
        description: str,
        requirements: str,
        compensation: str,
        application_details: str,

        tags: List[str] = list(),
        end_date: datetime = None,
        pay: str = None,
        term_type: TermType = None,
        number_positions: int = None,
        responsibilities: str = None,
        additional_info: str = None,
        application_link: str = None
):

    poster = db.session.query(User).filter_by(id=poster_id).first()
    if poster == None:
        return json_response(404, "Poster was not found.")

    conflict = db.session.query(Opportunity).filter(and_(
        func.lower(Opportunity.title) == func.lower(title),
        func.lower(Opportunity.organizer) == func.lower(organizer)
    )).first()

    if conflict is not None:
        return json_response(409, "A posting with the same title and organizer already exists.", conflict)

    today: datetime = datetime.now()
    if not is_paid:
        pay = None

    new_post = Opportunity(
        type=type,
        title=title,
        organizer=organizer,

        poster_id=poster_id,
        poster=poster,
        date_posted=today,
        last_modified=today,
        closing_date=closing_date,

        tags=list(),
        location_type=location_type,
        location=location,
        start_date=start_date,
        end_date=end_date,
        is_paid=is_paid,
        pay=pay,
        term=term_type,
        number_positions=number_positions,

        display_description=display_description,
        description=description,
        responsibilities=responsibilities,
        requirements=requirements,
        compensation=compensation,
        additional_info=additional_info,
        application_details=application_details,
        application_link=application_link,
    )

    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        create_opportunity_tag(name=tag, opportunity=new_post)

    db.session.commit()

    return json_response(201, "New Opportunity created successfully.", new_post)


def get_opportunity_posts(
        search_name: str = None,
        sort_method: str = None,
        type_filters: list[str] = [],
        term_filters: list[str] = [],
        location_filters: list[str] = [],
        pay_only: bool = False,
        tags: list[str] = [],
        tag_match_method: str = None):

    posts = db.session.query(Opportunity)

    queries = []
    if search_name:
        queries.append(Opportunity.title.icontains(search_name))

    if len(type_filters) > 0:
        type_queries = []
        for type in PostType:
            if type.value in type_filters:
                type_queries.append(Opportunity.type == type)
        queries.append(or_(*type_queries).self_group())

    if len(term_filters) > 0:
        type_queries = []
        for type in TermType:
            if type.value in term_filters:
                type_queries.append(Opportunity.term == type)
        queries.append(or_(*type_queries).self_group())

    if len(location_filters) > 0:
        type_queries = []
        for type in LocationType:
            if type.value in location_filters:
                type_queries.append(Opportunity.location_type == type)
        queries.append(or_(*type_queries).self_group())

    if pay_only:
        queries.append(Opportunity.is_paid == True)

    posts = posts.filter(and_(*queries))

    if len(tags) > 0:
        tag_queries = []
        for tag in tags:
            tag_queries.append(Opportunity.tags.any(name=tag))

        query = None
        if tag_match_method == "any":
            query = or_(*tag_queries)
        elif tag_match_method == "all":
            query = and_(*tag_queries)
        elif tag_match_method == "none":
            query = not_(or_(*tag_queries))
        else:
            query = or_(*tag_queries)

        if tag_match_method != "none":
            posts = posts.join(Opportunity.tags).filter(query)
        else:
            query2 = posts.filter(not_(Opportunity.tags.any()))
            posts = posts.join(Opportunity.tags).filter(query).union(query2)

    if sort_method:
        if sort_method == "recent":
            posts = posts.order_by(Opportunity.date_posted)
        elif sort_method == "alpha-asc":
            posts = posts.order_by(Opportunity.title)
        elif sort_method == "alpha-desc":
            posts = posts.order_by(Opportunity.title.desc())
        else:
            posts = posts.order_by(Opportunity.date_posted)

    posts = posts.all()

    if posts is None or len(posts) == 0:
        return json_response(404, "No opportunity posts found that match the given search criteria.", posts)

    return json_response(200, f"{len(posts)} opportunity posts have been retrieved.", posts)


def get_opportunity_by_organizer_and_title(organizer: str, title: str):
    opportunity = db.session.query(Opportunity).filter(
        and_(Opportunity.organizer == organizer, Opportunity.title == title)).first()

    if opportunity is None:
        return json_response(404, f"No opportunity post with organizer {organizer} and title {title} were found")

    return json_response(200, f"Opportunity post has been found.", opportunity)


def update_opportunity_post(
        id: int,
        type: PostType,
        title: str,
        organizer: str,
        closing_date: datetime,

        location_type: LocationType,
        location: str,
        start_date: datetime,
        is_paid: bool,

        display_description: str,
        description: str,
        requirements: str,
        compensation: str,
        application_details: str,

        tags: List[str] = list(),
        end_date: datetime = None,
        pay: str = None,
        term_type: TermType = None,
        number_positions: int = None,
        responsibilities: str = None,
        additional_info: str = None,
        application_link: str = None
):
    # Check if the post exists
    opportunity = db.session.query(Opportunity).filter_by(id=id).first()
    if opportunity is None:
        return json_response(404, f"This opportunity post doesn't exist.", id)

    # Check if a different post already uses this (title, organizer) pair
    matching_opportunity = db.session.query(Opportunity).filter(and_(
        func.lower(Opportunity.title) == func.lower(title),
        func.lower(Opportunity.organizer) == func.lower(organizer)
    )).first()
    if matching_opportunity is not None and matching_opportunity.id != opportunity.id:
        return json_response(409, f"Another opportunity post is already exists with this title and organization", matching_opportunity)

    opportunity.type = type
    opportunity.title = title
    opportunity.organizer = organizer
    opportunity.closing_date = closing_date

    opportunity.location_type = location_type
    opportunity.location = location
    opportunity.start_date = start_date
    opportunity.is_paid = is_paid

    opportunity.display_description = display_description
    opportunity.description = description
    opportunity.requirements = requirements
    opportunity.compensation = compensation
    opportunity.application_details = application_details

    if end_date is not None:
        opportunity.end_date = end_date
    if pay is not None:
        opportunity.pay = pay
    if term_type is not None:
        opportunity.term = term_type
    if number_positions is not None:
        opportunity.number_positions = number_positions
    if responsibilities is not None:
        opportunity.responsibilities = responsibilities
    if additional_info is not None:
        opportunity.additional_info = additional_info
    if application_link is not None:
        opportunity.application_link = application_link

    if tags is not None:
        opportunity.tags = list()
        for tag in tags:
            create_opportunity_tag(tag, opportunity, False)

    today: datetime = datetime.now()
    opportunity.last_modified = today

    db.session.add(opportunity)
    db.session.commit()

    return json_response(200, "Opportunity updated successfully.", opportunity)


def delete_opportunity_post(id: int):
    opportunity = db.session.query(Opportunity).filter_by(id=id).first()
    if opportunity is None:
        return json_response(404, f"Opportunity doesn't exist")

    db.session.delete(opportunity)
    db.session.commit()

    return json_response(200, f"Opportunity successfully deleted.")
