from typing import Optional

# Importaciones de la Lógica de Negocio y Core
from app.database.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.settings import settings  # Para acceder al tiempo de expiración del token
from app.service.auth_service import AuthService

# Creamos el router para la autenticación
router = APIRouter()


# --- Schemas de Datos (Se mueven al archivo schemas.py, pero los dejamos aquí temporalmente si es tu convención) ---
class GoogleLoginRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_email: Optional[str] = None
    user_name: Optional[str] = None


# --- Endpoints ---


@router.post("/google", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para el Login de Google. Recibe el ID Token, lo verifica
    y devuelve un JWT de sesión personalizado.
    """

    auth_service = AuthService(db)

    # 1. Verificar el ID Token con los servidores de Google
    user_info = auth_service.verify_google_id_token(request.id_token)

    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Google inválido, expirado o error de verificación.",
        )

    # 2. Obtener o Crear el usuario en la BD
    db_user = auth_service.get_or_create_user(user_info)

    # 3. Generar el JWT personalizado
    access_token = create_access_token(
        data={"user_id": db_user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_email=db_user.email,
        user_name=db_user.name,
    )
