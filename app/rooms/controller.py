# Controlador básico de Salas

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_rooms():
    return {"message": "Endpoint de salas - Por implementar"}

@router.post("/")
async def create_room():
    return {"message": "Crear sala - Por implementar"}