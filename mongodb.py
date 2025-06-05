#!/usr/bin/env python3
"""
create_mongo_tables.py

Este script se conecta a MongoDB usando los parámetros definidos en el archivo .env
y crea (o actualiza) las colecciones para almacenar las reseñas de los productos:
    - libro_resenas
    - dvd_resenas
    - revista_resenas

Cada colección se crea con un validador JSON que asegura que los documentos tengan
los campos "codigo_inventario" (tipo int) y "resena" (tipo string).


"""

import os
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Obtener la URL de conexión a MongoDB desde el .env (sin usar un valor por defecto)
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise Exception("La variable MONGO_URL no está definida en el archivo .env")

# Conectar al cliente MongoDB y seleccionar la base de datos para reseñas
client = MongoClient(MONGO_URL)
db = client["sigesbi_reviews"]

# Definir un esquema de validación JSON para las colecciones de reseñas.
# En estos esquemas, se valida que los documentos tengan 'codigo_inventario' (int)
# y 'resena' (string).
validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["codigo_inventario", "resena"],
        "properties": {
            "codigo_inventario": {
                "bsonType": "int",
                "description": "debe ser un entero y es requerido"
            },
            "resena": {
                "bsonType": "string",
                "description": "debe ser una cadena y es requerida"
            }
        }
    }
}

# Diccionario de colecciones a crear con su respectivo validator.
collections_to_create = {
    "libro_resenas": validator,
    "dvd_resenas": validator,
    "revista_resenas": validator,
}

def create_collections():
    for col_name, val in collections_to_create.items():
        try:
            # Se intenta crear la colección con el validator
            db.create_collection(col_name, validator=val)
            print(f"Collection '{col_name}' creada con éxito.")
        except CollectionInvalid:
            # La colección ya existe. Podemos actualizar el validator si fuera necesario.
            print(f"Collection '{col_name}' ya existe.")
        except Exception as e:
            print(f"Error al crear la colección '{col_name}': {e}")

if __name__ == "__main__":
    create_collections()
