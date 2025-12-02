import ctypes
import os

# ---- CARGAR DLLS ----
UFScanner = ctypes.WinDLL("UFScanner.dll")
UFExtractor = ctypes.WinDLL("UFExtractor.dll")

# ---- CONSTANTES ----
UFS_OK = 0
UFS_TEMPLATE_TYPE_SUPREMA = 2001
UFS_TEMPLATE_TYPE_ISO = 2002

# ---- FUNCIONES ----

def check(code, name):
    if code != UFS_OK:
        print(f"[ERROR] {name} devolvió {code}")
        exit(1)

def main():
    print("=== CAPTURA DE HUELLA (Python + BioMini) ===")

    # Inicializar SDK
    ret = UFScanner.UFS_Init()
    check(ret, "UFS_Init")

    # Actualizar escáneres
    ret = UFScanner.UFS_Update()
    check(ret, "UFS_Update")

    # Contar escáneres
    scannerCount = ctypes.c_int()
    ret = UFScanner.UFS_GetScannerNumber(ctypes.byref(scannerCount))
    check(ret, "UFS_GetScannerNumber")

    if scannerCount.value <= 0:
        print("No hay escáner conectado.")
        return

    # Obtener handle
    scanner = ctypes.c_void_p()
    ret = UFScanner.UFS_GetScannerHandle(0, ctypes.byref(scanner))
    check(ret, "UFS_GetScannerHandle")

    print("Coloca el dedo en el lector...")

    # Capturar huella
    ret = UFScanner.UFS_CaptureSingleImage(scanner)
    check(ret, "UFS_CaptureSingleImage")

    # Obtener info del buffer
    w = ctypes.c_int()
    h = ctypes.c_int()
    r = ctypes.c_int()

    ret = UFScanner.UFS_GetCaptureImageBufferInfo(scanner, ctypes.byref(w), ctypes.byref(h), ctypes.byref(r))
    check(ret, "UFS_GetCaptureImageBufferInfo")

    # Leer imagen RAW
    image_size = w.value * h.value
    buffer = (ctypes.c_ubyte * image_size)()

    ret = UFScanner.UFS_GetCaptureImageBuffer(scanner, buffer)
    check(ret, "UFS_GetCaptureImageBuffer")

    # Guardar RAW
    with open("huella_firma.dat", "wb") as f:
        f.write(bytes(buffer))

    print("Imagen RAW guardada.")

    # ---- PLANTILLA SUPREMA ----
    UFScanner.UFS_SetTemplateType(scanner, UFS_TEMPLATE_TYPE_SUPREMA)

    tpl_sup = (ctypes.c_ubyte * 2048)()
    tpl_size = ctypes.c_int()
    quality = ctypes.c_int()

    ret = UFScanner.UFS_ExtractEx(scanner, 2048, tpl_sup, ctypes.byref(tpl_size), ctypes.byref(quality))
    if ret == UFS_OK:
        with open("huella_plantilla_suprema.dat", "wb") as f:
            f.write(bytes(tpl_sup)[:tpl_size.value])
        print("Plantilla SUPREMA generada.")
    else:
        print("No se pudo generar plantilla SUPREMA.")

    # ---- PLANTILLA ISO ----
    UFScanner.UFS_SetTemplateType(scanner, UFS_TEMPLATE_TYPE_ISO)

    tpl_iso = (ctypes.c_ubyte * 2048)()
    tpl_iso_size = ctypes.c_int()

    ret = UFScanner.UFS_ExtractEx(scanner, 2048, tpl_iso, ctypes.byref(tpl_iso_size), ctypes.byref(quality))

    if ret == UFS_OK:
        with open("huella_plantilla_iso.dat", "wb") as f:
            f.write(bytes(tpl_iso)[:tpl_iso_size.value])
        print("Plantilla ISO generada.")
    else:
        print("No se pudo generar plantilla ISO.")

    UFScanner.UFS_Uninit()
    print("=== CAPTURA COMPLETADA ===")


if __name__ == "__main__":
    main()
