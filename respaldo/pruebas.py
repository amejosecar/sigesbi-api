from database import SessionLocal
from models import Libro

db = SessionLocal()

nuevo_libro = Libro(
    codigo_inventario=300,
    isbn="978-8408292456",
    numero_paginas=528,
    editorial="Booket",
    fecha_publicacion="2024-10-23",
    edicion="1",
    idioma="Español",
    peso_libro=335,
    formato_libro="Tapa blanda",
    tipo_literatura="Novelas juveniles de arte y arquitectura",
    resena="me he encariñado tanto con Leah y Logan"
)

db.add(nuevo_libro)
db.commit()
db.refresh(nuevo_libro)
print(nuevo_libro)
db.close()



from database import SessionLocal
from models import Libro

db = SessionLocal()

# Buscar el libro por código de inventario
libro = db.query(Libro).filter_by(codigo_inventario=300).first()

# Si existe, eliminarlo
if libro:
    db.delete(libro)
    db.commit()
    print("Libro eliminado exitosamente.")
else:
    print("El libro no existe en la base de datos.")

db.close()
