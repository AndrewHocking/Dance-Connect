from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length


class BugReportForm(FlaskForm):
    title = StringField(
        label="Issue Name",
        validators=[InputRequired()],
        name="title",
        render_kw={"placeholder": "Home Page doesn't load.",
                   "class": "form-control"}
    )
    description = TextAreaField(
        label="Description",
        validators=[InputRequired()],
        name="description",
        description="Describe the issue and what actions caused it.",
        render_kw={"placeholder": "Tried visiting the homepage, mid-way through posting a new event.",
                   "data-bs-dismiss": "modal", "class": "form-control", "aria-describedby": "description-help-block"}
    )
    cancel = SubmitField(
        label="Cancel",
        name="cancel",
        render_kw={"class": "btn btn-secondary"}
    )
    submit = SubmitField(
        label="Submit",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )
