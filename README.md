# sigesbi-api
# SiGesBi API

**SiGesBi API** es un sistema de gestión de biblioteca desarrollado en FastAPI. Permite administrar diferentes tipos de materiales (libros, revistas, DVDs), gestionar usuarios y controlar préstamos de forma sencilla, rápida y segura.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías y Herramientas](#tecnologías-y-herramientas)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints Principales](#endpoints-principales)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Características

- **CRUD Completo**: Permite crear, leer, actualizar y eliminar registros de libros, revistas, DVDs y usuarios.
- **Gestión de Préstamos**: Registra y controla los préstamos de materiales, incluyendo la devolución.
- **Relaciones de Datos**: Cada material pertenece a una entidad base (*MaterialBiblioteca*) que almacena datos comunes (título, autor, ubicación, disponibilidad y tipo de material).
- **Respuesta Anidada**: Las consultas devuelven la información completa tanto del material principal como de su entidad asociada (libro, revista o DVD).
- **Desarrollo Rápido**: Implementado con FastAPI, que incluye documentación interactiva automática.

## Tecnologías y Herramientas

- **[FastAPI](https://fastapi.tiangolo.com/)** – Framework web moderno y rápido para construir APIs con Python.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM para la gestión y manipulación de la base de datos.
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** – Validación y serialización de datos.
- **[Uvicorn](https://www.uvicorn.org/)** – Servidor ASGI para ejecutar la aplicación.
- **SQLite** – Motor de base de datos por defecto (configurable mediante variables de entorno).
- **python-dotenv** – Para la gestión de variables de entorno y configuración sensible.

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/sigesbi-api.git
   cd sigesbi-api
