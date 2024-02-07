import uuid

from flask_wtf import FlaskForm
from sqlalchemy import String, Column, Boolean
from sqlalchemy.dialects.postgresql import UUID
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

from blueprints import Base
from flask_login import LoginManager

login_manager = LoginManager()


class UserAccount(Base):
    __tablename__ = 'user_account'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    is_authenticated = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=False)

    def __repr__(self):
        return f"Username: {self.username!r} ID: {self.id!r}"

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        if not self.is_authenticated:
            return False
        if self.hashed_password == password:
            return True
        return False

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
    return UserAccount.get(user_id)
