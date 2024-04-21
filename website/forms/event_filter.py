from datetime import datetime
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
        choices=[('upcoming', "Upcoming"), ('alpha-asc',
                                            'Title (A-Z)'), ('alpha-desc', 'Title (Z-A)')],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    venue_is_mobility_aid_accessible = BooleanField(
        label="Accessible Venue",
        validators=[],
        name="venue_is_mobility_aid_accessible",
        render_kw={"placeholder": "", "class": "form-check-input"}
    )
    is_relaxed_performance = BooleanField(
        label="Relaxed Performance",
        validators=[],
        name="is_relaxed_performance",
        render_kw={"placeholder": "", "class": "form-check-input"}
    )
    is_photosensitivity_friendly = BooleanField(
        label="Photosensitivity Friendly",
        validators=[],
        name="is_photosensitivity_friendly",
        render_kw={"placeholder": "", "class": "form-check-input"}
    )
    is_hearing_accessible = BooleanField(
        label="Hearing Accessible",
        validators=[],
        name="is_hearing_accessible",
        render_kw={"placeholder": "", "class": "form-check-input"}
    )
    is_visually_accessible = BooleanField(
        label="Visually Accessible",
        validators=[],
        name="is_visually_accessible",
        render_kw={"placeholder": "", "class": "form-check-input"}
    )
    min_ticket_price = DecimalField(
        label="Minimum Ticket Price",
        validators=[NumberRange(min=0)],
        name="min_ticket_price",
        render_kw={"class": "form-control",
                   "aria-describedby": "min-ticket-price-help-block"}
    )
    max_ticket_price = DecimalField(
        label="Maximum Ticket Price",
        validators=[NumberRange(min=0)],
        name="max_ticket_price",
        render_kw={"class": "form-control",
                   "aria-describedby": "max-ticket-price-help-block"}
    )
    start_date = DateField(
        label="Start Date",
        name="start_date",
        default=datetime.now(),
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
        render_kw={"placeholder": "e.g. ballet, hip hop, contemporary",
                   "class": "form-control", "aria-describedby": "tags-help-block"}
    )
    match_all_tags = RadioField(
        label="Match all tags",
        name="match_all_tags",
        choices=[('False', "Match any of the following tags"),
                 ('True', 'Match all of the following tags')],
        default='False'
    )
    clear_filters = SubmitField(
        label="Clear filters",
        name="clear_filters",
        render_kw={"class": "btn btn-secondary"}
    )
