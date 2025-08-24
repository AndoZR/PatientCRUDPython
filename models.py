from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    tanggal_kunjungan = Column(Date, nullable=False)
    diagnosis = Column(Text)
    tindakan = Column(Text)
    dokter = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="admin")  # admin, dokter
    created_at = Column(DateTime(timezone=True), server_default=func.now())
