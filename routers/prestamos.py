# sigesbi-api/routers/prestamos.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Prestamo, MaterialBiblioteca, Usuario
from ..schemas import PrestamoResponse
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=PrestamoResponse)
def registrar_prestamo(
    codigo_inventario: int = Form(...),
    usuario_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Registra un préstamo de un material en la biblioteca usando datos de formulario.
    """
    # Validar usuario
    usuario = db.query(Usuario).filter_by(usuario_id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validar material
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=codigo_inventario).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    
    # Verificar disponibilidad del material
    if not material.disponible:
        raise HTTPException(status_code=400, detail="El material no está disponible para préstamo")
    
    # Crear el préstamo y actualizar la disponibilidad
    nuevo_prestamo = Prestamo(
        codigo_inventario=codigo_inventario,
        usuario_id=usuario_id,
        fecha_prestamo=datetime.now()
    )
    material.disponible = False
    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)
    return nuevo_prestamo

@router.get("/", response_model=list[PrestamoResponse])
def listar_prestamos(db: Session = Depends(get_db)):
    """
    Lista todos los préstamos pendientes (no devueltos).
    """
    prestamos = db.query(Prestamo).filter_by(devuelto=False).all()
    return prestamos

@router.post("/devolver/{prestamo_id}")
def devolver_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    """
    Marca un préstamo como devuelto, actualizando la fecha de devolución y la disponibilidad del material.
    """
    prestamo = db.query(Prestamo).filter_by(prestamo_id=prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if prestamo.devuelto:
        raise HTTPException(status_code=400, detail="El préstamo ya fue devuelto")
    
    prestamo.devuelto = True
    prestamo.fecha_devolucion = datetime.now()
    
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=prestamo.codigo_inventario).first()
    if material:
        material.disponible = True
    
    db.commit()
    return {"message": "Préstamo devuelto exitosamente"}
