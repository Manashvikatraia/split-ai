from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

from routes.expense import router as expense_router


# 🚀 CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📌 ROUTES
app.include_router(expense_router)


# 🏠 HOME
@app.get("/")
def home():

    return {
        "message": "Split AI Backend Running"
    }