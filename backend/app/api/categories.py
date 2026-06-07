from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/categories", tags=["categories"])


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


def _get_all_children_ids(cat: Category) -> list[str]:
    """递归获取所有子分类 ID"""
    ids = [cat.id]
    for child in cat.children:
        ids.extend(_get_all_children_ids(child))
    return ids


@router.delete("/{cat_id}")
def delete_category(cat_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == cat_id, Category.user_id == user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    # Unlink reminders before deleting category (包括子分类的提醒)
    from app.models.reminder import Reminder
    all_ids = _get_all_children_ids(cat)
    db.query(Reminder).filter(Reminder.category_id.in_(all_ids)).update({Reminder.category_id: None}, synchronize_session=False)
    db.delete(cat)
    db.commit()
    return {"ok": True}
