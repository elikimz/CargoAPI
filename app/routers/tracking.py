from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Tracking, Cargo
from app.schemas import TrackingCreate, TrackingResponse
from datetime import datetime

router = APIRouter()


@router.post("", response_model=TrackingResponse)
def create_tracking(tracking_data: TrackingCreate, db: Session = Depends(get_db)):
    """Create a new tracking record for cargo movement."""
    cargo = db.query(Cargo).filter(Cargo.id == tracking_data.cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    new_tracking = Tracking(
        cargo_id=tracking_data.cargo_id,
        location=tracking_data.location,
        status=tracking_data.status,
        timestamp=datetime.utcnow(),
    )

    db.add(new_tracking)
    db.commit()
    db.refresh(new_tracking)
    return new_tracking


@router.get("/{cargo_id}", response_model=list[TrackingResponse])
def get_tracking_by_cargo(cargo_id: int, db: Session = Depends(get_db)):
    """Retrieve tracking history for a specific cargo."""
    tracking_history = db.query(Tracking).filter(Tracking.cargo_id == cargo_id).all()
    if not tracking_history:
        raise HTTPException(status_code=404, detail="No tracking history found")
    return tracking_history


@router.put("/{tracking_id}", response_model=TrackingResponse)
def update_tracking(tracking_id: int, tracking_data: TrackingCreate, db: Session = Depends(get_db)):
    """Update tracking status or location."""
    tracking_entry = db.query(Tracking).filter(Tracking.id == tracking_id).first()
    if not tracking_entry:
        raise HTTPException(status_code=404, detail="Tracking entry not found")

    tracking_entry.location = tracking_data.location
    tracking_entry.status = tracking_data.status
    tracking_entry.timestamp = datetime.utcnow()

    db.commit()
    db.refresh(tracking_entry)
    return tracking_entry


@router.delete("/{tracking_id}")
def delete_tracking(tracking_id: int, db: Session = Depends(get_db)):
    """Delete a tracking entry."""
    tracking_entry = db.query(Tracking).filter(Tracking.id == tracking_id).first()
    if not tracking_entry:
        raise HTTPException(status_code=404, detail="Tracking entry not found")

    db.delete(tracking_entry)
    db.commit()
    return {"message": "Tracking entry deleted successfully"}
