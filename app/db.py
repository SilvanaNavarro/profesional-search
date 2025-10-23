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