# sigesbi_api/startup.py

from sqlalchemy import inspect
from .database import engine
from .models import Base

def init_sqlite():
    """Valida y crea las tablas en SQLite si no existen."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    if not existing_tables:
        # Si no existen tablas, las crea
        Base.metadata.create_all(engine)
        print("Tablas creadas en SQLite.")
    else:
        print("Tablas existentes en SQLite:", existing_tables)

def init_mongodb():
    """Valida y crea las colecciones en MongoDB si no existen."""
    # Se importa la función create_collections del módulo mongodb
    from .mongodb import create_collections, db
    
    # Definir las colecciones esperadas
    expected_collections = ["libro_resenas", "dvd_resenas", "revista_resenas"]
    existing = db.list_collection_names()
    missing = [col for col in expected_collections if col not in existing]
    
    if missing:
        print("Las siguientes colecciones no existen en MongoDB y serán creadas:", missing)
        create_collections()  # Esto creará las colecciones que faltan
    else:
        print("Todas las colecciones de MongoDB ya existen:", existing)

def init_databases():
    """Inicializa ambas bases de datos: SQLite y MongoDB."""
    init_sqlite()
    init_mongodb()
