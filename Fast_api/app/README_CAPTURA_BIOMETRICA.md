# Captura de Huella Biométrica - Bio Mini Plus 2

## Archivos principales

- `capturar_wrapper.py` — Wrapper Python que captura huella y genera `huella_firma.dat`
- `compilar.bat` — Script batch para compilar `capturar_wrapper.py` a `capturar.exe` (x64)
- `fastapi_huella_sdk.py` — Servidor FastAPI que expone endpoints de captura/verificación

## Requisitos

1. **Drivers del dispositivo Bio Mini Plus 2** instalados en Windows (nivel sistema)
2. **DLLs del SDK** en esta carpeta (`UFScanner.dll`, `UFMatcher.dll`, etc.)
3. **Python 64-bit** (conda env `face_recognition_env`)
4. **PyInstaller** (se instala automáticamente al compilar)
5. **Visual C++ Redistributable x64** (descarga e instala si falta)

## Pasos de configuración

### 1. Copiar DLLs del SDK
```powershell
# Copia todas las DLLs del SDK a esta carpeta:
# D:\proyecto reconocimiento_facial\Fast_api\app\
# Por ejemplo:
#   - UFScanner.dll
#   - UFMatcher.dll
#   - Otras DLLs necesarias del SDK
```

### 2. Compilar `capturar_wrapper.py` a `capturar.exe`

**Opción A — Usar el script batch (recomendado, más fácil):**
```powershell
# Desde PowerShell (no necesita ser Admin, pero recomendado)
cd D:\proyecto reconocimiento_facial\Fast_api\app
.\compilar.bat
```

**Opción B — Usar PyInstaller directamente (manual):**
```powershell
# Instalar PyInstaller si no lo tienes
pip install pyinstaller

# Compilar a .exe
cd D:\proyecto reconocimiento_facial\Fast_api\app
pyinstaller --onefile --name capturar capturar_wrapper.py

# El .exe estará en dist\capturar.exe, cópialo a la carpeta actual
copy dist\capturar.exe capturar.exe
```

### 3. Probar el ejecutable manualmente

```powershell
# Abre PowerShell como Administrador
cd D:\proyecto reconocimiento_facial\Fast_api\app
.\capturar.exe
```

Si funciona, debería:
- Crear `huella_firma.dat` en la carpeta `app`
- Crear `capturar_wrapper.log` con los detalles de ejecución

### 4. Ejecutar FastAPI con uvicorn

```powershell
# Activar entorno
conda activate face_recognition_env

# Desde la carpeta Fast_api (NO desde app)
cd D:\proyecto reconocimiento_facial\Fast_api
uvicorn app.fastapi_huella_sdk:app --reload --port 5000
```

### 5. Probar endpoints desde el navegador o PowerShell

```powershell
# Capturar huella (llamará a capturar.exe)
Invoke-RestMethod http://127.0.0.1:5000/huella/capturar

# Guardar huella
$body = @{
    nombre = "Juan"
    plantilla_base64 = "BASE64_DATA_AQUI"
}
Invoke-RestMethod -Uri http://127.0.0.1:5000/huella/guardar `
    -Method POST `
    -Body ($body | ConvertTo-Json) `
    -ContentType "application/json"

# Listar usuarios
Invoke-RestMethod http://127.0.0.1:5000/usuarios
```

## Estructura del flujo

1. **Frontend (React)** → solicita capturar huella
2. **FastAPI** (/huella/capturar) → invoca `capturar.exe`
3. **capturar.exe** (Python empaquetado) → llama API del SDK
4. **SDK** → captura dispositivo Bio Mini Plus 2
5. **SDK** → genera plantilla
6. **capturar.exe** → guarda `huella_firma.dat`
7. **FastAPI** → lee archivo, codifica en base64, devuelve JSON
8. **Frontend** → recibe plantilla base64 y guarda

## Solución de problemas

### Error: `capturar.exe` no se ejecuta
- Verifica que las DLLs del SDK estén en la carpeta `app`
- Asegúrate de instalar Visual C++ Redistributable x64
- Ejecuta uvicorn como Administrador si el SDK lo requiere

### Error: DLL no encontrada
- Copia todas las DLLs del SDK a `D:\proyecto reconocimiento_facial\Fast_api\app\`
- Alternativamente, añade esa carpeta a PATH de Windows

### Error: Dispositivo no detectado
- Verifica que los drivers estén instalados en Windows
- Conecta el dispositivo USB
- Abre Administrador de dispositivos (`devmgmt.msc`) y busca el dispositivo

### Logs de depuración
- Lee `capturar_wrapper.log` para ver detalles de la ejecución
- Lee los logs de uvicorn en la terminal para mensajes de FastAPI

## Notas

- El archivo `capturar_wrapper.py` es un template. Reemplaza la sección "PLACEHOLDER" con las llamadas API reales del SDK una vez tengas documentación o ejemplos del fabricante.
- Para acceso a la API del SDK desde Python con `ctypes`, necesitas:
  - Las DLLs (`.dll`) o librerías compartidas
  - La documentación de funciones/firmas (para mapear con `ctypes`)
  - O usar una librería Python de terceros (si existe para tu SDK)

## Referencias

- Documentación del SDK: Proporcionada por el fabricante del Bio Mini Plus 2
- PyInstaller: https://pyinstaller.org/
- ctypes (FFI en Python): https://docs.python.org/3/library/ctypes.html
