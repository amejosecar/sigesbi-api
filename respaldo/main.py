## sigesbi-api/main.py
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

