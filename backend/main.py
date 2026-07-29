from fastapi import FastAPI, Depends, HTTPException, status, Header, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func
from database import engine, Base, get_db
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
from models import Order, Mechanic, Bay, Client, Car, Service, Order_Item, Callback_Request


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Автомастерской",
    description="Система управления автомастерской",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
   allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
    user = None
    user_id = None
    role = None

    client = crud.get_client_by_login(db, login=request.login)
    if client and verify_password(request.password, client.password_hash):
        user = client
        user_id = client.id
        role = "client"

    if not user:
        mechanic = crud.get_mechanic_by_login(db, login=request.login)
        if mechanic and verify_password(request.password, mechanic.password_hash):
            user = mechanic
            user_id = mechanic.id
            role = "mechanic"

    if not user:
        admin = crud.get_admin_by_login(db, login=request.login)
        if admin and verify_password(request.password, admin.password_hash):
            user = admin
            user_id = admin.id
            role = "admin"

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль. Попробуйте снова."
        )
    
    access_token = create_access_token(data={"sub": str(user_id), "role": role})
    
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
        services = []
        for item in order.order_items:
            if item.service:
                services.append({
                    "name": item.service.name,
                    "quantity": item.quantity,
                    "price": float(item.fact_price) if item.fact_price else 0,
                    "specialization": item.service.req_specialization or "Универсал"
                })
        
        result.append({
            "id": order.id,
            "status": order.status,
            "client_name": order.client.full_name if order.client else "Неизвестно",
            "car_info": f"{order.car.brand_model} ({order.car.license_plate})" if order.car else "Неизвестно",
            "mechanic_name": order.mechanic.full_name if order.mechanic else "Не назначен",
            "bay_number": order.bay.number if order.bay else "Не назначен",
            "planned_start": order.planned_start.isoformat() if order.planned_start else None,
            "planned_end": order.planned_end.isoformat() if order.planned_end else None,
            "total_cost": float(order.total_cost) if order.total_cost else 0,
            "discount_amount": float(order.discount_amount) if order.discount_amount else 0,
            "final_cost": float(order.final_cost) if order.final_cost else 0,
            "payment_method": order.payment_method,
            "services": [
    {
        "name": item.service.name if item.service else "Неизвестно",
        "quantity": item.quantity,
        "price": float(item.fact_price) if item.fact_price else 0,
        "specialization": item.service.req_specialization if item.service else "Универсал"
    }
    for item in order.order_items
],
            "created_at": order.created_at.isoformat() if order.created_at else None
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
    
    required_specialization = None
    if order.order_items:
        service = db.query(Service).filter(Service.id == order.order_items[0].service_id).first()
        if service:
            required_specialization = service.req_specialization
    
    if assign_data.auto_assign:
        if not required_specialization:
            raise HTTPException(status_code=400, detail="Не удалось определить специализацию для услуги")
        
        available_mechanics = crud.get_available_mechanics(
            db, 
            specialization=required_specialization,
            start=order.planned_start,
            end=order.planned_end
        )
        
        if not available_mechanics:
            raise HTTPException(
                status_code=400, 
                detail=f"Нет свободных мастеров специализации '{required_specialization}' на это время"
            )
        
        order.mechanic_id = available_mechanics[0].id
    else:
        if assign_data.mechanic_id:
            if not crud.is_mechanic_available(db, assign_data.mechanic_id, order.planned_start, order.planned_end):
                raise HTTPException(status_code=400, detail="Выбранный мастер занят в это время")
            
            if required_specialization:
                mechanic = db.query(Mechanic).filter(Mechanic.id == assign_data.mechanic_id).first()
                if mechanic and mechanic.specialization != required_specialization:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Мастер {mechanic.full_name} имеет специализацию '{mechanic.specialization}', но требуется '{required_specialization}'"
                    )
            
            order.mechanic_id = assign_data.mechanic_id
        else:
            raise HTTPException(status_code=400, detail="Не выбран мастер")
    
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
    
    # ПРОВЕРКА СПЕЦИАЛИЗАЦИИ
    mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    if mechanic and order.order_items:
        for item in order.order_items:
            service = db.query(Service).filter(Service.id == item.service_id).first()
            if service and service.req_specialization and service.req_specialization != mechanic.specialization:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Ваша специализация '{mechanic.specialization}' не соответствует услуге '{service.name}' (требуется '{service.req_specialization}')"
                )
    
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

@app.get("/reports/mechanics-load", tags=["Отчеты"])
def get_mechanics_load(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """Отчет по загрузке мастеров за период"""
    mechanics = db.query(Mechanic).all()
    result = []
    
    for mechanic in mechanics:
        orders_count = db.query(func.count(Order.id)).filter(
            and_(
                Order.mechanic_id == mechanic.id,
                Order.status == 'Завершена',
                Order.created_at >= start_date,
                Order.created_at <= end_date
            )
        ).scalar() or 0
        
        total_revenue = db.query(func.sum(Order.final_cost)).filter(
            and_(
                Order.mechanic_id == mechanic.id,
                Order.status == 'Завершена',
                Order.created_at >= start_date,
                Order.created_at <= end_date
            )
        ).scalar() or 0
        
        result.append({
            "mechanic_id": mechanic.id,
            "full_name": mechanic.full_name,
            "specialization": mechanic.specialization,
            "orders_count": orders_count,
            "total_revenue": float(total_revenue)
        })
    
    return result

@app.get("/reports/discounted-clients", tags=["Отчеты"])
def get_discounted_clients(db: Session = Depends(get_db)):
    """Отчет по клиентам со скидкой"""
    clients = db.query(Client).filter(
        and_(
            Client.current_discount > 0,
            Client.visit_count > 0
        )
    ).order_by(Client.current_discount.desc()).all()
    
    result = []
    for client in clients:
        result.append({
            "id": client.id,
            "full_name": client.full_name,
            "phone": client.phone,
            "visit_count": client.visit_count,
            "current_discount": float(client.current_discount)
        })
    
    return {
        "total_discounted_clients": len(result),
        "clients": result
    }

@app.get("/admin/callbacks", tags=["Админ"])
def get_all_callbacks(db: Session = Depends(get_db)):
    callbacks = db.query(Callback_Request).order_by(Callback_Request.created_at.desc()).all()
    return [{
        "id": c.id,
        "client_name": c.client_name,
        "phone": c.phone,
        "status": c.status,
        "created_at": c.created_at.isoformat() if c.created_at else None
    } for c in callbacks]

@app.put("/admin/callbacks/{callback_id}/status", tags=["Админ"])
def update_callback_status(callback_id: int, status: str, db: Session = Depends(get_db)):
    callback = db.query(Callback_Request).filter(Callback_Request.id == callback_id).first()
    if not callback:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    callback.status = status
    db.commit()
    db.refresh(callback)
    
    return {"message": "Статус обновлен", "status": callback.status}

@app.get("/admin/callbacks/unread-count", tags=["Админ"])
def get_unread_callbacks_count(db: Session = Depends(get_db)):
    count = db.query(Callback_Request).filter(Callback_Request.status == "Ожидает обработки").count()
    return {"count": count}

@app.get("/clients/{client_id}/orders", tags=["Клиенты"])
def get_client_orders(client_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).options(
        joinedload(Order.car),
        joinedload(Order.mechanic),
        joinedload(Order.order_items).joinedload(Order_Item.service)
    ).filter(Order.client_id == client_id).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        services = []
        for item in order.order_items:
            services.append({
                "name": item.service.name if item.service else "Неизвестно",
                "quantity": item.quantity,
                "price": float(item.fact_price) if item.fact_price else 0
            })
        
        result.append({
            "id": order.id,
            "status": order.status,
            "planned_start": order.planned_start.isoformat() if order.planned_start else None,
            "planned_end": order.planned_end.isoformat() if order.planned_end else None,
            "total_cost": float(order.total_cost) if order.total_cost else 0,
            "discount_amount": float(order.discount_amount) if order.discount_amount else 0,
            "final_cost": float(order.final_cost) if order.final_cost else 0,
            "payment_method": order.payment_method,
            "car_info": f"{order.car.brand_model} ({order.car.license_plate})" if order.car else "Неизвестно",
            "mechanic_name": order.mechanic.full_name if order.mechanic else "Не назначен",
            "services": services
        })
    
    return result


@app.post("/admin/orders/{order_id}/split", tags=["Админ"])
def split_order(order_id: int, db: Session = Depends(get_db)):
    original_order = db.query(Order).filter(Order.id == order_id).first()
    if not original_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    if original_order.status != "Ожидает":
        raise HTTPException(status_code=400, detail="Можно разделить только ожидающие заказы")
    
    services_by_spec = {}
    for item in original_order.order_items:
        service = db.query(Service).filter(Service.id == item.service_id).first()
        if service:
            spec = service.req_specialization or "Универсал"
            if spec not in services_by_spec:
                services_by_spec[spec] = []
            services_by_spec[spec].append(item)
    
    if len(services_by_spec) <= 1:
        raise HTTPException(status_code=400, detail="Заказ не требует разделения (все услуги одной специализации)")
    
    original_order.status = "Разделен"
    
    sub_orders = []
    for spec, items in services_by_spec.items():
        total_cost = sum(item.fact_price * item.quantity for item in items)
        
        sub_order = Order(
            client_id=original_order.client_id,
            car_id=original_order.car_id,
            status="Ожидает",
            planned_start=original_order.planned_start,
            planned_end=original_order.planned_end,
            total_cost=total_cost,
            final_cost=total_cost,
            created_at=datetime.now()
        )
        db.add(sub_order)
        db.flush()
        
        for item in items:
            sub_item = Order_Item(
                order_id=sub_order.id,
                service_id=item.service_id,
                quantity=item.quantity,
                fact_price=item.fact_price
            )
            db.add(sub_item)
        
        sub_orders.append({
            "id": sub_order.id,
            "specialization": spec,
            "services_count": len(items),
            "total_cost": total_cost
        })
    
    db.commit()
    
    return {
        "message": f"Заказ #{original_order.id} разделен на {len(sub_orders)} подзаказа",
        "original_order_id": original_order.id,
        "sub_orders": sub_orders
    }