from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, BooleanField, SubmitField, DecimalField, TextAreaField, URLField, RadioField, DateField, TimeField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateEventOccurrenceForm(FlaskForm):
    date = DateField(
        label="Date ✽",
        name="date",
        render_kw={"class": "form-control date"}
    )
    start_time = TimeField(
        label="Start Time ✽",
        name="start_time",
        render_kw={"class": "form-control time"}
    )
    end_time = TimeField(
        label="End Time",
        name="end_time",
        render_kw={"class": "form-control time"}
    )
    is_relaxed_performance = BooleanField(
        label="This is a \"relaxed performance\"",
        name="is_relaxed_performance"
    )
    has_asl_interpreter = BooleanField(
        label="An ASL (American Sign Language) interpreter will be present.",
        name="has_asl_interpreter"
    )


class CreateEventForm(FlaskForm):
    title = StringField(
        label="Event Title ✽",
        validators=[DataRequired(), Length(
            min=1, max=100, message="Must be between 1 and 100 characters.")],
        name="title",
        render_kw={"placeholder": "e.g. The Nutcracker",
                   "class": "form-control"}
    )
    description = TextAreaField(
        label="Event Description ✽",
        validators=[DataRequired(), Length(
            max=10000, message="Maximum 10,000 characters.")],
        name="description",
        render_kw={"placeholder": "e.g. The classic ballet portraying a young girl's magical journey through a wondrous land filled with enchanting characters and holiday joy.", "class": "form-control"}
    )
    url = URLField(
        label="URL",
        name="url",
        render_kw={
            "placeholder": "e.g. https://www.yourlovelydancecompany.com/the-nutcracker/", "class": "form-control"}
    )
    tags = TextAreaField(
        label="Tags",
        name="tags",
        description="Separate tags by commas.",
        render_kw={"placeholder": "e.g. ballet, classic, holidays",
                   "class": "form-control", "aria-describedby": "tags-help-block"}
    )
    venue_name = StringField(
        label="Venue Name",
        name="venue_name",
        render_kw={
            "placeholder": "e.g. Clara Stahlbaum Centre for the Performing Arts", "class": "form-control"}
    )
    venue_address = StringField(
        label="Venue Address",
        name="venue_address",
        render_kw={
            "placeholder": "e.g. 4141 Sugarplum Dr., Toronto, M4Y 2E5", "class": "form-control"}
    )
    venue_is_wheelchair_accessible = RadioField(
        label="Venue Accessibility ✽",
        validators=[DataRequired()],
        name="venue_is_wheelchair_accessible",
        choices=[('False', 'This venue is NOT fully accessible to users of wheelchairs and other mobility devices.'),
                 ('True', 'This venue is fully accessible to users of wheelchairs and other mobility devices.')],
        default="False"
    )
    show_is_photosensitivity_friendly = RadioField(
        label="Photosensitivity ✽",
        validators=[DataRequired()],
        name="show_is_photosensitivity_friendly",
        choices=[('False', 'Some lighting effects used during this event may be unsafe for those who experience photosensitivity.'),
                 ('True', 'No lighting effects used during this event may be unsafe for those who experience photosensitivity.')],
        default="False"
    )
    accessibility_notes = TextAreaField(
        label="Accessibility Notes",
        name="accessibility_notes",
        render_kw={"placeholder": "e.g. The main entrance on the east side of the building is not accessible for all mobility aids, however there is an accessible entrance on the south side of the building.", "class": "form-control"}
    )
    min_ticket_price = DecimalField(
        label="Minimum Ticket Price",
        validators=[NumberRange(min=0)],
        name="min_ticket_price",
        description="Leave this blank to not display the minimum ticket price.",
        render_kw={"placeholder": "e.g. 0.00", "class": "form-control",
                   "aria-describedby": "min-ticket-price-help-block"}
    )
    max_ticket_price = DecimalField(
        label="Maximum Ticket Price",
        validators=[NumberRange(min=0)],
        name="max_ticket_price",
        description="Leave this blank to not display the maximum ticket price.",
        render_kw={"placeholder": "e.g. 149.99", "class": "form-control",
                   "aria-describedby": "max-ticket-price-help-block"}
    )
    num_occurrences = HiddenField(
        name="num_occurrences",
        default="1"
    )
    occurrences = FieldList(
        FormField(CreateEventOccurrenceForm), min_entries=50)
    submit = SubmitField(
        label="Submit",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )
