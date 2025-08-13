# Esquemas para el módulo de Salas

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class RoomBase(BaseModel):
    """Schema base para salas"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la sala")
    sede: str = Field(..., min_length=2, max_length=100, description="Sede donde se encuentra la sala")
    capacidad: int = Field(..., ge=1, le=50, description="Capacidad máxima de personas")
    recursos: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Recursos disponibles")

class RoomCreate(RoomBase):
    """Schema para crear una sala"""
    
    @validator('nombre')
    def validate_nombre(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('El nombre no puede estar vacío')
        return v.title()
    
    @validator('sede')
    def validate_sede(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('La sede no puede estar vacía')
        return v.title()
    
    @validator('recursos')
    def validate_recursos(cls, v):
        if v is None:
            return {}
        
        # Recursos permitidos
        allowed_recursos = {
            'proyector', 'wifi', 'pizarra', 'aire_acondicionado', 
            'video_conferencia', 'sonido', 'computador', 'tv'
        }
        
        if isinstance(v, dict):
            for key in v.keys():
                if key not in allowed_recursos:
                    raise ValueError(f'Recurso {key} no es válido. Recursos permitidos: {allowed_recursos}')
        
        return v

class RoomUpdate(BaseModel):
    """Schema para actualizar una sala"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    sede: Optional[str] = Field(None, min_length=2, max_length=100)
    capacidad: Optional[int] = Field(None, ge=1, le=50)
    recursos: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    
    @validator('nombre')
    def validate_nombre(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('El nombre no puede estar vacío')
            return v.title()
        return v
    
    @validator('sede')
    def validate_sede(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('La sede no puede estar vacía')
            return v.title()
        return v

class RoomResponse(BaseModel):
    """Schema para respuestas de salas"""
    id: int
    nombre: str
    sede: str
    capacidad: int
    recursos: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Sala Reuniones A",
                "sede": "Campus Norte",
                "capacidad": 8,
                "recursos": {
                    "proyector": True,
                    "wifi": True,
                    "pizarra": True,
                    "aire_acondicionado": True
                },
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }

class RoomSummary(BaseModel):
    """Schema resumido para listados"""
    id: int
    nombre: str
    sede: str
    capacidad: int
    is_active: bool
    recursos_count: int = 0
    
    class Config:
        from_attributes = True

class RoomList(BaseModel):
    """Schema para listas paginadas de salas"""
    rooms: List[RoomSummary]
    total: int
    page: int
    per_page: int
    pages: int
    
    class Config:
        schema_extra = {
            "example": {
                "rooms": [
                    {
                        "id": 1,
                        "nombre": "Sala Reuniones A",
                        "sede": "Campus Norte",
                        "capacidad": 8,
                        "is_active": True,
                        "recursos_count": 4
                    }
                ],
                "total": 25,
                "page": 1,
                "per_page": 10,
                "pages": 3
            }
        }

class RoomAvailability(BaseModel):
    """Schema para consultar disponibilidad"""
    room_id: int
    date: str
    available_slots: List[str]
    occupied_slots: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "room_id": 1,
                "date": "2024-02-15",
                "available_slots": ["09:00-10:00", "10:00-11:00", "14:00-15:00"],
                "occupied_slots": ["11:00-12:00", "13:00-14:00"]
            }
        }