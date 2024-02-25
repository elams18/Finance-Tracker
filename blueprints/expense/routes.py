from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from blueprints.expense import db
from blueprints.expense import Expense
expense = Blueprint('expense', __name__, template_folder='templates', static_folder='static')


@expense.route('/list', methods=['GET', 'POST'])
@login_required
def get_expenses():
    if request.method == 'GET':
        expenses = Expense.query.all()
        return render_template('expense/index.html', expenses=expenses, title="Expense", username=current_user.username)

@expense.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'GET':
        return redirect(url_for("expense.get_expenses"), code=302)
    json = request.get_json()
    expense = Expense(
        exp_title=json['title'],
        exp_description=json['description'],
        exp_amount=json['amount'],
        expense_user=current_user,
        exp_type=json['exp_type']
    )
    db.session.add(expense)
    db.commit()

    return redirect(url_for("expense.get_expenses"), code=302)