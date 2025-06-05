# sigesbi-api/routers/revistas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Revista, MaterialBiblioteca
from schemas import RevistaCreate, RevistaResponse
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/", response_model=RevistaResponse)
def agregar_revista(revista_data: RevistaCreate, db: Session = Depends(get_db)):
    """
    Agrega una nueva revista a la biblioteca.
    Si el registro en MaterialBiblioteca no existe, se crea usando los datos enviados.
    """
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=revista_data.codigo_inventario).first()
    if not material:
        material = MaterialBiblioteca(
            codigo_inventario=revista_data.codigo_inventario,
            titulo=revista_data.titulo,
            autor=revista_data.autor,
            tipo_material="Revista"
        )
        db.add(material)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear MaterialBiblioteca: {e}")
        db.refresh(material)
    
    revista_existente = db.query(Revista).filter_by(codigo_inventario=revista_data.codigo_inventario).first()
    if revista_existente:
        raise HTTPException(status_code=409, detail="Ya existe una revista con ese código de inventario")
    
    nuevo_revista = Revista(**revista_data.dict(exclude={"titulo", "autor"}))
    db.add(nuevo_revista)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar la revista: {e}")
    db.refresh(nuevo_revista)
    return nuevo_revista

@router.get("/", response_model=list[RevistaResponse])
def listar_revistas(db: Session = Depends(get_db)):
    revistas = db.query(Revista).options(joinedload(Revista.material)).all()
    return revistas

@router.get("/{codigo_inventario}", response_model=RevistaResponse)
def obtener_revista(codigo_inventario: int, db: Session = Depends(get_db)):
    revista = db.query(Revista).options(joinedload(Revista.material)).filter_by(codigo_inventario=codigo_inventario).first()
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada")
    return revista

@router.delete("/{codigo_inventario}")
def eliminar_revista(codigo_inventario: int, db: Session = Depends(get_db)):
    revista = db.query(Revista).filter_by(codigo_inventario=codigo_inventario).first()
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada")
    material = revista.material
    db.delete(revista)
    db.commit()
    if material:
        db.delete(material)
        db.commit()
    return {"message": "Revista y registro de material eliminado exitosamente"}
