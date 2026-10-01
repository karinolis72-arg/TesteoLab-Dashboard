#!/usr/bin/env python3
"""
Test NAUTA Endpoints - Validar que todos los endpoints funcionan
Ejecutar DESPUÉS de:
1. Crear tablas en Notion
2. Copiar IDs a .env
3. Reiniciar Flask (notion_api.py)
"""

import requests
import json
from datetime import datetime
import time

# URL base del servidor
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

def test_endpoint(method, path, data=None):
    """Testar un endpoint y retornar respuesta"""
    url = f"{BASE_URL}{path}"

    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=HEADERS, timeout=5)
        else:
            return None

        return {
            "status": response.status_code,
            "success": response.status_code == 200,
            "data": response.json() if response.text else {}
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "success": False,
            "error": str(e)
        }


def main():
    print("=" * 70)
    print("🤖 NAUTA - Test Endpoints")
    print("=" * 70)
    print(f"\nTesting: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    tests = [
        ("Health Check", "GET", "/api/health", None),
        ("NAUTA Status", "GET", "/api/nauta/status", None),
        ("Tareas Today", "GET", "/api/tasks/today", None),
        ("Top Q1 Tareas", "GET", "/api/tasks/top-q1", None),
        ("Hábitos", "GET", "/api/habits", None),
        ("NAUTA Rueda de Vida", "GET", "/api/nauta/rueda", None),
        ("NAUTA Hábitos", "GET", "/api/nauta/habitos", None),
        ("NAUTA Cierres Historial", "GET", "/api/nauta/cierres-historial?limit=7", None),
        ("NAUTA Briefing (JSON)", "GET", "/api/nauta/briefing", None),
        ("NAUTA Briefing (HTML)", "GET", "/api/nauta/briefing-html", None),
    ]

    results = []
    for test_name, method, path, data in tests:
        print(f"Testing: {test_name}...", end=" ")
        result = test_endpoint(method, path, data)

        if result and result.get("success"):
            print(f"✅ OK (HTTP {result.get('status')})")
            results.append((test_name, True, result))
        else:
            print(f"❌ FAILED")
            results.append((test_name, False, result))
            if result:
                print(f"   Error: {result.get('error', 'Unknown error')}")

    # Test POST endpoint
    print(f"\nTesting: Save Cierre (POST)...", end=" ")
    cierre_data = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "completadas": [{"id": "1", "titulo": "Task 1"}],
        "pendientes": [],
        "notas": "Test cierre from test script",
        "energia": "Alta"
    }
    result = test_endpoint("POST", "/api/nauta/save-cierre", cierre_data)
    if result and result.get("success"):
        print(f"✅ OK")
        results.append(("Save Cierre", True, result))
        print(f"   Persisted to Notion: {result.get('data', {}).get('persisted_to_notion')}")
    else:
        print(f"❌ FAILED")
        results.append(("Save Cierre", False, result))

    # Summary
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, success, result in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if not success and result and result.get("error"):
            print(f"   → {result.get('error')[:100]}")

    print(f"\n🎯 Score: {passed}/{total} endpoints funcionando ({passed*100//total}%)")

    if passed == total:
        print("\n✅ ¡EXCELENTE! Todos los endpoints funcionan.")
        print("   Fase 1 está LISTA para usar.")
    elif passed >= total * 0.8:
        print("\n⚠️  La mayoría funciona. Revisar los endpoint que fallaron.")
    else:
        print("\n❌ Hay problemas. Verificar:")
        print("   1. ¿Está corriendo Flask en puerto 5000?")
        print("   2. ¿.env tiene NAUTA_LOGS_DB_ID y RUEDA_VIDA_DB_ID?")
        print("   3. ¿Los IDs son válidos (sin espacios)?")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("Esperando 2 segundos para asegurar conexión...")
    time.sleep(2)
    main()
