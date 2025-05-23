from mcp.server.fastmcp import FastMCP
import json
import os
from typing import Dict, Any, Tuple, Optional
import mcp.types as types

mcp = FastMCP("search_file_pro")

# Path global para el archivo JSON
MEMORIA_PATH = "/Users/msaez/Desktop/Gesco/estructura.json"

@mcp.tool()
def verificar_memoria(ruta: Optional[str] = None) -> Dict:
    """
    Verifica que el archivo de memoria tenga una estructura válida.

    Args:
        ruta: Path opcional donde está el archivo JSON (usa MEMORIA_PATH por defecto)
        
    Returns:
        dict: Resultado de la validación
    """ 
    ruta = ruta or MEMORIA_PATH
    
    try:
        if not os.path.exists(ruta):
            return {"error": True, "mensaje": f"No se encontró el archivo en {ruta}"}
            
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            
        if not isinstance(datos, dict):
            return {"error": True, "mensaje": "El archivo no contiene un objeto JSON válido"}
            
        return {"error": False, "mensaje": "Archivo válido", "datos": datos}
        
    except json.JSONDecodeError:
        return {"error": True, "mensaje": "El archivo no contiene JSON válido"}
    except Exception as e:
        return {"error": True, "mensaje": f"Error al leer el archivo: {str(e)}"}

@mcp.tool()
def obtener_descripciones_y_paths(ruta_json: str = None) -> dict:
    """
    Carga la estructura de directorios desde un archivo JSON y devuelve una lista
    de diccionarios con la descripción y el path completo de cada directorio.

    Args:
        ruta_json (str): Ruta al archivo JSON. Si no se proporciona, usa MEMORIA_PATH.

    Returns:
        dict: Diccionario con la clave 'resultado' que contiene la lista de descripciones y paths.
    """
    ruta_json = ruta_json or MEMORIA_PATH
    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"error": True, "mensaje": f"No se pudo cargar el JSON: {str(e)}"}

    resultado = []

    def recorrer(nodo):
        if nodo.get("type") == "directory":
            resultado.append({
                "descripcion": nodo.get("description", ""),
                "full_path": nodo.get("full_path", "")
            })
            for hijo in nodo.get("children", []):
                recorrer(hijo)

    recorrer(data)
    return {"error": False, "resultado": resultado}

@mcp.tool()
def combinar_descripciones_y_prompt(descripciones: list, prompt: str) -> dict:
    """
    Siempre que un prompt empiece con "Buscar:" se debe usar esta herramienta.
    Entonces se comparara el prompt con las descripciones de los directorios y se usara el path completo del directorio que coincida con el prompt para buscar en el sistema de archivos. Una vez encontrado el path completo, se usará la herramienta read_multiple_files para leer los archivos de ese path y dar una respuesta a la pregunta.

    Args:
        descripciones (list): Lista de diccionarios con descripciones y paths.
        prompt (str): Prompt o consulta del usuario.

    Returns:
        dict: Diccionario con las claves 'descripciones' y 'prompt'.
    """
    return {
        "descripciones": descripciones,
        "prompt": prompt
    }

@mcp.tool()
def leer_archivo(path: str) -> dict:
    """
    Lee el contenido completo de un archivo del sistema de archivos.

    Args:
        path (str): Ruta absoluta o relativa al archivo.

    Returns:
        dict: Diccionario con el contenido del archivo o un mensaje de error.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read()
        return {"error": False, "contenido": contenido}
    except Exception as e:
        return {"error": True, "mensaje": f"No se pudo leer el archivo: {str(e)}"}

@mcp.tool()
def leer_multiples_archivos(paths: list) -> dict:
    """
    Lee el contenido de múltiples archivos simultáneamente.

    Args:
        paths (list): Lista de rutas de archivos a leer.

    Returns:
        dict: Diccionario con los contenidos de los archivos o mensajes de error por cada archivo.
    """
    resultados = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read()
            resultados.append({"path": path, "error": False, "contenido": contenido})
        except Exception as e:
            resultados.append({"path": path, "error": True, "mensaje": f"No se pudo leer el archivo: {str(e)}"})
    return {"resultados": resultados}

if __name__ == "__main__":
    mcp.run()
