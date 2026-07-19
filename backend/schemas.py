from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class ClientBase(BaseModel):
    full_name: str = Field(..., min_length=2, description="ФИО клиента")
    phone: str = Field(..., min_length=12, max_length=12, description="Номер телефона")
    email: EmailStr = Field(..., description="Корректный email адрес")

    @field_validator('phone', mode='before')
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        clean_v = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if clean_v.startswith('8') and len(clean_v) == 11 and clean_v[1:].isdigit():
            return '+7' + clean_v[1:]
        if clean_v.startswith('7') and len(clean_v) == 11 and clean_v[1:].isdigit():
            return '+7' + clean_v[1:]
        if not (clean_v.startswith('+7') and len(clean_v) == 12 and clean_v[2:].isdigit()):
            raise ValueError('Телефон должен быть в формате +7XXXXXXXXXX')
        return clean_v

class ClientCreate(ClientBase):
    password: str = Field(..., min_length=6, max_length=72, description="Пароль")

class ClientResponse(ClientBase):
    id: int
    visit_count: int
    current_discount: Decimal

    class Config:
        from_attributes = True

class CarBase(BaseModel):
    brand_model: str = Field(..., min_length=2, description="Марка и модель")
    license_plate: str = Field(..., description="Гос. номер")
    vin: Optional[str] = Field(None, description="VIN-код")

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int
    client_id: int

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, description="Название услуги")
    price: Decimal = Field(..., gt=0, description="Цена услуги")
    req_specialization: Optional[str] = Field(None, description="Требуемый профиль мастера")

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True

class BayBase(BaseModel):
    number: str = Field(..., description="Номер бокса")
    capacity: int = Field(default=2, ge=1, description="Вместимость")

class BayCreate(BayBase):
    pass

class BayResponse(BayBase):
    id: int

    class Config:
        from_attributes = True

class CallbackRequestBase(BaseModel):
    client_name: str = Field(..., min_length=2, description="Имя клиента")
    phone: str = Field(..., description="Телефон")

    @field_validator('phone', mode='before')
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        clean_v = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if clean_v.startswith('8') and len(clean_v) == 11:
            return '+7' + clean_v[1:]
        if clean_v.startswith('7') and len(clean_v) == 11:
            return '+7' + clean_v[1:]
        return clean_v

class CallbackRequestCreate(CallbackRequestBase):
    pass

class CallbackRequestResponse(CallbackRequestBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    login: str = Field(..., description="Email или телефон")
    password: str = Field(..., description="Пароль")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OrderItemCreate(BaseModel):
    service_id: int = Field(..., description="ID услуги из справочника")
    quantity: int = Field(default=1, ge=1, description="Количество")

class OrderCreate(BaseModel):
    client_id: int
    car_id: int
    mechanic_id: Optional[int] = Field(None, description="ID мастера (можно назначить позже)")
    bay_id: Optional[int] = Field(None, description="ID бокса (можно назначить позже)")
    planned_start: datetime
    planned_end: datetime
    payment_method: Optional[str] = None
    items: List[OrderItemCreate] = Field(..., description="Список услуг")

class OrderResponse(BaseModel):
    id: int
    client_id: int
    car_id: int
    mechanic_id: Optional[int]
    bay_id: Optional[int]
    status: str
    planned_start: datetime
    planned_end: datetime
    total_cost: Decimal
    discount_amount: Decimal
    final_cost: Decimal
    
    class Config:
        from_attributes = True