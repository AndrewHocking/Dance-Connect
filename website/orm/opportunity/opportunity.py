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

    today: datetime = datetime.now(timezone.utc)
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
