@echo off
REM Script para compilar capturar_wrapper.py en capturar.exe (x64)
REM Ejecutar como Administrador (opcional pero recomendado)

echo.
echo === Compilando capturar_wrapper.py con PyInstaller ===
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "capturar_wrapper.py" (
    echo Error: capturar_wrapper.py no encontrado en la carpeta actual
    echo Asegúrate de estar en: D:\proyecto reconocimiento_facial\Fast_api\app
    pause
    exit /b 1
)

REM Verificar que PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
)

REM Compilar a .exe (onefile, modo consola)
echo Compilando...
pyinstaller --onefile ^
    --console ^
    --name capturar ^
    --distpath . ^
    --specpath . ^
    --buildpath . ^
    capturar_wrapper.py

REM Copiar el exe a la carpeta actual (por si distpath no funciona)
if exist "dist\capturar.exe" (
    copy "dist\capturar.exe" "capturar.exe"
    echo.
    echo Compilación exitosa: capturar.exe generado
)

if exist "capturar.exe" (
    echo.
    echo === Archivo generado: capturar.exe ===
    echo Puedes probarlo manualmente:
    echo   .\capturar.exe
    echo.
) else (
    echo Error: capturar.exe no se generó correctamente
    pause
    exit /b 1
)

REM Limpiar archivos temporales (opcional)
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del capturar.spec 2>nul

echo Listo. Cierra esta ventana para continuar.
pause
