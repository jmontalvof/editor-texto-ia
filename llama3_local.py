import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")

def mejorar_texto_llama3(texto: str, accion: str) -> str:
    prompts = {
        "resumir": f"Resume este texto en español de forma clara y concisa:\n\n{texto}",
        "corregir": f"Corrige errores ortográficos y de estilo en este texto en español:\n\n{texto}",
        "expandir": f"Expande este texto en español, agregando más detalles y profundidad:\n\n{texto}",
        "variar": f"Reescribe este texto en español en un estilo diferente (más creativo o informal):\n\n{texto}"
    }
    prompt = prompts.get(accion.lower(), texto)

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )

    return response.json()["response"] if response.ok else "❌ Error al generar respuesta"

