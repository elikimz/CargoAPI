from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Notification, User
from app.schemas import NotificationCreate, NotificationResponse
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.post("", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    """Allows an admin to send a notification to a user."""
    user = db.query(User).filter(User.id == notification.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_notification = Notification(
        user_id=notification.user_id,
        message=notification.message,
        sent_at=datetime.utcnow()
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification

@router.get("", response_model=list[NotificationResponse])
def get_all_notifications(db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    """Allows an admin to view all notifications."""
    return db.query(Notification).all()

@router.get("/me", response_model=list[NotificationResponse])
def get_user_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Allows a logged-in user to view their own notifications."""
    return db.query(Notification).filter(Notification.user_id == current_user.id).all()

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    """Allows an admin to delete a notification."""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
