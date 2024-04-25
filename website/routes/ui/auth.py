from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ...models.user import User
from ...forms.auth import SignUpForm, LogInForm
from ...orm.user.user import create_user, get_user_by_email_or_username

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        response = get_user_by_email_or_username(email)
        if response["status_code"] == 200 and response["data"].password == password:
            flash('Logged in successfully!', category='success')
            login_user(response["data"], remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect login information, please try again.', category='error')

    return render_template("login.html", user=current_user, form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST':
        email = request.form.get('email')
        display_name = request.form.get('display_name')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')

        # TODO: Hash passwords
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            response = create_user(
                email=email, password=password1, display_name=display_name)
            if (response["status_code"] == 201):
                new_user: User = response["data"]
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash(response["message"], category=response["response_type"])

    return render_template("sign-up.html", user=current_user, form=form)
