from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/verify", response_model=UserOut)
def verify_auth(data: UserCreate, db: Session = Depends(get_db)):
    if not data.device_id:
        raise HTTPException(status_code=400, detail="device_id required")
    user = auth_service.get_or_create_user(db, data)
    return user


@router.get("/profile", response_model=UserOut)
def get_profile(x_device_id: str = Header(...), db: Session = Depends(get_db)):
    user = auth_service.get_user_by_device(db, x_device_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
