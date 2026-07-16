from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from decimal import Decimal

# Базовая схема с общими полями
class ClientBase(BaseModel):
    full_name: str = Field(..., min_length=3, description="ФИО клиента")
    phone: str = Field(..., min_length=12, max_length=12, description="Номер телефона")
    email: EmailStr = Field(..., description="Корректный email адрес")

    @field_validator('phone', mode='before')
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        
        # Очищаем номер от пробелов, тире и скобок
        clean_v = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Если пользователь ввел 89..., меняем 8 на +7
        if clean_v.startswith('8') and len(clean_v) == 11 and clean_v[1:].isdigit():
            return '+7' + clean_v[1:]
            
        # Если пользователь ввел 79..., добавляем +
        if clean_v.startswith('7') and len(clean_v) == 11 and clean_v[1:].isdigit():
            return '+7' + clean_v[1:]
        
        # Должно быть строго +7 и 10 цифр (всего 12 символов)
        if not (clean_v.startswith('+7') and len(clean_v) == 12 and clean_v[2:].isdigit()):
            raise ValueError('Телефон должен быть в формате +7XXXXXXXXXX (например, +79001234567)')
        
        return clean_v

# Схема для создания клиента
class ClientCreate(ClientBase):
    password: str = Field(..., min_length=6, max_length=72, description="Пароль для входа")

# Схема для ответа
class ClientResponse(ClientBase):
    id: int
    visit_count: int
    current_discount: Decimal

    class Config:
        from_attributes = True