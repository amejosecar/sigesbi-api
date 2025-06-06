# sigesbi_api/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from .routers import libros, revistas, dvds, usuarios, prestamos
from .templates import templates
from .startup import init_databases
from sigesbi_api.models import Base
from sigesbi_api.database import engine
import traceback
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="SiGesBi API",
    description="Sistema de Gestión de Biblioteca con FastAPI",
    version="1.0.0",
    debug=True
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc() if app.debug else ""
    logger.error(f"Error: {exc}\nTraceback: {tb}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detalle": str(exc),
            "trace": tb
        }
    )

@app.on_event("startup")
async def startup_event():
    init_databases()

app.include_router(libros.router, prefix="/libros", tags=["Libros"])
app.include_router(revistas.router, prefix="/revistas", tags=["Revistas"])
app.include_router(dvds.router, prefix="/dvds", tags=["DVDs"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(prestamos.router, prefix="/prestamos", tags=["Préstamos"])

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Bienvenido a SiGesBi API"})

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
