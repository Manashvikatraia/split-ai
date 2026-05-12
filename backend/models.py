from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from database import Base


# 🔐 USERS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        index=True
    )

    password = Column(String)


# 💸 EXPENSES
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float)

    paid_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# 🤝 SPLITS
class Split(Base):
    __tablename__ = "splits"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    expense_id = Column(
        Integer,
        ForeignKey("expenses.id")
    )

    amount = Column(Float)