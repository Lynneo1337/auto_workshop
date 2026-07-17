from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from schemas import ClientCreate, ClientResponse
import crud


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
    Регистрация нового клиента с проверкой уникальности.
    """
    existing_client = crud.get_client_by_email_or_phone(db, email=client.email, phone=client.phone)
    
    if existing_client:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email или телефоном уже зарегистрирован."
        )
    new_client = create_client(db=db, client_data=client)
    return new_client