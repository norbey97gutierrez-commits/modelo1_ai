from datetime import datetime, timedelta, timezone
from typing import Optional

# Importamos la función de dependencia de la BD
from app.database.db import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Importamos la configuración global
from app.core.settings import settings

# Importamos el modelo ORM del Usuario
# Importamos el esquema del usuario para la salida
from app.database import models, schemas

# --- Configuración JWT ---


# Esquema para el contenido del token (Payload)
class TokenData(BaseModel):
    user_id: Optional[str] = None


# Constantes de seguridad
ALGORITHM = "HS256"  # Algoritmo de hashing estándar
# La expiración ahora se toma de settings.py
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# 🆕 Esquema de seguridad para FastAPI: Define dónde esperar el token (Bearer)
# Se usa 'tokenUrl' aunque no implementemos el endpoint OAuth2 tradicional de token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/google")

# --- Funciones de Generación y Validación (SIN CAMBIOS) ---


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # ... (El cuerpo de la función create_access_token sigue igual) ...
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    # ... (El cuerpo de la función decode_access_token sigue igual) ...
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except JWTError:
        return None


# --- 🆕 Dependencia de Autenticación para Endpoints ---


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> schemas.User:
    """
    Dependencia de FastAPI para obtener el usuario autenticado a partir del JWT.
    Lanza HTTPException 401 si la autenticación falla.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o Token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decodificar el Token
    token_data = decode_access_token(token)

    if token_data is None:
        raise credentials_exception

    user_id = token_data.user_id

    if user_id is None:
        raise credentials_exception

    # 2. Buscar el Usuario en la BD
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        raise credentials_exception

    # 3. Devolver el usuario (convertido a esquema Pydantic para tipado)
    return schemas.User.model_validate(db_user)
