from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from typing import List
from schemas import (
    ClientCreate, ClientResponse, 
    CarCreate, CarResponse, 
    ServiceCreate, ServiceResponse,
    BayResponse,
    CallbackRequestCreate, CallbackRequestResponse,
    LoginRequest, Token, OrderCreate, OrderResponse, OrderCompleteRequest, 
    OrderCloseRequest,  MechanicAvailabilityRequest, MechanicResponse,
    RevenueReportResponse, PopularServiceResponse
)
import crud
from crud import verify_password, get_client_by_login
from auth import create_access_token
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Автомастерской",
    description="Система управления автомастерской",
    version="1.0.0"
)

@app.post("/clients/", response_model=ClientResponse, status_code=201, tags=["Клиенты"])
def register_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Регистрация нового клиента"""
    existing_client = crud.get_client_by_email_or_phone(db, email=client.email, phone=client.phone)
    if existing_client:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email или телефоном уже зарегистрирован."
        )
    return crud.create_client(db=db, client_data=client)

@app.post("/login", response_model=Token, tags=["Авторизация"])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Авторизация клиента"""
    client = get_client_by_login(db, login=request.login)
    if not client or not verify_password(request.password, client.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль"
        )
    access_token = create_access_token(data={"sub": str(client.id), "role": "client"})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/clients/{client_id}/cars/", response_model=CarResponse, status_code=201, tags=["Автомобили"])
def add_car(client_id: int, car: CarCreate, db: Session = Depends(get_db)):
    """Добавить автомобиль клиента"""
    client = crud.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return crud.create_car(db=db, car_data=car, client_id=client_id)

@app.get("/clients/{client_id}/cars/", response_model=List[CarResponse], tags=["Автомобили"])
def get_client_cars(client_id: int, db: Session = Depends(get_db)):
    """Получить все автомобили клиента"""
    return crud.get_cars_by_client(db, client_id=client_id)

@app.delete("/clients/cars/{car_id}", status_code=204, tags=["Автомобили"])
def delete_car(car_id: int, client_id: int, db: Session = Depends(get_db)):
    """Удалить автомобиль"""
    if not crud.delete_car(db, car_id=car_id, client_id=client_id):
        raise HTTPException(status_code=404, detail="Автомобиль не найден")
    return None

@app.get("/services/", response_model=List[ServiceResponse], tags=["Услуги"])
def get_services(db: Session = Depends(get_db)):
    """Получить список всех услуг"""
    return crud.get_services(db)

@app.post("/services/", response_model=ServiceResponse, status_code=201, tags=["Услуги"])
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Добавить новую услугу (для админа)"""
    return crud.create_service(db=db, service_data=service)

@app.get("/bays/", response_model=List[BayResponse], tags=["Боксы"])
def get_bays(db: Session = Depends(get_db)):
    """Получить список всех боксов"""
    return crud.get_bays(db)

@app.post("/callback/", response_model=CallbackRequestResponse, status_code=201, tags=["Обратный звонок"])
def request_callback(callback: CallbackRequestCreate, db: Session = Depends(get_db)):
    """Заказать обратный звонок"""
    return crud.create_callback_request(db=db, callback_data=callback)


@app.get("/")
def read_root():
    return {
        "message": "API Автомастерской работает!",
        "docs": "/docs"
    }

@app.post("/orders/", response_model=OrderResponse, status_code=201, tags=["Заказ-наряды"])
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        new_order = crud.create_order(db=db, order_data=order)
        return new_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/orders/{order_id}/complete", response_model=OrderResponse, tags=["Заказ-наряды"])
def mechanic_complete_order(
    order_id: int, 
    mechanic_id: int, 
    request: OrderCompleteRequest,
    db: Session = Depends(get_db)
):
    """
    Мастер отмечает заказ выполненным.
    """
    try:
        return crud.complete_order_by_mechanic(db, order_id, mechanic_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/orders/{order_id}/close", response_model=OrderResponse, tags=["Заказ-наряды"])
def admin_close_order(order_id: int, close_data: OrderCloseRequest, db: Session = Depends(get_db)):
    """
    Администратор закрывает заказ, принимает оплату и начисляет скидку.
    """
    try:
        return crud.close_order_by_admin(db, order_id, close_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/mechanics/available", response_model=List[MechanicResponse], tags=["Мастера"])
def find_available_mechanics(request: MechanicAvailabilityRequest, db: Session = Depends(get_db)):
    """
    Поиск свободных мастеров по специализации на заданное время.
    Возвращает список мастеров, у которых нет накладок в графике.
    """
    return crud.get_available_mechanics(
        db, 
        specialization=request.specialization, 
        start=request.planned_start, 
        end=request.planned_end
    )

@app.get("/reports/revenue", response_model=RevenueReportResponse, tags=["Отчеты"])
def get_revenue_report(
    start_date: datetime, 
    end_date: datetime, 
    db: Session = Depends(get_db)
):
    """
    Отчет по выручке за период (ФТ5).
    Принимает даты в формате ISO (например, 2023-01-01T00:00:00).
    """
    return crud.get_revenue_report(db, start=start_date, end=end_date)

@app.get("/reports/popular-services", response_model=List[PopularServiceResponse], tags=["Отчеты"])
def get_popular_services_report(
    start_date: datetime, 
    end_date: datetime, 
    limit: int = 5, 
    db: Session = Depends(get_db)
):
    """
    Отчет по популярным услугам за период (ФТ5).
    """
    return crud.get_popular_services_report(db, start=start_date, end=end_date, limit=limit)