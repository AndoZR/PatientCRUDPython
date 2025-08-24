from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Patient schemas
class PatientBase(BaseModel):
    nama: str
    tanggal_lahir: date
    tanggal_kunjungan: date
    diagnosis: Optional[str] = None
    tindakan: Optional[str] = None
    dokter: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    nama: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    tanggal_kunjungan: Optional[date] = None
    diagnosis: Optional[str] = None
    tindakan: Optional[str] = None
    dokter: Optional[str] = None

class Patient(PatientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str
    role: str = "admin"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
