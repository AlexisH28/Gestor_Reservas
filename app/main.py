# Punto de Entrada Principal de Gestor de Reservas

from fastapi import FastAPI
# from app.auth.controller import router as auth_router
from app.routes.example_route import router as example_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.utils.database import create_tables
from app.auth.controller import router as auth_router
from app.users.controller import router as users_router
from app.rooms.controller import router as rooms_router
from app.reservations.controller import router as reservations_router
from app.reports.controller import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación"""
    # Startup: Crear tablas si no existen
    print("🚀 Iniciando aplicación...")
    await create_tables()
    print("✅ Base de datos configurada")
    
    yield
    
    print("🔒 Cerrando aplicación...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API REST para gestionar reservas de salas de coworking",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(users_router, prefix="/users", tags=["Usuarios"])
app.include_router(rooms_router, prefix="/rooms", tags=["Salas"])
app.include_router(reservations_router, prefix="/reservations", tags=["Reservas"])
app.include_router(reports_router, prefix="/reports", tags=["Reportes"])


@app.get("/", tags=["Root"])
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "🟢 Activo"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
