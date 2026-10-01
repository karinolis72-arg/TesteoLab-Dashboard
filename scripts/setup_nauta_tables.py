#!/usr/bin/env python3
"""
Setup NAUTA - Crear tablas necesarias en Notion
Crea:
1. NAUTA Logs - para guardar cierres diarios
2. Rueda de Vida - para trackear balance de 8 áreas
"""

from notion_client import Client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
if not NOTION_TOKEN:
    print("❌ Error: NOTION_TOKEN no encontrado en .env")
    exit(1)

notion = Client(auth=NOTION_TOKEN)

# ID de la página padre (donde crearemos las tablas)
# Necesitas proporcionar el ID de tu workspace o una página existente
PARENT_PAGE_ID = "YOUR_PARENT_PAGE_ID"  # Reemplazar con ID real

def create_nauta_logs_table():
    """Crea tabla NAUTA Logs para guardar cierres diarios"""
    print("\n📋 Creando tabla NAUTA Logs...")

    try:
        response = notion.databases.create(
            parent={"page_id": PARENT_PAGE_ID},
            title=[{"type": "text", "text": {"content": "NAUTA Logs"}}],
            properties={
                "Fecha": {
                    "type": "date",
                    "date": {}
                },
                "Completadas": {
                    "type": "number",
                    "number": {"format": "number"}
                },
                "Pendientes": {
                    "type": "number",
                    "number": {"format": "number"}
                },
                "Energía": {
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "Baja", "color": "red"},
                            {"name": "Media", "color": "yellow"},
                            {"name": "Alta", "color": "green"}
                        ]
                    }
                },
                "Notas": {
                    "type": "rich_text",
                    "rich_text": {}
                },
                "Timestamp": {
                    "type": "created_time",
                    "created_time": {}
                }
            }
        )

        db_id = response["id"]
        print(f"✅ Tabla NAUTA Logs creada: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Error creando NAUTA Logs: {e}")
        return None


def create_rueda_vida_table():
    """Crea tabla Rueda de Vida para trackear 8 áreas"""
    print("\n📈 Creando tabla Rueda de Vida...")

    try:
        response = notion.databases.create(
            parent={"page_id": PARENT_PAGE_ID},
            title=[{"type": "text", "text": {"content": "Rueda de Vida"}}],
            properties={
                "Fecha": {
                    "type": "date",
                    "date": {}
                },
                "Área": {
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "Salud", "color": "red"},
                            {"name": "Trabajo", "color": "blue"},
                            {"name": "Familia", "color": "pink"},
                            {"name": "Finanzas", "color": "green"},
                            {"name": "Relaciones", "color": "purple"},
                            {"name": "Crecimiento", "color": "orange"},
                            {"name": "Diversión", "color": "yellow"},
                            {"name": "Espiritualidad", "color": "gray"}
                        ]
                    }
                },
                "Score": {
                    "type": "number",
                    "number": {"format": "number"}
                },
                "Notas": {
                    "type": "rich_text",
                    "rich_text": {}
                },
                "Timestamp": {
                    "type": "created_time",
                    "created_time": {}
                }
            }
        )

        db_id = response["id"]
        print(f"✅ Tabla Rueda de Vida creada: {db_id}")
        return db_id

    except Exception as e:
        print(f"❌ Error creando Rueda de Vida: {e}")
        return None


def main():
    print("=" * 60)
    print("🤖 SETUP NAUTA - Crear Tablas en Notion")
    print("=" * 60)

    print(f"\nUsando Notion Token: {NOTION_TOKEN[:20]}...")
    print(f"Parent Page ID: {PARENT_PAGE_ID}")

    nauta_logs_id = create_nauta_logs_table()
    rueda_vida_id = create_rueda_vida_table()

    print("\n" + "=" * 60)
    print("📌 PRÓXIMOS PASOS:")
    print("=" * 60)

    if nauta_logs_id:
        print(f"\n1. Copiar en notion_api.py línea ~44:")
        print(f'   NAUTA_LOGS_DB_ID = "{nauta_logs_id}"')

    if rueda_vida_id:
        print(f"\n2. Copiar en notion_api.py línea ~45:")
        print(f'   RUEDA_VIDA_DB_ID = "{rueda_vida_id}"')

    print("\n3. Ejecutar: python notion_api.py")
    print("4. Probar endpoints: /api/nauta/save-cierre, /api/nauta/rueda")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
