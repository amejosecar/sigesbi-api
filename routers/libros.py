# sigesbi_api/routers/libros.py

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Libro, MaterialBiblioteca
from ..schemas import LibroResponse
from sqlalchemy.exc import IntegrityError
from ..mongodb import insert_review, get_review, delete_review
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=LibroResponse)
def agregar_libro(
    codigo_inventario: int = Form(...),
    titulo: str = Form(...),
    autor: str = Form(...),
    isbn: str = Form(None),
    numero_paginas: int = Form(None),
    editorial: str = Form(None),
    fecha_publicacion: str = Form(None),
    edicion: str = Form(None),
    idioma: str = Form(None),
    peso_libro: float = Form(None),
    formato_libro: str = Form(None),
    tipo_literatura: str = Form(None),
    resena: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Agrega un nuevo libro a la biblioteca usando datos tipo formulario.
    El campo 'resena' se guarda en MongoDB y se asigna al atributo 'resena' del modelo.
    """
    # Verificar o crear registro en MaterialBiblioteca
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=codigo_inventario).first()
    if not material:
        material = MaterialBiblioteca(
            codigo_inventario=codigo_inventario,
            titulo=titulo,
            autor=autor,
            tipo_material="Libro"
        )
        db.add(material)
        try:
            db.commit()
            db.refresh(material)
            logger.info(f"Registro en MaterialBiblioteca creado (código: {codigo_inventario}).")
        except IntegrityError as ie:
            db.rollback()
            logger.error("Error al crear el registro de material", exc_info=ie)
            raise HTTPException(status_code=500, detail="Error al crear el registro de material")

    # Verificar si ya existe el libro
    libro_existente = db.query(Libro).filter_by(codigo_inventario=codigo_inventario).first()
    if libro_existente:
        raise HTTPException(status_code=409, detail="Ya existe un libro con ese código de inventario")
    
    # Crear el registro en Libro
    nuevo_libro = Libro(
        codigo_inventario=codigo_inventario,
        isbn=isbn,
        numero_paginas=numero_paginas,
        editorial=editorial,
        fecha_publicacion=fecha_publicacion,
        edicion=edicion,
        idioma=idioma,
        peso_libro=peso_libro,
        formato_libro=formato_libro,
        tipo_literatura=tipo_literatura
    )
    db.add(nuevo_libro)
    try:
        db.commit()
        db.refresh(nuevo_libro)
        logger.info(f"Libro insertado correctamente (código: {codigo_inventario}).")
    except IntegrityError as ie:
        db.rollback()
        logger.error("Error al insertar el libro", exc_info=ie)
        raise HTTPException(status_code=500, detail="Error al insertar el libro")
    
    # Operación en MongoDB: insertar y luego obtener la reseña
    if resena:
        insert_review("libro", codigo_inventario, resena)
    nuevo_libro.resena = get_review("libro", codigo_inventario)
    
    return nuevo_libro

@router.get("/", response_model=list[LibroResponse])
def listar_libros(db: Session = Depends(get_db)):
    libros = db.query(Libro).options(joinedload(Libro.material)).all()
    for libro in libros:
        libro.resena = get_review("libro", libro.codigo_inventario)
    return libros

@router.get("/{codigo_inventario}", response_model=LibroResponse)
def obtener_libro(codigo_inventario: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).options(joinedload(Libro.material))\
                         .filter_by(codigo_inventario=codigo_inventario).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    libro.resena = get_review("libro", codigo_inventario)
    return libro

@router.delete("/{codigo_inventario}")
def eliminar_libro(codigo_inventario: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter_by(codigo_inventario=codigo_inventario).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    material = libro.material
    if material:
        db.delete(material)
    db.delete(libro)
    db.commit()
    delete_review("libro", codigo_inventario)
    return {"message": "Libro y registro de material eliminado exitosamente"}
