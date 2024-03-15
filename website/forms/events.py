from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DecimalField, TextAreaField, URLField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange

class CreateEventForm(FlaskForm):
    title = StringField(
        "Event Title",
        validators=[DataRequired(), Length(min=1, max=100, message="Must be between 1 and 100 characters.")],
        name="title",
        render_kw={"placeholder": "e.g. The Nutcracker", "class" : "form-control"}
    )
    description = TextAreaField(
        "Event Description",
        validators=[DataRequired(), Length(max=10000, message="Maximum 10,000 characters.")],
        name="description",
        render_kw={"placeholder": "e.g. The classic ballet portraying a young girl's magical journey through a wondrous land filled with enchanting characters and holiday joy.", "class" : "form-control"}
    )
    url = URLField(
        "Event URL",
        name="url",
        render_kw={"placeholder": "e.g. https://www.yourlovelydancecompany.com/the-nutcracker/", "class" : "form-control"}
    )
    tags = TextAreaField(
        "Tags",
        name="tags",
        description="Separate tags by commas.",
        render_kw={"placeholder": "e.g. ballet, classic, holidays", "class" : "form-control", "aria-describedby" : "tags-help-block"}
    )
    venue_name = StringField(
        "Venue Name",
        name="venue_name",
        render_kw={"placeholder": "e.g. Clara Stahlbaum Centre for the Performing Arts", "class" : "form-control"}
    )
    venue_address = StringField(
        "Venue Address",
        name="venue_address",
        render_kw={"placeholder": "e.g. 4141 Sugarplum Dr., Toronto, M4Y 2E5", "class" : "form-control"}
    )
    venue_is_wheelchair_accessible = RadioField(
        "Venue Accessibility",
        name="venue_is_wheelchair_accessible",
        choices = [('False', 'This venue is NOT fully accessible to users of wheelchairs and other mobility devices.'), ('True', 'This venue is fully accessible to users of wheelchairs and other mobility devices.')],
    )
    accessibility_notes = TextAreaField(
        "Accessibility Notes",
        name="accessibility_notes",
        render_kw={"placeholder": "e.g. The main entrance on the east side of the building is not accessible, however there is an accessible entrance on the south side of the building. The inside of the building is fully accessible.", "class" : "form-control"}
    )
    min_ticket_price = DecimalField(
        "Minimum Ticket Price",
        validators=[NumberRange(min=0)],
        name="min_ticket_price",
        description="Leave this blank to not include display the minimum ticket price.",
        render_kw={"placeholder": "e.g. 0.00", "class" : "form-control", "aria-describedby" : "min-ticket-price-help-block"}
    )
    max_ticket_price = DecimalField(
        "Maximum Ticket Price",
        validators=[NumberRange(min=0)],
        name="max_ticket_price",
        description="Leave this blank to not include display the maximum ticket price.",
        render_kw={"placeholder": "e.g. 149.99", "class" : "form-control", "aria-describedby" : "max-ticket-price-help-block"}
    )
    submit = SubmitField(
        label="Submit",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )
