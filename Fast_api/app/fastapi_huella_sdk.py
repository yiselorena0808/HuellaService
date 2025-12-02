from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode
from datetime import datetime
import json
import os

app = FastAPI()

DATA_FILE = "registro_huellas.json"

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiarlo por ["http://localhost:5173"] para mayor seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HuellaRegistro(BaseModel):
    nombre: str
    plantilla_base64: str

@app.get("/huella/capturar")
def capturar_huella():
    try:
        import subprocess
        import sys
        from pathlib import Path

        # Buscar primero un archivo ya generado por el Demo (huella_firma.dat)
        app_dir = Path(__file__).resolve().parent
        huella_file = app_dir / "huella_firma.dat"

        # Si el demo ya creó el archivo huella_firma.dat, devolverlo inmediatamente
        if huella_file.exists():
            with open(huella_file, "rb") as f:
                contenido = f.read()
            plantilla = b64encode(contenido).decode("utf-8")
            return {"plantilla_base64": plantilla, "source": "file"}

        # Si no existe, intentar ejecutar el wrapper para generar la plantilla
        wrapper_path = app_dir / "capturar_wrapper.py"
        if not wrapper_path.exists():
            raise HTTPException(status_code=404, detail=f"Wrapper no encontrado: {wrapper_path}")

        proc = subprocess.run(
            [sys.executable, str(wrapper_path)],
            cwd=str(app_dir),
            capture_output=True,
            text=True,
            timeout=60,
        )

        if proc.returncode != 0:
            detail = {
                "msg": "El capturador devolvió un error",
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "nota": "Ejecutado directamente con Python (sin exe)",
            }
            return JSONResponse(status_code=500, content=detail)

        # Comprobar que el archivo de huella fue creado por el wrapper
        if not huella_file.exists():
            return JSONResponse(status_code=404, content={"error": "Archivo de huella no encontrado después de ejecutar el capturador"})

        with open(huella_file, "rb") as f:
            contenido = f.read()

        plantilla = b64encode(contenido).decode("utf-8")
        return {"plantilla_base64": plantilla, "source": "wrapper"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/huella/guardar")
def guardar_huella(data: HuellaRegistro):
    entrada = {
        "nombre": data.nombre,
        "plantilla_base64": data.plantilla_base64,
        "fecha": datetime.now().isoformat()
    }

    registros = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            registros = json.load(f)

    registros.append(entrada)
    with open(DATA_FILE, "w") as f:
        json.dump(registros, f, indent=2)

    return {"mensaje": "Huella guardada correctamente ✅"}

@app.post("/huella/verificar")
def verificar_huella(data: HuellaRegistro):
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="No hay huellas registradas")

    with open(DATA_FILE, "r") as f:
        registros = json.load(f)

    registros_usuario = [r for r in registros if r["nombre"] == data.nombre]
    if not registros_usuario:
        return {"resultado": "Usuario no encontrado ❌"}

    ultima = registros_usuario[-1]
    coinciden = ultima["plantilla_base64"] == data.plantilla_base64
    return {"resultado": "Huella verificada ✅" if coinciden else "Huella no coincide ❌"}

@app.get("/usuarios")
def listar_usuarios():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        registros = json.load(f)

    return [
        {"nombre": r["nombre"], "fecha": r["fecha"]}
        for r in registros
    ]
