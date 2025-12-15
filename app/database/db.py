# app/database/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.settings import settings

# Configuración de SQLAlchemy
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 1. Crear Engine (Conexión a la DB)
# pool_pre_ping ayuda a reconectar si la conexión se pierde
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# 2. Sesión para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base para los modelos ORM
Base = declarative_base()


# 4. Función de Inicialización (Creación de Tablas)
def init_db():
    """Importa todos los modelos para que se registren en Base.metadata y crea las tablas."""
    print("Intentando crear tablas...")

    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente o ya existentes.")


# 5. Función de Dependencia (Get DB)
def get_db():
    """Dependencia para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
