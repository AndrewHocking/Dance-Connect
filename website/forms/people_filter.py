from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField
from wtforms.validators import InputRequired
from ..models.user import OrgType, Roles

class OrganizationCheckbox(FlaskForm):
    pass

for type in OrgType:
    setattr(
        OrganizationCheckbox, 
        type.name.lower(),
        BooleanField(label=type.name, name=type.name, render_kw={"class": "form-check-input"})
    )

class FiltersCheckbox(FlaskForm):
    pass

for role in Roles:
    setattr(
        FiltersCheckbox,
        role.name.lower(),
        BooleanField(label=role.value, name=role.name, render_kw={"class": "form-check-input"})
    )

class PeopleFilter(FlaskForm):
    search = StringField(
        label="Search",
        validators=[],
        name="search",
        render_kw={"placeholder": "Search", "class" : "form-control"}
    )
    sortOption = SelectField(
        label="Sort",
        validators=[],
        name="sort",
        choices=[('alpha-asc', 'Name (A-Z)'), ('alpha-desc', 'Name (Z-A)')],
        render_kw={"placeholder": "", "class" : "form-select"}
    )
    organizationType = FormField(OrganizationCheckbox, description="Organization Type")
    filters = FormField(FiltersCheckbox, description="Role/Profession")
    search_button = SubmitField(
        label="Search",
        name="search_button",
        render_kw={"class": "btn btn-primary", "value": "Search"}
    )
    apply_filters = SubmitField(
        label="Apply Filters",
        name="apply_filters",
        render_kw={"class": "btn btn-primary form-control mb-2", "value": "Apply Filters"}
    )
    clear_filters = SubmitField(
        label="Clear filters",
        name="clear_filters",
        render_kw={"class": "btn btn-secondary form-control", "value": "Clear Filters"}
    )


def fillOrganizationData(form: OrganizationCheckbox, tags: list[str]):
    for type in OrgType:
        if type.name in tags:
            form[type.name.lower()].data = True

def fillFilterData(form: FiltersCheckbox, tags: list[str]):
    for role in Roles:
        if role.name in tags:
            form[role.name.lower()].data = True