# sigesbi-api/routers/revistas.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..models import Revista, MaterialBiblioteca
from ..schemas import RevistaResponse
from ..mongodb import insert_review, get_review, delete_review


router = APIRouter()

@router.post("/", response_model=RevistaResponse)
def agregar_revista(
    codigo_inventario: int = Form(...),
    titulo: str = Form(...),
    autor: str = Form(...),
    isbn: str = Form(None),
    numero_edicion: int = Form(None),
    fecha_publicacion: str = Form(None),
    resena: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Agrega una nueva revista a la biblioteca usando datos tipo formulario.
    Almacena la reseña en MongoDB.
    """
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=codigo_inventario).first()
    if not material:
        material = MaterialBiblioteca(
            codigo_inventario=codigo_inventario,
            titulo=titulo,
            autor=autor,
            tipo_material="Revista"
        )
        db.add(material)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al crear el material")
    
    revista_existente = db.query(Revista).filter_by(codigo_inventario=codigo_inventario).first()
    if revista_existente:
        raise HTTPException(status_code=409, detail="Ya existe una revista con ese código de inventario")
    
    nuevo_revista = Revista(
        codigo_inventario=codigo_inventario,
        isbn=isbn,
        numero_edicion=numero_edicion,
        fecha_publicacion=fecha_publicacion
    )
    db.add(nuevo_revista)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar la revista")
    
    db.refresh(nuevo_revista)
    if resena:
        insert_review("revista", codigo_inventario, resena)
    revista_dict = nuevo_revista.__dict__
    revista_dict["resena"] = get_review("revista", codigo_inventario)
    return revista_dict

@router.get("/", response_model=list[RevistaResponse])
def listar_revistas(db: Session = Depends(get_db)):
    """
    Lista todas las revistas, incluyendo la reseña almacenada en MongoDB.
    """
    revistas = db.query(Revista).options(joinedload(Revista.material)).all()
    result = []
    for revista in revistas:
        revista_dict = revista.__dict__
        revista_dict["resena"] = get_review("revista", revista.codigo_inventario)
        result.append(revista_dict)
    return result

@router.get("/{codigo_inventario}", response_model=RevistaResponse)
def obtener_revista(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Obtiene la información de una revista por su código de inventario,
    incluyendo la reseña almacenada en MongoDB.
    """
    revista = db.query(Revista).options(joinedload(Revista.material))\
                               .filter_by(codigo_inventario=codigo_inventario).first()
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada")
    revista_dict = revista.__dict__
    revista_dict["resena"] = get_review("revista", codigo_inventario)
    return revista_dict

@router.delete("/{codigo_inventario}")
def eliminar_revista(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Elimina una revista y su registro asociado en MaterialBiblioteca,
    además elimina la reseña en MongoDB.
    """
    revista = db.query(Revista).filter_by(codigo_inventario=codigo_inventario).first()
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada")
    
    material = revista.material
    if material:
        db.delete(material)
    db.delete(revista)
    db.commit()
    delete_review("revista", codigo_inventario)
    return {"message": "Revista y registro de material eliminado exitosamente"}
