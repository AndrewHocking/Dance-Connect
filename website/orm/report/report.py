from sqlalchemy import func, and_, or_, not_

from ... import db, json_response
from ...models.report import BugReport, UserReport, OpportunityReport, EventReport
from ...models.user import User
from ...models.event import Event
from ...models.opportunity import Opportunity


def add_bug_report(title: str, description: str):
    report = BugReport(
        title=title,
        description=description
    )

    db.session.add(report)
    db.session.commit()

    return json_response(201, "Successfully submitted new bug report.", report)


def add_user_report(reason: str, details: str, reporter_id: int, reported_user_id: int):
    reporter: User = db.session.query(User).filter_by(id=reporter_id).first()
    if reporter is None:
        return json_response(404, "Reporting user was not found")

    reported: User = db.session.query(
        User).filter_by(id=reported_user_id).first()
    if reported is None:
        return json_response(404, "Reported user was not found")

    report = UserReport(
        reason=reason,
        details=details,
        reporter_id=reporter.id,
        reporter=reporter,
        reported_user_id=reported.id,
        reported_user=reported,
    )

    db.session.add(report)
    db.session.commit()

    return json_response(201, "Successfully submitted new user report.", report)


def add_event_report(reason: str, details: str, reporter_id: int, reported_event_id: int):
    reporter: User = db.session.query(User).filter_by(id=reporter_id).first()
    if reporter is None:
        return json_response(404, "Reporting user was not found")

    event: Event = db.session.query(Event).filter_by(
        id=reported_event_id).first()
    if event is None:
        return json_response(404, "Reported event was not found")

    report = EventReport(
        reason=reason,
        details=details,
        reporter_id=reporter.id,
        reporter=reporter,
        reported_event_id=event.id,
        reported_event=event,
    )

    db.session.add(report)
    db.session.commit()

    return json_response(201, "Successfully submitted new event report.", report)


def add_opportunity_report(reason: str, details: str, reporter_id: int, reported_opportunity_id: int):
    reporter: User = db.session.query(User).filter_by(id=reporter_id).first()
    if reporter is None:
        return json_response(404, "Reporting user was not found")

    opportunity: Opportunity = db.session.query(
        Opportunity).filter_by(id=reported_opportunity_id).first()
    if opportunity is None:
        return json_response(404, "Reported opportunity was not found")

    report = OpportunityReport(
        reason=reason,
        details=details,
        reporter_id=reporter.id,
        reporter=reporter,
        reported_opportunity_id=opportunity.id,
        reported_opportunity=opportunity,
    )

    db.session.add(report)
    db.session.commit()

    return json_response(201, "Successfully submitted new opportunity report.", report)


# Did user X report user Y?
def did_user_report_user(reporter_id: int, reported_user_id: int):
    report = db.session.query(UserReport).filter_by(
        reporter_id=reporter_id, reported_user_id=reported_user_id).first()

    return json_response(200, f"User report has {"not" if report is None else ""} been found", report)


# Did user X report event Y?
def did_user_report_event(reporter_id: int, reported_event_id: int):
    report = db.session.query(EventReport).filter_by(
        reporter_id=reporter_id, reported_event_id=reported_event_id).first()

    return json_response(200, f"Event report has {"not" if report is None else ""} been found", report)


# Did user X report opportunity Y?
def did_user_report_opportunity(reporter_id: int, reported_opportunity_id: int):
    report = db.session.query(OpportunityReport).filter_by(
        reporter_id=reporter_id, reported_opportunity_id=reported_opportunity_id).first()

    return json_response(200, f"Opportunity report has {"not" if report is None else ""} been found", report)


def remove_user_report(reporter_id: int, reported_user_id: int):
    report = db.session.query(UserReport).filter_by(
        reporter_id=reporter_id, reported_user_id=reported_user_id).first()
    if report is None:
        return json_response(404, "No such user report was found.")

    db.session.delete(report)
    db.session.commit()

    return json_response(200, f"User report has been succesfully canceled.")


def remove_event_report(reporter_id: int, reported_event_id: int):
    report = db.session.query(EventReport).filter_by(
        reporter_id=reporter_id, reported_event_id=reported_event_id).first()
    if report is None:
        return json_response(404, "No such event report was found.")

    db.session.delete(report)
    db.session.commit()

    return json_response(200, f"Event report has been succesfully canceled.")


def remove_opportunity_report(reporter_id: int, reported_opportunity_id: int):
    report = db.session.query(OpportunityReport).filter_by(
        reporter_id=reporter_id, reported_opportunity_id=reported_opportunity_id).first()
    if report is None:
        return json_response(404, "No such opportunity report was found.")

    db.session.delete(report)
    db.session.commit()

    return json_response(200, f"Opportunity report has been succesfully canceled.")
