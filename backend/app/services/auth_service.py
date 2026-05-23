import hashlib
import base64
import logging
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from app.models.user import User
from app.schemas.user import UserCreate
from app.config import get_settings

logger = logging.getLogger(__name__)

_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        key = get_settings().secret_key
        raw = hashlib.sha256(key.encode()).digest()
        _fernet = Fernet(base64.urlsafe_b64encode(raw))
    return _fernet


def encrypt_api_key(api_key: str) -> str:
    return _get_fernet().encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted: str) -> str:
    return _get_fernet().decrypt(encrypted.encode()).decode()


def get_or_create_user(db: Session, user_data: UserCreate) -> User:
    user = db.query(User).filter(User.device_id == user_data.device_id).first()
    if user:
        if user_data.email:
            user.email = user_data.email
        if user_data.api_key:
            user.api_key_encrypted = encrypt_api_key(user_data.api_key)
        if user_data.api_provider:
            user.api_provider = user_data.api_provider
        db.commit()
        db.refresh(user)
        return user

    user = User(
        device_id=user_data.device_id,
        email=user_data.email,
        api_key_encrypted=encrypt_api_key(user_data.api_key) if user_data.api_key else None,
        api_provider=user_data.api_provider,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_device(db: Session, device_id: str) -> User | None:
    return db.query(User).filter(User.device_id == device_id).first()
