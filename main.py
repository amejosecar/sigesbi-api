## sigesbi/main.py
from fastapi import FastAPI
#from routers import libros, revistas, dvds, usuarios, prestamos
from routers import libros, revistas, dvds, usuarios, prestamos


app = FastAPI(title="SiGesBi API", description="Sistema de Gestión de Biblioteca con FastAPI")

# Registrar los routers
app.include_router(libros.router, prefix="/libros", tags=["Libros"])
app.include_router(revistas.router, prefix="/revistas", tags=["Revistas"])
app.include_router(dvds.router, prefix="/dvds", tags=["DVDs"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(prestamos.router, prefix="/prestamos", tags=["Préstamos"])

# Ruta raíz
@app.get("/")
def home():
    return {"message": "Bienvenido a la API de SiGesBi - Sistema de Gestión de Biblioteca con FastAPI"}

# Ejecutar en modo desarrollo con uvicorn
# uvicorn main:app --reload


# Explicación
# Se crea la instancia app con FastAPI.

# Se incluyen los routers de cada módulo (libros.py, revistas.py, etc.) para mantener la app organizada.

# Se define la ruta principal (/) para dar la bienvenida.

# El comentario final recuerda cómo ejecutar el servidor con Uvicorn.
