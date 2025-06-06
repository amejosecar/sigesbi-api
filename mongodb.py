#sigesbi_api/mongodb.py
#!/usr/bin/env python3
"""
mongodb.py

Se conecta a MongoDB usando los parámetros definidos en el archivo .env
y gestiona las colecciones para almacenar las reseñas de los productos.
Incluye funciones para insertar, obtener y eliminar reseñas.
"""

import os
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise Exception("La variable MONGO_URL no está definida en el archivo .env")

client = MongoClient(MONGO_URL)
db = client["sigesbi_reviews"]

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
            db.create_collection(col_name, validator=val)
            print(f"Collection '{col_name}' creada con éxito.")
        except CollectionInvalid:
            print(f"Collection '{col_name}' ya existe.")
        except Exception as e:
            print(f"Error al crear la colección '{col_name}': {e}")

def insert_review(material_type: str, codigo_inventario: int, review: str):
    """
    Inserta una reseña en la colección correspondiente.
    """
    collection_name = f"{material_type}_resenas"
    result = db[collection_name].insert_one({
        "codigo_inventario": codigo_inventario,
        "resena": review
    })
    return result

def get_review(material_type: str, codigo_inventario: int):
    """
    Retorna la reseña asociada al material especificado.
    """
    collection_name = f"{material_type}_resenas"
    doc = db[collection_name].find_one({"codigo_inventario": codigo_inventario})
    return doc["resena"] if doc and "resena" in doc else None

def delete_review(material_type: str, codigo_inventario: int):
    """
    Elimina la reseña asociada al material especificado.
    """
    collection_name = f"{material_type}_resenas"
    result = db[collection_name].delete_one({"codigo_inventario": codigo_inventario})
    return result

if __name__ == "__main__":
    create_collections()
