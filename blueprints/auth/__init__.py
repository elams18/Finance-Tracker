from flask import Blueprint
from flask import redirect, url_for

from flask_login import LoginManager
import uuid
from flask import render_template, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from sqlalchemy.dialects.postgresql import UUID
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from werkzeug.security import check_password_hash
from config import db

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    user = UserAccount.query.filter_by(id=user_id).first()
    if user and user.is_authenticated:
        return user
    return None


auth_bp = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)


class UserAccount(db.Model):
    __tablename__ = "user_account"

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Username: {self.username!r} ID: {self.id!r}"

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @classmethod
    def get(cls, user_id):
        pass


class RegistrationForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "confirm_password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log In")


@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "GET":
        return render_template("auth/index.html", title="Login", form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = UserAccount.query.filter_by(
            username=username
        ).first()  # need to write this as an actual query executor
        if user is None or (not user.check_password(password)):
            return render_template(
                "auth/index.html",
                title="Login",
                error="Invalid username or password",
                form=form,
            )

        # business logic done, now to check authentication
        user.is_authenticated = True
        db.session.commit()
        load_user(user.id)
        check = login_user(user, True)

        next = request.args.get("next")
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return flask.abort(400)

        return redirect(url_for("expense.get_expenses"), code=302)
    else:
        error = form.errors
        return render_template("auth/index.html", title="Login", error=error, form=form)


@auth_bp.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("auth/index.html", title="Register", form=form)

    if form.validate_on_submit():
        user_result = UserAccount.query.filter_by(username=form.username.data).first()

        if user_result:
            error = "User already exists"
            return render_template(
                "auth/index.html", title="Register", form=form, error=error
            )

        # if not user.get_id() == 'None':
        #     error = 'User already exists'
        #     return render_template('auth/index.html', title='Register', form=form, error=error)

        if (
            form.password.data != form.confirm_password.data
            or not form.confirm_password
        ):
            error = "Passwords must match"
            return render_template(
                "auth/index.html", title="Register", form=form, error=error
            )

        name = form.name.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
        email = form.email.data

        created_user = UserAccount(
            username=username, hashed_password=password, name=name, email=email
        )

        created_user.id = uuid.uuid4()
        db.session.add(created_user)
        db.session.commit()

        if created_user.get_id():
            error = "Error creating user"
            return render_template(
                "auth/index.html", title="Register", form=form, error=error
            )

        return redirect(url_for("expense.get_expenses"))

    else:
        error = form.errors
        return render_template(
            "auth/index.html", title="Register", error=error, form=form
        )


@login_required
@auth_bp.route("/logout")
def logout():
    user = logout_user()
    if user is not None:
        return redirect(url_for("auth.login_page"))


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    form = LoginForm()
    return redirect(url_for("auth.login_page"))


def url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False):
    """
    Return ``True`` if the url uses an allowed host and a safe scheme.

    Always return ``False`` on an empty url.

    If ``require_https`` is ``True``, only 'https' will be considered a valid
    scheme, as opposed to 'http' and 'https' with the default, ``False``.

    Note: "True" doesn't entail that a URL is "safe". It may still be e.g.
    quoted incorrectly. Ensure to also use django.utils.encoding.iri_to_uri()
    on the path component of untrusted URLs.
    """
    if url is not None:
        url = url.strip()
    if not url:
        return False
    if allowed_hosts is None:
        allowed_hosts = set()
    elif isinstance(allowed_hosts, str):
        allowed_hosts = {allowed_hosts}
    # Chrome treats \ completely as / in paths but it could be part of some
    # basic auth credentials so we need to check both URLs.
    return _url_has_allowed_host_and_scheme(
        url, allowed_hosts, require_https=require_https
    ) and _url_has_allowed_host_and_scheme(
        url.replace("\\", "/"), allowed_hosts, require_https=require_https
    )
