# sigesbi-api/routers/dvds.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import DVD, MaterialBiblioteca
from schemas import DVDResponse
from sqlalchemy.exc import IntegrityError
from ..mongodb import insert_review, get_review, delete_review


router = APIRouter()

@router.post("/", response_model=DVDResponse)
def agregar_dvd(
    codigo_inventario: int = Form(...),
    titulo: str = Form(...),
    autor: str = Form(...),
    isbn: str = Form(None),
    duracion: int = Form(None),
    formato: str = Form(None),
    resena: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Agrega un nuevo DVD a la biblioteca usando datos tipo formulario.
    Almacena la reseña en MongoDB.
    """
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=codigo_inventario).first()
    if not material:
        material = MaterialBiblioteca(
            codigo_inventario=codigo_inventario,
            titulo=titulo,
            autor=autor,
            tipo_material="DVD"
        )
        db.add(material)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al crear el material")

    dvd_existente = db.query(DVD).filter_by(codigo_inventario=codigo_inventario).first()
    if dvd_existente:
        raise HTTPException(status_code=409, detail="Ya existe un DVD con ese código de inventario")

    nuevo_dvd = DVD(
        codigo_inventario=codigo_inventario,
        isbn=isbn,
        duracion=duracion,
        formato=formato
    )
    db.add(nuevo_dvd)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar el DVD")

    db.refresh(nuevo_dvd)
    if resena:
        insert_review("dvd", codigo_inventario, resena)
    dvd_dict = nuevo_dvd.__dict__
    dvd_dict["resena"] = get_review("dvd", codigo_inventario)
    return dvd_dict

@router.get("/", response_model=list[DVDResponse])
def listar_dvds(db: Session = Depends(get_db)):
    """
    Lista todos los DVDs, incluyendo la reseña almacenada en MongoDB.
    """
    dvds = db.query(DVD).options(joinedload(DVD.material)).all()
    result = []
    for dvd in dvds:
        dvd_dict = dvd.__dict__
        dvd_dict["resena"] = get_review("dvd", dvd.codigo_inventario)
        result.append(dvd_dict)
    return result

@router.get("/{codigo_inventario}", response_model=DVDResponse)
def obtener_dvd(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Obtiene un DVD por su código de inventario, incluyendo la reseña almacenada en MongoDB.
    """
    dvd = db.query(DVD).options(joinedload(DVD.material)).filter_by(codigo_inventario=codigo_inventario).first()
    if not dvd:
        raise HTTPException(status_code=404, detail="DVD no encontrado")
    dvd_dict = dvd.__dict__
    dvd_dict["resena"] = get_review("dvd", codigo_inventario)
    return dvd_dict

@router.delete("/{codigo_inventario}")
def eliminar_dvd(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Elimina un DVD y su registro asociado en MaterialBiblioteca,
    además elimina la reseña en MongoDB.
    """
    dvd = db.query(DVD).filter_by(codigo_inventario=codigo_inventario).first()
    if not dvd:
        raise HTTPException(status_code=404, detail="DVD no encontrado")

    material = dvd.material
    db.delete(dvd)
    db.commit()
    if material:
        db.delete(material)
        db.commit()
    delete_review("dvd", codigo_inventario)
    return {"message": "DVD y registro de material eliminado exitosamente"}
