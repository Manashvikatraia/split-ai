from pydantic import BaseModel
from typing import List


# 🔐 USER AUTH

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# 💸 EXPENSE

class ExpenseCreate(BaseModel):
    payer: str
    amount: float
    participants: List[str]