from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField
from wtforms.validators import InputRequired

class OrganizationCheckbox(FlaskForm):
    individual = BooleanField(label="Individual", name="individual", render_kw={"class": ""})
    group = BooleanField(label="Group", name="group", render_kw={"class": ""})
    organization = BooleanField(label="Organization", name="organization", render_kw={"class": ""})

class FiltersCheckbox(FlaskForm):
    choreographer = BooleanField(label="Individual", name="Search", render_kw={"class": ""})
    designer = BooleanField(label="Designer", name="designer", render_kw={"class": ""})
    writer = BooleanField(label="Writer", name="writer", render_kw={"class": ""})
    producer = BooleanField(label="Producer", name="producer", render_kw={"class": ""})
    stageManager = BooleanField(label="Stage Manager", name="stage-manager", render_kw={"class": ""})
    other = BooleanField(label="Other", name="other", render_kw={"class": ""})

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
        choices=[('alpha-desc', 'Name (A-Z)'), ('alpha-asc', 'Name (Z-A)')],
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