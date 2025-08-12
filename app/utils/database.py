# Configuración Base de Datos

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.config.settings import settings

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creación engine de SQLAlchemy
try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,  
        pool_pre_ping=True,   
        pool_recycle=300,     
        pool_size=10,         
        max_overflow=20       
    )
    logger.info("✅ Engine de base de datos creado exitosamente")
except SQLAlchemyError as e:
    logger.error(f"❌ Error creando engine de base de datos: {e}")
    raise

# Crear sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()
metadata = MetaData()


async def get_db():
    
    # Dependencia para obtener sesión de base de datos

    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"❌ Error en sesión de base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


async def create_tables():
    try:
        # Importar todos los modelos para que sean registrados
        from app.auth.model import User
        from app.rooms.model import Room
        from app.reservations.model import Reservation
        
        logger.info("📊 Creando tablas de base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
        
    except SQLAlchemyError as e:
        logger.error(f"❌ Error creando tablas: {e}")
        raise
    except ImportError as e:
        logger.error(f"❌ Error importando modelos: {e}")
        raise


async def drop_tables():
    
    # Eliminar todas las tablas ⚠️
    
    if not settings.DEBUG:
        raise Exception("❌ No se puede eliminar tablas en producción")
    
    try:
        logger.warning("⚠️ Eliminando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("✅ Tablas eliminadas exitosamente")
    except SQLAlchemyError as e:
        logger.error(f"❌ Error eliminando tablas: {e}")
        raise


def test_connection():
    """
    - Probar la conexión a la base de datos
    - Retorna True si la conexión es exitosa
    """
    try:
        connection = engine.connect()
        connection.close()
        logger.info("✅ Conexión a base de datos exitosa")
        return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Error conectando a base de datos: {e}")
        return False


# Ejecutar test de conexión al importar
if __name__ == "__main__":
    test_connection()