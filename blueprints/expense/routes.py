from flask import Blueprint, request, render_template
from flask_login import login_required, current_user

from blueprints.expense import Expense
from db_config import session
from blueprints.auth import UserAccount

expense = Blueprint('expense', __name__, template_folder='templates', static_folder='static')


@expense.route('/list', methods=['GET', 'POST'])
@login_required
def get_expenses():
    if request.method == 'GET':
        expenses_query = session.query(Expense)
        with session.execute(expenses_query) as expenses:
            return render_template('expense/index.html', expenses=expenses.all(), title="Expense", username=current_user.username)
