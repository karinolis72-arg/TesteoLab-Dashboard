import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

token = os.environ["NOTION_TOKEN"]
notion = Client(auth=token)
db_id = 'ed93c7e6-68c9-4d93-8b93-2b40970d55c1'

# 1. Archive old tasks
print("Archiving old tasks...")
has_more = True
start_cursor = None
while has_more:
    res = notion.databases.query(database_id=db_id, start_cursor=start_cursor)
    for row in res.get("results", []):
        try:
            notion.pages.update(page_id=row["id"], archived=True)
            print(f"Archived {row['id']}")
        except Exception as e:
            print(f"Failed to archive {row['id']}: {e}")
    has_more = res.get("has_more")
    start_cursor = res.get("next_cursor")

print("Done archiving.")

# 2. Add 5 Tasks for FASE 0
tasks = [
    {
        "Name": "Documentar framework BLAST + Context Engineering",
        "Módulo": "GENERAL",
        "Asignado a": "SISTEMA",
        "BLAST Step": "Blueprint",
        "Estado": "DONE",
        "originado por": "YO",
        "Esfuerzo": "S",
        "Prioridad": "Crítica",
        "Timeline FASE": "FASE 0"
    },
    {
        "Name": "Crear base de datos 'Sobre Mí'",
        "Módulo": "SISTEMA",
        "Asignado a": "SISTEMA",
        "BLAST Step": "Architecture",
        "Estado": "DONE",
        "originado por": "SISTEMA",
        "Esfuerzo": "M",
        "Prioridad": "Alta",
        "Timeline FASE": "FASE 0"
    },
    {
        "Name": "Configurar Roadmap Master",
        "Módulo": "SISTEMA",
        "Asignado a": "SISTEMA",
        "BLAST Step": "Architecture",
        "Estado": "IN PROGRESS",
        "originado por": "SISTEMA",
        "Esfuerzo": "M",
        "Prioridad": "Alta",
        "Timeline FASE": "FASE 0",
        "Bloqueadores": "Agregar columna Chat Agente + Vistas"
    },
    {
        "Name": "Setup cronométrico NAUTA (8:30 AM briefing)",
        "Módulo": "NAUTA",
        "Asignado a": "NAUTA",
        "BLAST Step": "Architecture",
        "Estado": "TODO",
        "originado por": "SISTEMA",
        "Esfuerzo": "L",
        "Prioridad": "Crítica",
        "Timeline FASE": "FASE 0"
    },
    {
        "Name": "Setup cronométrico NAUTA (21:30 log cierre)",
        "Módulo": "NAUTA",
        "Asignado a": "NAUTA",
        "BLAST Step": "Architecture",
        "Estado": "TODO",
        "originado por": "SISTEMA",
        "Esfuerzo": "M",
        "Prioridad": "Crítica",
        "Timeline FASE": "FASE 0"
    }
]

print("Adding new tasks...")
db_info = notion.databases.retrieve(db_id)
props_schema = db_info["properties"]

for t in tasks:
    properties = {}
    
    # Text types
    for key in ["Name", "Bloqueadores", "Notas"]:
        if key in t and t[key]:
            if key in props_schema:
                prop_type = props_schema[key]["type"]
                if prop_type == "title":
                    properties[key] = {"title": [{"text": {"content": t[key]}}]}
                elif prop_type == "rich_text":
                    properties[key] = {"rich_text": [{"text": {"content": t[key]}}]}
    
    # Select types
    for key in ["Módulo", "Asignado a", "BLAST Step", "Estado", "originado por", "Esfuerzo", "Prioridad", "Timeline FASE"]:
        if key in t and t[key]:
            if key in props_schema:
                prop_type = props_schema[key]["type"]
                if prop_type == "select":
                    properties[key] = {"select": {"name": t[key]}}
                elif prop_type == "multi_select":
                    properties[key] = {"multi_select": [{"name": t[key]}]}
                elif prop_type == "rich_text":
                    properties[key] = {"rich_text": [{"text": {"content": t[key]}}]}

    try:
        notion.pages.create(
            parent={"database_id": db_id},
            properties=properties
        )
        print(f"Created: {t['Name']}")
    except Exception as e:
        print(f"Failed to create {t['Name']}: {e}")

print("Upload complete!")
