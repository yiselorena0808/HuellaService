@echo off
REM compilar_capturar.bat
REM Script para compilar capturar.cpp usando MSVC (cl) o MinGW (g++) en Windows.
REM USO:
REM   1) Abrir "x64 Native Tools Command Prompt for VS" para MSVC, o PowerShell/CMD con MinGW en PATH.
REM   2) (Opcional) Establecer variables de entorno:
REM        set SDK_INC=C:\Path\To\SDK\include
REM        set SDK_LIB=C:\Path\To\SDK\lib\x64
REM   3) Ejecutar este script desde el directorio que contiene `capturar.cpp`.

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
@echo off
REM compilar_capturar.bat
REM Script para compilar capturar.cpp usando MSVC (cl) o MinGW (g++) en Windows.
REM USO:
REM   1) Abrir "x64 Native Tools Command Prompt for VS" para MSVC, o PowerShell/CMD con MinGW en PATH.
REM   2) (Opcional) Establecer variables de entorno:
REM        set SDK_INC=C:\Path\To\SDK\include
REM        set SDK_LIB=C:\Path\To\SDK\lib\x64
REM   3) Ejecutar este script desde el directorio que contiene `capturar.cpp`.

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
@echo off
REM compilar_capturar.bat
REM Script para compilar capturar.cpp usando MSVC (cl) o MinGW (g++) en Windows.
REM USO:
REM   1) Abrir "x64 Native Tools Command Prompt for VS" para MSVC, o PowerShell/CMD con MinGW en PATH.
REM   2) Establecer variables de entorno (opcional):
REM        set SDK_INC=C:\Ruta\SDK\include
REM        set SDK_LIB=C:\Ruta\SDK\lib\x64
REM      Si no, edita el script para poner las rutas.
REM   3) Ejecutar: compilar_capturar.bat

setlocal

























































pauseendlocalecho === Fin script. Si la compilacion falló, revisa las rutas SDK_INC y SDK_LIB y que tengas las librerias (.lib/.a) adecuadas. ===)    echo g++ not found. No compiler available (cl or g++ not found).) else (    )        echo MinGW compilation failed.    ) else (        goto :EOF        echo === compilacion MinGW exitosa: %OUT% ===    if %ERRORLEVEL%==0 (    g++ -std=c++17 -O2 -I"%SDK_INC%" %SRC% -L"%SDK_LIB%" -lUFScanner -lUFMatcher -o %OUT%    echo Compiling (g++)...    REM Ej: UFScanner.lib (import lib) puede ser enlazado directamente si supportado. Ajusta según tu SDK.    REM Ajustar nombres de librerias (pueden ser .a o .lib import libs). Usa -L para lib path y -l nombres sin prefijos/lib ext.        )        echo WARNING: SDK_LIB not set. If linking fails, set SDK_LIB to your SDK lib x64 path.    if "%SDK_LIB%"=="" (    )        echo WARNING: SDK_INC not set. If compilation fails, set SDK_INC to your SDK include path.    if "%SDK_INC%"=="" (    echo Found g++, compiling with MinGW...if %ERRORLEVEL%==0 (where g++ >nul 2>&1
nrem Intentar MinGW g++)    echo MSVC cl not found. Trying MinGW g++ if available...) else (    )        echo MSVC compilation failed (cl returned error). Trying MinGW...    ) else (        goto :EOF        echo === compilacion MSVC exitosa: %OUT% ===    if %ERRORLEVEL%==0 (    cl /EHsc /MD /I "%SDK_INC%" %SRC% /link /LIBPATH:"%SDK_LIB%" %SDK_LIBS% /OUT:%OUT%    echo Compiling (cl)...        set SDK_LIBS=UFScanner.lib UFMatcher.lib    REM ajustar nombres de librerias del SDK si las tienes (UFScanner.lib UFMatcher.lib)        )        echo WARNING: SDK_LIB not set. If linking fails, set SDK_LIB to your SDK lib x64 path.    if "%SDK_LIB%"=="" (    )        echo WARNING: SDK_INC not set. If compilation fails, set SDK_INC to your SDK include path.    if "%SDK_INC%"=="" (    echo Found MSVC cl, compiling with cl...if %ERRORLEVEL%==0 (where cl >nul 2>&1
nrem Primero intentar MSVC (cl)
necho === Compilando %SRC% -> %OUT% ===set SRC=capturar.cpp
nset OUT=capturar.exenrem Archivo fuente y salida