from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def get_or_create_user(db: Session, user_data: UserCreate) -> User:
    user = db.query(User).filter(User.device_id == user_data.device_id).first()
    if user:
        if user_data.api_key:
            user.api_key_encrypted = user_data.api_key
        if user_data.api_provider:
            user.api_provider = user_data.api_provider
        db.commit()
        db.refresh(user)
        return user

    user = User(
        device_id=user_data.device_id,
        api_key_encrypted=user_data.api_key,
        api_provider=user_data.api_provider,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_device(db: Session, device_id: str) -> User | None:
    return db.query(User).filter(User.device_id == device_id).first()
