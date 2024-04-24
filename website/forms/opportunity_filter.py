import enum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField, TextAreaField
from ..models.opportunity import TermType, PostType, LocationType


class LocationCheckbox(FlaskForm):
    pass


for type in LocationType:
    setattr(
        LocationCheckbox,
        type.name,
        BooleanField(label=type.value, name=type.value,
                     render_kw={"class": "form-check-input"})
    )


class TypeCheckbox(FlaskForm):
    pass


for type in PostType:
    setattr(
        TypeCheckbox,
        type.name,
        BooleanField(label=type.value, name=type.value,
                     render_kw={"class": "form-check-input"})
    )


class CompensationCheckbox(FlaskForm):
    is_paid = BooleanField(label="Paid", name="Paid", render_kw={
                           "class": "form-check-input"})


class TermCheckbox(FlaskForm):
    pass


for type in TermType:
    setattr(
        TermCheckbox,
        type.name,
        BooleanField(label=type.value, name=type.value,
                     render_kw={"class": "form-check-input"})
    )


class OpportunityFilter(FlaskForm):
    search = StringField(
        label="Search",
        validators=[],
        name="search",
        render_kw={"placeholder": "Search", "class": "form-control"}
    )
    sort_option = SelectField(
        label="Sort",
        validators=[],
        name="sort",
        choices=[('recent', 'Date Posted (Latest)'), ('alpha-asc',
                                                      'Title (A-Z)'), ('alpha-desc', 'Title (Z-A)')],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    opportunity_type = FormField(TypeCheckbox, description="Type")
    compensation_type = FormField(
        CompensationCheckbox, description="Compensation")
    term_type = FormField(TermCheckbox, description="Term")
    location_type = FormField(LocationCheckbox, description="Location")
    match_all_tags = SelectField(
        label="Match all tags",
        name="match_all_tags",
        choices=[('any', "any"),
                 ('all', 'all'),
                 ('none', 'none')],
        default='any',
        render_kw={"placeholder": "",
                   "class": "form-select form-select-sm m-0"}
    )
    tags = TextAreaField(
        label="Tags",
        name="tags",
        description="Separate tags by commas.",
        render_kw={"placeholder": "e.g. ballet, hip hop, contemporary",
                   "class": "form-control", "aria-describedby": "tags-help-block"}
    )
    search_button = SubmitField(
        label="Search",
        name="search_button",
        render_kw={"class": "btn btn-primary", "value": "Search"}
    )
    apply_filters = SubmitField(
        label="Apply Filters",
        name="apply_filters",
        render_kw={"class": "btn btn-primary form-control mb-2",
                   "value": "Apply Filters"}
    )
    clear_filters = SubmitField(
        label="Clear filters",
        name="clear_filters",
        render_kw={"class": "btn btn-secondary form-control",
                   "value": "Clear Filters"}
    )


def fill_post_type_data(form: TypeCheckbox, filters: list[str]):
    for type in PostType:
        if type.value in filters:
            form[type.name].data = True


def fill_location_type_data(form: LocationCheckbox, filters: list[str]):
    for location in LocationType:
        if location.value in filters:
            form[location.name].data = True


def fill_term_type_data(form: TermCheckbox, filters: list[str]):
    for term in TermType:
        if term.value in filters:
            form[term.name].data = True


def fill_compensation_type_data(form: CompensationCheckbox, is_paid: bool):
    if is_paid:
        form.is_paid.data = True
