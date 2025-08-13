# Esquemas para el módulo de Reservas

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date, time
from app.reservations.model import ReservationStatus

class ReservationBase(BaseModel):
    """Schema base para reservas"""
    sala_id: int = Field(..., gt=0, description="ID de la sala a reservar")
    fecha: date = Field(..., description="Fecha de la reserva")
    hora_inicio: time = Field(..., description="Hora de inicio (formato HH:MM)")
    hora_fin: time = Field(..., description="Hora de fin (formato HH:MM)")

class ReservationCreate(ReservationBase):
    @validator('fecha')
    def validate_fecha(cls, v):
        if v < date.today():
            raise ValueError('No se pueden hacer reservas en fechas pasadas')
        
        # No más de 30 días de anticipación
        from datetime import timedelta
        max_date = date.today() + timedelta(days=30)
        if v > max_date:
            raise ValueError('No se pueden hacer reservas con más de 30 días de anticipación')
        
        return v
    
    @validator('hora_fin')
    def validate_horario(cls, v, values):
        if 'hora_inicio' not in values:
            return v
        
        hora_inicio = values['hora_inicio']
        
        # Verificar que hora_fin sea después de hora_inicio
        if v <= hora_inicio:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        
        # Verificar que sea exactamente 1 hora
        inicio_minutes = hora_inicio.hour * 60 + hora_inicio.minute
        fin_minutes = v.hour * 60 + v.minute
        duracion = fin_minutes - inicio_minutes
        
        if duracion != 60:
            raise ValueError('Las reservas deben ser de exactamente 1 hora')
        
        # Verificar horarios de trabajo (8:00 - 18:00)
        if hora_inicio.hour < 8 or v.hour > 18:
            raise ValueError('Las reservas solo pueden hacerse entre 8:00 y 18:00')
        
        # Verificar que sean en punto
        if hora_inicio.minute != 0 or v.minute != 0:
            raise ValueError('Las reservas solo pueden hacerse en horarios en punto (ej: 09:00-10:00)')
        
        return v

class ReservationUpdate(BaseModel):
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    
    @validator('fecha')
    def validate_fecha(cls, v):
        if v and v < date.today():
            raise ValueError('No se pueden reprogramar reservas a fechas pasadas')
        return v

class ReservationResponse(BaseModel):
    id: int
    usuario_id: int
    sala_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: ReservationStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Información relacionada (se llena en el service)
    usuario_nombre: Optional[str] = None
    sala_nombre: Optional[str] = None
    sala_sede: Optional[str] = None
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "usuario_id": 1,
                "sala_id": 1,
                "fecha": "2024-02-15",
                "hora_inicio": "09:00:00",
                "hora_fin": "10:00:00",
                "estado": "confirmada",
                "created_at": "2024-02-01T10:30:00",
                "usuario_nombre": "Juan Pérez",
                "sala_nombre": "Sala Reuniones A",
                "sala_sede": "Campus Norte"
            }
        }

class ReservationSummary(BaseModel):
    id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: ReservationStatus
    sala_nombre: str
    sala_sede: str
    
    class Config:
        from_attributes = True

class ReservationList(BaseModel):
    reservations: List[ReservationSummary]
    total: int
    page: int
    per_page: int
    pages: int

class ReservationStats(BaseModel):
    total_reservations: int
    active_reservations: int
    cancelled_reservations: int
    this_month_reservations: int
    most_used_room: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "total_reservations": 45,
                "active_reservations": 12,
                "cancelled_reservations": 5,
                "this_month_reservations": 18,
                "most_used_room": "Sala Reuniones A"
            }
        }

class ReservationFilter(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    sala_id: Optional[int] = None
    estado: Optional[ReservationStatus] = None
    usuario_id: Optional[int] = None  # Solo para admin

# Schema para cancelación de reserva
class ReservationCancel(BaseModel):
    motivo: Optional[str] = Field(None, max_length=200, description="Motivo de la cancelación")

# Schema para el dashboard
class UserReservationDashboard(BaseModel):
    upcoming_reservations: List[ReservationSummary]
    past_reservations_count: int
    cancelled_reservations_count: int
    total_hours_reserved: int
    
    class Config:
        schema_extra = {
            "example": {
                "upcoming_reservations": [
                    {
                        "id": 1,
                        "fecha": "2024-02-15",
                        "hora_inicio": "09:00:00",
                        "hora_fin": "10:00:00",
                        "estado": "confirmada",
                        "sala_nombre": "Sala A",
                        "sala_sede": "Campus Norte"
                    }
                ],
                "past_reservations_count": 10,
                "cancelled_reservations_count": 2,
                "total_hours_reserved": 25
            }
        }