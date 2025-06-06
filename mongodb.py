#sigesbi_api/mongodb.py
#!/usr/bin/env python3
"""
mongodb.py

Este script se conecta a MongoDB usando los parámetros definidos en el archivo .env
y crea (o actualiza) las colecciones para almacenar las reseñas de los productos:
    - libro_resenas
    - dvd_resenas
    - revista_resenas

Además, se definen funciones adicionales para insertar, obtener y eliminar reseñas.
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
    """
    Crea las colecciones especificadas con su esquema de validación,
    o indica si ya existen.
    """
    for col_name, val in collections_to_create.items():
        try:
            # Se intenta crear la colección con el validator
            db.create_collection(col_name, validator=val)
            print(f"Collection '{col_name}' creada con éxito.")
        except CollectionInvalid:
            print(f"Collection '{col_name}' ya existe.")
        except Exception as e:
            print(f"Error al crear la colección '{col_name}': {e}")

# Funciones adicionales para gestionar reseñas

def insert_review(material_type: str, codigo_inventario: int, review: str):
    """
    Inserta una reseña para el material especificado.
    
    Parámetros:
      material_type: 'libro', 'dvd' o 'revista'
      codigo_inventario: código único del material
      review: texto de la reseña
      
    Retorna el resultado de la operación de inserción.
    """
    collection_name = f"{material_type}_resenas"
    result = db[collection_name].insert_one({
        "codigo_inventario": codigo_inventario,
        "resena": review
    })
    return result

def get_review(material_type: str, codigo_inventario: int):
    """
    Devuelve la reseña asociada al material especificado.
    
    Parámetros:
      material_type: 'libro', 'dvd' o 'revista'
      codigo_inventario: código único del material
      
    Si no se encuentra ninguna reseña, devuelve None.
    """
    collection_name = f"{material_type}_resenas"
    doc = db[collection_name].find_one({"codigo_inventario": codigo_inventario})
    return doc["resena"] if doc and "resena" in doc else None

def delete_review(material_type: str, codigo_inventario: int):
    """
    Elimina la reseña asociada al material especificado.
    
    Parámetros:
      material_type: 'libro', 'dvd' o 'revista'
      codigo_inventario: código único del material
      
    Retorna el resultado de la operación de eliminación.
    """
    collection_name = f"{material_type}_resenas"
    result = db[collection_name].delete_one({"codigo_inventario": codigo_inventario})
    return result

if __name__ == "__main__":
    create_collections()
