from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.expense import router as expense_router

app = FastAPI()

# ✅ Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expense_router)

@app.get("/")
def home():
    return {"message": "Split AI Backend Running"}