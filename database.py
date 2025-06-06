# sigesbi_api/database.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la ruta del directorio actual de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"BASE_DIR: {BASE_DIR}")  # Para depuración

# Construir la ruta de la base de datos dentro de sigesbi_api
db_path = os.path.join(BASE_DIR, "sigesbi.db")
# Si la variable DATABASE_URL no está establecida en .env, se utiliza la ruta construida
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
