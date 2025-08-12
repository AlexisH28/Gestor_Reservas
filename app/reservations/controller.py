# Controlador básico de Reservas

from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_my_reservations():
    return {"message": "Mis reservas - Por implementar"}

@router.post("/")
async def create_reservation():
    return {"message": "Crear reserva - Por implementar"}