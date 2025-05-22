from mcp.server.fastmcp import FastMCP
import os
import json
from typing import Dict, List, Union, Tuple, Optional
from datetime import datetime
import mcp.types as types

mcp = FastMCP("filesystem_pro")


# # Ruta global para el archivo de memoria
MEMORIA_PATH = "/Users/msaez/Desktop/Gesco"
MEMORIA_FILENAME = "estructura_directorios.json"

# # Esquema de validación
# ESQUEMA_NODO = {
#     "file": ["name", "type"],
#     "directory": ["name", "type", "description", "children"]
# }


@mcp.tool()
def guardar_memoria(resultado, ruta):
    """
    Guarda un resultado (diccionario JSON) en la ruta especificada.

    Parámetros:
    - resultado (dict): El contenido JSON a guardar.
    - ruta (str): Ruta completa del archivo (incluyendo nombre y extensión), ej: "/directorio/estructura_directorios.json"
    """
    try:
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)

        # Guardar el resultado en formato JSON
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(resultado, archivo, ensure_ascii=False, indent=4)

        print(f"Resultado guardado en: {ruta}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

@mcp.tool()
def leer_estructura_directorios(ruta_analizar: str, force: bool = False) -> Dict[str, Union[str, List]]:
    """
    Lee la estructura de directorios del path especificado, guarda el resultado
    en el path especificado y devuelve la estructura.

    Args:
        ruta_analizar: Path del directorio a analizar
        force: Si es True, sobreescribe el archivo sin preguntar

    Returns:
        dict: Estructura de directorios en formato diccionario anidado
    """
    def explorar_directorio(path: str) -> Dict[str, Union[str, List]]:
        nombre = os.path.basename(path)
        if nombre.startswith('.') and nombre != os.path.basename(ruta_analizar):
            return None

        estructura = {
            'name': nombre,
            'type': 'directory',
            'description': '',
            'children': [],
            'full_path': os.path.abspath(path)
        }

        try:
            elementos = os.listdir(path)
            for elemento in sorted(elementos):
                if elemento.startswith('.'):
                    continue
                ruta_completa = os.path.join(path, elemento)
                if os.path.isdir(ruta_completa):
                    subestructura = explorar_directorio(ruta_completa)
                    if subestructura is not None:
                        estructura['children'].append(subestructura)
                else:
                    archivo = {
                        'name': elemento,
                        'type': 'file',
                        'full_path': os.path.abspath(ruta_completa)
                    }
                    estructura['children'].append(archivo)
        except PermissionError:
            estructura['error'] = 'Sin permisos de acceso'
        except Exception as e:
            estructura['error'] = str(e)

        return estructura

    if not os.path.exists(ruta_analizar):
        return {'error': 'La ruta no existe'}

    if not os.path.isdir(ruta_analizar):
        return {'error': 'La ruta no es un directorio'}

    resultado = explorar_directorio(ruta_analizar)

    # Ruta fija de guardado
    ruta_guardar = "/Users/msaez/Desktop/Gesco/estructura.json"

    try:
        # Crear el directorio si no existe (aunque en este caso siempre existe)
        os.makedirs(os.path.dirname(ruta_guardar), exist_ok=True)

        with open(ruta_guardar, 'w', encoding='utf-8') as archivo:
            json.dump(resultado, archivo, ensure_ascii=False, indent=4)

        print(f"Resultado guardado en: {ruta_guardar}")
        resultado['archivo_generado'] = ruta_guardar
    except Exception as e:
        resultado['error_guardado'] = f"Error al guardar el archivo JSON: {str(e)}"

    return resultado

if __name__ == "__main__":
    mcp.run()