# Documentación mnctl

## Comandos CRUD

### crear | create | mk

Crea una nueva nota con el contenido especificado.

```bash
mnctl crear "Contenido de la nota"
mnctl create "Bug fix: authentication middleware"
mnctl mk "TODO: refactor user service"
```

**Salida:**

```
Se creó nota con ID 1:
   >>> Contenido de la nota
```

### leer | read | id

Lee una nota específica por su ID.

```bash
mnctl leer 1
mnctl read 1
mnctl id 1
```

**Salida:**

```
ID: 1 | FECHA: 2025-01-15 14:30:22
   >>> Contenido de la nota
```

### listar | list | ls

Lista todas las notas almacenadas.

```bash
mnctl listar
mnctl list
mnctl ls
```

**Salida:**

```
ID: 1 | FECHA: 2025-01-15 14:30:22
   >>> Contenido de la nota

ID: 2 | FECHA: 2025-01-15 15:45:10
   >>> Otra nota...
```

### modificar | modify | update | mod

Modifica el contenido de una nota existente.

```bash
mnctl modificar 1 "Nuevo contenido"
mnctl modify 1 "Updated content"
mnctl update 1 "Fixed content"
mnctl mod 1 "Final version"
```

**Salida:**

```
Nota 1 modificada exitosamente:
   >>> Nuevo contenido
```

### eliminar | remove | delete | rm

Elimina una nota por su ID.

```bash
mnctl eliminar 1
mnctl remove 1
mnctl delete 1
mnctl rm 1
```

**Salida:**

```
Nota 1 eliminada exitosamente.
```

## Comandos de Búsqueda

### buscar | search | find | grep

Busca notas que contengan el texto especificado.

```bash
mnctl buscar "authentication"
mnctl search "TODO"
mnctl find "bug"
mnctl grep "refactor"
```

**Salida:**

```
Encontradas 2 nota(s) con 'authentication':
ID: 1 | FECHA: 2025-01-15 14:30:22
   >>> Bug fix: authentication middleware...
```

## Comandos de Import/Export

### exportar | export | out

Exporta una nota a un archivo.

```bash
mnctl exportar 1                    # Genera nota_1.txt
mnctl export 1 --filename "bug.txt"
mnctl out 1 "report.md"
```

**Estructura del archivo:**

```
ID: 1
Fecha: 2025-01-15 14:30:22
Contenido:
Bug fix: authentication middleware
```

### importar | import | in

Importa contenido de un archivo como nueva nota.

```bash
mnctl importar "changelog.txt"
mnctl import "requirements.txt"
mnctl in "notes.md"
```

**Salida:**

```
Archivo importado como nota ID 3:
   >>> # Changelog...
```

## Comandos de IA

### mejorar | enhance

Mejora el contenido de una nota usando IA.

```bash
mnctl mejorar 1
mnctl enhance 1
```

**Flujo:**

```
Mejorando: Bug fix: authentication middleware...

[=== CONTENIDO MEJORADO ===]
# Authentication Middleware Bug Fix

## Issue Description
Fixed critical bug in authentication middleware...

¿Desea reemplazar la nota original con la versión mejorada? [y/N]:
```

### resumir | summarize | sum

Resume una nota utilizando IA.

```bash
mnctl resumir 1
mnctl summarize 1
mnctl sum 1
```

**Flujo:**

```
Resumiendo: Documentación completa del API...

[=== RESUMEN ===]
El API incluye endpoints REST para autenticación, 
gestión de usuarios y procesamiento de datos...

¿Desea guardar el resumen como una nueva nota? [y/N]:
```

### traducir | translate | trans

Traduce una nota al idioma especificado.

```bash
mnctl traducir 1 "english"
mnctl translate 1 "français"
mnctl trans 1 "português"
```

**Flujo:**

```
Traduciendo a english la nota: Documentation...

[=== TRADUCCIÓN A ENGLISH ===]
# Complete API Documentation

Authentication endpoints and user management...

¿Desea guardar la traducción como una nueva nota? [y/N]:
```

### preguntar | ask

Hace una pregunta sobre el contenido de una nota específica.

```bash
mnctl preguntar 1 "¿Cuáles son los endpoints principales?"
mnctl ask 1 "What are the security requirements?"
```

**Flujo:**

```
Preguntando sobre nota 1: '¿Cuáles son los endpoints principales?'

[=== RESPUESTA ===]
Basándome en el contenido, los endpoints principales son:
1. /auth/login - Autenticación de usuarios
2. /users/* - Gestión de usuarios
3. /data/* - Procesamiento de datos
```

## Configuración

### Uso de config personalizado

```bash
mnctl --config "custom.toml" listar
mnctl -c "production.toml" crear "Production note"
```

### Estructura config.toml

```toml
[database]
active = "data/db/notes.db"
prompts = "data/prompts.json"

[logger]
cli = "data/log/cli.log"
router = "data/log/router.log"
prompts = "data/log/prompts.log"
stream = false
```

**Parámetros:**

- `database.active`: Ruta a la base de datos SQLite
- `database.prompts`: Archivo de configuración de prompts IA
- `logger.cli`: Log de operaciones CLI
- `logger.router`: Log del router interno
- `logger.prompts`: Log de operaciones IA
- `logger.stream`: Habilita logging en tiempo real

## Inicialización Automática

Al ejecutar cualquier comando por primera vez:

1. **config.toml**: Se crea configuración por defecto
2. **prompts.json**: Se generan templates IA básicos
3. **notes.db**: Se inicializa base de datos SQLite
4. **log/**: Se crean directorios de logging

### Confirmaciones interactivas

```
No se otorgó o no existe una configuración válida.
¿Desea crear una en la ruta 'data/config.toml'? [Y/n]:

No existe o no se detectó una configuración de prompts.
¿Desea crear una en la ruta 'data/prompts.json'? [Y/n]:
```

## Casos de Uso

### Flujo básico

```bash
# 1. Crear nota
mnctl crear "Implementar cache Redis"

# 2. Mejorar estructura
mnctl mejorar 1

# 3. Generar resumen
mnctl resumir 1

# 4. Exportar resultado
mnctl exportar 1 "task-summary.md"
```

### Procesamiento de documentos

```bash
# 1. Importar archivo
mnctl importar "specs.md"

# 2. Analizar contenido
mnctl preguntar 2 "¿Cuáles son los requisitos técnicos?"

# 3. Traducir para equipo internacional
mnctl traducir 2 "english"

# 4. Buscar información específica
mnctl buscar "authentication"
```

### Gestión multi-idioma

```bash
# Documento base en español
mnctl crear "Documentación técnica del sistema"

# Versiones en otros idiomas
mnctl traducir 1 "english"
mnctl traducir 1 "português"
mnctl traducir 1 "français"

# Búsqueda cross-idioma
mnctl buscar "technical"
mnctl buscar "técnica"
```


## Sistema de Prompts (Detalles técnicos)

### Estructura prompts.json

```json
{
  "mejorar": {
    "system": "Eres un editor experto. Mejora el texto manteniendo el significado original.",
    "template": "Mejora este texto:\n\n{content}",
    "max_tokens": 1024
  },
  "resumir": {
    "system": "Eres un experto en síntesis. Crea resúmenes concisos y precisos.",
    "template": "Resume este texto en máximo 3 párrafos:\n\n{content}",
    "max_tokens": 512
  },
  "traducir": {
    "system": "Eres un traductor profesional. Traduce con precisión manteniendo el contexto.",
    "template": "Traduce este texto a {language}:\n\n{content}",
    "max_tokens": 1024
  },
  "preguntar": {
    "system": "Eres un asistente analítico. Responde basándote únicamente en el contenido proporcionado.",
    "template": "Basándote en este texto:\n\n{content}\n\nResponde: {question}",
    "max_tokens": 512
  }
}
```

### Variables de Template

- `{content}`: Contenido de la nota
- `{language}`: Idioma de destino (solo traducir)
- `{question}`: Pregunta del usuario (solo preguntar)

> <small>**Nota**: modificar placeholders puede generar errores si no se manejan bien dentro de su modulo correspondiente</small>

### Estructura de Prompt

- `system`: Contexto y rol del asistente IA
- `template`: Plantilla del prompt con variables
- `max_tokens`: Límite de tokens para la respuesta <small>(Equivalente a la maxima longitud de respuesta)</small>

> **Nota:** podes cambiar estas configuraciones para adaptar la IA a tus necesidades

## Gestión de Errores

### Errores comunes

- **Nota no encontrada**: ID inexistente
	- <small>Nota: chequea con `mnctl listar`</small>
- **Archivo corrupto**: JSON inválido en prompts.json
	- <small>Fix: corregir estructura o eliminar para reinicializar template</small>
- **Base de datos inaccesible**: Permisos o ruta incorrecta
	- <small>Nota: evita usar rutas que requieran privilegios de sudo/admin</small>
- **API IA no disponible**: Falta `GEMINI_API_KEY` en `.env`
	- <small>Nota: ver `.env.example`</small>

### Logs de debug

```bash
# Ver logs en tiempo real (requiere stream = true)
tail -f data/log/cli.log
tail -f data/log/router.log
tail -f data/log/prompts.log
```

