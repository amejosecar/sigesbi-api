# sigesbi-api/database.py
# 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sigesbi.db")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
