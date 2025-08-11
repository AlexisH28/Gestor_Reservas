# Definimos las rutas de la API

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List

from app.utils.database import get_db
from app.utils.dependencies import get_current_user, require_admin, validate_pagination
from app.auth.service import UserService
from app.auth.schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate, UserCreateByAdmin,
    Token, UserList, UserSummary
)

# Configuración del Router

# Crear router para agrupar endpoints de autenticación
router = APIRouter()

# Esquema de seguridad para documentación Swagger
security = HTTPBearer()

# Endpoints de autenticación

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Permite a una persona crear una cuenta nueva en el sistema"
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
): 
    # Crear servicio y registrar usuario
    user_service = UserService(db)
    new_user = await user_service.create_user(user_data)
    
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autenticar usuario y obtener token JWT"
)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    
    # 1. Autenticar usuario (verifica email/password)
    user = await user_service.authenticate_user(
        credentials.email, 
        credentials.password
    )
    
    # 2. Crear token JWT
    token_data = await user_service.create_access_token_for_user(user)
    
    return token_data

# Endpoints de Información de Usuario

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener mi información",
    description="Obtener datos del usuario autenticado"
)
async def get_my_profile(
    current_user = Depends(get_current_user)
):
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Actualizar mi información",
    description="Permite al usuario actualizar sus datos personales"
)
async def update_my_profile(
    user_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    
    # Si no es admin, quitar el campo rol del update
    if current_user.rol != "admin":
        user_data.rol = None
    
    updated_user = await user_service.update_user(current_user.id, user_data)
    return updated_user

# Endpoints de Administración --> Solo Admin

@router.get(
    "/users",
    response_model=List[UserSummary],
    summary="Listar usuarios (Admin)",
    description="Obtener lista de todos los usuarios del sistema",
    dependencies=[Depends(require_admin)]
)
async def get_all_users(
    pagination: tuple = Depends(validate_pagination),
    include_inactive: bool = True,
    db: Session = Depends(get_db)
):
    skip, limit = pagination
    user_service = UserService(db)
    
    users = await user_service.get_all_users(
        skip=skip, 
        limit=limit,
        include_inactive=include_inactive
    )
    
    return users

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario (Admin)",
    description="Permite al admin crear usuarios con rol específico",
    dependencies=[Depends(require_admin)]
)
async def create_user_by_admin(
    user_data: UserCreateByAdmin,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    new_user = await user_service.create_user_by_admin(user_data)
    return new_user

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID (Admin)",
    description="Obtener información completa de un usuario específico",
    dependencies=[Depends(require_admin)]
)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    return user

@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario (Admin)",
    description="Permite al admin actualizar cualquier usuario",
    dependencies=[Depends(require_admin)]
)
async def update_user_by_admin(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = await user_service.update_user(user_id, user_data)
    return updated_user

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario (Admin)",
    description="Eliminar permanentemente un usuario del sistema",
    dependencies=[Depends(require_admin)]
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    
    # 204 No Content = operación exitosa, sin body de respuesta
    return None


@router.patch(
    "/users/{user_id}/deactivate",
    response_model=UserResponse,
    summary="Desactivar usuario (Admin)",
    description="Desactivar usuario sin eliminarlo",
    dependencies=[Depends(require_admin)]
)
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    deactivated_user = await user_service.deactivate_user(user_id)
    return deactivated_user


@router.patch(
    "/users/{user_id}/activate",
    response_model=UserResponse,
    summary="Activar usuario (Admin)",
    description="Reactivar un usuario desactivado",
    dependencies=[Depends(require_admin)]
)
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    activated_user = await user_service.activate_user(user_id)
    return activated_user

# Endpoints de Estadística --> Admin

@router.get(
    "/users/stats/count",
    summary="Estadísticas de usuarios (Admin)",
    description="Obtener conteo de usuarios activos e inactivos",
    dependencies=[Depends(require_admin)]
)
async def get_users_stats(
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    
    total_users = await user_service.count_users(include_inactive=True)
    active_users = await user_service.count_users(include_inactive=False)
    inactive_users = total_users - active_users
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    }