#sigesbi/routers/usuarios.py
# 

# sigesbi/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from schemas import UsuarioCreate, UsuarioResponse

router = APIRouter()

@router.post("/", response_model=UsuarioResponse)
def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter_by(email=usuario_data.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo_usuario = Usuario(**usuario_data.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(usuario_id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(usuario_id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}
