import ctypes
import os
import sys
import json
import base64
import time
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.platform == "win32":
    os.add_dll_directory(BASE_DIR)

UFScanner = ctypes.WinDLL(os.path.join(BASE_DIR, "UFScanner.dll"))
UFS_OK = 0
UFS_TEMPLATE_TYPE_SUPREMA = 2001

def capturar_huella_estable():
    ret = UFScanner.UFS_Init()
    if ret != UFS_OK:
        raise Exception(f"UFS_Init error: {ret}")

    scanner = ctypes.c_void_p()
    try:
        UFScanner.UFS_Update()
        time.sleep(0.5)

        count = ctypes.c_int()
        UFScanner.UFS_GetScannerNumber(ctypes.byref(count))
        if count.value < 1:
            raise Exception("❌ No hay escáner Suprema conectado.")

        UFScanner.UFS_GetScannerHandle(0, ctypes.byref(scanner))

        ret = UFScanner.UFS_CaptureSingleImage(scanner)
        if ret != UFS_OK:
            raise Exception(f"UFS_CaptureSingleImage error: {ret}")

        ret = UFScanner.UFS_SetTemplateType(scanner, UFS_TEMPLATE_TYPE_SUPREMA)
        if ret != UFS_OK:
            raise Exception(f"UFS_SetTemplateType error: {ret}")

        tpl = (ctypes.c_ubyte * 2048)()
        tpl_size = ctypes.c_int()
        quality = ctypes.c_int()

        ret = UFScanner.UFS_ExtractEx(scanner, 2048, tpl,
                                      ctypes.byref(tpl_size),
                                      ctypes.byref(quality))
        if ret != UFS_OK:
            raise Exception(f"UFS_ExtractEx error: {ret}")

        plantilla = bytes(tpl)[:tpl_size.value]
        plantilla_b64 = base64.b64encode(plantilla).decode("utf-8")

        return plantilla_b64, quality.value

    finally:
        try:
            UFScanner.UFS_ClearCaptureImageBuffer(scanner)
        except:
            pass
        UFScanner.UFS_Uninit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Se debe enviar el ID del usuario"}))
        sys.exit(0)

    id_usuario = sys.argv[1]

    try:
        template_b64, calidad = capturar_huella_estable()
        print(json.dumps({
            "id_usuario": id_usuario,
            "template": template_b64,
            "quality": calidad
        }))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
