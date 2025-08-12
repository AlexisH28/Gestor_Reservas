# Utilidades para el apartado de Seguridad

from datetime import datetime, timedelta
from typing import Union, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.config.settings import settings

# Implementación de hashing para las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()
    
    # Configurar tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Generar token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> dict:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Verificar que el token tenga el campo 'sub' (subject)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        return payload
        
    except JWTError:
        raise credentials_exception


def create_reset_token(user_id: int) -> str:
    
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": str(user_id),
        "type": "reset_password",
        "exp": expire
    }
    
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_reset_token(token: str) -> Optional[int]:
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Verificar que sea un token de reset
        if payload.get("type") != "reset_password":
            return None
            
        user_id = payload.get("sub")
        if user_id is None:
            return None
            
        return int(user_id)
        
    except (JWTError, ValueError):
        return None


def validate_password_strength(password: str) -> bool:
    
    # Requisitos mínimos:
    # - Al menos 8 caracteres
    # - Al menos 1 mayúscula
    # - Al menos 1 minúscula  
    # - Al menos 1 número
    
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit