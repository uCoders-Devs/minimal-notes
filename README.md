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
