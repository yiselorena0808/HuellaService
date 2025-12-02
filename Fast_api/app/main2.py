from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import requests
import base64
from datetime import datetime
import os

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Configuración
# -----------------------------
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "yiselorena0808/huellas.pat"
GITHUB_BRANCH = "main"

if not GITHUB_TOKEN:
    raise RuntimeError("No se encontró la variable de entorno GITHUB_TOKEN")

HEADERS_SUPABASE = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

HEADERS_GITHUB = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

class HuellaRequest(BaseModel):
    id_usuario: int

# -----------------------------
# Función de comparación placeholder
# -----------------------------
def comparar_huellas(template_guardado: bytes, template_nuevo: bytes) -> int:
    # Aquí va tu algoritmo real (UFMatcher o similar)
    return 88

# -----------------------------
# Guardar huella
# -----------------------------
@app.post("/huella/guardar")
def guardar_huella(data: HuellaRequest):
    try:
        # Captura huella
        proceso = subprocess.run(
            ["python", "captura_estable.py", str(data.id_usuario)],
            capture_output=True,
            text=True
        )
        resultado = json.loads(proceso.stdout)
        if "error" in resultado:
            raise HTTPException(status_code=500, detail=resultado["error"])

        plantilla_bytes = base64.b64decode(resultado["template"])
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo = f"huella_{data.id_usuario}_{timestamp}.dat"
        ruta_en_repo = f"huellas/{nombre_archivo}"

        # -----------------------------
        # Subir archivo a GitHub
        # -----------------------------
        github_payload = {
            "message": f"Agregar huella {nombre_archivo}",
            "content": base64.b64encode(plantilla_bytes).decode("utf-8"),
            "branch": GITHUB_BRANCH
        }

        r = requests.put(
            f"https://api.github.com/repos/{GITHUB_REPO}/contents/{ruta_en_repo}",
            headers=HEADERS_GITHUB,
            data=json.dumps(github_payload)
        )

        if r.status_code not in (200, 201):
            raise HTTPException(status_code=500, detail=f"Error subiendo archivo a GitHub: {r.text}")

        # URL raw de GitHub
        url_publica = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{ruta_en_repo}"

        # -----------------------------
        # Guardar URL en Supabase
        # -----------------------------
        payload = {
            "id_usuario": data.id_usuario,
            "huella_template": url_publica
        }

        r_db = requests.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            headers={**HEADERS_SUPABASE, "Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        if r_db.status_code not in (200, 201):
            raise HTTPException(status_code=500, detail=f"Error guardando en Supabase: {r_db.text}")

        return {
            "mensaje": "Huella guardada correctamente",
            "calidad": resultado.get("quality"),
            "url": url_publica
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Verificar huella
# -----------------------------
@app.post("/huella/verificar")
def verificar_huella(data: HuellaRequest):
    try:
        # Captura nueva huella
        proceso = subprocess.run(
            ["python", "captura_estable.py", str(data.id_usuario)],
            capture_output=True,
            text=True
        )
        cap = json.loads(proceso.stdout)
        if "error" in cap:
            raise HTTPException(status_code=500, detail=cap["error"])

        template_nueva = base64.b64decode(cap["template"])

        # Obtener URL guardada en Supabase
        r_db = requests.get(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id_usuario=eq.{data.id_usuario}",
            headers=HEADERS_SUPABASE
        )
        registro = r_db.json()
        if not registro:
            return {"resultado": "No existe registro de huella para este usuario", "score": None}

        url_archivo = registro[0]["huella_template"]

        # Descargar archivo desde GitHub (raw)
        r_file = requests.get(url_archivo)
        if r_file.status_code != 200:
            raise HTTPException(status_code=500, detail="No se pudo descargar el archivo desde GitHub")
        template_guardada = r_file.content

        # Comparación
        score = comparar_huellas(template_guardada, template_nueva)
        resultado = "Coincide" if score >= 80 else "NO coincide"

        return {
            "resultado": resultado,
            "score": score,
            "calidad": cap.get("quality"),
            "url_guardada": url_archivo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
