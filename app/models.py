from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base  # Assuming database.py initializes SQLAlchemy

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)  # Hashed password
    role = Column(Enum("admin", "customer", name="user_roles"), default="customer")
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    preferred_language = Column(String(50), nullable=True)  # Allow users to update this later
    company_name = Column(String(100), nullable=True)  # Allow users to update this later
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    sent_cargo = relationship("Cargo", foreign_keys="Cargo.sender_id", back_populates="sender")
    received_cargo = relationship("Cargo", foreign_keys="Cargo.receiver_id", back_populates="receiver")
    notifications = relationship("Notification", back_populates="user")

class Cargo(Base):
    __tablename__ = "cargo"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    weight = Column(Float, nullable=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    current_location = Column(String(100), nullable=True)
    status = Column(Enum("pending", "in transit", "delivered", name="cargo_status"), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_cargo")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_cargo")
    tracking_history = relationship("Tracking", back_populates="cargo", cascade="all, delete-orphan")

class Tracking(Base):
    __tablename__ = "tracking"

    id = Column(Integer, primary_key=True, index=True)
    cargo_id = Column(Integer, ForeignKey("cargo.id"), nullable=False)
    location = Column(String(100), nullable=False)
    status = Column(Enum("in transit", "delivered", name="tracking_status"), default="in transit")
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cargo = relationship("Cargo", back_populates="tracking_history")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")
