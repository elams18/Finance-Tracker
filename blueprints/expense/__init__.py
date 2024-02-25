import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db
class Expense(db.Model):
    __tablename__ = 'expense'

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
    exp_payment_status = db.Column(db.String, default=ExpensePaymentStatus.PENDING, nullable=False)

    expense_user = db.Column(UUID, db.ForeignKey('user_account.id'), nullable=False)