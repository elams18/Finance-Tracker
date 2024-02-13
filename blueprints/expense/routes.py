from flask import Blueprint, request
from flask_login import login_required

from blueprints.expense import Expense
from db_config import session
from blueprints.auth import login_manager, load_user

expense = Blueprint('expense', __name__, template_folder='templates', static_folder='static')


@expense.route('/list', methods=['GET', 'POST'])
@login_required
def get_expenses():
    if request.method == 'GET':
        expenses_query = session.query(Expense)
        with session.execute(expenses_query) as expenses:
            return 'Expenses', expenses.all()
