from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField
from wtforms.validators import InputRequired
from ..models.user import ORG_TYPES, ROLES

class OrganizationCheckbox(FlaskForm):
    individual = BooleanField(label=ORG_TYPES.INDIVIDUAL, name=ORG_TYPES.INDIVIDUAL, render_kw={"class": ""})
    group = BooleanField(label=ORG_TYPES.GROUP, name=ORG_TYPES.GROUP, render_kw={"class": ""})
    organization = BooleanField(label=ORG_TYPES.ORGANIZATION, name=ORG_TYPES.ORGANIZATION, render_kw={"class": ""})

class FiltersCheckbox(FlaskForm):
    choreographer = BooleanField(label=ROLES.CHOREOGRAPHER, name=ROLES.CHOREOGRAPHER, render_kw={"class": ""})
    designer = BooleanField(label=ROLES.DESIGNER, name=ROLES.DESIGNER, render_kw={"class": ""})
    writer = BooleanField(label=ROLES.WRITER, name=ROLES.WRITER, render_kw={"class": ""})
    producer = BooleanField(label=ROLES.PRODUCER, name=ROLES.PRODUCER, render_kw={"class": ""})
    stageManager = BooleanField(label=ROLES.STAGEMANAGER, name=ROLES.STAGEMANAGER, render_kw={"class": ""})
    other = BooleanField(label=ROLES.OTHER, name=ROLES.OTHER, render_kw={"class": ""})

class PeopleFilter(FlaskForm):
    searchName = StringField(
        label="Search",
        validators=[],
        name="search",
        render_kw={"placeholder": "Artist Name", "class" : "form-control"}
    )
    sortOption = SelectField(
        label="Sort",
        validators=[],
        name="sort",
        choices=[('alpha-asc', 'Name (A-Z)'), ('alpha-desc', 'Name (Z-A)')],
        render_kw={"placeholder": "", "class" : "form-control"}
    )
    organizationType = FormField(OrganizationCheckbox, description="Organization Type")
    filters = FormField(FiltersCheckbox, description="Role/Profession")
    searchSubmit = SubmitField(
        label="Search",
        name="submit",
        render_kw={"class": "btn btn-primary", "value": "Search"}
    )
    applyFilterSubmit = SubmitField(
        label="Apply Filters",
        name="submit",
        render_kw={"class": "btn btn-primary form-control mb-2", "value": "Apply Filters"}
    )
    clearFilterSubmit = SubmitField(
        label="Clear Filters",
        name="submit",
        render_kw={"class": "btn btn-secondary form-control", "value": "Clear Filters"}
    )


def fillOrganizationData(form: OrganizationCheckbox, tags: list[str]):
    if ORG_TYPES.INDIVIDUAL in tags:
        form.individual.data = True
    if ORG_TYPES.GROUP in tags:
        form.group.data = True
    if ORG_TYPES.ORGANIZATION in tags:
        form.organization.data = True

def fillFilterData(form: FiltersCheckbox, tags: list[str]):
    if ROLES.CHOREOGRAPHER in tags:
        form.choreographer.data = True
    if ROLES.DESIGNER in tags:
        form.designer.data = True
    if ROLES.WRITER in tags:
        form.writer.data = True
    if ROLES.PRODUCER in tags:
        form.producer.data = True
    if ROLES.STAGEMANAGER in tags:
        form.stageManager.data = True
    if ROLES.OTHER in tags:
        form.other.data = True