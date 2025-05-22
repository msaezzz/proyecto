from mcp.server.fastmcp import FastMCP
import os
import json
from typing import Dict, List, Union, Tuple, Optional
from datetime import datetime
import mcp.types as types

# PROMPTS = {
#     "encontrar-recurso": types.Prompt(
#         name="encontrar-recurso",
#         description="Encontrar un recurso en el sistema",
#         arguments=[
#             types.PromptArgument(
#                 name="query",
#                 description="Pregunta para encontrar un recurso",
#                 required=True
#             )
#         ]
#     )
# }

mcp = FastMCP("filesystem_pro")

# @mcp.list_prompts()
# async def list_prompts() -> list[types.Prompt]:
#     return list(PROMPTS.values())

# @mcp.get_prompt()
# async def get_prompt(
#     name: str, arguments: dict[str, str] | None = None
# ) -> types.GetPromptResult:
#     if name not in PROMPTS:
#         raise ValueError(f"Prompt not found: {name}")


#     if name == "explain-code":
#         code = arguments.get("code") if arguments else ""
#         language = arguments.get("language", "Unknown") if arguments else "Unknown"
#         return types.GetPromptResult(
#             messages=[
#                 types.PromptMessage(
#                     role="user",
#                     content=types.TextContent(
#                         type="text",
#                         text=f"Explain how this {language} code works:\n\n{code}"
#                     )
#                 )
#             ]
#         )

#     raise ValueError("Prompt not found")
    

# # Ruta global para el archivo de memoria
# MEMORIA_PATH = os.path.join(os.path.expanduser("~"), "Desktop/Gesco")
# MEMORIA_FILENAME = "estructura_directorios.json"

# # Esquema de validación
# ESQUEMA_NODO = {
#     "file": ["name", "type"],
#     "directory": ["name", "type", "description", "children"]
# }


# def validar_estructura(estructura: Dict) -> Tuple[bool, str]:
#     """
#     Valida que la estructura del JSON sea correcta.
    
#     Args:
#         estructura: Diccionario con la estructura a validar
        
#     Returns:
#         Tuple[bool, str]: (es_válido, mensaje_error)
#     """
#     def validar_nodo(nodo: Dict, path: str = "") -> Tuple[bool, str]:
#         # Validar campos requeridos básicos
#         if "type" not in nodo or "name" not in nodo:
#             return False, f"Nodo en {path} no tiene los campos requeridos (type, name)"
            
#         tipo = nodo["type"]
#         if tipo not in ESQUEMA_NODO:
#             return False, f"Tipo inválido '{tipo}' en {path}"
            
#         # Validar campos según el tipo
#         for campo in ESQUEMA_NODO[tipo]:
#             if campo not in nodo:
#                 return False, f"Campo '{campo}' requerido faltante en {path}"
                
#         # Para directorios, validar recursivamente los hijos
#         if tipo == "directory":
#             if not isinstance(nodo["children"], list):
#                 return False, f"Campo 'children' debe ser una lista en {path}"
                
#             for i, hijo in enumerate(nodo["children"]):
#                 path_hijo = f"{path}/{nodo['name']}" if path else nodo['name']
#                 valido, error = validar_nodo(hijo, path_hijo)
#                 if not valido:
#                     return False, error
                    
#         return True, ""
        
#     return validar_nodo(estructura)

# @mcp.tool()
# def verificar_memoria(ruta: Optional[str] = None) -> Dict:
#     """
#     Verifica que el archivo de memoria tenga una estructura válida.
    
#     Args:
#         ruta: Path opcional donde está el archivo JSON (usa MEMORIA_PATH por defecto)
        
#     Returns:
#         dict: Resultado de la validación
#     """
#     try:
#         ruta_json = get_memoria_path(ruta)
#         if not os.path.exists(ruta_json):
#             return {"error": "No existe el archivo de estructura"}
            
#         with open(ruta_json, 'r', encoding='utf-8') as f:
#             estructura = json.load(f)
            
#         valido, error = validar_estructura(estructura)
        
#         if not valido:
#             return {
#                 "valido": False,
#                 "error": error
#             }
            
#         return {
#             "valido": True,
#             "mensaje": "La estructura es válida"
#         }
        
#     except json.JSONDecodeError:
#         return {
#             "valido": False,
#             "error": "El archivo no es un JSON válido"
#         }
#     except Exception as e:
#         return {
#             "valido": False,
#             "error": f"Error al verificar la estructura: {str(e)}"
#         }

def get_memoria_path(ruta: Optional[str] = None) -> str:
    """
    Obtiene la ruta completa del archivo de memoria.
    
    Args:
        ruta: Path opcional donde buscar/guardar el archivo
        
    Returns:
        str: Ruta completa al archivo de memoria
    """
    base_path = ruta if ruta else MEMORIA_PATH
    return os.path.join(base_path, MEMORIA_FILENAME)

@mcp.tool()
def guardar_memoria(datos: Dict, ruta: Optional[str] = None, force: bool = False) -> Tuple[bool, str, str]:
    """
    Guarda los datos proporcionados en un archivo JSON.
    Si ya existe un archivo, pregunta antes de sobreescribir y lo respalda con extensión .bkp
        
    Args:
        datos: Diccionario con los datos a guardar
        ruta: Path opcional donde guardar el archivo (usa MEMORIA_PATH por defecto)
        force: Si es True, sobreescribe sin preguntar. Si es False, pregunta antes de sobreescribir.
        
    Returns:
        Tuple[bool, str, str]: (éxito, nombre_archivo, mensaje_error)
            - éxito: True si se guardó correctamente, False si hubo error
            - nombre_archivo: Nombre del archivo generado (vacío si hubo error)
            - mensaje_error: Descripción del error (vacío si no hubo error)
    """
    try:
        ruta_json = get_memoria_path(ruta)
        ruta_backup = f"{ruta_json}.bkp"
        
        if os.path.exists(ruta_json) and not force:
            return False, "", f"El archivo {MEMORIA_FILENAME} ya existe. Use force=True para sobreescribir."
        
        if os.path.exists(ruta_json):
            if os.path.exists(ruta_backup):
                os.remove(ruta_backup)
            os.rename(ruta_json, ruta_backup)
        
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            
        return True, MEMORIA_FILENAME, ""
        
    except Exception as e:
        return False, "", f"Error al guardar el archivo JSON: {str(e)}"

# @mcp.tool()
# def listar_directorios(ruta: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
#     """
#     Lee el archivo de estructura y devuelve una lista de todos los directorios
#     con sus descripciones, ignorando directorios ocultos (que comienzan con punto).
    
#     Args:
#         ruta: Path opcional donde está el archivo JSON (usa MEMORIA_PATH por defecto)
        
#     Returns:
#         dict: Diccionario con la lista de directorios y sus descripciones
#     """
#     try:
#         ruta_json = get_memoria_path(ruta)
#         if not os.path.exists(ruta_json):
#             return {"error": "No existe el archivo de estructura"}
            
#         with open(ruta_json, 'r', encoding='utf-8') as f:
#             estructura = json.load(f)
            
#         directorios = []
        
#         def explorar_nodo(nodo: Dict, ruta_actual: str = ""):
#             if nodo['type'] == 'directory' and not nodo['name'].startswith('.'):
#                 ruta_completa = os.path.join(ruta_actual, nodo['name'])
#                 directorios.append({
#                     "ruta": ruta_completa,
#                     "nombre": nodo['name'],
#                     "descripcion": nodo.get('description', '')
#                 })
                
#                 for child in nodo.get('children', []):
#                     explorar_nodo(child, ruta_completa)
        
#         explorar_nodo(estructura)
        
#         return {
#             "directorios": sorted(directorios, key=lambda x: x['ruta'])
#         }
        
#     except Exception as e:
#         return {"error": f"Error al leer los directorios: {str(e)}"}

@mcp.tool()
def actualizar_descripcion_directorio(ruta_relativa: str, descripcion: str, ruta: Optional[str] = None) -> Dict:
    """
    Actualiza la descripción de un directorio específico en la estructura.
    
    Args:
        ruta_relativa: Path relativo del directorio a actualizar
        descripcion: Nueva descripción para el directorio
        ruta: Path opcional donde está el archivo JSON (usa MEMORIA_PATH por defecto)
        
    Returns:
        dict: Estructura actualizada
    """
    try:
        ruta_json = get_memoria_path(ruta)
        if not os.path.exists(ruta_json):
            return {"error": "No existe el archivo de estructura"}
            
        with open(ruta_json, 'r', encoding='utf-8') as f:
            estructura = json.load(f)
            
        def actualizar_nodo(nodo: Dict, path_parts: List[str]) -> bool:
            if not path_parts:
                if nodo['type'] == 'directory':
                    nodo['description'] = descripcion
                    return True
                return False
                
            current = path_parts[0]
            if nodo['type'] != 'directory':
                return False
                
            for child in nodo['children']:
                if child['name'] == current:
                    return actualizar_nodo(child, path_parts[1:])
            return False
            
        path_parts = [p for p in ruta_relativa.split('/') if p]
        if actualizar_nodo(estructura, path_parts):
            exito, _, error = guardar_memoria(estructura, ruta, force=True)
            if not exito:
                return {"error": error}
            return estructura
        else:
            return {"error": "No se encontró el directorio especificado"}
            
    except Exception as e:
        return {"error": f"Error al actualizar la descripción: {str(e)}"}

@mcp.tool()
def leer_estructura_directorios(ruta_analizar: str, ruta_guardar: Optional[str] = None, force: bool = False) -> Dict[str, Union[str, List]]:
    """
    Lee la estructura de directorios del path especificado, guarda el resultado
    en un archivo JSON y devuelve la estructura.
    
    Args:
        ruta_analizar: Path del directorio a analizar
        ruta_guardar: Path opcional donde guardar el archivo JSON (usa MEMORIA_PATH por defecto)
        force: Si es True, sobreescribe el archivo sin preguntar
        
    Returns:
        dict: Estructura de directorios en formato diccionario anidado
    """
    def explorar_directorio(path: str) -> Dict[str, Union[str, List]]:
        nombre = os.path.basename(path)
        # Si es un directorio oculto (excepto el directorio actual), retornamos None
        if nombre.startswith('.') and nombre != os.path.basename(ruta_analizar):
            return None
            
        estructura = {
            'name': nombre,
            'type': 'directory',
            'description': '',
            'children': [],
            'full_path': os.path.abspath(path)  # Agregamos el path completo
        }
        
        # Agregar metadatos básicos
        estructura = agregar_metadatos_basicos(estructura, path)
        
        try:
            elementos = os.listdir(path)
            
            for elemento in sorted(elementos):
                # Ignorar elementos ocultos
                if elemento.startswith('.'):
                    continue
                    
                ruta_completa = os.path.join(path, elemento)
                
                if os.path.isdir(ruta_completa):
                    subestructura = explorar_directorio(ruta_completa)
                    # Solo agregamos la subestructura si no es None (no es oculta)
                    if subestructura is not None:
                        estructura['children'].append(subestructura)
                else:
                    archivo = {
                        'name': elemento,
                        'type': 'file',
                        'full_path': os.path.abspath(ruta_completa)  # Agregamos el path completo
                    }
                    # Agregar metadatos básicos al archivo
                    archivo = agregar_metadatos_basicos(archivo, ruta_completa)
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
    
    exito, nombre_archivo, error = guardar_memoria(resultado, ruta_guardar, force=force)
    
    if exito:
        resultado['archivo_generado'] = nombre_archivo
    else:
        resultado['error_guardado'] = error
    
    return resultado

@mcp.tool()
def actualizar_memoria(ruta: Optional[str] = None) -> Dict:
    """
    Actualiza la estructura de directorios existente con nuevos archivos y directorios,
    manteniendo las descripciones y metadatos existentes.
    
    Args:
        ruta: Path opcional donde está el archivo JSON (usa MEMORIA_PATH por defecto)
        
    Returns:
        dict: Estructura actualizada con los nuevos elementos
    """
    try:
        # Leer estructura existente
        ruta_json = get_memoria_path(ruta)
        if not os.path.exists(ruta_json):
            return {"error": "No existe el archivo de estructura"}
            
        with open(ruta_json, 'r', encoding='utf-8') as f:
            estructura_actual = json.load(f)
            
        # Obtener la ruta base del directorio a analizar
        ruta_base = os.path.dirname(ruta_json)
        
        def actualizar_nodo(nodo_actual: Dict, path: str) -> Dict:
            """
            Actualiza recursivamente un nodo de la estructura, preservando metadatos.
            """
            # Si el nodo es un archivo, no necesita actualización
            if nodo_actual['type'] == 'file':
                return nodo_actual
                
            # Crear diccionario de elementos existentes para búsqueda rápida
            elementos_existentes = {
                child['name']: child 
                for child in nodo_actual.get('children', [])
            }
            
            nuevos_elementos = []
            try:
                # Listar contenido actual del directorio
                for elemento in sorted(os.listdir(path)):
                    ruta_elemento = os.path.join(path, elemento)
                    
                    # Ignorar elementos ocultos
                    if elemento.startswith('.'):
                        continue
                        
                    # Si el elemento ya existe, actualizarlo recursivamente
                    if elemento in elementos_existentes:
                        if os.path.isdir(ruta_elemento):
                            nuevo_nodo = actualizar_nodo(
                                elementos_existentes[elemento],
                                ruta_elemento
                            )
                        else:
                            nuevo_nodo = elementos_existentes[elemento]
                    # Si es nuevo, crear entrada
                    else:
                        if os.path.isdir(ruta_elemento):
                            nuevo_nodo = {
                                'name': elemento,
                                'type': 'directory',
                                'description': '',
                                'children': []
                            }
                            nuevo_nodo = actualizar_nodo(nuevo_nodo, ruta_elemento)
                        else:
                            nuevo_nodo = {
                                'name': elemento,
                                'type': 'file'
                            }
                    
                    nuevos_elementos.append(nuevo_nodo)
                    
            except PermissionError:
                nodo_actual['error'] = 'Sin permisos de acceso'
            except Exception as e:
                nodo_actual['error'] = str(e)
            
            # Actualizar children manteniendo el resto de la estructura igual
            nodo_actual['children'] = nuevos_elementos
            return nodo_actual
            
        # Actualizar estructura completa
        estructura_actualizada = actualizar_nodo(estructura_actual, ruta_base)
        
        # Guardar estructura actualizada
        exito, nombre_archivo, error = guardar_memoria(estructura_actualizada, ruta, force=True)
        
        if not exito:
            return {"error": error}
            
        return estructura_actualizada
        
    except Exception as e:
        return {"error": f"Error al actualizar la estructura: {str(e)}"}

@mcp.tool()
def agregar_metadatos(ruta_relativa: str, metadatos: Dict, ruta: Optional[str] = None) -> Dict:
    """
    Agrega o actualiza metadatos para un directorio o archivo específico.
    
    Args:
        ruta_relativa: Path relativo del elemento a actualizar
        metadatos: Diccionario con los metadatos a agregar/actualizar
        ruta: Path opcional donde está el archivo JSON (usa MEMORIA_PATH por defecto)
        
    Returns:
        dict: Estructura actualizada
    """
    try:
        ruta_json = get_memoria_path(ruta)
        if not os.path.exists(ruta_json):
            return {"error": "No existe el archivo de estructura"}
            
        with open(ruta_json, 'r', encoding='utf-8') as f:
            estructura = json.load(f)
            
        def actualizar_nodo(nodo: Dict, path_parts: List[str]) -> bool:
            if not path_parts:
                # Agregar/actualizar metadatos preservando los existentes
                nodo_meta = nodo.get('metadata', {})
                nodo_meta.update({
                    **metadatos,
                    'ultima_modificacion': datetime.now().isoformat()
                })
                nodo['metadata'] = nodo_meta
                return True
                
            current = path_parts[0]
            if nodo['type'] != 'directory':
                return False
                
            for child in nodo['children']:
                if child['name'] == current:
                    return actualizar_nodo(child, path_parts[1:])
            return False
            
        path_parts = [p for p in ruta_relativa.split('/') if p]
        if actualizar_nodo(estructura, path_parts):
            exito, _, error = guardar_memoria(estructura, ruta, force=True)
            if not exito:
                return {"error": error}
            return estructura
        else:
            return {"error": "No se encontró el elemento especificado"}
            
    except Exception as e:
        return {"error": f"Error al actualizar metadatos: {str(e)}"}

def agregar_metadatos_basicos(nodo: Dict, ruta: str) -> Dict:
    """
    Agrega metadatos básicos a un nodo de la estructura.
    """
    try:
        stat = os.stat(ruta)
        nodo['metadata'] = {
            'creado': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modificado': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'tamano': stat.st_size,
            'permisos': oct(stat.st_mode)[-3:],
            'ultima_actualizacion': datetime.now().isoformat()
        }
    except:
        nodo['metadata'] = {
            'ultima_actualizacion': datetime.now().isoformat()
        }
    return nodo

@mcp.tool()
def encontrar_directorio_relevante(prompt: str) -> Dict:
    """
    Analiza un prompt que comienza con "Pregunta:" y determina el directorio
    más relevante para responder esa pregunta.
    
    Args:
        prompt: String que comienza con "Pregunta:" seguido de la consulta
        
    Returns:
        dict: Diccionario con la ruta del directorio más relevante o error
    """
    if not prompt.startswith("Pregunta:"):
        return {"error": "El prompt debe comenzar con 'Pregunta:'"}
        
    try:
        # Leer el archivo de estructura
        ruta_json = get_memoria_path()
        if not os.path.exists(ruta_json):
            return {"error": "No existe el archivo de estructura"}
            
        with open(ruta_json, 'r', encoding='utf-8') as f:
            estructura = json.load(f)
            
        # Obtener lista de todos los directorios con sus descripciones
        resultado = listar_directorios()
        if "error" in resultado:
            return resultado
            
        directorios = resultado["directorios"]
        if not directorios:
            return {"error": "No se encontraron directorios para analizar"}
            
        # Extraer la pregunta del prompt
        pregunta = prompt[9:].strip()  # Eliminar "Pregunta:" y espacios
        
        # Encontrar el directorio más relevante basado en la descripción
        mejor_match = None
        mejor_score = 0
        
        for dir_info in directorios:
            # Crear un texto combinado de ruta y descripción para comparar
            texto_dir = f"{dir_info['ruta']} {dir_info['descripcion']}"
            
            # Calcular cuántas palabras de la pregunta aparecen en el texto del directorio
            palabras_pregunta = set(pregunta.lower().split())
            palabras_dir = set(texto_dir.lower().split())
            
            coincidencias = len(palabras_pregunta.intersection(palabras_dir))
            
            if coincidencias > mejor_score:
                mejor_score = coincidencias
                mejor_match = dir_info
                
        if mejor_match is None:
            return {"error": "No se encontró un directorio relevante"}
            
        return {"ruta": mejor_match["ruta"]}
        
    except Exception as e:
        return {"error": f"Error al buscar directorio relevante: {str(e)}"}


if __name__ == "__main__":
    mcp.run()