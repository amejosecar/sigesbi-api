# sigesbi-api/models.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MaterialBiblioteca(Base):
    __tablename__ = "material_biblioteca"
    codigo_inventario = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    ubicacion = Column(String)
    disponible = Column(Boolean, default=True)
    tipo_material = Column(String, nullable=False)

    # Relaciones
    libro = relationship("Libro", uselist=False, back_populates="material")
    revista = relationship("Revista", uselist=False, back_populates="material")
    dvd = relationship("DVD", uselist=False, back_populates="material")
    prestamos = relationship("Prestamo", back_populates="material", cascade="all, delete-orphan")

class Libro(Base):
    __tablename__ = "libro"
    codigo_inventario = Column(Integer, ForeignKey("material_biblioteca.codigo_inventario"), primary_key=True)
    isbn = Column(String)
    numero_paginas = Column(Integer)
    editorial = Column(String)
    fecha_publicacion = Column(String)
    edicion = Column(String)
    idioma = Column(String)
    peso_libro = Column(Float)
    formato_libro = Column(String)
    tipo_literatura = Column(String)
    resena = Column(String)

    material = relationship("MaterialBiblioteca", back_populates="libro")

class Revista(Base):
    __tablename__ = "revista"
    codigo_inventario = Column(Integer, ForeignKey("material_biblioteca.codigo_inventario"), primary_key=True)
    isbn = Column(String)
    numero_edicion = Column(Integer)
    fecha_publicacion = Column(String)

    material = relationship("MaterialBiblioteca", back_populates="revista")

class DVD(Base):
    __tablename__ = "dvd"
    codigo_inventario = Column(Integer, ForeignKey("material_biblioteca.codigo_inventario"), primary_key=True)
    isbn = Column(String)
    duracion = Column(Integer)
    formato = Column(String)

    material = relationship("MaterialBiblioteca", back_populates="dvd")

class Usuario(Base):
    __tablename__ = "usuarios"
    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    fecha_registro = Column(DateTime, default=datetime.now)

    prestamos = relationship("Prestamo", back_populates="usuario", cascade="all, delete-orphan")

class Prestamo(Base):
    __tablename__ = "prestamos"
    prestamo_id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_inventario = Column(Integer, ForeignKey("material_biblioteca.codigo_inventario"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    fecha_prestamo = Column(DateTime, default=datetime.now)
    fecha_devolucion = Column(DateTime)
    devuelto = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="prestamos")
    material = relationship("MaterialBiblioteca", back_populates="prestamos")
