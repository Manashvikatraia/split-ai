from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ✅ ADD THIS

from database import engine, Base
import models
from routes.expense import router as expense_router

app = FastAPI()

# ✅ ADD THIS BLOCK (right after app = FastAPI())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(expense_router)