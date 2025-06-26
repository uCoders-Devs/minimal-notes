#!/bin/bash

# Test script para Minimal Notes CLI
# Data entry testing para subir ejemplos limpios a GitHub

set -e

# Limpiar entorno
rm -rf data/db/ data/log/ data/prompts.json .test/
mkdir .test

echo "=== TESTING MINIMAL-NOTES CLI ==="

# Test 1: Crear notas básicas
echo "1. Creando notas de ejemplo..."
python cli/cli.py crear "Mi primera nota de ejemplo"
python cli/cli.py crear "Lista de tareas: comprar leche, estudiar Python, hacer ejercicio"
python cli/cli.py crear "Notas de reunión: discutir arquitectura del sistema, revisar PRs pendientes"
python cli/cli.py crear "Ideas para proyecto: implementar cache Redis, optimizar queries SQL"
python cli/cli.py crear "Recordatorio: backup de base de datos cada domingo a las 3 AM"

# Test 2: Listar todas las notas
echo "2. Listando todas las notas..."
python cli/cli.py listar

# Test 3: Leer notas específicas
echo "3. Leyendo notas por ID..."
python cli/cli.py leer 1
python cli/cli.py leer 3
python cli/cli.py leer 5

# Test 4: Buscar notas
echo "4. Buscando notas por contenido..."
python cli/cli.py buscar "Python"
python cli/cli.py buscar "proyecto"
python cli/cli.py buscar "base de datos"

# Test 5: Modificar notas
echo "5. Modificando contenido de notas..."
python cli/cli.py modificar 1 "Mi primera nota modificada con más contenido detallado"
python cli/cli.py modificar 2 "Lista actualizada: comprar leche, estudiar Python avanzado, hacer ejercicio, leer documentación"

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
python cli/cli.py importar .test/import_test.txt
python cli/cli.py importar .test/api_docs.txt

# Test 8: Exportar notas
echo "8. Exportando notas a archivos..."
python cli/cli.py exportar 1 --filename ".test/nota_exportada_1.txt"
python cli/cli.py exportar 6 --filename ".test/nota_api_docs.txt"

# Test 9: Funciones IA
echo "9. Probando funciones de IA..."
python cli/cli.py mejorar 1
python cli/cli.py resumir 7
python cli/cli.py preguntar 7 "¿Cuáles son los endpoints disponibles?"
python cli/cli.py traducir 1 "english"
python cli/cli.py traducir 1 "aleman"
python cli/cli.py traducir 1 "binario"

# Test 10: Crear más contenido variado
echo "10. Creando contenido adicional..."
python cli/cli.py crear "Bug report: Error 500 en endpoint /api/users cuando payload excede 1MB"
python cli/cli.py crear "Performance notes: Query optimizada reduce tiempo de 2.3s a 0.8s"
python cli/cli.py crear "Deploy checklist: tests passed, migrations run, rollback plan ready"
python cli/cli.py crear "Code review feedback: refactor auth middleware, add error handling"

# Test 11: Verificar eliminación
echo "11. Probando eliminación de notas..."
python cli/cli.py eliminar 2
python cli/cli.py listar

# Test 12: Crear estructura de ejemplo final
echo "12. Creando estructura final para GitHub..."
python cli/cli.py crear "Configuración de entorno: NODE_ENV=production, PORT=3000, DB_URL=postgresql://..."
python cli/cli.py crear "Arquitectura del sistema: Frontend React + Backend Node.js + PostgreSQL + Redis"
python cli/cli.py crear "Métricas: 95% uptime, 200ms response time, 10k DAU"

# Listado final
echo "=== ESTADO FINAL ==="
python cli/cli.py listar

echo "=== TESTING COMPLETADO ==="
echo "Archivos generados durante el testing.s"
ls -la .test/
tree data/
