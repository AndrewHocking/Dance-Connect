from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class SignUpForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[InputRequired()],
        name="email",
        render_kw={"placeholder": "Enter email", "class" : "form-control"}
    )
    first_name = StringField(
        label="Name",
        validators=[InputRequired()],
        name="name",
        render_kw={"placeholder": "Enter your name", "class" : "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired()],
        name="password",
        render_kw={"placeholder": "Enter password", "class" : "form-control"}
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[InputRequired()],
        name="confirm_password",
        render_kw={"placeholder": "Re-enter password", "class" : "form-control"}
    )
    submit = SubmitField(
        label="Sign Up",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )

class LogInForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[InputRequired()],
        name="email",
        render_kw={"placeholder": "Enter email", "class" : "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired()],
        name="password",
        render_kw={"placeholder": "Enter password", "class" : "form-control"}
    )
    submit = SubmitField(
        label="Log In",
        name="submit",
        render_kw={"class": "btn btn-primary"}
    )
