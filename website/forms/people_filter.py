from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField
from wtforms.validators import InputRequired
from ..models.user import OrgType, Roles

class OrganizationCheckbox(FlaskForm):
    individual = BooleanField(label="Individual", name="individual", render_kw={"class": "form-check-input"})
    group = BooleanField(label="Group", name="group", render_kw={"class": "form-check-input"})
    organization = BooleanField(label="Organization", name="organization", render_kw={"class": "form-check-input"})

class FiltersCheckbox(FlaskForm):
    choreographer = BooleanField(label="Choreographer", name="choreographer", render_kw={"class": "form-check-input"})
    designer = BooleanField(label="Designer", name="designer", render_kw={"class": "form-check-input"})
    writer = BooleanField(label="Writer", name="writer", render_kw={"class": "form-check-input"})
    producer = BooleanField(label="Producer", name="producer", render_kw={"class": "form-check-input"})
    stageManager = BooleanField(label="Stage Manager", name="stageManager", render_kw={"class": "form-check-input"})
    other = BooleanField(label="Other", name="other", render_kw={"class": "form-check-input"})

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
        name="submit",
        render_kw={"class": "btn btn-primary", "value": "Search"}
    )
    apply_filters = SubmitField(
        label="Apply Filters",
        name="submit",
        render_kw={"class": "btn btn-primary form-control mb-2", "value": "Apply Filters"}
    )
    clear_filters = SubmitField(
        label="Clear Filters",
        name="submit",
        render_kw={"class": "btn btn-secondary form-control", "value": "Clear Filters"}
    )


def fillOrganizationData(form: OrganizationCheckbox, tags: list[str]):
    if OrgType.Individual.name in tags:
        form.individual.data = True
    if OrgType.Group.name in tags:
        form.group.data = True
    if OrgType.Organization.name in tags:
        form.organization.data = True

def fillFilterData(form: FiltersCheckbox, tags: list[str]):
    if Roles.Choreographer.name in tags:
        form.choreographer.data = True
    if Roles.Designer.name in tags:
        form.designer.data = True
    if Roles.Writer.name in tags:
        form.writer.data = True
    if Roles.Producer.name in tags:
        form.producer.data = True
    if Roles.StageManager.name in tags:
        form.stageManager.data = True
    if Roles.Other.name in tags:
        form.other.data = True