# Excepciones personalizadas

from fastapi import HTTPException, status

# Excepciones de Autenticación y Usuarios

class UserAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario registrado con el email: {email}"
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int = None, email: str = None):
        if user_id:
            detail = f"Usuario con ID {user_id} no encontrado"
        elif email:
            detail = f"Usuario con email {email} no encontrado"
        else:
            detail = "Usuario no encontrado"
            
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InactiveUserException(HTTPException):
    """
    Excepción para usuarios inactivos
    Se lanza cuando un usuario inactivo intenta hacer login
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tu cuenta está inactiva. Contacta al administrador."
        )


# Excepciones de Salas

class RoomNotFoundException(HTTPException):
    def __init__(self, room_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala con ID {room_id} no encontrada"
        )

class RoomNotAvailableException(HTTPException):
    def __init__(self, room_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La sala con ID {room_id} no está disponible"
        )

class RoomAlreadyExistsException(HTTPException):
    def __init__(self, room_name: str, sede: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una sala llamada '{room_name}' en {sede}"
        )


# Excepciones de Reservas

class ReservationNotFoundException(HTTPException):
    def __init__(self, reservation_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reservation_id} no encontrada"
        )

class TimeSlotNotAvailableException(HTTPException):
    def __init__(self, fecha: str, hora_inicio: str, hora_fin: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El horario {hora_inicio} - {hora_fin} del {fecha} ya está reservado"
        )

class InvalidTimeBlockException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las reservas deben ser de exactamente 1 hora"
        )

class PastDateReservationException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden hacer reservas en fechas pasadas"
        )

class ReservationLimitExceededException(HTTPException):
    def __init__(self, limit: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Has excedido el límite de {limit} reservas por día"
        )

class CannotCancelReservationException(HTTPException):
    def __init__(self, reason: str = "No se puede cancelar esta reserva"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=reason
        )

class UserPenalizedException(HTTPException):
    def __init__(self, until_date: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Estás penalizado hasta el {until_date} por exceso de cancelaciones"
        )


# Excepciones Generales

class ValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class InsufficientPermissionsException(HTTPException):
    def __init__(self, action: str = "realizar esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes permisos para {action}"
        )

class DatabaseException(HTTPException):
    def __init__(self, detail: str = "Error interno del servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

