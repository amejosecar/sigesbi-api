# templates.py
import os
from fastapi.templating import Jinja2Templates

# Define el directorio de las plantillas. Se asume que la carpeta 'templates' se encuentra en la raíz del proyecto.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)
