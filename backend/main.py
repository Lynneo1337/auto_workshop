from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from schemas import ClientCreate, ClientResponse
from crud import create_client


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Приложение запущено"}

@app.get("/health")
def health_check():
    return {"status": "OK", "database": "connected"}

@app.post("/clients/", response_model=ClientResponse, status_code=201, tags=["Клиенты"])
def register_client(client: ClientCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового клиента.
    Принимает данные, хеширует пароль и сохраняет в БД.
    """
    # Добавить проверку: а не занят ли уже этот email или phone?
    
    new_client = create_client(db=db, client_data=client)
    return new_client