# sigesbi/settings.py
# Configuración global del proyecto SIGESBI

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    """ Clase para manejar la configuración global del proyecto """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sigesbi.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecreto")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"

settings = Settings()


# 📂 Explicación
# Se usa dotenv para manejar variables de entorno de forma segura.

# Settings encapsula variables globales como DATABASE_URL, SECRET_KEY y DEBUG_MODE.

# Se evita exponer configuraciones sensibles en el código fuente.


# 📂 Explicación  del achivo requriemiento
# fastapi → Framework principal para la API.

# uvicorn → Servidor ASGI para ejecutar la aplicación.

# sqlalchemy → ORM para la gestión de base de datos.

# pydantic → Validación de datos en FastAPI.

# python-dotenv → Manejo de variables de entorno.