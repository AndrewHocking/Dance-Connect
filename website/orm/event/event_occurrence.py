from ...models.event.event_occurrence import EventOccurrence
from ... import db, json_response
from ...models.event import Event
from datetime import datetime, timedelta


def create_event_occurrence(
    event: Event,
    start_time: datetime,
    end_time: datetime,
    is_relaxed_performance: bool,
    is_photosensitivity_friendly: bool,
    is_hearing_accessible: bool,
    is_visually_accessible: bool,
    commit_db_after_creation: bool = True
):
    while end_time and end_time < start_time:
        end_time = end_time + timedelta(days=1)

    new_occurrence = EventOccurrence(
        event_id=event.id,
        event=event,
        start_time=start_time,
        end_time=end_time,
        is_relaxed_performance=is_relaxed_performance,
        is_photosensitivity_friendly=is_photosensitivity_friendly,
        is_hearing_accessible=is_hearing_accessible,
        is_visually_accessible=is_visually_accessible
    )

    db.session.add(new_occurrence)
    if commit_db_after_creation:
        db.session.commit()

    return json_response(201, "Event occurrence created successfully.", new_occurrence)


def delete_event_occurrence(event_occurrence: EventOccurrence, commit_db_after_deletion: bool = True):
    db.session.delete(event_occurrence)
    if commit_db_after_deletion:
        db.session.commit()

    return json_response(200, "Event occurrence deleted successfully.")
