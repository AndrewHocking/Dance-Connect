from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models.user import User
from flask_login import login_user, login_required, logout_user, current_user
from ...forms.auth import SignUpForm, LogInForm
from ...orm.user.user import create_user

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

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
