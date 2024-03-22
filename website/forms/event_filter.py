from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DecimalField, DateField
from wtforms.validators import DataRequired, Length, NumberRange


class EventFilterForm(FlaskForm):
    sort = SelectField(
        label="Sort",
        validators=[],
        name="sort",
        choices=[('alpha-asc', 'Name (A-Z)'), ('alpha-desc', 'Name (Z-A)')],
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
        description="Leave this blank to not display the minimum ticket price.",
        render_kw={"class" : "form-control", "aria-describedby" : "min-ticket-price-help-block"}
    )
    max_ticket_price = DecimalField(
        label="Maximum Ticket Price",
        validators=[NumberRange(min=0)],
        name="max_ticket_price",
        description="Leave this blank to not display the maximum ticket price.",
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
    clear_filters = SubmitField(
        label="Clear filters",
        name="clear_filters",
        render_kw={"class": "btn btn-secondary"}
    )