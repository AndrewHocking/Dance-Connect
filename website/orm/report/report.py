from sqlalchemy import func, and_, or_, not_

from ... import db, json_response
from ...models.report import BugReport


def add_bug_report(title: str, description: str):
    report = BugReport(
        title=title,
        description=description
    )

    db.session.add(report)
    db.session.commit()

    return json_response(201, "Successfully submitted new bug report.", report)
