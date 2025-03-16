# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models import Cargo, User
# from app.schemas import CargoCreate, CargoUpdate, CargoResponse
# from app.database import get_db
# from app.routers.auth import get_current_user
# from datetime import datetime
# import json

# router = APIRouter()

# # Define allowed status values
# VALID_CARGO_STATUSES = {"pending", "in transit", "delivered"}

# @router.post("", response_model=CargoResponse)
# def create_cargo(
#     cargo_data: CargoCreate, 
#     db: Session = Depends(get_db), 
#     current_user: User = Depends(get_current_user)
# ):
#     """Create a new cargo shipment. Sender is set automatically."""
    
#     # Validate ENUM status
#     if cargo_data.status not in VALID_CARGO_STATUSES:
#         raise HTTPException(status_code=400, detail="Invalid status value")

#     new_cargo = Cargo(
#         tracking_number=cargo_data.tracking_number,
#         description=cargo_data.description,
#         weight=cargo_data.weight,
#         sender_id=current_user.id,  # Auto-assign sender_id from authenticated user
#         receiver_id=cargo_data.receiver_id,
#         current_location=cargo_data.current_location,
#         status=cargo_data.status,
#         created_at=datetime.utcnow()
#     )
    
#     db.add(new_cargo)
#     db.commit()
#     db.refresh(new_cargo)
#     return new_cargo

# @router.get("/{cargo_id}", response_model=CargoResponse)
# def get_cargo(cargo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     """Retrieve cargo details by ID. Sender or receiver can access it."""
#     cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    
#     if not cargo:
#         raise HTTPException(status_code=404, detail="Cargo not found")

#     if cargo.sender_id != current_user.id and cargo.receiver_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized to view this cargo")

#     return cargo

# @router.get("", response_model=list[CargoResponse])
# def get_all_cargo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     """Retrieve all cargo related to the authenticated user (sent or received)."""
#     cargo_list = db.query(Cargo).filter(
#         (Cargo.sender_id == current_user.id) | (Cargo.receiver_id == current_user.id)
#     ).all()  # Don't use LIMIT here
    
#     return cargo_list

# @router.put("/{cargo_id}", response_model=CargoResponse)
# def update_cargo(
#     cargo_id: int, 
#     cargo_update: CargoUpdate, 
#     db: Session = Depends(get_db), 
#     current_user: User = Depends(get_current_user)
# ):
#     """Update cargo details. Only the sender can update it."""
#     cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()

#     if not cargo:
#         raise HTTPException(status_code=404, detail="Cargo not found")

#     if cargo.sender_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Only sender can update this cargo")
    
#     # Debugging: Print received data
#     print("Received Update Data:", json.dumps(cargo_update.dict(), indent=4))

#     # Validate ENUM status
#     if cargo_update.status and cargo_update.status not in VALID_CARGO_STATUSES:
#         raise HTTPException(status_code=400, detail="Invalid status value")

#     if not any([cargo_update.tracking_number, cargo_update.description, cargo_update.weight, cargo_update.current_location, cargo_update.status]):
#         raise HTTPException(status_code=400, detail="No fields to update")

#     # Update fields explicitly if provided
#     if cargo_update.tracking_number is not None:
#         cargo.tracking_number = cargo_update.tracking_number
#     if cargo_update.description is not None:
#         cargo.description = cargo_update.description
#     if cargo_update.weight is not None:
#         cargo.weight = cargo_update.weight
#     if cargo_update.current_location is not None:
#         cargo.current_location = cargo_update.current_location
#     if cargo_update.status is not None:
#         cargo.status = cargo_update.status
    
#     db.commit()
#     db.refresh(cargo)
#     return cargo

# @router.delete("/{cargo_id}")
# def delete_cargo(cargo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     """Delete cargo. Only the sender can delete it."""
#     cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()

#     if not cargo:
#         raise HTTPException(status_code=404, detail="Cargo not found")

#     if cargo.sender_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Only sender can delete this cargo")

#     db.delete(cargo)
#     db.commit()
#     return {"message": "Cargo deleted successfully"}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Cargo, User
from app.schemas import CargoCreate, CargoUpdate, CargoResponse
from app.database import get_db
from app.routers.auth import get_current_user
from datetime import datetime
import json

router = APIRouter()

# Define allowed status values
VALID_CARGO_STATUSES = {"pending", "in transit", "delivered",}

@router.post("", response_model=CargoResponse)
def create_cargo(
    cargo_data: CargoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new cargo shipment. Sender is set automatically."""

    # Validate ENUM status
    if cargo_data.status not in VALID_CARGO_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status value")

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

    if current_user.role != "admin" and cargo.sender_id != current_user.id and cargo.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this cargo")

    return cargo

@router.get("", response_model=list[CargoResponse])
def get_all_cargo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve all cargo related to the authenticated user (sent or received)."""
    if current_user.role == "admin":
        cargo_list = db.query(Cargo).all()
    else:
        cargo_list = db.query(Cargo).filter(
            (Cargo.sender_id == current_user.id) | (Cargo.receiver_id == current_user.id)
        ).all()  # Don't use LIMIT here

    return cargo_list

@router.put("/{cargo_id}", response_model=CargoResponse)
def update_cargo(
    cargo_id: int,
    cargo_update: CargoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update cargo details. Only the sender or admin can update it."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    if current_user.role != "admin" and cargo.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only sender or admin can update this cargo")

    # Debugging: Print received data
    print("Received Update Data:", json.dumps(cargo_update.dict(), indent=4))

    # Validate ENUM status
    if cargo_update.status and cargo_update.status not in VALID_CARGO_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status value")

    if not any([cargo_update.tracking_number, cargo_update.description, cargo_update.weight, cargo_update.current_location, cargo_update.status]):
        raise HTTPException(status_code=400, detail="No fields to update")

    # Update fields explicitly if provided
    if cargo_update.tracking_number is not None:
        cargo.tracking_number = cargo_update.tracking_number
    if cargo_update.description is not None:
        cargo.description = cargo_update.description
    if cargo_update.weight is not None:
        cargo.weight = cargo_update.weight
    if cargo_update.current_location is not None:
        cargo.current_location = cargo_update.current_location
    if cargo_update.status is not None:
        cargo.status = cargo_update.status

    db.commit()
    db.refresh(cargo)
    return cargo

@router.delete("/{cargo_id}")
def delete_cargo(cargo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete cargo. Only the sender or admin can delete it."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    if current_user.role != "admin" and cargo.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only sender or admin can delete this cargo")

    db.delete(cargo)
    db.commit()
    return {"message": "Cargo deleted successfully"}
