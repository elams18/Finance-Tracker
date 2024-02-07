from flask import Blueprint, render_template, redirect, request
from blueprints.auth import LoginForm, UserAccount
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
    if request.method == "GET":
        return render_template('auth/index.html', title='Register')