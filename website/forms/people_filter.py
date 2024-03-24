from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField
from wtforms.validators import InputRequired
from ..models.user import OrgType, Roles

class OrganizationCheckbox(FlaskForm):
    individual = BooleanField(label=OrgType.Individual.name, name=OrgType.Individual.name, render_kw={"class": ""})
    group = BooleanField(label=OrgType.Group.name, name=OrgType.Group.name, render_kw={"class": ""})
    organization = BooleanField(label=OrgType.Organization.name, name=OrgType.Organization.name, render_kw={"class": ""})

class FiltersCheckbox(FlaskForm):
    choreographer = BooleanField(label=Roles.Choreographer.name, name=Roles.Choreographer.name, render_kw={"class": ""})
    designer = BooleanField(label=Roles.Designer.name, name=Roles.Designer.name, render_kw={"class": ""})
    writer = BooleanField(label=Roles.Writer.name, name=Roles.Writer.name, render_kw={"class": ""})
    producer = BooleanField(label=Roles.Producer.name, name=Roles.Producer.name, render_kw={"class": ""})
    stageManager = BooleanField(label=Roles.StageManager.name, name=Roles.StageManager.name, render_kw={"class": ""})
    other = BooleanField(label=Roles.Other.name, name=Roles.Other.name, render_kw={"class": ""})

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