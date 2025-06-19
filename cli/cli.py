import sys
import typer
from typing import Optional

from dataclasses import dataclass

from prompts import PromptManager
from router import Router
from logger import Logger

app = typer.Typer()


@dataclass
class AppContext:
    router: Router
    logger: Logger
    pm: PromptManager


@app.callback()
def cli(ctx: typer.Context,
        config: Optional[str] = typer.Option(
            None,
            "--config", "-c",
            help="Ruta al archivo de configuración TOML"
        )
    ):
    """Inicializa la aplicación CLI de notas con configuración flexible."""
    router_instance = Router()
    config_path = config if config else router_instance.config_path

    if not router_instance.parse_config(config_path):
        typer.echo("No se otorgó o no existe una configuración válida.")
        if typer.confirm(f"¿Desea crear una en la ruta '{config_path}'?", default=True):
            router_instance.create_config_file(config_path)
            router_instance.parse_config(config_path)
        else:
            typer.echo("Usando configuración en memoria por defecto.")

    # A partir de este punto hay logs (Router pos config)
    logger_instance = Logger("Minimal-Notes", log_file=router_instance.cli_log, stream=router_instance.stream).get()

    try:
        pm_instance = PromptManager(
            prompts_file=router_instance.prompts_file, 
            log_file=router_instance.prompts_log
        )
    except ValueError as e:
        typer.echo(str(e))
        logger_instance.critical(f"El archivo {router_instance.prompts_file} está corrupto.")
        sys.exit(1)

    if not pm_instance.file_exists:
        typer.echo("No existe o no se detectó una configuración de prompts.")
        if typer.confirm(f"¿Desea crear una en la ruta '{router_instance.prompts_file}'?", default=True):
            pm_instance.save_prompts(prompts=pm_instance.prompts)
            logger_instance.debug(f"Se creó la configuración default de prompts en: {router_instance.prompts_file}")
        else:
            typer.echo("Usando configuración en memoria por defecto.")

    # Objeto de contexto flexible como AppContext
    ctx.obj = AppContext(
        router=router_instance,
        pm=pm_instance,
        logger=logger_instance
    )


# Comandos CRUD
@app.command("crear")
@app.command("mk")
def crear(ctx: typer.Context, content: str):
    """Crea una nueva nota con el contenido especificado."""
    router = ctx.obj.router
    logger = ctx.obj.logger

    note_id = router.new_note(content)
    if note_id:
        typer.echo(f"Se creó nota con ID {note_id}:")
        typer.echo(f"   >>> {content[:50]}{'...' if len(content) > 50 else ''}")
        logger.info(f"Nota creada: ID={note_id}")
    else:
        typer.echo("Error: No se pudo crear la nota.")
        logger.error("Falló la creación de nota")
        sys.exit(1)


@app.command("listar")
@app.command("ls")
def listar(ctx: typer.Context):
    """Lista todas las notas almacenadas."""
    router = ctx.obj.router
    notes = router.read_notes()

    if not notes:
        typer.echo(f"No hay notas almacenadas en: '{router.database_file}'")
        return

    for n in notes:
        typer.echo(f"ID: {n[0]} | FECHA: {n[2]}")
        typer.echo(f"   >>> {n[1][:50]}{'...' if len(n[1]) > 50 else ''}\n")


@app.command("leer")
@app.command("id")
def leer(ctx: typer.Context, note_id: int):
    """Lee una nota específica por su ID."""
    router = ctx.obj.router
    notes = router.read_notes()

    if not notes:
        typer.echo(f"No hay notas en: '{router.database_file}'")
        sys.exit(1)

    note = next((n for n in notes if n[0] == note_id), None)
    if not note:
        typer.echo(f"No se encontró la nota con el ID {note_id}")
        sys.exit(1)

    typer.echo(f"ID: {note[0]} | FECHA: {note[2]}")
    typer.echo(f"   >>> {note[1]}")


@app.command("modificar")
@app.command("mod")
def modificar(ctx: typer.Context, note_id: int, content: str):
    """Modifica el contenido de una nota existente."""
    router = ctx.obj.router
    logger = ctx.obj.logger

    if router.update_note(note_id, content):
        typer.echo(f"Nota {note_id} modificada exitosamente:")
        typer.echo(f"   >>> {content[:50]}{'...' if len(content) > 50 else ''}")
        logger.info(f"Nota modificada: ID={note_id}")
    else:
        typer.echo(f"Error: No se pudo modificar la nota {note_id}")
        logger.error(f"Falló modificación de nota ID={note_id}")
        sys.exit(1)


@app.command("eliminar")
@app.command("rm")
def eliminar(ctx: typer.Context, note_id: int):
    """Elimina una nota por su ID."""
    router = ctx.obj.router
    logger = ctx.obj.logger

    if router.delete_note(note_id):
        typer.echo(f"Nota {note_id} eliminada exitosamente.")
        logger.info(f"Nota eliminada: ID={note_id}")
    else:
        typer.echo(f"Error: No se pudo eliminar la nota {note_id}")
        logger.error(f"Falló eliminación de nota ID={note_id}")
        sys.exit(1)


# Comandos Adicionales
@app.command("buscar")
@app.command("grep")
def buscar(ctx: typer.Context, query: str):
    """Busca notas que contengan el texto especificado."""
    router = ctx.obj.router
    notes = router.read_notes()

    if not notes:
        typer.echo("No hay notas para buscar.")
        return

    matches = [n for n in notes if query.lower() in n[1].lower()]

    if not matches:
        typer.echo(f"No se encontraron notas que contengan: '{query}'")
        return

    typer.echo(f"Encontradas {len(matches)} nota(s) con '{query}':")
    for n in matches:
        typer.echo(f"ID: {n[0]} | FECHA: {n[2]}")
        typer.echo(f"   >>> {n[1][:50]}{'...' if len(n[1]) > 50 else ''}\n")


@app.command()
def exportar(ctx: typer.Context, note_id: int, filename: Optional[str] = None):
    """Exporta una nota a un archivo."""
    router = ctx.obj.router
    logger = ctx.obj.logger
    notes = router.read_notes()

    if not notes:
        typer.echo("No hay notas para exportar.")
        sys.exit(1)
    
    note = next((n for n in notes if n[0] == note_id), None)
    if not note:
        typer.echo(f"No se encontró la nota con ID {note_id}")
        sys.exit(1)

    # Generar nombre de archivo si no se proporciona
    if not filename:
        filename = f"nota_{note_id}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"ID: {note[0]}\n")
            f.write(f"Fecha: {note[2]}\n")
            f.write(f"Contenido:\n{note[1]}\n")

        typer.echo(f"Nota {note_id} exportada a: {filename}")
        logger.info(f"Nota exportada: ID={note_id} -> {filename}")
    except Exception as e:
        typer.echo(f"Error exportando nota: {e}")
        logger.error(f"Error exportando nota ID={note_id}: {e}")
        sys.exit(1)


@app.command()
def importar(ctx: typer.Context, file_path: str):
    """Importa contenido de un archivo como nueva nota."""
    router = ctx.obj.router
    logger = ctx.obj.logger

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            typer.echo("El archivo está vacío o no contiene texto válido.")
            sys.exit(1)

        note_id = router.new_note(content)
        if note_id:
            typer.echo(f"Archivo importado como nota ID {note_id}:")
            typer.echo(f"   >>> {content[:50]}{'...' if len(content) > 50 else ''}")
            logger.info(f"Archivo importado: {file_path} -> ID={note_id}")
        else:
            typer.echo("Error: No se pudo importar el archivo.")
            logger.error(f"Falló importación de: {file_path}")
            sys.exit(1)

    except FileNotFoundError:
        typer.echo(f"Error: No se encontró el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        typer.echo(f"Error leyendo archivo: {e}")
        logger.error(f"Error importando {file_path}: {e}")
        sys.exit(1)


# Comandos IA. TODO: Tratar de refactorizar y encapsular la logica (Simplificar código).
@app.command()
def mejorar(ctx: typer.Context, note_id: int):
    """Mejora el contenido de una nota usando IA."""
    router = ctx.obj.router
    pm = ctx.obj.pm
    logger = ctx.obj.logger

    notes = router.read_notes()
    if not notes:
        typer.echo("No hay notas disponibles.")
        sys.exit(1)

    note = next((n for n in notes if n[0] == note_id), None)
    if not note:
        typer.echo(f"No se encontró la nota con el ID {note_id}")
        sys.exit(1)

    content = note[1]
    typer.echo(f"Mejorando: {content[:50]}{'...' if len(content) > 50 else ''}")

    result = pm.execute_prompt("mejorar", content=content)
    if result:
        typer.echo("\n[=== CONTENIDO MEJORADO ===]")
        typer.echo(result)
        logger.info(f"Nota mejorada: ID={note_id}")

        if typer.confirm("¿Desea reemplazar la nota original con la versión mejorada?"):
            if router.update_note(note_id, result):
                typer.echo("Nota actualizada exitosamente.")
                logger.info(f"Nota reemplazada con versión mejorada: ID={note_id}")
    else:
        typer.echo("Error: No se pudo mejorar la nota.")
        logger.error(f"Falló mejora de nota ID={note_id}")


@app.command() 
def traducir(ctx: typer.Context, note_id: int, language: str):
    """Traduce una nota al idioma especificado."""
    router = ctx.obj.router
    pm = ctx.obj.pm
    logger = ctx.obj.logger

    notes = router.read_notes()
    if not notes:
        typer.echo("No hay notas disponibles.")
        sys.exit(1)

    note = next((n for n in notes if n[0] == note_id), None)
    if not note:
        typer.echo(f"No se encontró la nota con el ID {note_id}")
        logger.debug(f"No se encontró la nota con el ID {note_id}")
        sys.exit(1)

    content = note[1]
    typer.echo(f"Traduciendo a {language} la nota: {content[:50]}{'...' if len(content) > 50 else ''}")

    result = pm.execute_prompt("traducir", content=content, language=language)
    if result:
        typer.echo(f"\n[=== TRADUCCIÓN A {language.upper()} ===]")
        typer.echo(result)
        logger.info(f"Nota traducida: ID={note_id} -> {language}")
        
        if typer.confirm("¿Desea guardar la traducción como una nueva nota?"):
            new_id = router.new_note(f"[Traducción a {language}]\n{result}")
            if new_id:
                typer.echo(f"Traducción guardada como nota ID {new_id}")
                logger.info(f"Traducción guardada: ID={new_id}")
    else:
        typer.echo("Error: No se pudo traducir la nota.")
        logger.error(f"Falló traducción de nota ID={note_id}")


@app.command()
def resumir(ctx: typer.Context, note_id: int):
    """Resume una nota utilizando IA."""
    router = ctx.obj.router
    pm = ctx.obj.pm
    logger = ctx.obj.logger

    notes = router.read_notes()
    if not notes:
        typer.echo("No hay notas disponibles.")
        sys.exit(1)

    note = next((n for n in notes if n[0] == note_id), None)
    if not note:
        typer.echo(f"No se encontró la nota con el ID {note_id}")
        sys.exit(1)

    content = note[1]
    typer.echo(f"Resumiendo: {content[:50]}{'...' if len(content) > 50 else ''}")
    
    result = pm.execute_prompt("resumir", content=content)
    if result:
        typer.echo("\n[=== RESUMEN ===]")
        typer.echo(result)
        logger.info(f"Nota resumida: ID={note_id}")

        if typer.confirm("¿Desea guardar el resumen como una nueva nota?"):
            new_id = router.new_note(f"[Resumen de nota {note_id}]\n{result}")
            if new_id:
                typer.echo(f"Resumen guardado como nota ID {new_id}")
                logger.info(f"Resumen guardado: ID={new_id}")
    else:
        typer.echo("Error: No se pudo resumir la nota.")
        logger.error(f"Falló resumen de nota ID={note_id}")


@app.command()
def preguntar(ctx: typer.Context, note_id: int, question: str):
    """Hace una pregunta sobre el contenido de una nota específica."""
    router = ctx.obj.router
    pm = ctx.obj.pm
    logger = ctx.obj.logger

    notes = router.read_notes()
    if not notes:
        typer.echo("No hay notas disponibles.")
        sys.exit(1)

    note = next((n for n in notes if n[0] == note_id), None)
    if not note:
        typer.echo(f"No se encontró la nota con el ID {note_id}")
        sys.exit(1)

    content = note[1]
    typer.echo(f"Preguntando sobre nota {note_id}: '{question}'")

    result = pm.execute_prompt("preguntar", content=content, question=question)
    if result:
        typer.echo("\n[=== RESPUESTA ===]")
        typer.echo(result)
        logger.info(f"Pregunta procesada para nota ID={note_id}")
    else:
        typer.echo("Error: No se pudo procesar la pregunta.")
        logger.error(f"Falló pregunta para nota ID={note_id}")

# TODO: Feature -> Interfaz para que el usuario cree sus propios prompts para la IA.
# TODO: Feature -> Comando para cambiar la base de datos activa desde CLI.
# TODO: Agregar mas decoración al CLI: usando la libreria rich para generar contenido mas visual.
# TODO: Dar una ultima limpieza y refactorizacion a la estructura completa del CLI.
# TODO: Realizar busqueda profunda de bugs y fallas de optimización. 

if __name__ == "__main__":
    app()