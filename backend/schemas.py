from pydantic import BaseModel
from typing import List


# 🔐 SIGNUP
class UserCreate(BaseModel):

    username: str
    password: str


# 🔐 LOGIN
class UserLogin(BaseModel):

    username: str
    password: str


# 🔑 TOKEN RESPONSE
class Token(BaseModel):

    access_token: str
    token_type: str


# 💸 EXPENSE
class ExpenseCreate(BaseModel):

    payer: str
    amount: float
    participants: List[str]