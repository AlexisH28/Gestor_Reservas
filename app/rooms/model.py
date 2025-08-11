# Representación Salas de Coworking 

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import List, Optional
import json

from app.utils.database import Base

class Room(Base):
    """
    Modelo Room - Representa una sala de coworking
    """
    __tablename__ = "rooms"
    
    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)
    
    # Información básica
    nombre = Column(String(100), nullable=False, index=True)
    sede = Column(String(100), nullable=False, index=True)
    capacidad = Column(Integer, nullable=False)
    
    # Recursos disponibles (como JSON)
    recursos = Column(JSON, nullable=True)
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reservas = relationship(
        "Reservation",
        back_populates="sala",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Room(id={self.id}, nombre='{self.nombre}', sede='{self.sede}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "sede": self.sede,
            "capacidad": self.capacidad,
            "recursos": self.recursos,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }