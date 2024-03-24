from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, SelectField, BooleanField, DecimalField, DateField, TextAreaField
from wtforms.validators import NumberRange


class EventFilterForm(FlaskForm):
    search = StringField(
        label="Search",
        name="search",
        render_kw={"placeholder": "Search", "class": "form-control"}
    )
    search_button = SubmitField(
        label="Search",
        name="search_button",
        render_kw={"class": "btn btn-primary"}
    )
    sort = SelectField(
        label="Sort",
        validators=[],
        name="sort",
        choices=[('upcoming', "Upcoming"), ('alpha-asc', 'Title (A-Z)'), ('alpha-desc', 'Title (Z-A)')],
        render_kw={"placeholder": "", "class" : "form-select"}
    )
    accessible_venue = BooleanField(
        label="Accessible Venue",
        validators=[],
        name="accessible_venue",
        render_kw={"placeholder": "", "class" : "form-check-input"}
    )
    asl_interpreter = BooleanField(
        label="ASL Interpreter",
        validators=[],
        name="asl_interpreter",
        render_kw={"placeholder": "", "class" : "form-check-input"}
    )
    relaxed_performance = BooleanField(
        label="Relaxed Performance",
        validators=[],
        name="relaxed_performance",
        render_kw={"placeholder": "", "class" : "form-check-input"}
    )
    min_ticket_price = DecimalField(
        label="Minimum Ticket Price",
        validators=[NumberRange(min=0)],
        name="min_ticket_price",
        render_kw={"class" : "form-control", "aria-describedby" : "min-ticket-price-help-block"}
    )
    max_ticket_price = DecimalField(
        label="Maximum Ticket Price",
        validators=[NumberRange(min=0)],
        name="max_ticket_price",
        render_kw={"class" : "form-control", "aria-describedby" : "max-ticket-price-help-block"}
    )
    start_date = DateField(
        label="Start Date",
        name="start_date",
        render_kw={"class": "form-control"}
    )
    end_date = DateField(
        label="End Date",
        name="end_date",
        render_kw={"class": "form-control"}
    )
    
    apply_filters = SubmitField(
        label="Apply filters",
        name="apply_filters",
        render_kw={"class": "btn btn-primary"}
    )
    tags = TextAreaField(
        label="Tags",
        name="tags",
        description="Separate tags by commas.",
        render_kw={"placeholder": "e.g. ballet, hip hop, contemporary", "class" : "form-control", "aria-describedby" : "tags-help-block"}
    )
    match_all_tags = RadioField(
        label="Match all tags",
        name="match_all_tags",
        choices=[('False', "Match any of the following tags"), ('True', 'Match all of the following tags')],
        default='False'
    )
    clear_filters = SubmitField(
        label="Clear filters",
        name="clear_filters",
        render_kw={"class": "btn btn-secondary"}
    )