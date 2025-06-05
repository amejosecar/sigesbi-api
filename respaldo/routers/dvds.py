# sigesbi-api/routers/dvds.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import DVD, MaterialBiblioteca
from schemas import DVDCreate, DVDResponse
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/", response_model=DVDResponse)
def agregar_dvd(dvd_data: DVDCreate, db: Session = Depends(get_db)):
    """
    Agrega un nuevo DVD a la biblioteca.
    Si el registro en MaterialBiblioteca no existe, se crea usando los datos enviados.
    """
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=dvd_data.codigo_inventario).first()
    if not material:
        material = MaterialBiblioteca(
            codigo_inventario=dvd_data.codigo_inventario,
            titulo=dvd_data.titulo,
            autor=dvd_data.autor,
            tipo_material="DVD"
        )
        db.add(material)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear MaterialBiblioteca: {e}")
        db.refresh(material)
    
    dvd_existente = db.query(DVD).filter_by(codigo_inventario=dvd_data.codigo_inventario).first()
    if dvd_existente:
        raise HTTPException(status_code=409, detail="Ya existe un DVD con ese código de inventario")
    
    nuevo_dvd = DVD(**dvd_data.dict(exclude={"titulo", "autor"}))
    db.add(nuevo_dvd)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar el DVD: {e}")
    db.refresh(nuevo_dvd)
    return nuevo_dvd

@router.get("/", response_model=list[DVDResponse])
def listar_dvds(db: Session = Depends(get_db)):
    dvds = db.query(DVD).options(joinedload(DVD.material)).all()
    return dvds

@router.get("/{codigo_inventario}", response_model=DVDResponse)
def obtener_dvd(codigo_inventario: int, db: Session = Depends(get_db)):
    dvd = db.query(DVD).options(joinedload(DVD.material)).filter_by(codigo_inventario=codigo_inventario).first()
    if not dvd:
        raise HTTPException(status_code=404, detail="DVD no encontrado")
    return dvd

@router.delete("/{codigo_inventario}")
def eliminar_dvd(codigo_inventario: int, db: Session = Depends(get_db)):
    dvd = db.query(DVD).filter_by(codigo_inventario=codigo_inventario).first()
    if not dvd:
        raise HTTPException(status_code=404, detail="DVD no encontrado")
    material = dvd.material
    db.delete(dvd)
    db.commit()
    if material:
        db.delete(material)
        db.commit()
    return {"message": "DVD y registro de material eliminado exitosamente"}
