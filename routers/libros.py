# sigesbi-api/routers/libros.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Libro, MaterialBiblioteca
from schemas import LibroResponse
from sqlalchemy.exc import IntegrityError
from ..mongodb import insert_review, get_review, delete_review


router = APIRouter()

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
    El campo 'resena' se guarda en MongoDB.
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
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al crear el registro de material")
    
    # Verificar si ya existe el libro
    libro_existente = db.query(Libro).filter_by(codigo_inventario=codigo_inventario).first()
    if libro_existente:
        raise HTTPException(status_code=409, detail="Ya existe un libro con ese código de inventario")
    
    # Crear el registro en libros (no se asigna 'resena' en SQLite, se gestiona en MongoDB)
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
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar el libro")
    
    db.refresh(nuevo_libro)
    # Insertar la reseña en MongoDB si se proporcionó
    if resena:
        insert_review("libro", codigo_inventario, resena)
    # Leer la reseña de MongoDB para adjuntarla en la respuesta
    mongo_resena = get_review("libro", codigo_inventario)
    libro_dict = nuevo_libro.__dict__
    libro_dict["resena"] = mongo_resena
    return libro_dict

@router.get("/", response_model=list[LibroResponse])
def listar_libros(db: Session = Depends(get_db)):
    """
    Lista todos los libros con la información del material asociado,
    incluyendo la reseña almacenada en MongoDB.
    """
    libros = db.query(Libro).options(joinedload(Libro.material)).all()
    result = []
    for libro in libros:
        libro_dict = libro.__dict__
        libro_dict["resena"] = get_review("libro", libro.codigo_inventario)
        result.append(libro_dict)
    return result

@router.get("/{codigo_inventario}", response_model=LibroResponse)
def obtener_libro(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Obtiene la información de un libro por su código de inventario,
    incluyendo la reseña almacenada en MongoDB.
    """
    libro = db.query(Libro).options(joinedload(Libro.material))\
                         .filter_by(codigo_inventario=codigo_inventario).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    libro_dict = libro.__dict__
    libro_dict["resena"] = get_review("libro", codigo_inventario)
    return libro_dict

@router.delete("/{codigo_inventario}")
def eliminar_libro(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Elimina un libro y su registro asociado en MaterialBiblioteca,
    además elimina la reseña en MongoDB.
    """
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
