## sigesbi-api/main.py
# sigesbi-api/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routers import libros, revistas, dvds, usuarios, prestamos
from templates import templates  # Importa la configuración de templates desde un módulo separado

app = FastAPI(
    title="SiGesBi API",
    description="Sistema de Gestión de Biblioteca con FastAPI",
    version="1.0.0"
)

# Registrar los routers
app.include_router(libros.router, prefix="/libros", tags=["Libros"])
app.include_router(revistas.router, prefix="/revistas", tags=["Revistas"])
app.include_router(dvds.router, prefix="/dvds", tags=["DVDs"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(prestamos.router, prefix="/prestamos", tags=["Préstamos"])

# Endpoint de bienvenida (opcional)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Bienvenido a SiGesBi API"})

# Endpoints para servir formularios HTML para cada modelo
@app.get("/formulario-libros", response_class=HTMLResponse)
def formulario_libros(request: Request):
    return templates.TemplateResponse("libros.html", {"request": request})

@app.get("/formulario-revistas", response_class=HTMLResponse)
def formulario_revistas(request: Request):
    return templates.TemplateResponse("revistas.html", {"request": request})

@app.get("/formulario-dvds", response_class=HTMLResponse)
def formulario_dvds(request: Request):
    return templates.TemplateResponse("dvds.html", {"request": request})

@app.get("/formulario-usuarios", response_class=HTMLResponse)
def formulario_usuarios(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request": request})
