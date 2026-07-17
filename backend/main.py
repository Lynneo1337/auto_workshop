from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from schemas import ClientCreate, ClientResponse, LoginRequest, Token
import crud
from crud import verify_password, get_client_by_login
from auth import create_access_token

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

@app.post("/login", response_model=Token, tags=["Авторизация"])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Авторизация пользователя (Вход в систему).
    """
    client = get_client_by_login(db, login=request.login)
    
    if not client or not verify_password(request.password, client.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль. Попробуйте снова или восстановите пароль."
        )
    
    access_token = create_access_token(data={"sub": str(client.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}