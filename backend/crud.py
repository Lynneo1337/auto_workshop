from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import Client, Car, Service, Bay, Callback_Request, Mechanic, Admin, Order, Order_Item, Discount_Rule
from schemas import ClientCreate, CarCreate, ServiceCreate, CallbackRequestCreate
import bcrypt
from datetime import datetime

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