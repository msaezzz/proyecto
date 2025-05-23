from mcp.server.fastmcp import FastMCP
import os
import json
from typing import Dict, List, Union, Tuple, Optional
from datetime import datetime
import mcp.types as types

mcp = FastMCP("filesystem_pro")


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

@mcp.tool()
def agregar_descripcion_repo(json_path: str, nombre_repo: str, descripcion: str) -> dict:
    """
    Añade o modifica la descripción de un directorio (repo) en el JSON de estructura de directorios.

    Parámetros:
    - json_path (str): Ruta al archivo JSON.
    - nombre_repo (str): Nombre del directorio (repo) al que se le quiere añadir la descripción.
    - descripcion (str): Descripción a añadir.

    Returns:
        dict: Resultado de la operación (éxito o error)
    """
    import json
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            estructura = json.load(f)
    except Exception as e:
        return {"error": f"No se pudo leer el archivo JSON: {str(e)}"}

    def buscar_y_actualizar(nodo):
        if nodo.get('type') == 'directory' and nodo.get('name') == nombre_repo:
            nodo['description'] = descripcion
            return True
        for child in nodo.get('children', []):
            if buscar_y_actualizar(child):
                return True
        return False

    encontrado = buscar_y_actualizar(estructura)

    if encontrado:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(estructura, f, ensure_ascii=False, indent=4)
            return {"success": f"Descripción añadida/modificada para el repo '{nombre_repo}'."}
        except Exception as e:
            return {"error": f"No se pudo guardar el archivo JSON: {str(e)}"}
    else:
        return {"error": f"No se encontró el repo '{nombre_repo}' en la estructura."}

@mcp.tool()
def obtener_descripciones_directorios(json_path: str) -> dict:
    """
    Devuelve un diccionario con el nombre de cada directorio, su descripción y su path completo.

    Parámetros:
    - json_path (str): Ruta al archivo JSON.

    Returns:
        dict: {nombre_directorio: {"descripcion": ..., "full_path": ...}, ...}
    """
    import json
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            estructura = json.load(f)
    except Exception as e:
        return {"error": f"No se pudo leer el archivo JSON: {str(e)}"}

    descripciones = {}

    def recolectar(nodo):
        if nodo.get('type') == 'directory':
            descripciones[nodo.get('name')] = {
                'descripcion': nodo.get('description', ''),
                'full_path': nodo.get('full_path', '')
            }
            for child in nodo.get('children', []):
                recolectar(child)

    recolectar(estructura)
    return descripciones

if __name__ == "__main__":
    mcp.run()