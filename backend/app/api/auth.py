from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut, AuthResponse
from app.services import auth_service, token_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/verify", response_model=AuthResponse)
def verify_auth(data: UserCreate, db: Session = Depends(get_db)):
    if not data.device_id:
        raise HTTPException(status_code=400, detail="device_id required")
    user = auth_service.get_or_create_user(db, data)
    token = token_service.generate_token(user.id, user.device_id)
    return AuthResponse(user=UserOut.model_validate(user), token=token)


@router.get("/profile", response_model=UserOut)
def get_profile(user=Depends(get_current_user)):
    return user


@router.post("/logout")
def logout(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if token_service.revoke_token(token):
        return {"ok": True}
    raise HTTPException(status_code=401, detail="Invalid token")
