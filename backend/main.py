from fastapi import FastAPI, Depends, HTTPException, status, Header, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import engine, Base, get_db
import models
from typing import List, Optional
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
from auth import create_access_token, SECRET_KEY, ALGORITHM
from datetime import datetime
import jwt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import Order, Mechanic, Bay, Client, Car, Service, Order_Item


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Автомастерской",
    description="Система управления автомастерской",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
   allow_origins=["http://localhost:5173"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
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
    """
    Универсальный вход в систему для Клиента, Мастера и Администратора.
    """
    user = None
    user_id = None

    if request.role == "client":
        user = crud.get_client_by_login(db, login=request.login)
        if user: user_id = user.id
    elif request.role == "mechanic":
        user = crud.get_mechanic_by_login(db, login=request.login)
        if user: user_id = user.id
    elif request.role == "admin":
        user = crud.get_admin_by_login(db, login=request.login)
        if user: user_id = user.id
    else:
        raise HTTPException(status_code=400, detail="Неверно указана роль (client/mechanic/admin)")

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль. Попробуйте снова."
        )
    
    access_token = create_access_token(data={"sub": str(user_id), "role": request.role})
    
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

@app.get("/mechanics/", tags=["Мастера"])
def get_all_mechanics(db: Session = Depends(get_db)):
    mechanics = db.query(Mechanic).all()
    return [{"id": m.id, "full_name": m.full_name, "specialization": m.specialization} for m in mechanics]

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

@app.get("/me", tags=["Профиль"])
def get_my_profile(Authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Возвращает профиль пользователя на основе его JWT токена.
    """
    try:
        token = Authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
            
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Неверный или истекший токен")

    if role == "client":
        user = crud.get_client_by_id(db, int(user_id))
        if not user: raise HTTPException(404, "Клиент не найден")
        return {"role": role, "data": {"id": user.id, "name": user.full_name, "discount": user.current_discount, "visitCount": user.visit_count}}
        
    elif role == "mechanic":
        return {"role": role, "data": {"id": user_id, "message": "Профиль мастера"}}
        
    elif role == "admin":
        return {"role": role, "data": {"id": user_id, "message": "Профиль администратора"}}
        
    raise HTTPException(400, "Неизвестная роль")

@app.get("/admin/orders", tags=["Админ"])
def get_all_orders_enriched(db: Session = Depends(get_db)):
    orders = db.query(Order).options(
        joinedload(Order.client),
        joinedload(Order.car),
        joinedload(Order.mechanic),
        joinedload(Order.bay),
        joinedload(Order.order_items).joinedload(Order_Item.service)
    ).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "status": order.status,
            "planned_start": order.planned_start.isoformat() if order.planned_start else None,
            "planned_end": order.planned_end.isoformat() if order.planned_end else None,
            "total_cost": float(order.total_cost) if order.total_cost else 0,
            "final_cost": float(order.final_cost) if order.final_cost else 0,
            "client_name": order.client.full_name if order.client else "Неизвестно",
            "car_info": f"{order.car.brand_model} ({order.car.license_plate})" if order.car else "Неизвестно",
            "mechanic_name": order.mechanic.full_name if order.mechanic else "Не назначен",
            "bay_number": order.bay.number if order.bay else "Не назначен"
        })
    
    return result

class OrderAssignRequest(BaseModel):
    mechanic_id: Optional[int] = None
    bay_id: Optional[int] = None
    auto_assign: bool = True

@app.put("/admin/orders/{order_id}/assign", tags=["Админ"])
def assign_order(order_id: int, assign_data: OrderAssignRequest, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    if assign_data.auto_assign:
        if not order.order_items:
            raise HTTPException(status_code=400, detail="В заявке нет услуг для определения специализации")

        service = db.query(Service).filter(Service.id == order.order_items[0].service_id).first()
        specialization = service.req_specialization if service else None
        
        available_mechanics = crud.get_available_mechanics(
            db, 
            specialization=specialization or "",
            start=order.planned_start,
            end=order.planned_end
        )
        
        if not available_mechanics:
            raise HTTPException(
                status_code=400, 
                detail=f"Нет свободных мастеров{' (' + specialization + ')' if specialization else ''} на это время"
            )
        
        order.mechanic_id = available_mechanics[0].id
    
    if assign_data.bay_id:
        if not crud.is_bay_available(db, assign_data.bay_id, order.planned_start, order.planned_end):
            raise HTTPException(status_code=400, detail="Выбранный бокс занят")
        order.bay_id = assign_data.bay_id
    else:
        available_bays = crud.get_available_bays(db, order.planned_start, order.planned_end)
        if not available_bays:
            raise HTTPException(status_code=400, detail="Нет свободных боксов на это время")
        order.bay_id = available_bays[0].id
    
    order.status = "В работе"
    db.commit()
    db.refresh(order)
    
    return {
        "message": "Заявка успешно назначена",
        "status": order.status,
        "mechanic_id": order.mechanic_id,
        "bay_id": order.bay_id
    }

class OrderCompleteRequest(BaseModel):
    comment: Optional[str] = None

@app.post("/mechanic/orders/{order_id}/complete", tags=["Мастер"])
def mechanic_complete_order(
    order_id: int, 
    complete_data: OrderCompleteRequest,
    mechanic_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    if order.mechanic_id != mechanic_id:
        raise HTTPException(status_code=403, detail="Этот заказ назначен не вам")
    
    if order.status != "В работе":
        raise HTTPException(status_code=400, detail=f"Нельзя завершить заказ со статусом '{order.status}'")
    
    order.status = "Выполнено"
    db.commit()
    db.refresh(order)
    
    return {"message": "Работы отмечены как выполненные", "status": order.status}

@app.get("/mechanic/orders", tags=["Мастер"])
def get_mechanic_orders(mechanic_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).options(
        joinedload(Order.client),
        joinedload(Order.car)
    ).filter(
        Order.mechanic_id == mechanic_id,
        Order.status.in_(["В работе", "Ожидает"])
    ).order_by(Order.planned_start).all()
    
    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "status": order.status,
            "planned_start": order.planned_start.isoformat() if order.planned_start else None,
            "client_name": order.client.full_name if order.client else "Неизвестно",
            "car_info": f"{order.car.brand_model} ({order.car.license_plate})" if order.car else "Неизвестно",
            "services": [
                {
                    "name": item.service.name,
                    "quantity": item.quantity
                } for item in order.order_items
            ]
        })
    
    return result