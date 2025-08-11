# Lógica de Negocio

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime, timedelta
from app.auth.model import User, UserRole
from app.auth.schemas import UserCreate, UserUpdate, UserCreateByAdmin
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.utils.exceptions import (
    UserAlreadyExistsException, 
    UserNotFoundException,
    InvalidCredentialsException,
    InactiveUserException
)
from app.config.settings import settings

class UserService:
    def __init__(self, db: Session):
        self.db = db

    # Métodos de Consulta -->
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    async def get_all_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        include_inactive: bool = True
    ) -> List[User]:
        query = self.db.query(User)
        
        # Filtrar solo activos si se especifica
        if not include_inactive:
            query = query.filter(User.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    async def count_users(self, include_inactive: bool = True) -> int:
        query = self.db.query(User)
        
        if not include_inactive:
            query = query.filter(User.is_active == True)
        
        return query.count()
    
    # Métodos de Creación -->
    
    async def create_user(self, user_data: UserCreate) -> User:
        
        # 1. Verificar que el email no existe
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(user_data.email)
        
        # 2. Hashear la contraseña
        password_hash = get_password_hash(user_data.password)
        
        # 3. Crear objeto User
        db_user = User(
            nombre=user_data.nombre,
            email=user_data.email,
            contraseña_hash=password_hash,
            rol=UserRole.USER,  # Nuevos usuarios son 'user' por defecto
            is_active=True
        )
        
        # 4. Guardar en base de datos
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)  # Obtiene el ID asignado
            return db_user
            
        except IntegrityError:
            # Si hay error de integridad (ej: email duplicado)
            self.db.rollback()
            raise UserAlreadyExistsException(user_data.email)
    
    async def create_user_by_admin(self, user_data: UserCreateByAdmin) -> User:

        # Verificar email único
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(user_data.email)
        
        # Crear usuario con datos completos
        password_hash = get_password_hash(user_data.password)
        
        db_user = User(
            nombre=user_data.nombre,
            email=user_data.email,
            contraseña_hash=password_hash,
            rol=user_data.rol,
            is_active=user_data.is_active
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
            
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsException(user_data.email)
    
    # Métodos de Autenticación
    
    async def authenticate_user(self, email: str, password: str) -> User:
        
        # 1. Buscar usuario por email
        user = await self.get_user_by_email(email)
        if not user:
            raise InvalidCredentialsException()
        
        # 2. Verificar contraseña
        if not verify_password(password, user.contraseña_hash):
            raise InvalidCredentialsException()
        
        # 3. Verificar que esté activo
        if not user.is_active:
            raise InactiveUserException()
        
        return user
    
    async def create_access_token_for_user(self, user: User) -> dict:
        
        # Datos que van dentro del token
        token_data = {
            "sub": str(user.id),  # "subject" = ID del usuario
            "email": user.email,
            "rol": user.rol.value
        }
        
        # Crear token con tiempo de expiración
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(token_data, expires_delta)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # En segundos
            "user": user
        }
    
    # Métodos de Actualización -->
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        
        # 1. Buscar usuario
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        
        # 2. Actualizar campos que vengan en el request
        update_data = user_data.dict(exclude_unset=True)  # Solo campos no None
        
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)  # user.nombre = "Nuevo Nombre"
        
        # 3. Actualizar timestamp
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
            
        except IntegrityError:
            self.db.rollback()
            # Si el error es por email duplicado
            if user_data.email:
                raise UserAlreadyExistsException(user_data.email)
            raise
    
    async def deactivate_user(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def activate_user(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    # Métodos de Eliminación -->
    
    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        
        self.db.delete(user)
        self.db.commit()
        return True