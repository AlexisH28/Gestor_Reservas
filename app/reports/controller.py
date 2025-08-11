# Reportes de Gestión 

# Controlador básico de reportes

from fastapi import APIRouter

router = APIRouter()

@router.get("/most-booked-rooms")
async def get_most_booked_rooms():
    return {"message": "Salas más reservadas - Por implementar"}

@router.get("/user-hours/{user_id}")
async def get_user_hours(user_id: int):
    return {"message": f"Horas del usuario {user_id} - Por implementar"}