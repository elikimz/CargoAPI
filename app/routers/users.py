
from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.routers.auth import get_current_user, require_role
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserResponse, UserUpdate




router = APIRouter()



@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Retrieve all users (admin only)."""
    users = db.query(User).all()
    return users

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Allows anyone to update any user's detailss."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields only if they are provided
    user.phone_number = user_update.phone_number or user.phone_number
    user.address = user_update.address or user.address
    user.preferred_language = user_update.preferred_language or user.preferred_language
    user.company_name = user_update.company_name or user.company_name

    db.commit()
    db.refresh(user)
    return user

    # Retrieve the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields only if they are provided
    user.phone_number = user_update.phone_number or user.phone_number
    user.address = user_update.address or user.address
    user.preferred_language = user_update.preferred_language or user.preferred_language
    user.company_name = user_update.company_name or user.company_name

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """Allows admin to delete a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
