from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings  # Importamos la URL de la BD

# 🆕 Importamos los modelos ORM que definen las tablas

# 1. Configuración de la conexión a la BD
# Usamos la URL definida en settings.py (que debe ser 'postgresql://...')
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 🆕 Crear el motor de la base de datos
# Se eliminan los argumentos específicos de SQLite (connect_args)
# Se añade 'pool_pre_ping=True' para robustez en conexiones de red (PostgreSQL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

# 2. Configuración de la Sesión
# SessionLocal se usa para crear sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base Declarativa para los Modelos ORM
# Base se usa para heredar y definir las clases de modelos de la BD
Base = declarative_base()


# 4. Función de Dependencia para FastAPI
def get_db():
    """
    Función de dependencia que proporciona una sesión de BD por petición.
    Garantiza que la sesión se cierre después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 5. 🆕 Función de Inicialización de la Base de Datos
def init_db():
    """
    Crea todas las tablas en la Base de Datos (PostgreSQL) si no existen.
    Esta función se debe llamar al iniciar la aplicación (en main.py).
    """
    # Llama a create_all para que SQLAlchemy lea todos los modelos
    # que heredan de Base (importados desde app.database.models) y cree las tablas.
    Base.metadata.create_all(bind=engine)
