from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services import auth_service


def get_current_user(x_device_id: str = Header(...), db: Session = Depends(get_db)) -> User:
    user = auth_service.get_user_by_device(db, x_device_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
