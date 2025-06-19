# minimal-notes

CLI minimalista para gestión de notas con SQLite y resumen mediante LLM (IA).

## Descripción

Proyecto dividido en módulos independientes:

-   **backend/**: lógica de persistencia SQLite y módulo de llamadas a APIs externas (POST con `requests`).
-   **cli/**: manejador de comandos que invoca al handler del backend.
-   **docs/**: documentación de uso interno y arquitectura.
-   **data/**: ejemplos de entrada y salida para pruebas y demostraciones.
-   **README.md**: descripción general y estructura.

## Estructura

```
minimal-notes/
├── docs/       # Documentación del backend y CLI
├── cli/        # Interface de línea de comandos (handler mínimo)
├── backend/    # Módulo SQLite y módulo API
├── data/       # Ejemplos de uso y datos de prueba
└── README.md   # Este archivo
```

## Ultimos Testings

Se le adjunto a modo de nota el ultimo log (`.test/testing_definitivo.log`) de testing completo (Usuario + Log Stream) y se le ordeno realizar una sintesis sobre si mismo.

```sh
$: mnctl preguntar 18 "Realiza una breve sintesis y promedio de todos los ultimos testeos realizados a este mismo programa."

Preguntando sobre nota 18: 'Realiza una breve sintesis y promedio de todos los ultimos testeos realizados a este mismo programa.'

[=== RESPUESTA ===]
El texto describe una prueba exhaustiva de la herramienta de línea de comandos `mnctl` (Minimal-Notes CLI). La prueba incluye la creación, listado, lectura, búsqueda, modificación, importación y exportación de notas. También se prueban funciones de inteligencia artificial como mejora de notas, resumen, preguntas sobre notas y traducción a varios idiomas (inglés, alemán y binario). Finalmente, se elimina una nota y se crean notas adicionales para simular una estructura final.

En resumen, la herramienta parece funcionar correctamente en todas las pruebas realizadas, incluyendo la manipulación básica de notas, la importación/exportación y las funcionalidades de IA.  La herramienta finaliza con 16 notas en la base de datos, después de la eliminación de una nota y la creación de otras nuevas durante el proceso de testeo.
```

## Flujo de trabajo colaborativo (Git)

### Ramas

-   `main`: rama protegida, solo recibe versiones estables (releases).
-   `testing`: rama protegida, integración de cambios. Se testean acá antes de subir a producción.
-   `backend-dev`: desarrollo de backend.
-   `cli-dev`: desarrollo de interfaz CLI.

### Flujo

```text
backend-dev ┐
cli-dev     ┴── PR → testing   # Se integran y testean los cambios
↓
PR → main      # Solo versiones estables se suben a main
```

### Reglas

-   Nadie pushea directo a `main` ni `testing`.
-   Todo cambio va vía Pull Request.
-   Los tests se ejecutan sobre `testing`.
-   Solo versiones validadas pasan a `main`.

## Colaboradores oficiales

-   [**Tomas-SC**](https://github.com/Tomas-SC)
-   [**Blu**](https://github.com/bluware-dev)
