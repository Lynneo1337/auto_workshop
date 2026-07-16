from sqlalchemy.orm import Session
from models import Client
from schemas import ClientCreate
import bcrypt


def get_password_hash(password: str) -> str:
    """Превращает обычный пароль в безопасный хеш с помощью bcrypt"""
    pwd_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли введенный пароль с хешем в базе (понадобится для входа)"""
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def create_client(db: Session, client_data: ClientCreate) -> Client:
    """Создает нового клиента в базе данных"""
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