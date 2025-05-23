# Documentación de scripts MCP

Este repositorio contiene dos scripts principales que forman parte de un sistema para analizar, describir y consultar la estructura de directorios y archivos de un proyecto. Ambos scripts están diseñados para ser utilizados como herramientas dentro de un entorno MCP (Multi-Component Platform).

## 1. `server.py`

### ¿Para qué sirve?

Este script permite analizar la estructura de un directorio, guardar esa estructura en un archivo JSON, añadir descripciones a los directorios (por ejemplo, para documentar repositorios o carpetas importantes) y obtener un resumen de las descripciones y rutas de todos los directorios.

### Funcionalidades principales

- **guardar_memoria**: Guarda un diccionario JSON en la ruta especificada.
- **leer_estructura_directorios**: Analiza recursivamente la estructura de un directorio y la guarda en un archivo JSON (`estructura.json`). Incluye información sobre subdirectorios y archivos.
- **agregar_descripcion_repo**: Permite añadir o modificar la descripción de un directorio concreto dentro del archivo de estructura.
- **obtener_descripciones_directorios**: Devuelve un diccionario con el nombre, descripción y ruta completa de cada directorio encontrado en la estructura.

Este script es útil para documentar y explorar grandes bases de código o proyectos con múltiples carpetas, facilitando la navegación y el entendimiento de la estructura.

---

## 2. `app.py`

### ¿Para qué sirve?

Este script está orientado a la consulta y validación de la estructura de directorios previamente guardada en el archivo JSON (`estructura.json`). Permite verificar la validez del archivo, extraer descripciones y rutas, y leer archivos o múltiples archivos de forma sencilla.

### Funcionalidades principales

- **verificar_memoria**: Comprueba que el archivo de estructura (`estructura.json`) existe y tiene un formato válido.
- **obtener_descripciones_y_paths**: Extrae una lista de descripciones y rutas completas de todos los directorios del archivo de estructura.
- **combinar_descripciones_y_prompt**: Prepara la información para búsquedas basadas en prompts, facilitando la integración con sistemas de consulta automática.
- **leer_archivo**: Lee el contenido completo de un archivo dado su path.
- **leer_multiples_archivos**: Lee el contenido de varios archivos a la vez, devolviendo los resultados en una lista.

Este script es ideal para construir herramientas de búsqueda, validación y consulta sobre la estructura de un proyecto previamente analizado.

---

## Requisitos

- Python 3.x
- Las rutas y nombres de archivo están configurados para un entorno específico. Es posible que debas adaptarlos a tu sistema.

## Uso

Ambos scripts están diseñados para ser ejecutados como módulos MCP y exponen sus funciones como herramientas (`@mcp.tool()`). Puedes integrarlos en flujos de trabajo automatizados o usarlos como backend para asistentes inteligentes que necesiten explorar y documentar proyectos de código.

---

## Sistema de Gestión y Búsqueda de Directorios

Este sistema proporciona una solución completa para gestionar, analizar y buscar en estructuras de directorios, con capacidades de búsqueda semántica y análisis de metadatos.

## Características Principales

### 1. Sistema Base (`server.py`)
- Lectura y análisis de estructura de directorios
- Sistema de respaldo automático de datos
- Gestión de descripciones y metadatos
- Filtrado de directorios ocultos
- Preservación de metadatos en actualizaciones

### 2. Sistema de Búsqueda (`search.py`)
- Búsqueda por nombre con expresiones regulares
- Filtrado por metadatos (fechas, tamaños, etc.)
- Búsqueda en contenido de archivos
- Generación de estadísticas de búsqueda

### 3. Búsqueda Semántica (`semantic_search.py`)
- Sugerencias basadas en preguntas en lenguaje natural
- Análisis de similitud de texto
- Extracción de palabras clave
- Recomendaciones contextuales

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Sistema Base
```python
from server import leer_estructura_directorios, actualizar_descripcion_directorio

# Leer estructura
estructura = leer_estructura_directorios("./mi_directorio")

# Actualizar descripción
actualizar_descripcion_directorio("Ventas", "Documentos del departamento de ventas")
```

### Búsqueda
```python
from search import buscar_por_nombre, filtrar_por_metadata

# Buscar por nombre
resultados = buscar_por_nombre("ventas.*2023")

# Filtrar por metadata
criterios = {
    'fecha_creacion': {
        'desde': '2023-01-01',
        'hasta': '2023-12-31'
    },
    'archivos': {
        'min': 5,
        'max': 100
    }
}
resultados = filtrar_por_metadata(criterios)
```

### Búsqueda Semántica
```python
from semantic_search import sugerir_directorios, procesar_pregunta

# Sugerir directorios
sugerencias = sugerir_directorios("¿Dónde están los informes de ventas?")

# Procesar pregunta
analisis = procesar_pregunta("¿Cuándo se crearon los últimos informes financieros?")
```

## Estructura de Datos

### Formato JSON
```json
{
    "directorio/ejemplo": {
        "descripcion": "Descripción del directorio",
        "metadata": {
            "fecha_creacion": "2023-01-01T00:00:00",
            "fecha_modificacion": "2023-12-31T23:59:59",
            "archivos": 10,
            "subdirectorios": 5
        }
    }
}
```

## Contribución

1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información. 