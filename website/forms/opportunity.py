import enum
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField, TextAreaField, URLField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, URL, ValidationError, NumberRange
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


def validate_duration(form, field):
    print('Validate Duration')
    if form.duration_type.data == 'definite' and field.data == None:
        raise ValidationError('Must specify end date if duration is bounded.')

    raise ValidationError(
        'Must specify pay estimate if pay/benefits are offered.')


def validate_pay(form, field):
    print('Validate Pay')
    if form.is_paid.data == True and field.data == None:
        raise ValidationError(
            'Must specify pay estimate if pay/benefits are offered.')

    raise ValidationError(
        'Must specify pay estimate if pay/benefits are offered.')


class CreateOpportunityForm(FlaskForm):
    type = SelectField(
        label="Opportunity Type",
        validators=[],
        name="type",
        default=PostType.AUDITION.name,
        choices=[(e.name, e.value) for e in PostType],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    title = StringField(
        label="Post Title",
        validators=[DataRequired(), Length(
            min=1, max=100, message="Title must be between 1 and 100 characters.")],
        name="title",
        render_kw={"placeholder": "Title of the Post", "class": "form-control"}
    )
    organizer = StringField(
        label="Organization",
        validators=[DataRequired(), Length(
            min=1, max=100, message="Organization must be between 1 and 100 characters.")],
        name="organizer",
        render_kw={"placeholder": "Associated Organization",
                   "class": "form-control"}
    )

    close_date = DateField(
        label="Application Deadline",
        name="deadline",
        render_kw={"class": "form-control date"},
        validators=[DataRequired()]
    )

    tags = TextAreaField(
        label="Tags",
        name="tags",
        description="Separate tags by commas.",
        render_kw={"placeholder": "e.g. ballet, hip hop, contemporary",
                   "class": "form-control", "aria-describedby": "tags-help-block"}
    )
    location_type = SelectField(
        label="Location Type",
        validators=[DataRequired()],
        name="location_type",
        default=LocationType.IN_PERSON.name,
        choices=[(e.name, e.value) for e in LocationType],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    location = StringField(
        label="Location",
        validators=[DataRequired(), Length(
            min=1, max=100, message="Location must be between 1 and 100 characters.")],
        name="location",
        render_kw={"placeholder": "Location of the Opportunity",
                   "class": "form-control"}
    )
    duration_type = SelectField(
        label="Duration",
        validators=[DataRequired()],
        name="duration",
        default='definite',
        choices=[('finite', 'Fixed Length'), ('indefinite', 'Unbound')],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    start_date = DateField(
        label="Start Date",
        name="start_date",
        render_kw={"class": "form-control date"},
        validators=[DataRequired()]
    )
    end_date = DateField(
        label="End Date",
        name="end_date",
        render_kw={"class": "form-control date"},
        validators=[validate_duration]
    )
    is_paid = BooleanField(
        label="Will Pay/Benefits Be Offered?",
        name="is_paid",
        render_kw={"class": "form-check-input"}
    )
    pay = StringField(
        label="Pay Estimate",
        validators=[validate_pay, Length(
            min=1, max=100, message="Pay Estimate must be between 1 and 100 characters.")],
        name="pay",
        render_kw={"placeholder": "e.g. $5,500, $32/hr",
                   "class": "form-control"}
    )

    def validate_duration_type(form, field):
        print('Validate Pay')
        if form.duration_type.data == 'definite' and field.data == None:
            raise ValidationError(
                'Must specify end date if duration is bounded.')

        raise ValidationError(
            'Must specify pay estimate if pay/benefits are offered.')

    term = SelectField(
        label="Term",
        validators=[],
        name="term",
        default='',
        choices=[(None, 'None'), *[(e.name, e.value) for e in TermType]],
        render_kw={"placeholder": "", "class": "form-select"}
    )
    number_positions = IntegerField(
        label="Number of Available Positions/Seats",
        validators=[NumberRange(min=0)],
        name="number_positions",
        description="This field is optional.",
        render_kw={"class": "form-control", "placeholder": "e.g. 9",
                   "aria-describedby": "number-positions-help-block"}
    )

    display_description = StringField(
        label="Display Description",
        validators=[DataRequired(), Length(
            min=1, max=100, message="Display Description must be between 1 and 100 characters.")],
        name="display_description",
        render_kw={"placeholder": "Short description to be displayed on the search page.",
                   "class": "form-control"}
    )
    description = TextAreaField(
        label="Description",
        name="description",
        description="Full Description of Post.",
        render_kw={"class": "form-control", "id": "description-editor",
                   "aria-describedby": "description-help-block"}
    )
    responsibilities = TextAreaField(
        label="Responsibilities",
        name="responsibilities",
        description="Successful Applicant's Roles/Responsibilities. This field is optional.",
        render_kw={"class": "form-control", "id": "responsibilities-editor",
                   "aria-describedby": "responsibilities-help-block"}
    )
    requirements = TextAreaField(
        label="Requirements",
        name="requirements",
        description="Required Qualifications to Apply.",
        render_kw={"class": "form-control", "id": "requirements-editor",
                   "aria-describedby": "requirements-help-block"}
    )
    compensation = TextAreaField(
        label="Compensation and Benefits",
        name="compensation",
        description="Successful Applicant's Compensation/Benefits. If no pay is offered, provide a reason for individuals to apply.",
        render_kw={"class": "form-control", "id": "compensation-editor",
                   "aria-describedby": "compensation-help-block"}
    )
    additional = TextAreaField(
        label="Additional Information",
        name="additional",
        description="Share Any Additional Details. This field is optional.",
        render_kw={"class": "form-control", "id": "additional-editor",
                   "aria-describedby": "additional-help-block"}
    )
    application = TextAreaField(
        label="Application Details",
        name="application",
        description="Required Steps to Apply.",
        render_kw={"class": "form-control", "id": "application-editor",
                   "aria-describedby": "application-help-block"}
    )
    application_link = URLField(
        label="Link to Apply",
        validators=[URL(require_tld=True, allow_ip=False,
                        message="Application URL is invalid.")],
        name="application_link",
        render_kw={"class": "form-control",
                   "placeholder": "e.g. https://www.apply_here.com/"}
    )

    submit = SubmitField(
        label="Submit",
        name="submit",
        render_kw={"class": "btn btn-primary form-control", "id": "submit",
                   "value": "Submit"}
    )
    cancel = SubmitField(
        label="Cancel",
        name="cancel",
        render_kw={"class": "btn btn-secondary form-control", "id": "cancel", "type": "button",
                   "value": "Cancel"}
    )
