#!/bin/bash

# Test script para mnctl - Minimal Notes CLI
# Data entry testing para subir ejemplos limpios a GitHub

set -e

# Limpiar entorno
rm -rf data/db/ data/log/ data/prompts.json .test/
mkdir .test

echo "=== TESTING MINIMAL-NOTES CLI ==="

# Test 1: Crear notas básicas
echo "1. Creando notas de ejemplo..."
mnctl crear "Mi primera nota de ejemplo"
mnctl crear "Lista de tareas: comprar leche, estudiar Python, hacer ejercicio"
mnctl crear "Notas de reunión: discutir arquitectura del sistema, revisar PRs pendientes"
mnctl crear "Ideas para proyecto: implementar cache Redis, optimizar queries SQL"
mnctl crear "Recordatorio: backup de base de datos cada domingo a las 3 AM"

# Test 2: Listar todas las notas
echo "2. Listando todas las notas..."
mnctl listar

# Test 3: Leer notas específicas
echo "3. Leyendo notas por ID..."
mnctl leer 1
mnctl leer 3
mnctl leer 5

# Test 4: Buscar notas
echo "4. Buscando notas por contenido..."
mnctl buscar "Python"
mnctl buscar "proyecto"
mnctl buscar "base de datos"

# Test 5: Modificar notas
echo "5. Modificando contenido de notas..."
mnctl modificar 1 "Mi primera nota modificada con más contenido detallado"
mnctl modificar 2 "Lista actualizada: comprar leche, estudiar Python avanzado, hacer ejercicio, leer documentación"

# Test 6: Crear contenido para importar
echo "6. Creando archivos para importar..."
echo "Contenido importado desde archivo de texto plano" > .test/import_test.txt
echo "Documentación del API REST:
- GET /api/notes - Lista todas las notas
- POST /api/notes - Crea nueva nota
- PUT /api/notes/{id} - Actualiza nota
- DELETE /api/notes/{id} - Elimina nota" > .test/api_docs.txt

# Test 7: Importar archivos
echo "7. Importando archivos como notas..."
mnctl importar .test/import_test.txt
mnctl importar .test/api_docs.txt

# Test 8: Exportar notas
echo "8. Exportando notas a archivos..."
mnctl exportar 1 --filename ".test/nota_exportada_1.txt"
mnctl exportar 6 --filename ".test/nota_api_docs.txt"

# Test 9: Funciones IA
echo "9. Probando funciones de IA..."
mnctl mejorar 1
mnctl resumir 7
mnctl preguntar 7 "¿Cuáles son los endpoints disponibles?"
mnctl traducir 1 "english"
mnctl traducir 1 "aleman"
mnctl traducir 1 "binario"

# Test 10: Crear más contenido variado
echo "10. Creando contenido adicional..."
mnctl crear "Bug report: Error 500 en endpoint /api/users cuando payload excede 1MB"
mnctl crear "Performance notes: Query optimizada reduce tiempo de 2.3s a 0.8s"
mnctl crear "Deploy checklist: tests passed, migrations run, rollback plan ready"
mnctl crear "Code review feedback: refactor auth middleware, add error handling"

# Test 11: Verificar eliminación
echo "11. Probando eliminación de notas..."
mnctl eliminar 2
mnctl listar

# Test 12: Crear estructura de ejemplo final
echo "12. Creando estructura final para GitHub..."
mnctl crear "Configuración de entorno: NODE_ENV=production, PORT=3000, DB_URL=postgresql://..."
mnctl crear "Arquitectura del sistema: Frontend React + Backend Node.js + PostgreSQL + Redis"
mnctl crear "Métricas: 95% uptime, 200ms response time, 10k DAU"

# Listado final
echo "=== ESTADO FINAL ==="
mnctl listar

echo "=== TESTING COMPLETADO ==="
echo "Archivos generados durante el testing.s"
ls -la .test/
tree data/
