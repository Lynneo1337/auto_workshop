from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from models import Client, Car, Service, Bay, Callback_Request, Mechanic, Admin, Order, Order_Item, Discount_Rule, Order, Order_Item, Service, Mechanic
from schemas import ClientCreate, CarCreate, ServiceCreate, CallbackRequestCreate, OrderCreate, OrderCloseRequest
import bcrypt
from datetime import datetime
from typing import List


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def get_client_by_email_or_phone(db: Session, email: str, phone: str):
    return db.query(Client).filter(
        or_(Client.email == email, Client.phone == phone)
    ).first()

def get_client_by_id(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def create_client(db: Session, client_data: ClientCreate) -> Client:
    hashed_password = get_password_hash(client_data.password)
    db_client = Client(
        full_name=client_data.full_name,
        phone=client_data.phone,
        email=client_data.email,
        password_hash=hashed_password,
        visit_count=0,
        current_discount=0.0
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_cars_by_client(db: Session, client_id: int):
    return db.query(Car).filter(Car.client_id == client_id).all()

def create_car(db: Session, car_data: CarCreate, client_id: int) -> Car:
    db_car = Car(**car_data.model_dump(), client_id=client_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def delete_car(db: Session, car_id: int, client_id: int) -> bool:
    car = db.query(Car).filter(Car.id == car_id, Car.client_id == client_id).first()
    if car:
        db.delete(car)
        db.commit()
        return True
    return False

def get_services(db: Session):
    return db.query(Service).all()

def create_service(db: Session, service_data: ServiceCreate) -> Service:
    db_service = Service(**service_data.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_bays(db: Session):
    return db.query(Bay).all()

def get_available_bays(db: Session, start_time: datetime, end_time: datetime):
    """Проверка доступности боксов (ФТ4)"""
    busy_bays = db.query(Bay.id).join(Order).filter(
        and_(
            Order.status.not_in(['Завершена', 'Отменена']),
            or_(
                and_(Order.planned_start <= start_time, Order.planned_end >= start_time),
                and_(Order.planned_start <= end_time, Order.planned_end >= end_time),
                and_(Order.planned_start >= start_time, Order.planned_end <= end_time)
            )
        )
    ).all()
    
    all_bays = db.query(Bay).all()
    available = [bay for bay in all_bays if bay.id not in [b[0] for b in busy_bays]]
    return available

def create_callback_request(db: Session, callback_data: CallbackRequestCreate) -> Callback_Request:
    db_callback = Callback_Request(**callback_data.model_dump())
    db.add(db_callback)
    db.commit()
    db.refresh(db_callback)
    return db_callback

def get_client_by_login(db: Session, login: str):
    return db.query(Client).filter(
        or_(Client.email == login, Client.phone == login)
    ).first()

def get_mechanic_by_login(db: Session, login: str):
    return db.query(Mechanic).filter(Mechanic.login == login).first()

def get_admin_by_login(db: Session, login: str):
    return db.query(Admin).filter(Admin.login == login).first()


def get_discount_percent(db: Session, visit_count: int) -> float:
    rule = db.query(Discount_Rule).filter(
        Discount_Rule.min_visits <= visit_count,
        Discount_Rule.max_visits >= visit_count
    ).first()
    
    return float(rule.discount_percent) if rule else 0.0

def is_bay_available(db: Session, bay_id: int, start: datetime, end: datetime) -> bool:
    bay = db.query(Bay).filter(Bay.id == bay_id).first()
    if not bay:
        return False
        
    overlapping_orders_count = db.query(func.count(Order.id)).filter(
        and_(
            Order.bay_id == bay_id,
            Order.status.notin_(['Завершена', 'Отменена']),
            Order.planned_start < end,
            Order.planned_end > start
        )
    ).scalar()
    
    return (overlapping_orders_count + 1) <= bay.capacity

def create_order(db: Session, order_data: OrderCreate) -> Order:
    if order_data.bay_id:
        if not is_bay_available(db, order_data.bay_id, order_data.planned_start, order_data.planned_end):
            raise ValueError("Выбранный бокс занят в это время или превышен лимит вместимости.")
            
    client = get_client_by_id(db, order_data.client_id)
    if not client:
        raise ValueError("Клиент не найден.")
        
    total_cost = 0.0
    order_items_data = []
    
    for item in order_data.items:
        service = db.query(Service).filter(Service.id == item.service_id).first()
        if not service:
            raise ValueError(f"Услуга с ID {item.service_id} не найдена.")
            
        item_cost = float(service.price) * item.quantity
        total_cost += item_cost
        order_items_data.append({
            "service_id": item.service_id,
            "quantity": item.quantity,
            "fact_price": service.price # Фактическая цена на момент создания
        })
        
    discount_percent = get_discount_percent(db, client.visit_count)
    discount_amount = total_cost * (discount_percent / 100)
    final_cost = total_cost - discount_amount
    
    db_order = Order(
        client_id=order_data.client_id,
        car_id=order_data.car_id,
        mechanic_id=order_data.mechanic_id,
        bay_id=order_data.bay_id,
        status="Ожидает", # Начальный статус
        planned_start=order_data.planned_start,
        planned_end=order_data.planned_end,
        payment_method=order_data.payment_method,
        total_cost=total_cost,
        discount_amount=discount_amount,
        final_cost=final_cost
    )
    
    db.add(db_order)
    db.flush() 
    
    for item_data in order_items_data:
        db_item = Order_Item(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_item)
        
    db.commit()
    db.refresh(db_order)
    
    return db_order

def complete_order_by_mechanic(db: Session, order_id: int, mechanic_id: int) -> Order:
    """
    Мастер отмечает заказ выполненным.
    Проверка: заказ должен быть назначен этому мастеру и быть в статусе 'В работе'.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Заказ не найден")
    if order.mechanic_id != mechanic_id:
        raise ValueError("Этот заказ не назначен вам")
    if order.status != "В работе":
        raise ValueError("Нельзя завершить работы: заказ не в статусе 'В работе'")
        
    order.status = "Выполнено"
    db.commit()
    db.refresh(order)
    return order

def close_order_by_admin(db: Session, order_id: int, close_data: OrderCloseRequest) -> Order:
    """
    Администратор закрывает заказ, принимает оплату и обновляет скидку клиента (ФТ3).
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Заказ не найден")
    if order.status not in ["Выполнено", "В работе"]:
        raise ValueError("Нельзя закрыть заказ с текущим статусом")
        
    order.status = "Завершена"
    order.payment_method = close_data.payment_method
    
    client = db.query(Client).filter(Client.id == order.client_id).first()
    if client:
        client.visit_count += 1
        
        rule = db.query(Discount_Rule).filter(
            Discount_Rule.min_visits <= client.visit_count,
            Discount_Rule.max_visits >= client.visit_count
        ).first()
        
        if rule:
            client.current_discount = rule.discount_percent
            
    db.commit()
    db.refresh(order)
    return order


def get_available_mechanics(db: Session, specialization: str, start: datetime, end: datetime) -> List[Mechanic]:
    """
    Находит свободных мастеров по специализации на заданное время.
    """
    mechanics = db.query(Mechanic).filter(Mechanic.specialization == specialization).all()
    
    available_mechanics = []
    
    for mechanic in mechanics:
        overlapping_orders = db.query(Order).filter(
            and_(
                Order.mechanic_id == mechanic.id,
                Order.status.notin_(['Завершена', 'Отменена']),
                Order.planned_start < end,
                Order.planned_end > start
            )
        ).count()
        
        if overlapping_orders == 0:
            available_mechanics.append(mechanic)
            
    return available_mechanics

def get_revenue_report(db: Session, start: datetime, end: datetime) -> dict:
    """
    Считает общую выручку и количество заказов за период.
    Учитываем только заказы со статусом 'Завершена'.
    """
    result = db.query(
        func.sum(Order.final_cost),
        func.count(Order.id)
    ).filter(
        Order.status == 'Завершена',
        Order.created_at >= start,
        Order.created_at <= end
    ).first()

    total_revenue = float(result[0]) if result[0] else 0.0
    
    return {
        "total_revenue": total_revenue,
        "total_orders": result[1]
    }

def get_popular_services_report(db: Session, start: datetime, end: datetime, limit: int = 5) -> list:
    """
    Находит топ самых заказываемых услуг за период.
    """
    result = db.query(
        Service.name,
        func.sum(Order_Item.quantity),
        func.sum(Order_Item.fact_price * Order_Item.quantity)
    ).join(Order_Item, Service.id == Order_Item.service_id)\
      .join(Order, Order_Item.order_id == Order.id)\
      .filter(
          Order.status == 'Завершена',
          Order.created_at >= start,
          Order.created_at <= end
      )\
      .group_by(Service.name).order_by(func.sum(Order_Item.quantity).desc()).limit(limit).all()

    return [
        {
            "service_name": row[0],
            "total_quantity": int(row[1]),
            "total_revenue": float(row[2])
        } for row in result
    ]