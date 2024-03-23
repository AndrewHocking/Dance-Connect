from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class SignUpForm(FlaskForm):
    email = EmailField(
        label="Email address",
        validators=[InputRequired()],
        name="email",
        render_kw={"placeholder": "name@example.com", "class" : "form-control"}
    )
    display_name = StringField(
        label="Display name",
        validators=[InputRequired()],
        name="name",
        render_kw={"placeholder": "Jane Doe", "class" : "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired()],
        name="password",
        render_kw={"placeholder": "hunter2", "class" : "form-control"}
    )
    confirm_password = PasswordField(
        label="Confirm password",
        validators=[InputRequired()],
        name="confirm_password",
        render_kw={"placeholder": "hunter2", "class" : "form-control"}
    )
    submit = SubmitField(
        label="Sign Up",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )

class LogInForm(FlaskForm):
    email = EmailField(
        label="Email address",
        validators=[InputRequired()],
        name="email",
        render_kw={"placeholder": "name@example.com", "class" : "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired()],
        name="password",
        render_kw={"placeholder": "hunter2", "class" : "form-control"}
    )
    submit = SubmitField(
        label="Log In",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )
