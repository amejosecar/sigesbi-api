# sigesbi-api/settings.py
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
