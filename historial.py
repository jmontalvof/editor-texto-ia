import json
import os
from datetime import datetime
from uuid import uuid4

RUTA_HISTORIAL = "historial.json"

def guardar_version(texto_original, accion, resultado):
    entrada = {
        "id": str(uuid4()),
        "fecha": datetime.now().isoformat(),
        "accion": accion,
        "texto_original": texto_original,
        "resultado": resultado
    }

    if os.path.exists(RUTA_HISTORIAL):
        with open(RUTA_HISTORIAL, "r") as f:
            datos = json.load(f)
    else:
        datos = []

    datos.append(entrada)

    with open(RUTA_HISTORIAL, "w") as f:
        json.dump(datos, f, indent=2)

    return entrada["id"]

def obtener_historial():
    if os.path.exists(RUTA_HISTORIAL):
        with open(RUTA_HISTORIAL, "r") as f:
            return json.load(f)
    return []

def obtener_version_por_id(version_id):
    historial = obtener_historial()
    for entrada in historial:
        if entrada["id"] == version_id:
            return entrada
    return None

