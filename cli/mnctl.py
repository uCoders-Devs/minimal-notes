# Esta es la version para Windows del Wrapper.
from sys import argv, exit

def custom_help():
    from rich.table import Table
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import box

    console = Console()

    header = Panel.fit(
        "[cyan bold]    Bienvenido a Minimal Notes CLI![/cyan bold]    ",
        border_style="purple",
        box=box.ROUNDED,
    )
    console.print(header)

    # Tabla de comandos
    commands = Table(box=box.SIMPLE_HEAVY)
    commands.add_column("Comando   ", style="bold bright_blue", no_wrap=True)
    commands.add_column("")
    commands.add_column("Descripción", style="default")
    commands.add_row("crear",     "[red]->[default]",   "Crear nueva nota")
    commands.add_row("leer",      "[red]->[default]",   "Leer nota vía ID")
    commands.add_row("modificar", "[red]->[default]",   "Modificar nota vía ID")
    commands.add_row("eliminar",  "[red]->[default]",   "Eliminar nota vía ID ")
    commands.add_row("listar",    "[red]->[default]",   "Listar notas")
    commands.add_row("buscar",    "[red]->[default]",   "Buscar nota vía texto")
    commands.add_row("exportar",  "[red]->[default]",   "Exportar notas")
    commands.add_row("importar",  "[red]->[default]",   "Importar notas")
    
    ai_commands = Table(box=box.SIMPLE_HEAVY)
    ai_commands.add_column("[bright_magenta]+Extra IA ", style="bold green1")
    ai_commands.add_column("")
    ai_commands.add_column("Descripción")
    ai_commands.add_row("mejorar",   "[red]->[default]",   "Mejorar nota vía ID")
    ai_commands.add_row("resumir",   "[red]->[default]",   "Resumir nota vía ID")
    ai_commands.add_row("preguntar", "[red]->[default]",   "Preguntar sobre nota ")
    ai_commands.add_row("traducir",  "[red]->[default]",   "Traducir nota vía ID")

    console.print(commands, ai_commands)
    console.print("'[bold yellow]mnctl <[green]comando[/green]> --help[/bold yellow]' para mejor ayuda.\n")

# Intercepta el comando help para mostrar un comportamiento personalizado (Mejora de Rendimiento)
args = argv[1:]
if not args or args[0] in ["--help", "-h"]:
    custom_help()
    exit(0)

if __name__ == "__main__":
    from cli import app
    app()