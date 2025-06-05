# sigesbi-api/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import Form

# 📚 Esquema para MaterialBiblioteca
class MaterialBase(BaseModel):
    titulo: str = Form(...)
    autor: str = Form(...)
    ubicacion: Optional[str] = Form(None)
    tipo_material: str = Form(...)

class MaterialCreate(MaterialBase):
    disponible: Optional[bool] = Form(True)

class MaterialResponse(MaterialBase):
    codigo_inventario: int
    disponible: bool

    class Config:
        from_attributes = True

# 📖 Esquema para Libros
class LibroBase(BaseModel):
    isbn: Optional[str] = Form(None)
    numero_paginas: Optional[int] = Form(None)
    editorial: Optional[str] = Form(None)
    fecha_publicacion: Optional[str] = Form(None)
    edicion: Optional[str] = Form(None)
    idioma: Optional[str] = Form(None)
    peso_libro: Optional[float] = Form(None)
    formato_libro: Optional[str] = Form(None)
    tipo_literatura: Optional[str] = Form(None)
    resena: Optional[str] = Form(None)

class LibroCreate(LibroBase):
    codigo_inventario: int = Form(...)
    titulo: str = Form(...)  
    autor: str = Form(...)  

class LibroResponse(BaseModel):
    material: MaterialResponse
    codigo_inventario: int
    isbn: Optional[str] = None
    numero_paginas: Optional[int] = None
    editorial: Optional[str] = None
    fecha_publicacion: Optional[str] = None
    edicion: Optional[str] = None
    idioma: Optional[str] = None
    peso_libro: Optional[float] = None
    formato_libro: Optional[str] = None
    tipo_literatura: Optional[str] = None
    resena: Optional[str] = None

    class Config:
        from_attributes = True

# 📕 Esquema para Revistas
class RevistaBase(BaseModel):
    isbn: Optional[str] = Form(None)
    numero_edicion: Optional[int] = Form(None)
    fecha_publicacion: Optional[str] = Form(None)

class RevistaCreate(RevistaBase):
    codigo_inventario: int = Form(...)
    titulo: str = Form(...)  
    autor: str = Form(...)  

class RevistaResponse(BaseModel):
    material: MaterialResponse
    codigo_inventario: int
    isbn: Optional[str] = None
    numero_edicion: Optional[int] = None
    fecha_publicacion: Optional[str] = None

    class Config:
        from_attributes = True

# 📀 Esquema para DVDs
class DVDBase(BaseModel):
    isbn: Optional[str] = Form(None)
    duracion: Optional[int] = Form(None)
    formato: Optional[str] = Form(None)

class DVDCreate(DVDBase):
    codigo_inventario: int = Form(...)
    titulo: str = Form(...)  
    autor: str = Form(...)  

class DVDResponse(BaseModel):
    material: MaterialResponse
    codigo_inventario: int
    isbn: Optional[str] = None
    duracion: Optional[int] = None
    formato: Optional[str] = None

    class Config:
        from_attributes = True

# 👤 Esquema para Usuarios
class UsuarioBase(BaseModel):
    nombre: str = Form(...)
    apellido: str = Form(...)
    email: EmailStr = Form(...)

class UsuarioCreate(UsuarioBase):
    pass  

class UsuarioResponse(UsuarioBase):
    usuario_id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

# 🔄 Esquema para Préstamos
class PrestamoBase(BaseModel):
    codigo_inventario: int = Form(...)
    usuario_id: int = Form(...)

class PrestamoCreate(PrestamoBase):
    pass  

class PrestamoResponse(BaseModel):
    prestamo_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    devuelto: bool

    class Config:
        from_attributes = True
