# sigesbi/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
from ..database import get_db
from ..models import Usuario
from ..schemas import UsuarioCreate, UsuarioResponse

router = APIRouter()

# POST con JSON (existente)
@router.post("/", response_model=UsuarioResponse)
def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario_data.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo_usuario = Usuario(**usuario_data.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# POST desde formulario (x-www-form-urlencoded)
@router.post("/formulario", response_model=UsuarioResponse)
def registrar_usuario_form(
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Servir formulario HTML sin Jinja2
@router.get("/form", response_class=HTMLResponse)
def mostrar_form_usuario():
    ruta = os.path.join("templates", "form_usuario.html")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Formulario no encontrado")

# Listar usuarios
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

# Obtener usuario por id
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Eliminar usuario
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}
