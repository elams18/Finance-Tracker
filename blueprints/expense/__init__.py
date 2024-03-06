import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from config import db
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user


class Expense(db.Model):
    __tablename__ = "expense"

    class ExpenseType(enum.IntEnum):
        """Enumeration of
        expense types
        Food, Outing, Groceries, Dresses, Gift, other
        """

        Food = 1
        Outing = 2
        Groceries = 3
        Dresses = 4
        Gift = 5
        Other = 6

    class ExpensePaymentStatus(enum.StrEnum):
        PAID = "PA"
        PENDING = "PN"

    class ExpensePaymentType(enum.StrEnum):
        URGENT = "URGENT"
        NORMAL = "NORMAL"
        IMMEDIATE = "IMMEDIATE"

    exp_id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    exp_title = db.Column(db.String, nullable=False)
    exp_description = db.Column(db.String, nullable=True)
    exp_amount = db.Column(db.Float, nullable=False)
    exp_created_at = db.Column(db.Date, nullable=False)
    exp_updated_at = db.Column(db.Date, nullable=False)
    exp_type = db.Column(db.Integer, default=ExpenseType.Food, nullable=False)
    exp_status = db.Column(db.String, default=ExpensePaymentType.NORMAL, nullable=False)
    exp_payment_status = db.Column(
        db.String, default=ExpensePaymentStatus.PENDING, nullable=False
    )

    expense_user = db.Column(UUID, db.ForeignKey("user_account.id"), nullable=False)


expense = Blueprint(
    "expense", __name__, template_folder="templates", static_folder="static"
)


@expense.route("/list", methods=["GET", "POST"])
@login_required
def get_expenses():
    if request.method == "GET":
        expenses = Expense.query.all()
        return render_template(
            "expense/index.html",
            expenses=expenses,
            title="Expense",
            username=current_user.username,
        )


@expense.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "GET":
        return redirect(url_for("expense.get_expenses"), code=302)
    json = request.get_json()
    expense = Expense(
        exp_title=json["title"],
        exp_description=json["description"],
        exp_amount=json["amount"],
        expense_user=current_user,
        exp_type=json["exp_type"],
    )
    db.session.add(expense)
    db.commit()

    return redirect(url_for("expense.get_expenses"), code=302)
