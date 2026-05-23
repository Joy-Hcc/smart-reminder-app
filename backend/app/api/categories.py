from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.services import auth_service

router = APIRouter(prefix="/api/categories", tags=["categories"])


def get_current_user(x_device_id: str = Header(...), db: Session = Depends(get_db)):
    user = auth_service.get_user_by_device(db, x_device_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@router.get("", response_model=list[CategoryOut])
def list_categories(user=Depends(get_current_user), db: Session = Depends(get_db)):
    cats = db.query(Category).filter(Category.user_id == user.id, Category.parent_id == None).order_by(Category.sort_order).all()
    return cats


@router.post("", response_model=CategoryOut)
def create_category(data: CategoryCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    cat = Category(user_id=user.id, **data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.put("/{cat_id}", response_model=CategoryOut)
def update_category(cat_id: str, data: CategoryUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == cat_id, Category.user_id == user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}")
def delete_category(cat_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == cat_id, Category.user_id == user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"ok": True}
