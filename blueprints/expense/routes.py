from flask import Blueprint, request, render_template
from flask_login import login_required, current_user

from blueprints.expense import Expense
expense = Blueprint('expense', __name__, template_folder='templates', static_folder='static')


@expense.route('/list', methods=['GET', 'POST'])
@login_required
def get_expenses():
    if request.method == 'GET':
        expenses = Expense.query.all()
        return render_template('expense/index.html', expenses=expenses, title="Expense", username=current_user.username)
