import enum
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from blueprints import Base

class Expense(Base):
    __tablename__ = 'expense'

    class expense_types(enum.IntEnum):
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

    exp_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    exp_name = Column(String, nullable=False)
    exp_description = Column(String, nullable=True)
    exp_created_at = Column(DateTime, nullable=False)
    exp_updated_at = Column(DateTime, nullable=False)
    exp_type = Column(Integer, default=expense_types.Food, nullable=False)

    expense_user = Column(UUID, ForeignKey('user_account.id'), nullable=False)