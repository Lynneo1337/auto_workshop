from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, comment="Уникальный ID клиента")
    full_name = Column(String, comment="ФИО")
    phone = Column(String, unique=True, index=True, comment="Используется для входа")
    email = Column(String, unique=True, index=True, comment="Используется для входа")
    password_hash = Column(String, comment="Хеш пароля")
    visit_count = Column(Integer, default=0, comment="Счетчик посещений")
    current_discount = Column(Numeric, default=0.0, comment="Текущий % скидки")