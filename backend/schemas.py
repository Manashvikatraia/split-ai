from pydantic import BaseModel
from typing import List

class ExpenseCreate(BaseModel):
    payer: str
    amount: float
    participants: List[str]