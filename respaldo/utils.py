# sigesbi-api/utils.py
# 
from fastapi.responses import JSONResponse
from typing import Any

def respuesta_personalizada(mensaje: str, codigo: int = 200, data: Any = None):
    """ 
    Genera una respuesta JSON personalizada con mensaje, código de estado y datos opcionales.
    """
    return JSONResponse(content={"mensaje": mensaje, "datos": data}, status_code=codigo)

def validar_codigo_inventario(codigo: int) -> bool:
    """ Valida que un código de inventario sea un número positivo. """
    return isinstance(codigo, int) and codigo > 0



