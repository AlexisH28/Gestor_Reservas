from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.utils.database import Base

# Enum para Roles de Usuario

class UserRole(str, enum.Enum):
    USER = "user"      # Usuario normal --> puede hacer reservas
    ADMIN = "admin"    # Administrador --> puede gestionar todo

# Modelo User 

class User(Base):
    __tablename__ = "users"
    
    id = Column(
        Integer, 
        primary_key=True,    
        index=True,          
        autoincrement=True   
    )
    
    # Nombre completo del usuario
    nombre = Column(
        String(100),         
        nullable=False,      
        index=True          
    )
    
    # Email --> debe ser único en toda la tabla
    email = Column(
        String(255),        
        unique=True,        
        nullable=False,      
        index=True          
    )
    
    # Contraseña hasheada 
    contraseña_hash = Column(
        String(255),         
        nullable=False       
    )
    
    # Rol del usuario (user o admin)
    rol = Column(
        Enum(UserRole),      
        nullable=False,      
        default=UserRole.USER,  # Por defecto, nuevo usuario = 'user'
        index=True         
    )
    
    # Si el usuario está activo o no
    is_active = Column(
        Boolean,             
        default=True,        
        nullable=False       
    )
    
    # Fecha de creación --> Se llena automáticamente
    created_at = Column(
        DateTime(timezone=True),           
        server_default=func.now(),         
        nullable=False
    )
    
    # Fecha de última actualización
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),        
        onupdate=func.now(),  # Se actualiza automáticamente al modificar
        nullable=False
    )
    
    # Relación con reservas: Un usuario puede tener muchas reservas
    reservas = relationship(
        "Reservation",           
        back_populates="usuario",  
        cascade="all, delete-orphan"  # Si elimino user, elimina sus reservas
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', rol='{self.rol}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol.value,  # .value convierte el Enum a string
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_admin(self) -> bool:
        return self.rol == UserRole.ADMIN
    
    def can_make_reservation(self) -> bool:
        return self.is_active
    
    def can_admin_rooms(self) -> bool:
        return self.is_active and self.rol == UserRole.ADMIN
    
    def can_view_all_reservations(self) -> bool:
        return self.is_active and self.rol == UserRole.ADMIN