"""
UsersController - Endpoints específicos de gestión de usuarios
Separado del auth para organizar mejor las rutas
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.utils.database import get_db
from app.utils.dependencies import get_current_user, require_admin, validate_pagination
from app.auth.service import UserService
from app.auth.model import UserRole
from app.auth.schemas import UserResponse, UserSummary, UserList

# ============================================
# CONFIGURACIÓN DEL ROUTER
# ============================================

router = APIRouter()


# ============================================
# ENDPOINTS PÚBLICOS DE USUARIOS
# ============================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Mi perfil",
    description="Obtener información del usuario autenticado"
)
async def get_my_profile(
    current_user = Depends(get_current_user)
):
    """
    Obtener perfil del usuario logueado
    
    Este endpoint está duplicado aquí y en /auth/me
    para dar flexibilidad en las rutas
    """
    return current_user


# ============================================
# ENDPOINTS DE ADMINISTRACIÓN
# ============================================

@router.get(
    "/",
    response_model=UserList,
    summary="Listar usuarios (Admin)",
    description="Obtener lista paginada de usuarios",
    dependencies=[Depends(require_admin)]
)
async def list_users(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Registros por página"),
    search: Optional[str] = Query(None, description="Buscar por nombre o email"),
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Listar usuarios con filtros y paginación
    
    Filtros disponibles:
    - **search**: Busca en nombre y email
    - **role**: Filtra por rol (user/admin)
    - **active**: Filtra por estado activo
    """
    user_service = UserService(db)
    
    # TODO: Implementar filtros de búsqueda en el service
    # Por ahora solo paginación básica
    users = await user_service.get_all_users(
        skip=skip,
        limit=limit,
        include_inactive=True
    )
    
    total = await user_service.count_users(include_inactive=True)
    pages = (total + limit - 1) // limit  # Cálculo de páginas totales
    
    return UserList(
        users=users,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit,
        pages=pages
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario",
    description="Obtener información de un usuario específico"
)
async def get_user(
    user_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener información de un usuario
    
    Reglas:
    - Los usuarios pueden ver su propia información
    - Solo admin puede ver información de otros usuarios
    """
    # Si no es admin y no es su propio perfil, denegar acceso
    if current_user.rol != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes ver información de otros usuarios"
        )
    
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario (Admin)",
    description="Eliminar permanentemente un usuario",
    dependencies=[Depends(require_admin)]
)
async def delete_user(
    user_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Eliminar usuario permanentemente
    
    Validaciones:
    - Solo admin puede eliminar usuarios
    - Admin no puede eliminarse a sí mismo
    - Se eliminan también las reservas del usuario
    """
    # Validar que admin no se elimine a sí mismo
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    
    return None  # 204 No Content