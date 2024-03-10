import random
from flask_sqlalchemy import SQLAlchemy
import requests
from config import db
import os
import uuid


class EmailUserRegisterCode(db.Model):
    __tablename__ = "email_user_register_code"
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String, unique=True)
    email_code = db.Column(db.String)
    created_at = db.Column(db.Date, default=db.func.now())


def send_verification_mail(user_id: str, email: str):
    MAIL_CODE = str(int(random.random() * 10000))
    SMTP_DOMAIN = os.getenv("SMTP_DOMAIN")
    SMTP_API_KEY = os.getenv("SMTP_API_KEY")
    email_user_code = EmailUserRegisterCode.query.filter_by(user_id=user_id).first()
    print(email_user_code.email_code)
    if email_user_code:
        email_user_code.email_code = MAIL_CODE
        db.session.commit()
    else:
        email_user_code = EmailUserRegisterCode()
        email_user_code.email_code = MAIL_CODE
        email_user_code.user_id = user_id
        db.session.add(email_user_code)

    return requests.post(
        f"https://api.mailgun.net/v3/{SMTP_DOMAIN}/messages",
        auth=("api", f"{SMTP_API_KEY}"),
        data={
            "from": f"<mailgun@{SMTP_DOMAIN}>",
            "to": [email],
            "subject": "Verify to sign up",
            "text": f"Add this code to sign up: {MAIL_CODE}",
        },
    )
