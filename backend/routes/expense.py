from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import ExpenseCreate
from database import SessionLocal
import models

from openai import OpenAI

# 🔥 OPENROUTER AI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=""
)

router = APIRouter()


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🤖 AI PARSER
def ai_extract(text):

    prompt = f"""
    Extract:
    - payer
    - amount
    - participants

    from this expense sentence:

    "{text}"

    Return ONLY JSON.

    Example:
    {{
      "payer": "sai",
      "amount": 3000,
      "participants": ["mia", "ria"]
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return eval(result)


# ➕ ADD EXPENSE
@router.post("/add-expense")
def add_expense(expense: dict, db: Session = Depends(get_db)):

    # 🤖 Use AI if text exists
    if "text" in expense:

        ai_data = ai_extract(expense["text"])

        payer = ai_data["payer"]
        amount = ai_data["amount"]
        participants = ai_data["participants"]

    else:
        payer = expense["payer"]
        amount = expense["amount"]
        participants = expense["participants"]

    # include payer
    participants = list(set(participants))

    if payer not in participants:
        participants.append(payer)

    split_amount = amount / len(participants)

    # create/find users dynamically
    user_ids = {}

    for person in participants:

        existing = db.query(models.User).filter(
            models.User.name == person
        ).first()

        if existing:
            user_ids[person] = existing.id

        else:
            new_user = models.User(
                name=person,
                email=f"{person}@mail.com",
                password="1234"
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            user_ids[person] = new_user.id

    # create expense
    db_expense = models.Expense(
        amount=amount,
        paid_by=user_ids[payer]
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    balances = {}

    for person in participants:
        balances[person] = -split_amount

    balances[payer] += amount

    # store splits
    for person, amt in balances.items():

        split = models.Split(
            user_id=user_ids[person],
            expense_id=db_expense.id,
            amount=amt
        )

        db.add(split)

    db.commit()

    return {
        "message": "Expense added",
        "balances": balances
    }


# 💰 BALANCES
@router.get("/balances")
def get_balances(db: Session = Depends(get_db)):

    splits = db.query(models.Split).all()

    balances = {}

    for split in splits:

        user = db.query(models.User).filter(
            models.User.id == split.user_id
        ).first()

        balances[user.name] = balances.get(
            user.name,
            0
        ) + split.amount

    return balances


# 🤝 SETTLEMENT
@router.get("/settle")
def settle_up(db: Session = Depends(get_db)):

    splits = db.query(models.Split).all()

    balances = {}

    for split in splits:

        user = db.query(models.User).filter(
            models.User.id == split.user_id
        ).first()

        balances[user.name] = balances.get(
            user.name,
            0
        ) + split.amount

    debtors = []
    creditors = []

    for user, amount in balances.items():

        if amount < 0:
            debtors.append([user, -amount])

        elif amount > 0:
            creditors.append([user, amount])

    transactions = []

    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):

        d_user, d_amt = debtors[i]
        c_user, c_amt = creditors[j]

        pay = min(d_amt, c_amt)

        transactions.append({
            "from": d_user,
            "to": c_user,
            "amount": pay
        })

        debtors[i][1] -= pay
        creditors[j][1] -= pay

        if debtors[i][1] == 0:
            i += 1

        if creditors[j][1] == 0:
            j += 1

    return transactions


# 🧾 HISTORY
@router.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):

    expenses = db.query(models.Expense).all()

    result = []

    for exp in expenses:

        user = db.query(models.User).filter(
            models.User.id == exp.paid_by
        ).first()

        result.append({
            "id": exp.id,
            "amount": exp.amount,
            "payer": user.name
        })

    return result