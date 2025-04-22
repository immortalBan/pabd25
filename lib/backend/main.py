from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from models import models, schemas
from models.database import SessionLocal, engine
from auth.admin import admin_app
from auth.auth import get_current_user
from auth.init_db import init_db

models.Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение админки
admin_app.mount_to(app)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/current_model")
async def get_current_model(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    # Здесь будет логика получения текущей модели
    return {"current_model": "model_v1.pkl"}