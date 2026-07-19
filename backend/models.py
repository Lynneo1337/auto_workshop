from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, comment="ФИО")
    phone = Column(String, unique=True, index=True, comment="Используется для входа")
    email = Column(String, unique=True, index=True, comment="Используется для входа")
    password_hash = Column(String, comment="Хеш пароля (НФТ2)")
    visit_count = Column(Integer, default=0, comment="Счетчик посещений для ФТ3")
    current_discount = Column(Numeric, default=0.0, comment="Текущий % скидки")
    
    cars = relationship("Car", back_populates="client", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="client")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), comment="Связь с клиентом (ФТ1)")
    brand_model = Column(String, comment="Марка и модель")
    license_plate = Column(String, comment="Гос. номер")
    vin = Column(String, comment="VIN-код")
    
    client = relationship("Client", back_populates="cars")
    orders = relationship("Order", back_populates="car")

class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, comment="ФИО мастера")
    specialization = Column(String, comment="Профиль мастера (ФТ2)")
    login = Column(String, unique=True, index=True, comment="Логин для входа")
    password_hash = Column(String, comment="Хеш пароля")

    orders = relationship("Order", back_populates="mechanic")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, comment="ФИО администратора")
    login = Column(String, unique=True, index=True, comment="Логин для входа")
    password_hash = Column(String, comment="Хеш пароля")

class Bay(Base):
    __tablename__ = "bays"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, comment="Номер бокса")
    capacity = Column(Integer, default=2, comment="Лимит вместимости (ФТ4)")
    
    orders = relationship("Order", back_populates="bay")

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, comment="Название услуги (ФТ6)")
    price = Column(Numeric, comment="Фиксированная цена")
    req_specialization = Column(String, comment="Требуемый профиль мастера")
    
    order_items = relationship("Order_Item", back_populates="service")

class Discount_Rule(Base):
    __tablename__ = "discount_rules"

    id = Column(Integer, primary_key=True, index=True)
    min_visits = Column(Integer, comment="Минимальное количество посещений")
    max_visits = Column(Integer, comment="Максимальное количество посещений")
    discount_percent = Column(Numeric, comment="Правила начисления скидок (ФТ3)")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, comment="Заказ-наряд (ФТ2)")
    client_id = Column(Integer, ForeignKey("clients.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"), comment="Назначенный мастер")
    bay_id = Column(Integer, ForeignKey("bays.id"), comment="Назначенный бокс")
    status = Column(String, comment="Ожидает / В работе / Выполнено / Завершена")
    planned_start = Column(DateTime, comment="Планируемое начало")
    planned_end = Column(DateTime, comment="Планируемое окончание")
    total_cost = Column(Numeric, comment="Общая стоимость до скидки")
    discount_amount = Column(Numeric, comment="Сумма скидки")
    final_cost = Column(Numeric, comment="Итоговая стоимость")
    payment_method = Column(String, comment="Способ оплаты")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Дата создания")
    
    client = relationship("Client", back_populates="orders")
    car = relationship("Car", back_populates="orders")
    mechanic = relationship("Mechanic", back_populates="orders")
    bay = relationship("Bay", back_populates="orders")
    order_items = relationship("Order_Item", back_populates="order", cascade="all, delete-orphan")

class Order_Item(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), comment="Связь с заказ-нарядом")
    service_id = Column(Integer, ForeignKey("services.id"), comment="Связь с услугой")
    quantity = Column(Integer, default=1, comment="Количество")
    fact_price = Column(Numeric, comment="Фактическая цена")
    
    order = relationship("Order", back_populates="order_items")
    service = relationship("Service", back_populates="order_items")

class Callback_Request(Base):
    __tablename__ = "callback_requests"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, comment="Имя клиента")
    phone = Column(String, comment="Телефон для связи")
    status = Column(String, default="Ожидает обработки", comment="Ожидает обработки / Обработана")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Дата создания")