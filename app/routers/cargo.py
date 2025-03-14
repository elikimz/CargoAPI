from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Cargo, User
from app.schemas import CargoCreate, CargoResponse
from app.database import get_db
from app.routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("", response_model=CargoResponse)
def create_cargo(
    cargo_data: CargoCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Create a new cargo shipment. Sender is set automatically."""
    new_cargo = Cargo(
        tracking_number=cargo_data.tracking_number,
        description=cargo_data.description,
        weight=cargo_data.weight,
        sender_id=current_user.id,  # Auto-assign sender_id from authenticated user
        receiver_id=cargo_data.receiver_id,
        current_location=cargo_data.current_location,
        status=cargo_data.status,
        created_at=datetime.utcnow()
    )
    db.add(new_cargo)
    db.commit()
    db.refresh(new_cargo)
    return new_cargo

@router.get("/{cargo_id}", response_model=CargoResponse)
def get_cargo(cargo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve cargo details by ID. Sender or receiver can access it."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    if cargo.sender_id != current_user.id and cargo.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this cargo")

    return cargo

@router.get("", response_model=list[CargoResponse])
def get_all_cargo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve all cargo related to the authenticated user (sent or received)."""
    cargo_list = db.query(Cargo).filter(
        (Cargo.sender_id == current_user.id) | (Cargo.receiver_id == current_user.id)
    ).all()

    return cargo_list

@router.put("/{cargo_id}", response_model=CargoResponse)
def update_cargo(
    cargo_id: int, 
    cargo_update: CargoCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Update cargo details. Only the sender can update it."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    if cargo.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only sender can update this cargo")

    # Update fields
    cargo.tracking_number = cargo_update.tracking_number or cargo.tracking_number
    cargo.description = cargo_update.description or cargo.description
    cargo.weight = cargo_update.weight or cargo.weight
    cargo.current_location = cargo_update.current_location or cargo.current_location
    cargo.status = cargo_update.status or cargo.status

    db.commit()
    db.refresh(cargo)
    return cargo

@router.delete("/{cargo_id}")
def delete_cargo(cargo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete cargo. Only the sender can delete it."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    if cargo.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only sender can delete this cargo")

    db.delete(cargo)
    db.commit()
    return {"message": "Cargo deleted successfully"}
