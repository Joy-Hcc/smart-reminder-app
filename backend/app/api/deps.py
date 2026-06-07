from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services import auth_service, token_service


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    token = authorization.replace("Bearer ", "")
    token_data = token_service.verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
