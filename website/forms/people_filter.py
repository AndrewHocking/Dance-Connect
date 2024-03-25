import enum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField, TextAreaField
from ..models.user import UserType


class Roles(enum.Enum):
    CHOREOGRAPHER: str = "Choreographer"
    DESIGNER: str = "Designer"
    WRITER: str = "Writer"
    PRODUCER: str = "Producer"
    STAGE_MANAGER: str = "Stage Manager"
    OTHER: str = "Other"


class OrganizationCheckbox(FlaskForm):
    pass


for type in UserType:
    setattr(
        OrganizationCheckbox,
        type.name,
        BooleanField(label=type.value, name=type.value,
                     render_kw={"class": "form-check-input"})
    )


class FiltersCheckbox(FlaskForm):
    pass


for role in Roles:
    setattr(
        FiltersCheckbox,
        role.name,
        BooleanField(label=role.value, name=role.value,
                     render_kw={"class": "form-check-input"})
    )


class PeopleFilter(FlaskForm):
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
        choices=[('alpha-asc', 'Name (A-Z)'), ('alpha-desc', 'Name (Z-A)')],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    user_type = FormField(OrganizationCheckbox, description="User Type")
    filters = FormField(FiltersCheckbox, description="Role/Profession")
    other_tags = TextAreaField(
        label="Role Tags",
        name="other_tags",
        description="Separate tags by commas.",
        render_kw={"placeholder": "e.g. set manager, costume designer",
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


def fill_organization_data(form: OrganizationCheckbox, tags: list[str]):
    for type in UserType:
        if type.value in tags:
            form[type.name].data = True


def fill_filter_data(form: FiltersCheckbox, tags: list[str]):
    for role in Roles:
        if role.value in tags:
            form[role.name].data = True
