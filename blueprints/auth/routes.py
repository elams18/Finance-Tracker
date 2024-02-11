import uuid
import json
from flask import Blueprint, render_template, redirect, request
from db_config import session

from blueprints.auth import LoginForm, RegistrationForm, UserAccount, load_user
from werkzeug.security import generate_password_hash, check_password_hash

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
        user_query = session.query(UserAccount).filter_by(username=username) # need to write this as an actual query executor
        with session.execute(user_query) as user_results:
            user = user_results.first()
            if user is None or (len(user) == 1 and not user[0].check_password(password)):
                return render_template('auth/index.html', title='Login', error='Invalid username or password', form=form)

        # business logic done, now to check authentication
        load_user(user)

        next = request.args.get('next')
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return flask.abort(400)

        return redirect(next or "/")
    else:
        error = form.errors
        return render_template('auth/index.html', title='Login', error=error, form=form)


@auth.route('/register', methods=['POST', "GET"])
def register_page():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template('auth/index.html', title='Register', form=form)

    if form.validate_on_submit():
        user_query = session.query(UserAccount).filter_by(username=form.username.data)

        with session.execute(user_query) as user_results:
            user_result = user_results.fetchall()
            if user_result:
                error = 'User already exists'
                return render_template('auth/index.html', title='Register', form=form, error=error)

        # if not user.get_id() == 'None':
        #     error = 'User already exists'
        #     return render_template('auth/index.html', title='Register', form=form, error=error)

        if form.password.data != form.confirm_password.data or not form.confirm_password:
            error = 'Passwords must match'
            return render_template('auth/index.html', title='Register', form=form, error=error)

        name = form.name.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
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

    else:
        error = form.errors
        return render_template('auth/index.html', title='Login', error=error, form=form)