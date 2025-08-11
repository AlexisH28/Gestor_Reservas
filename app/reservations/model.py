
# Representa las Reservas de Salas


from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.utils.database import Base


class ReservationStatus(str, enum.Enum):
    """Estados posibles de una reserva"""
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"


class Reservation(Base):
    __tablename__ = "reservations"
    
    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)
    
    # Llaves foráneas
    usuario_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    sala_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Información de la reserva
    fecha = Column(Date, nullable=False, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    
    # Estado de la reserva
    estado = Column(
        Enum(ReservationStatus),
        default=ReservationStatus.CONFIRMADA,
        nullable=False,
        index=True
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    usuario = relationship("User", back_populates="reservas")
    sala = relationship("Room", back_populates="reservas")
    
    def __repr__(self):
        return f"<Reservation(id={self.id}, usuario_id={self.usuario_id}, sala_id={self.sala_id})>"