import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Tuple, Optional

from logger import Logger

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.gemini import generate

DEFAULT_PROMPTS = {
    "mejorar": {
        "system": "Eres un editor experto. Mejora el texto manteniendo el significado original. Sé conciso y claro.",
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
    },
    "corregir": {
        "system": "Eres un corrector ortográfico y gramatical experto. Corrige errores sin cambiar el estilo.",
        "template": "Corrige errores ortográficos y gramaticales:\n\n{content}",
        "max_tokens": 1024
    }
}


class PromptManager:
    """Gestor de prompts minimalista con logging disciplinado"""

    def __init__(self, prompts_file: str = "data/prompts.json", log_file: str = "data/logs/prompts.log", log_stream: bool = False):
        self.prompts_file = Path(prompts_file)
        self.logger = Logger("PromptManager", log_file=log_file, stream=log_stream).get()
        self.prompts, self.file_exists = self.load_prompts()
        
        self.logger.info(f"PromptManager inicializado: file={prompts_file}, exists={self.file_exists}")


    def load_prompts(self, prompts_filepath: Optional[str] = None) -> Tuple[Dict[str, Dict[str, Any]], bool]:
        """Carga prompts desde archivo o devuelve defaults"""
        path = Path(prompts_filepath) if prompts_filepath else self.prompts_file
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            self.logger.debug(f"Prompts cargados desde {path}: {len(prompts)} prompts")
            return (prompts, True)
        except FileNotFoundError:
            self.logger.warning(f"Archivo de prompts no encontrado: {path}, usando defaults")
            return (DEFAULT_PROMPTS, False)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON corrupto en {path}: {e}")
            raise ValueError(f"JSON corrupto en {path}")


    def save_prompts(self, prompts: Dict[str, Dict[str, Any]]) -> None:
        """Guarda prompts al archivo JSON con logging"""
        try:
            self.prompts_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.prompts_file, 'w', encoding='utf-8') as f:
                json.dump(prompts, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Prompts guardados: {len(prompts)} prompts -> {self.prompts_file}")
        except Exception as e:
            self.logger.error(f"Error guardando prompts en {self.prompts_file}: {e}")
            raise


    def list_prompts(self) -> list[str]:
        """Lista nombres de prompts disponibles"""
        prompts = list(self.prompts.keys())
        self.logger.debug(f"Listando {len(prompts)} prompts disponibles")
        return prompts


    def get_prompt(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtiene configuración de prompt por nombre"""
        prompt = self.prompts.get(name)
        if prompt:
            self.logger.debug(f"Prompt '{name}' encontrado")
        else:
            self.logger.warning(f"Prompt '{name}' no existe")
        return prompt


    def add_prompt(self, name: str, system: str, template: str, max_tokens: int = 512) -> bool:
        """Añade nuevo prompt con logging disciplinado"""
        if not name or not system or not template:
            self.logger.error("Parámetros inválidos para add_prompt")
            return False
            
        overwrite = name in self.prompts
        self.prompts[name] = {
            "system": system,
            "template": template,
            "max_tokens": max_tokens
        }
        
        try:
            self.save_prompts(self.prompts)
            action = "sobrescrito" if overwrite else "añadido"
            self.logger.info(f"Prompt '{name}' {action} exitosamente")
            return True
        except Exception as e:
            self.logger.error(f"Error añadiendo prompt '{name}': {e}")
            return False


    def delete_prompt(self, name: str) -> bool:
        """Elimina prompt por nombre con logging"""
        if name not in self.prompts:
            self.logger.warning(f"Intento de eliminar prompt inexistente: '{name}'")
            return False

        del self.prompts[name]
        
        try:
            self.save_prompts(self.prompts)
            self.logger.info(f"Prompt '{name}' eliminado exitosamente")
            return True
        except Exception as e:
            self.logger.error(f"Error eliminando prompt '{name}': {e}")
            return False


    def execute_prompt(self, name: str, **kwargs) -> Optional[str]:
        """
        Ejecuta prompt con parámetros y logging completo
        
        Args:
            name: Nombre del prompt
            **kwargs: Variables para el template
            
        Returns:
            Respuesta de Gemini o None si falla
        """
        self.logger.debug(f"Ejecutando prompt '{name}' con args: {list(kwargs.keys())}")
        
        prompt_config = self.get_prompt(name)
        if not prompt_config:
            self.logger.error(f"Prompt '{name}' no encontrado para ejecución")
            return None

        try:
            # Formatear template
            formatted_prompt = prompt_config["template"].format(**kwargs)
            content_preview = formatted_prompt[:100] + "..." if len(formatted_prompt) > 100 else formatted_prompt
            self.logger.debug(f"Prompt formateado: {content_preview}")

            # Llamar a Gemini
            self.logger.info(f"Llamando a Gemini para prompt '{name}' (max_tokens={prompt_config['max_tokens']})")
            result = generate(
                prompt=formatted_prompt,
                sysprompt=prompt_config["system"],
                max_tokens=prompt_config["max_tokens"]
            )
            
            if result:
                result_preview = result[:100] + "..." if len(result) > 100 else result
                self.logger.info(f"Prompt '{name}' ejecutado exitosamente: {len(result)} chars")
                self.logger.debug(f"Resultado: {result_preview}")
            else:
                self.logger.error(f"Gemini devolvió resultado vacío para prompt '{name}'")
                
            return result
            
        except KeyError as e:
            self.logger.error(f"Variable faltante en template '{name}': {e}")
            raise ValueError(f"Variable faltante en template: {e}")
        except Exception as e:
            self.logger.error(f"Error ejecutando prompt '{name}': {e}")
            return None


def test_prompts():
    """Test básico CRUD con logging"""
    print("[PROMPT MANAGER TEST]")

    pm = PromptManager(log_stream=True)
    print(f"✓ Prompts disponibles: {pm.list_prompts()}")

    # Test mejorar
    result = pm.execute_prompt("mejorar", content="esto esta mal escrito y tiene errores")
    print(f"✓ Mejorar: {result[:100]}{'...' if result and len(result)>100 else ''}" if result else "✗ Falló mejorar")

    # Test resumir
    long_text = "Este es un texto muy largo que necesita ser resumido. " * 10
    result = pm.execute_prompt("resumir", content=long_text)
    print(f"✓ Resumir: {result[:100]}{'...' if result and len(result)>100 else ''}" if result else "✗ Falló resumir")

    # Test prompt custom
    pm.add_prompt("custom", "Eres un experto matemático", "Responde: {query}", 256)
    result = pm.execute_prompt("custom", query="Cuánto es 2+2")
    print(f"✓ Custom: {result}" if result else "✗ Falló custom")


if __name__ == "__main__":
    test_prompts()