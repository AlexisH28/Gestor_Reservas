# Dependencias para FastAPI

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.utils.database import get_db
from app.utils.security import verify_token
from app.auth.model import User
from app.auth.service import UserService

# Configurar esquema de autenticación Bearer
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:

    # Verificar token
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buscar usuario en la base de datos
    user_service = UserService(db)
    user = await user_service.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador para realizar esta acción"
        )
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


def validate_pagination(
    skip: int = 0,
    limit: int = 100
) -> tuple[int, int]:
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'skip' debe ser mayor o igual a 0"
        )
    
    if limit <= 0 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'limit' debe estar entre 1 y 100"
        )
    
    return skip, limit


def validate_room_exists(
    room_id: int,
    db: Session = Depends(get_db)
) -> int:
    from app.rooms.service import RoomService
    
    room_service = RoomService(db)
    room = room_service.get_room_by_id(room_id)
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala con ID {room_id} no encontrada"
        )
    
    if not room.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sala no está disponible"
        )
    
    return room_id


def validate_user_can_modify_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> int:
    from app.reservations.service import ReservationService
    
    reservation_service = ReservationService(db)
    reservation = reservation_service.get_reservation_by_id(reservation_id)
    
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reservation_id} no encontrada"
        )
    
    # Solo el propietario o un admin pueden modificar
    if reservation.usuario_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar esta reserva"
        )
    
    return reservation_id