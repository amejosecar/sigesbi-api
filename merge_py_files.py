#!/usr/bin/env python3
import os

# Lista de rutas de los archivos a incluir, tanto .py como .html,
# usando raw strings (r"") para evitar problemas de secuencias de escape en Windows.
paths_to_process = [
    r"C:\americo\API\sigesbi-api\database.py",
    r"C:\americo\API\sigesbi-api\main.py",
    r"C:\americo\API\sigesbi-api\models.py",
    r"C:\americo\API\sigesbi-api\schemas.py",
    r"C:\americo\API\sigesbi-api\settings.py",
    r"C:\americo\API\sigesbi-api\templates.py",
    r"C:\americo\API\sigesbi-api\utils.py",
    r"C:\americo\API\sigesbi-api\routers\dvds.py",
    r"C:\americo\API\sigesbi-api\routers\libros.py",
    r"C:\americo\API\sigesbi-api\routers\prestamos.py",
    r"C:\americo\API\sigesbi-api\routers\revistas.py",
    r"C:\americo\API\sigesbi-api\routers\usuarios.py",
    r"C:\americo\API\sigesbi-api\routers\__init__.py",
    r"C:\americo\API\sigesbi-api\templates\dvds.html",
    r"C:\americo\API\sigesbi-api\templates\index.html",
    r"C:\americo\API\sigesbi-api\templates\libros.html",
    r"C:\americo\API\sigesbi-api\templates\revistas.html",
    r"C:\americo\API\sigesbi-api\templates\usuarios.html"
]

def write_files_to_txt(file_paths, output_file):
    """
    Escribe el contenido de cada archivo en 'file_paths' dentro de 'output_file'.
    Antes del contenido de cada archivo se inserta:
      - Una línea divisoria (40 guiones)
      - Una línea con la ruta y nombre del archivo (formateado como comentario)
    """
    with open(output_file, "w", encoding="utf8") as outf:
        for file_path in file_paths:
            # Línea divisoria
            outf.write("-" * 40 + "\n")
            # Encabezado con la ruta y el nombre del archivo
            outf.write(f"# {file_path}\n")
            # Leer y escribir el contenido del archivo
            try:
                with open(file_path, "r", encoding="utf8") as f:
                    outf.write(f.read())
            except Exception as e:
                outf.write(f"# Error al leer este archivo: {e}\n")
            outf.write("\n")
    print(f"Se han copiado {len(file_paths)} archivos a '{output_file}'.")

if __name__ == "__main__":
    output_file = "merged_output.txt"
    write_files_to_txt(paths_to_process, output_file)
