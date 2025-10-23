from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birthdate: str
    rut: str = Field(unique=True)
    email: str = Field(unique=True)
    phone: Optional[str] = None
    password_hash: str
    verified: bool = Field(default=False)


class Professional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    career: str
    rut: str = Field(unique=True)
    email: str = Field(unique=True)
    phone: Optional[str] = None
    password_hash: str
    description_services: str
    photo_profile_path: Optional[str] = None
    photo_id_card_path: Optional[str] = None
    certificate_path: Optional[str] = None
    verified: bool = Field(default=False)


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    professional_id: int = Field(foreign_key="professional.id")
    date: str
    time: str
    payment_id: Optional[str] = None
    payment_status: str = Field(default="pending")
    created_at: str


class ProfessionalAvailability(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    professional_id: int = Field(foreign_key="professional.id")
    date: str
    time_slot: str
    is_available: bool = Field(default=True)
    is_booked: bool = Field(default=False)


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    professional_id: int = Field(foreign_key="professional.id")
    booking_id: int = Field(foreign_key="booking.id", unique=True)
    rating: int
    comment: str
    created_at: str


from enum import Enum


class PlanType(str, Enum):
    BASICO = "basico"
    PROFESIONAL = "profesional"
    SENIOR = "senior"


class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    professional_id: int = Field(foreign_key="professional.id", unique=True)
    plan: PlanType = Field(default=PlanType.BASICO)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    payment_id: Optional[str] = None
    status: str = Field(default="active")


class ProfessionalMedia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    professional_id: int = Field(foreign_key="professional.id")
    media_type: str
    file_path: str
    description: Optional[str] = None