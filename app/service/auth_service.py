from datetime import datetime
from typing import Any, Dict, Optional

from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database import models


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def verify_google_id_token(self, id_token_str: str) -> Optional[Dict[str, Any]]:
        """
        Verifica el ID Token de Google y devuelve el payload del usuario.
        """
        try:
            request = requests.Request()

            # 🆕 Usamos settings.GOOGLE_CLIENT_ID para la verificación
            payload = id_token.verify_oauth2_token(
                id_token_str, request, settings.GOOGLE_CLIENT_ID
            )

            # ... (Resto del código de la función sigue igual) ...
            user_id = payload["sub"]

            return {
                "id": user_id,
                "email": payload["email"],
                "name": payload.get("name"),
                "picture": payload.get("picture"),
            }

        except ValueError:
            # Token inválido, expirado o error en el CLIENT_ID
            return None
        except Exception as e:
            print(f"Error durante la verificación de Google Token: {e}")
            return None

    def get_or_create_user(self, user_data: Dict[str, Any]) -> models.User:
        """
        Busca un usuario por su ID de Google (sub). Si no existe, lo crea.

        Args:
            user_data: Diccionario con id, email, name, picture.

        Returns:
            models.User: La instancia del usuario ORM.
        """
        user_id = user_data["id"]

        # 1. Buscar usuario existente
        db_user = self.db.query(models.User).filter(models.User.id == user_id).first()

        if db_user:
            # 2. Usuario encontrado
            return db_user

        # 3. Usuario no encontrado, crearlo
        new_user = models.User(
            id=user_id,
            email=user_data["email"],
            name=user_data.get("name"),
            picture=user_data.get("picture"),
            created_at=datetime.utcnow(),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user
