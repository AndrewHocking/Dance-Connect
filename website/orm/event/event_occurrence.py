from ...models.event.event_occurrence import EventOccurrence
from ... import db, json_response
from ...models.event import Event
from datetime import datetime

def create_event_occurrence(
    event: Event,
    start_time: datetime,
    end_time: datetime,
    is_relaxed_performance: bool,
    has_asl_interpreter: bool,
    commit_db_after_creation: bool = True
):
    new_occurrence = EventOccurrence(
        event_id = event.id,
        event = event,
        start_time = start_time,
        end_time = end_time,
        is_relaxed_performance = is_relaxed_performance,
        has_asl_interpreter = has_asl_interpreter
    )

    db.session.add(new_occurrence)
    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event occurrence created successfully.", new_occurrence)

def read_event_occurrence():
    #TODO: Add filters
    event_occurrences = db.session.query(EventOccurrence).all()
    return json_response(200, f"{len(event_occurrences)} event occurrences found.", event_occurrences)
