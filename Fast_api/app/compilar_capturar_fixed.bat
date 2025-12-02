@echo off
REM compilar_capturar_fixed.bat
REM Versión limpia del script para compilar capturar.cpp con MSVC o MinGW.

REM USO:
REM   1) Abrir "x64 Native Tools Command Prompt for VS" para MSVC, o PowerShell/CMD con MinGW en PATH.
REM   2) (Opcional) Establecer variables de entorno si tu SDK está en rutas personalizadas:
REM        set SDK_INC=C:\Path\To\SDK\include
REM        set SDK_LIB=C:\Path\To\SDK\lib\x64
REM   3) Ejecutar: .\compilar_capturar_fixed.bat

setlocal enabledelayedexpansion

set "SRC=capturar.cpp"
set "OUT=capturar.exe"

if "%SDK_INC%"=="" (
  echo WARNING: SDK_INC no está establecido. Ajusta SDK include si es necesario.
)
if "%SDK_LIB%"=="" (
  echo WARNING: SDK_LIB no está establecido. Ajusta SDK lib path si es necesario.
)

echo Buscando compiladores (MSVC cl o MinGW g++)...
where cl >nul 2>&1
if %ERRORLEVEL%==0 goto do_msvc

where g++ >nul 2>&1
if %ERRORLEVEL%==0 goto do_gcc

echo ERROR: No se encontró compilador 'cl' ni 'g++' en PATH. Instala Visual Studio (Build Tools) o MinGW y vuelve a intentarlo.
exit /b 2

:do_msvc
echo === Compilando con MSVC (cl) ===
set "SDK_LIBS=UFScanner.lib UFMatcher.lib"
cl /EHsc /MD /I "%SDK_INC%" "%SRC%" /link /LIBPATH:"%SDK_LIB%" %SDK_LIBS% /OUT:%OUT%
if %ERRORLEVEL%==0 (
  echo === compilacion MSVC exitosa: %OUT% ===
  goto :EOF
) else (
  echo MSVC cl devolvió error. Intentando MinGW g++...
)

:do_gcc
echo === Compilando con MinGW (g++) ===
g++ -std=c++17 -O2 -I"%SDK_INC%" "%SRC%" -L"%SDK_LIB%" -lUFScanner -lUFMatcher -o "%OUT%"
if %ERRORLEVEL%==0 (
  echo === compilacion MinGW exitosa: %OUT% ===
  goto :EOF
) else (
  echo ERROR: La compilacion con g++ falló. Revisa rutas y nombres de librerías.
  exit /b 3
)

:EOF
endlocal
echo === Fin del script ===
