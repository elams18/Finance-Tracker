import uuid
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from blueprints.auth import LoginForm, RegistrationForm, UserAccount, load_user, db
from werkzeug.security import generate_password_hash

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
        user = UserAccount.query.filter_by(username=username).first()  # need to write this as an actual query executor
        if user is None or (not user.check_password(password)):
            return render_template('auth/index.html', title='Login', error='Invalid username or password',
                                   form=form)

        # business logic done, now to check authentication
        user.is_authenticated = True
        db.session.commit()
        load_user(user.id)
        check = login_user(user, True)

        next = request.args.get('next')
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return flask.abort(400)

        return redirect(url_for('expense.get_expenses'), code=302)
    else:
        error = form.errors
        return render_template('auth/index.html', title='Login', error=error, form=form)


@auth.route('/register', methods=['POST', "GET"])
def register_page():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template('auth/index.html', title='Register', form=form)

    if form.validate_on_submit():
        user_result = UserAccount.query.filter_by(username=form.username.data).first()

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

        created_user = UserAccount(username=username,
                                   hashed_password=password,
                                   name=name,
                                   email=email)

        created_user.id = uuid.uuid4()
        db.session.add(created_user)
        db.session.commit()

        if created_user.get_id() is 'None':
            error = 'Error creating user'
            return render_template('auth/index.html', title='Register', form=form, error=error)

        return redirect(url_for('expense.get_expenses'))

    else:
        error = form.errors
        return render_template('auth/index.html', title='Register', error=error, form=form)


@login_required
@auth.route('/logout')
def logout():
    user = logout_user()
    if user is not None:
        return redirect(url_for('auth.login_page'))
