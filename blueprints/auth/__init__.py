import uuid

from flask import redirect, url_for
from flask_wtf import FlaskForm
from sqlalchemy.dialects.postgresql import UUID
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from werkzeug.security import check_password_hash
from app import db

from flask_login import LoginManager

login_manager = LoginManager()

class UserAccount(db.Model):
    __tablename__ = 'user_account'

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

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

@login_manager.user_loader
def load_user(user_id):
    user = UserAccount.query.filter_by(id=user_id).first()
    if user and user.is_authenticated:
        return user
    return None

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    form = LoginForm()
    return redirect(url_for('auth.login_page'))

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
    return (
        _url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=require_https) and
        _url_has_allowed_host_and_scheme(url.replace('\\', '/'), allowed_hosts, require_https=require_https)
    )

