from sqlalchemy import inspect
from sigesbi_api.database import engine


# Crear un inspector a partir del engine
inspector = inspect(engine)

# Obtener la lista de nombres de las tablas existentes en la base de datos
existing_tables = inspector.get_table_names()

if "material_biblioteca" in existing_tables:
    print("La tabla 'material_biblioteca' existe.")
else:
    print("La tabla 'material_biblioteca' no existe.")
