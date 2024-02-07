import uuid

from flask import Blueprint, render_template, redirect, request
from db_config import session

from blueprints.auth import LoginForm, RegistrationForm, UserAccount
auth = Blueprint(
    'auth', __name__, template_folder='templates', static_folder='static'
)

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/index.html', title='Login', form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = UserAccount(username=username)
        if user is None or not user.check_password(password):
            return render_template('auth/index.html', title='Login', error='Invalid username or password', form=form)

        return redirect("/")


@auth.route('/register', methods=['POST', "GET"])
def register_page():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template('auth/index.html', title='Register', form=form)

    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data or not form.confirm_password:
            error = 'Passwords must match'
            return render_template('auth/index.html', title='Register', form=form, error=error)

        user = UserAccount(username=form.username)
        if not user.get_id() == 'None':
            error = 'User already exists'
            return render_template('auth/index.html', title='Register', form=form, error=error)

        name = form.name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data

        created_user =  UserAccount(username=username,
                                   hashed_password=password,
                                   name=name,
                                   email=email)

        created_user.id = uuid.uuid4()
        session.add(created_user)
        session.commit()

        if created_user.get_id() is 'None':
            error = 'Error creating user'
            return render_template('auth/index.html', title='Register', form=form, error=error)

        return redirect("/")