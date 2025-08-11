# Configuración de la Aplicación usando Pydantic Settings

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración principal de la aplicación"""
    
    # Información de la aplicación
    APP_NAME: str = "Coworking Booking API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Base de datos MySQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "campus2023"
    DB_NAME: str = "coworking_db"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construye la URL de la base de datos"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # JWT Configuration
    SECRET_KEY: str = "281209"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de reservas
    RESERVATION_BLOCK_HOURS: int = 1  # Bloques de 1 hora exactos
    MAX_RESERVATION_DAYS_ADVANCE: int = 30  # Máximo 30 días de anticipación
    MAX_DAILY_RESERVATIONS_PER_USER: int = 3  # Máximo 3 reservas por día por usuario
    
    # Sistema de penalizaciones
    MAX_CANCELLATIONS_PER_MONTH: int = 3  # Máximo 3 cancelaciones por mes
    PENALTY_DAYS: int = 7  # Días de penalización por exceso de cancelaciones
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
