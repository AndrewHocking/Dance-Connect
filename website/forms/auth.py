from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class SignUpForm(FlaskForm):
    email = EmailField(
        label="Email address",
        validators=[InputRequired(), Length(
            max=72, message="Email must be at most 72 characters long.")],
        name="email",
        render_kw={"placeholder": "name@example.com", "class": "form-control"}
    )
    display_name = StringField(
        label="Display name",
        validators=[InputRequired(), Length(
            max=35, message="Name must be 10 to 35 characters long.")],
        name="display_name",
        render_kw={"placeholder": "Jane Doe", "class": "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired(), Length(
            max=72, message="Password must be 10 to 72 characters long.")],
        name="password",
        render_kw={"placeholder": "hunter2", "class": "form-control"}
    )
    confirm_password = PasswordField(
        label="Confirm password",
        validators=[InputRequired(), Length(
            max=72, message="Confirm Password must be 10 to 72 characters long.")],
        name="confirm_password",
        render_kw={"placeholder": "hunter2", "class": "form-control"}
    )
    submit = SubmitField(
        label="Sign Up",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )


class LogInForm(FlaskForm):
    email = StringField(
        label="Email address or username",
        validators=[InputRequired(), Length(
            max=72, message="Email must be at most 72 characters long.")],
        name="email",
        render_kw={"placeholder": "name@example.com", "class": "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired(), Length(
            max=72, message="Password must be 10 to 72 characters long.")],
        name="password",
        render_kw={"placeholder": "hunter2", "class": "form-control"}
    )
    submit = SubmitField(
        label="Log In",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )
