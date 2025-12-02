import json
import sys
import requests
import subprocess
import base64
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE
import os

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def comparar_huellas(template_guardado: bytes, template_nuevo: bytes) -> int:
    # Placeholder real: aquí va tu algoritmo de comparación
    return 88

if len(sys.argv) < 2:
    print(json.dumps({"error": "Se debe enviar ID del usuario"}))
    sys.exit(0)

id_usuario = sys.argv[1]

# 1️⃣ Obtener huella guardada desde Supabase
r = requests.get(
    f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id_usuario=eq.{id_usuario}",
    headers=headers
)

try:
    data = r.json()
except:
    print(json.dumps({"error": "Supabase no devolvió JSON"}))
    sys.exit(0)

if not data:
    print(json.dumps({
        "resultado": "NO existe registro de huella para este usuario",
        "score": None
    }))
    sys.exit(0)

try:
    # Descarga el archivo .dat desde GitHub
    url_archivo = data[0]["huella_template"]
    r_file = requests.get(url_archivo)
    if r_file.status_code != 200:
        raise Exception("No se pudo descargar el archivo desde GitHub")
    template_guardado = r_file.content
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(0)

# 2️⃣ Capturar nueva huella
proceso = subprocess.run(
    ["python", "captura_estable.py", id_usuario],
    capture_output=True, text=True
)

if proceso.returncode != 0 or not proceso.stdout:
    print(json.dumps({"error": "captura_estable.py no produjo salida"}))
    sys.exit(0)

try:
    cap = json.loads(proceso.stdout)
except Exception:
    print(json.dumps({"error": "Salida inválida de captura_estable.py"}))
    sys.exit(0)

if "template" not in cap:
    print(json.dumps({"error": "Captura sin template"}))
    sys.exit(0)

template_nuevo = base64.b64decode(cap["template"])

# 3️⃣ Comparar
score = comparar_huellas(template_guardado, template_nuevo)
resultado = "Coincide" if score >= 80 else "NO coincide"

print(json.dumps({
    "resultado": resultado,
    "score": score,
    "calidad": cap.get("quality")
}))
