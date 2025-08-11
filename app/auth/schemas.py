# Estructuración de Datos

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.auth.model import UserRole

# Estructura Registro de Usuario

class UserCreate(BaseModel):
    
    nombre: str = Field(
        ...,  
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario"
    )
    
    email: EmailStr = Field(
        ...,
        description="Email válido del usuario"
    )
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Contraseña (mínimo 8 caracteres)"
    )
    
    @validator('nombre')
    def validate_nombre(cls, v):
        
        # Eliminar espacios extra
        v = v.strip()
        
        # Verificar que no esté vacío después del strip
        if not v:
            raise ValueError('El nombre no puede estar vacío')
        
        # Verificar que no tenga solo números
        if v.isdigit():
            raise ValueError('El nombre no puede ser solo números')
            
        return v.title()  # Convierte a formato título: "Juan Pérez"
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        
        # Verificar que tenga al menos una mayúscula
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        
        # Verificar que tenga al menos una minúscula
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        
        # Verificar que tenga al menos un número
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        
        return v

# Estructura para el Login

class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email del usuario registrado"
    )
    
    password: str = Field(
        ...,
        min_length=1,  # Solo verificamos que no esté vacío
        description="Contraseña del usuario"
    )

# Estructura para Respuestas

class UserResponse(BaseModel):
    id: int
    nombre: str
    email: str
    rol: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        # Permite que Pydantic trabaje con objetos SQLAlchemy
        from_attributes = True
        
        # Ejemplo de respuesta en la documentación de Swagger
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Juan Pérez",
                "email": "juan@example.com",
                "rol": "user",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }

class UserSummary(BaseModel):
    id: int
    nombre: str
    email: str
    rol: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True

# Estructura para JWT 

class Token(BaseModel):
    
    access_token: str = Field(
        ...,
        description="Token JWT para autenticación"
    )
    
    token_type: str = Field(
        default="bearer",
        description="Tipo de token (siempre 'bearer')"
    )
    
    expires_in: int = Field(
        ...,
        description="Tiempo de expiración en segundos"
    )
    
    user: UserResponse = Field(
        ...,
        description="Información básica del usuario autenticado"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@example.com",
                    "rol": "user",
                    "is_active": True
                }
            }
        }

class TokenData(BaseModel):
    """
    Schema para los datos dentro del token JWT
    Usado internamente para validar tokens
    """
    user_id: Optional[int] = None
    email: Optional[str] = None

# Estructuras de Administración

class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )
    
    email: Optional[EmailStr] = None
    
    is_active: Optional[bool] = None
    
    # Solo admin puede cambiar roles
    rol: Optional[UserRole] = None
    
    @validator('nombre')
    def validate_nombre_update(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('El nombre no puede estar vacío')
            return v.title()
        return v

class UserCreateByAdmin(BaseModel):
    
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    rol: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    
    @validator('nombre')
    def validate_nombre(cls, v):
        return v.strip().title()

# Estructura para Listados

class UserList(BaseModel):
    users: list[UserSummary]
    total: int
    page: int
    per_page: int
    pages: int
    
    class Config:
        schema_extra = {
            "example": {
                "users": [
                    {
                        "id": 1,
                        "nombre": "Juan Pérez",
                        "email": "juan@example.com",
                        "rol": "user",
                        "is_active": True
                    }
                ],
                "total": 50,
                "page": 1,
                "per_page": 10,
                "pages": 5
            }
        }