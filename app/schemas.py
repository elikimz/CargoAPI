from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "customer"
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    sub: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    preferred_language: Optional[str] = None  # Allow users to update later
    company_name: Optional[str] = None  # Allow users to update later
    is_active: bool

    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    preferred_language: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True





class CargoCreate(BaseModel):
    tracking_number: str
    description: str
    weight: Optional[float] = None
    receiver_id: int  # Sender ID is automatically assigned
    current_location: Optional[str] = None
    status: Optional[str] = "pending"  # Default status

class CargoResponse(BaseModel):
    id: int
    tracking_number: str
    description: str
    weight: Optional[float] = None
    sender_id: int
    receiver_id: int
    current_location: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class TrackingCreate(BaseModel):
    cargo_id: int
    location: str
    status: str  # "in transit" or "delivered"

class TrackingResponse(TrackingCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True



class NotificationCreate(BaseModel):
    user_id: int
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    sent_at: datetime

    class Config:
        orm_mode = True
