from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
_api_key = os.getenv("GEMINI_API_KEY")
_client = genai.Client(api_key=_api_key)

def generate(
    prompt: str,
    sysprompt: str = "",
    max_tokens: int = 512,
    model: str = "gemini-2.0-flash"
) -> str:
    """Genera texto con Gemini.

    Args:
        prompt (str): texto de entrada
        sysprompt (str): system instruction
        max_tokens (int): máximo de tokens de salida
        model (str): modelo a utilizar

    Returns:
        str: texto generado
    """
    config = types.GenerateContentConfig(
        system_instruction=sysprompt,
        max_output_tokens=max_tokens,
    )
    response = _client.models.generate_content(
        model=model,
        config=config,
        contents=prompt
    )
    return response.text

