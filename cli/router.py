import os
import sys
import tomllib
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Tuple

from logger import Logger

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.handler import notes_handler

DEFAULT_PATHS = {
    "config": Path("data/config.toml"),
    "notes.db": Path("data/db/notes.db"),
    "prompts.json": Path("data/prompts.json"),
    "prompts.log": Path("data/log/prompts.log"),
    "router.log": Path("data/log/router.log"),
    "cli.log": Path("data/log/cli.log"),
}


class Router:
    """Router para gestión de notas con config TOML."""

    def __init__(self, config_path: Optional[Union[str, Path]] = None, 
                 config: Optional[Dict[str, Any]] = None, 
                 stream: Optional[bool] = None) -> None:
        """Inicializa Router con config flexible."""
        self.config_path = Path(config_path) if config_path else DEFAULT_PATHS["config"]

        self.config = self._load_config(config)
        self.database_file = self.config.get("database", {}).get("active", str(DEFAULT_PATHS["notes.db"]))
        self.prompts_file = self.config.get("database", {}).get("prompts", str(DEFAULT_PATHS["prompts.json"]))
        self.router_log = self.config.get("logger", {}).get("router", str(DEFAULT_PATHS["router.log"]))
        self.prompts_log = self.config.get("logger", {}).get("prompts", str(DEFAULT_PATHS["prompts.log"]))
        self.cli_log = self.config.get("logger", {}).get("cli", str(DEFAULT_PATHS["cli.log"]))
        self.stream = stream if stream is not None else self.config.get("logger", {}).get("stream", False)
        self._ensure_paths()

        self.logger = Logger("Router",log_file=self.router_log, stream=self.stream).get()
        self.logger.debug(f"Router init: {self.config}")


    def _ensure_paths(self) -> None:
        """Asegura que existan directorios padre."""
        Path(self.database_file).parent.mkdir(parents=True, exist_ok=True)
        Path(self.prompts_file).parent.mkdir(parents=True, exist_ok=True)
        Path(self.router_log).parent.mkdir(parents=True, exist_ok=True)


    def _load_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Carga config con prioridad: param > file > default."""
        if config:
            return config.copy()

        try:
            with open(self.config_path, 'rb') as f:
                return tomllib.load(f)
        except (FileNotFoundError, tomllib.TOMLDecodeError):
            return tomllib.loads(self._default_toml())


    def _default_toml(self) -> str:
        """Genera TOML default."""
        return f"""[database]
active = "{DEFAULT_PATHS['notes.db']}"
prompts = "{DEFAULT_PATHS['prompts.json']}"

[logger]
cli = "{DEFAULT_PATHS['cli.log']}"
router = "{DEFAULT_PATHS['router.log']}"
prompts = "{DEFAULT_PATHS['prompts.log']}"
stream = false"""

    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Valida estructura TOML."""
        required = {
            "database": ["active"],
            "logger": ["router", "stream"]
        }

        for section, keys in required.items():
            if section not in config or not isinstance(config[section], dict):
                return False
            if not all(key in config[section] for key in keys):
                return False
        return True


    def parse_config(self, file_path: Optional[Union[str, Path]] = None) -> bool:
        """Parsea y recarga config desde archivo."""
        path = Path(file_path) if file_path else self.config_path

        try:
            with open(path, 'rb') as f:
                new_config = tomllib.load(f)

            if not self._validate_config(new_config):
                self.logger.error(f"Config inválida: {path}")
                return False

            if new_config == self.config:
                self.logger.debug(f"Config '{path}': sin cambios")
                return True

            self.config = new_config
            self._reinit_components()
            self.logger.info(f"Config recargada: {path}")
            return True

        except FileNotFoundError:
            self.logger.warning(f"Config no encontrada: {path}")
            return False
        except tomllib.TOMLDecodeError as e:
            self.logger.error(f"TOML error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            return False


    def _reinit_components(self) -> None:
        """Reinicializa componentes tras cambio de config."""
        self.database_file = self.config["database"]["active"]
        self.prompts_file = self.config["database"]["prompts"]
        self.router_log = self.config["logger"]["router"]
        self.prompts_log = self.config["logger"]["prompts"]
        self.cli_log = self.config["logger"]["cli"]
        self.stream = self.config["logger"]["stream"]

        self._ensure_paths()
        self.logger = Logger("Router", log_file=self.router_log, stream=self.stream).get()
        self.logger.info("Componentes reinicializados")


    def create_config_file(self, file_path: Optional[Union[str, Path]] = None) -> bool:
        """Crea archivo config default."""
        path = Path(file_path) if file_path else DEFAULT_PATHS["config"]

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self._default_toml())
            self.logger.info(f"Config creada: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creando config: {e}")
            return False


    # CRUD Operations
    def new_note(self, content: str) -> Optional[int]:
        """Crea nota nueva."""
        content = content.strip()
        if not content:
            self.logger.error("Contenido vacío")
            return None

        try:
            note_id = notes_handler("create", self.database_file, content=content)
            self.logger.debug(f"Nota creada: id={note_id}")
            return note_id
        except Exception as e:
            self.logger.error(f"Error creando nota: {e}")
            return None


    def read_notes(self) -> Optional[List[Tuple]]:
        """Lee todas las notas."""
        try:
            notes = notes_handler("read", self.database_file)
            self.logger.debug(f"{len(notes)} notas leídas")
            return notes
        except Exception as e:
            self.logger.error(f"Error leyendo notas: {e}")
            return None


    def update_note(self, note_id: int, content: str) -> Optional[bool]:
        """Actualiza nota existente."""
        content = content.strip()
        if not content:
            self.logger.error("Contenido vacío")
            return False

        try:
            notes_handler("update", self.database_file, note_id=note_id, content=content)
            self.logger.debug(f"Nota id={note_id} actualizada")
            return True
        except Exception as e:
            self.logger.error(f"Error actualizando nota id={note_id}: {e}")
            return None


    def delete_note(self, note_id: int) -> Optional[bool]:
        """Elimina nota por ID."""
        try:
            notes_handler("delete", self.database_file, note_id=note_id)
            self.logger.debug(f"Nota id={note_id} eliminada")
            return True
        except Exception as e:
            self.logger.error(f"Error eliminando nota id={note_id}: {e}")
            return None


    def get_summary(self) -> Dict[str, Any]:
        """Resumen de config para debug."""
        return {
            "database_file": self.database_file,
            "logger_file": self.router_log,
            "stream_enabled": self.stream,
            "config_valid": self._validate_config(self.config)
        }


def main() -> None:
    """Test básico CRUD."""
    print("[ROUTER TEST]")
    
    router = Router()
    print(f"✓ Router init: DB={router.database_file}")
    
    # Asegurar config
    if not router.parse_config(file_path=router.config_path):
        router.logger.error("No se detecto una config o la actual esta corrupta")
        if input("¿Desea crear una nueva configuracion? [Y/n]: ") != "n":
            print("Creando config default...")
            router.create_config_file()
            router.parse_config(router.DEFAULTS["config"])
    
    # Test CRUD
    note_id = router.new_note("Test note")
    print(f"✓ Created: id={note_id}")
    
    notes = router.read_notes()
    print(f"✓ Read: {len(notes)} notes")
    
    if notes:
        first_id = notes[0][0]
        router.update_note(first_id, "Updated content")
        print(f"✓ Updated: id={first_id}")
        
        notes = router.read_notes()
        print(f"✓ Re-read: {len(notes)} notes")
        
        router.delete_note(notes[-1][0])
        print(f"✓ Deleted: id={notes[-1][0]}")
    
    summary = router.get_summary()
    print(f"✓ Summary: {summary}")


if __name__ == "__main__":
    main()