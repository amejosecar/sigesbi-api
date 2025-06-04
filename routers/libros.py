#sigesbi/routers/libros.py
# 

# sigesbi/routers/libros.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Libro, MaterialBiblioteca
from schemas import LibroCreate, LibroResponse
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/", response_model=LibroResponse)
def agregar_libro(libro_data: LibroCreate, db: Session = Depends(get_db)):
    """
    Agrega un nuevo libro a la biblioteca.
    Si el registro en MaterialBiblioteca no existe, se crea usando los datos enviados.
    """
    # Verificar si existe el registro en MaterialBiblioteca
    material = db.query(MaterialBiblioteca).filter_by(codigo_inventario=libro_data.codigo_inventario).first()
    if not material:
        material = MaterialBiblioteca(
            codigo_inventario=libro_data.codigo_inventario,
            titulo=libro_data.titulo,
            autor=libro_data.autor,
            tipo_material="Libro"
        )
        db.add(material)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear MaterialBiblioteca: {e}")
        db.refresh(material)
    
    # Verificar duplicados en la tabla Libro (opcional)
    libro_existente = db.query(Libro).filter_by(codigo_inventario=libro_data.codigo_inventario).first()
    if libro_existente:
        raise HTTPException(status_code=409, detail="Ya existe un libro con ese código de inventario")
    
    # Crear el registro del libro (excluyendo 'titulo' y 'autor', ya usados para MaterialBiblioteca)
    nuevo_libro = Libro(**libro_data.dict(exclude={"titulo", "autor"}))
    db.add(nuevo_libro)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar el libro: {e}")
    db.refresh(nuevo_libro)
    return nuevo_libro

@router.get("/", response_model=list[LibroResponse])
def listar_libros(db: Session = Depends(get_db)):
    """
    Lista todos los libros, incluyendo la información del material asociado.
    """
    libros = db.query(Libro).options(joinedload(Libro.material)).all()
    return libros

@router.get("/{codigo_inventario}", response_model=LibroResponse)
def obtener_libro(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Obtiene la información de un libro específico, junto con su registro en MaterialBiblioteca.
    """
    libro = db.query(Libro).options(joinedload(Libro.material)).filter_by(codigo_inventario=codigo_inventario).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.delete("/{codigo_inventario}")
def eliminar_libro(codigo_inventario: int, db: Session = Depends(get_db)):
    """
    Elimina un libro y, además, elimina el registro asociado en MaterialBiblioteca.
    """
    libro = db.query(Libro).filter_by(codigo_inventario=codigo_inventario).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    material = libro.material
    db.delete(libro)
    db.commit()
    if material:
        db.delete(material)
        db.commit()
    return {"message": "Libro y registro de material eliminado exitosamente"}
