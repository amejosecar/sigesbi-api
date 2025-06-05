# sigesbi-api/database.py
# 
# # from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


from sqlalchemy import create_engine  # ✅ Agregar esta línea
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde el archivo de configuración
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sigesbi.db")

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

