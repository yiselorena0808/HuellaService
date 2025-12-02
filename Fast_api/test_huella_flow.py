#!/usr/bin/env python3
"""
test_huella_flow.py — Prueba completa del flujo de captura, guardado y verificación
Ejecutar: python test_huella_flow.py
"""

import requests
import json
from pathlib import Path

API_URL = "http://127.0.0.1:5000"

def test_flow():
    """Prueba el flujo completo: capturar → guardar → verificar"""
    
    print("=" * 60)
    print("PRUEBA COMPLETA DEL FLUJO DE HUELLA BIOMÉTRICA")
    print("=" * 60)
    
    # 1. Capturar huella
    print("\n1️⃣  CAPTURANDO HUELLA...")
    try:
        res = requests.get(f"{API_URL}/huella/capturar", timeout=60)
        if res.status_code != 200:
            print(f"❌ Error: {res.status_code}")
            print(f"Respuesta: {res.json()}")
            return False
        
        data = res.json()
        plantilla = data.get("plantilla_base64")
        
        if not plantilla:
            print("❌ No se recibió plantilla_base64")
            return False
        
        print(f"✅ Huella capturada correctamente")
        print(f"   Tamaño de plantilla: {len(plantilla)} caracteres")
    except Exception as e:
        print(f"❌ Error capturando: {e}")
        return False
    
    # 2. Guardar huella
    print("\n2️⃣  GUARDANDO HUELLA...")
    nombre = "TestUser123"
    try:
        res = requests.post(
            f"{API_URL}/huella/guardar",
            json={"nombre": nombre, "plantilla_base64": plantilla},
            timeout=10
        )
        
        if res.status_code != 200:
            print(f"❌ Error: {res.status_code}")
            print(f"Respuesta: {res.json()}")
            return False
        
        data = res.json()
        print(f"✅ Huella guardada: {data.get('mensaje')}")
    except Exception as e:
        print(f"❌ Error guardando: {e}")
        return False
    
    # 3. Verificar huella (misma plantilla)
    print("\n3️⃣  VERIFICANDO HUELLA (misma plantilla)...")
    try:
        res = requests.post(
            f"{API_URL}/huella/verificar",
            json={"nombre": nombre, "plantilla_base64": plantilla},
            timeout=10
        )
        
        if res.status_code != 200:
            print(f"❌ Error: {res.status_code}")
            print(f"Respuesta: {res.json()}")
            return False
        
        data = res.json()
        resultado = data.get("resultado", "")
        print(f"✅ Verificación: {resultado}")
        
        if "✅" in resultado:
            print("   ✅ La huella coincide (verificación exitosa)")
        else:
            print("   ⚠️  La huella no coincide")
    except Exception as e:
        print(f"❌ Error verificando: {e}")
        return False
    
    # 4. Listar usuarios
    print("\n4️⃣  LISTANDO USUARIOS...")
    try:
        res = requests.get(f"{API_URL}/usuarios", timeout=10)
        
        if res.status_code != 200:
            print(f"❌ Error: {res.status_code}")
            return False
        
        usuarios = res.json()
        print(f"✅ Total de usuarios: {len(usuarios)}")
        for u in usuarios:
            print(f"   - {u.get('nombre')} (registrado: {u.get('fecha')})")
    except Exception as e:
        print(f"❌ Error listando usuarios: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ FLUJO COMPLETO EXITOSO")
    print("=" * 60)
    return True

if __name__ == "__main__":
    import sys
    success = test_flow()
    sys.exit(0 if success else 1)
