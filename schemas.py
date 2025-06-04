# sigesbi/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# =============================================================================
# 📚 Esquema para MaterialBiblioteca
# =============================================================================
class MaterialBase(BaseModel):
    titulo: str
    autor: str
    ubicacion: Optional[str] = None
    tipo_material: str

class MaterialCreate(MaterialBase):
    disponible: Optional[bool] = True

class MaterialResponse(MaterialBase):
    codigo_inventario: int
    disponible: bool

    class Config:
        from_attributes = True

# =============================================================================
# 📖 Esquema para Libros
# =============================================================================
class LibroBase(BaseModel):
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

# --- Solución 1: El cliente debe enviar también los datos completos del material ---
class LibroCreate(LibroBase):
    codigo_inventario: int
    titulo: str        # Campo para MaterialBiblioteca
    autor: str         # Campo para MaterialBiblioteca

# Actualización para que la respuesta incluya el bloque "material" (se muestra primero)
class LibroResponse(BaseModel):
    material: MaterialResponse
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
    codigo_inventario: int

    class Config:
        from_attributes = True

# =============================================================================
# 📕 Esquema para Revistas
# =============================================================================
class RevistaBase(BaseModel):
    isbn: Optional[str] = None
    numero_edicion: Optional[int] = None
    fecha_publicacion: Optional[str] = None

class RevistaCreate(RevistaBase):
    codigo_inventario: int
    titulo: str
    autor: str

class RevistaResponse(BaseModel):
    material: MaterialResponse
    isbn: Optional[str] = None
    numero_edicion: Optional[int] = None
    fecha_publicacion: Optional[str] = None
    codigo_inventario: int

    class Config:
        from_attributes = True

# =============================================================================
# 📀 Esquema para DVDs
# =============================================================================
class DVDBase(BaseModel):
    isbn: Optional[str] = None
    duracion: Optional[int] = None
    formato: Optional[str] = None

class DVDCreate(DVDBase):
    codigo_inventario: int
    titulo: str
    autor: str

class DVDResponse(BaseModel):
    material: MaterialResponse
    isbn: Optional[str] = None
    duracion: Optional[int] = None
    formato: Optional[str] = None
    codigo_inventario: int

    class Config:
        from_attributes = True

# =============================================================================
# 👤 Esquema para Usuarios
# =============================================================================
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    pass  # No requiere información adicional para la creación

class UsuarioResponse(UsuarioBase):
    usuario_id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

# =============================================================================
# 🔄 Esquema para Préstamos
# =============================================================================
class PrestamoBase(BaseModel):
    codigo_inventario: int
    usuario_id: int

class PrestamoCreate(PrestamoBase):
    pass  # No requiere información adicional

class PrestamoResponse(PrestamoBase):
    prestamo_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    devuelto: bool

    class Config:
        from_attributes = True
