#!/usr/bin/env python3
"""
TesteoLab Notion API Backend
Provides REST API endpoints to fetch task and habit data from Notion
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)
logging.basicConfig(level=logging.INFO)

# Notion Database IDs
TAREAS_DB_ID = "b16c0cfb-a9b0-4667-872d-d7d43a1c2f88"
HABITOS_DB_ID = "79f96f1b-fbcd-439d-821b-f128314474e7"

# Will be populated by Notion queries
tasks_cache = {}
habits_cache = {}
last_sync = None


def query_notion_tareas(filters: Dict = None) -> List[Dict[str, Any]]:
    """
    Query TAREAS from Notion
    This would use the Notion API in production
    For now, returns mock data that matches the structure
    """
    from notion_client import Client

    # Try to initialize Notion client
    try:
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))

        # Build query
        query_filter = {
            "and": [
                {"property": "Estado", "select": {"is_not_empty": True}}
            ]
        }

        if filters:
            if filters.get("flag_q"):
                query_filter["and"].append({
                    "property": "Flag_Q",
                    "select": {"equals": filters["flag_q"]}
                })
            if filters.get("estado"):
                query_filter["and"].append({
                    "property": "Estado",
                    "select": {"equals": filters["estado"]}
                })
            if filters.get("fecha_programada"):
                query_filter["and"].append({
                    "property": "Fecha_programada",
                    "date": {"equals": filters["fecha_programada"]}
                })

        # Query database
        response = notion.databases.query(
            database_id=TAREAS_DB_ID,
            filter=query_filter,
            sorts=[
                {"property": "Prioridad", "direction": "ascending"},
                {"property": "Fecha_programada", "direction": "ascending"}
            ]
        )

        # Transform results
        tasks = []
        for page in response["results"]:
            props = page["properties"]
            tasks.append({
                "id": page["id"],
                "titulo": props.get("Título", {}).get("title", [{}])[0].get("text", {}).get("content", "Sin título"),
                "estado": props.get("Estado", {}).get("select", {}).get("name", ""),
                "prioridad": props.get("Prioridad", {}).get("select", {}).get("name", ""),
                "flag_q": props.get("Flag_Q", {}).get("select", {}).get("name", ""),
                "categoria": props.get("Categoría", {}).get("select", {}).get("name", ""),
                "tipo": props.get("Tipo", {}).get("select", {}).get("name", ""),
                "energia": props.get("Energía", {}).get("select", {}).get("name", ""),
                "duracion_bloque": props.get("Duración_bloque", {}).get("number", 0),
                "tiempo_estimado": props.get("Tiempo_estimado", {}).get("number", 0),
                "fecha_programada": props.get("Fecha_programada", {}).get("date", {}).get("start", ""),
                "asignado": props.get("Asignado", {}).get("select", {}).get("name", ""),
            })

        return tasks
    except Exception as e:
        logging.error(f"Error querying Notion: {e}")
        return []


def get_top_q1_tasks(limit: int = 4) -> List[Dict[str, Any]]:
    """Get top Q1 tasks for NAUTA briefing"""
    tasks = query_notion_tareas({
        "flag_q": "Q1"
    })

    # Filter out completed
    tasks = [t for t in tasks if t["estado"] != "✓ Completada"]

    # Sort by priority and scheduled time
    priority_order = {"Alta": 0, "Media": 1, "Baja": 2}
    tasks.sort(key=lambda x: (
        priority_order.get(x["prioridad"], 3),
        x.get("fecha_programada", "")
    ))

    return tasks[:limit]


def get_today_tasks() -> List[Dict[str, Any]]:
    """Get tasks scheduled for today"""
    today = datetime.now().strftime("%Y-%m-%d")
    tasks = query_notion_tareas({
        "fecha_programada": today
    })
    return [t for t in tasks if t["estado"] != "✓ Completada"]


def get_habits() -> List[Dict[str, Any]]:
    """Get all habits"""
    from notion_client import Client

    try:
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        response = notion.databases.query(
            database_id=HABITOS_DB_ID,
            sorts=[{"property": "Prioridad", "direction": "ascending"}]
        )

        habits = []
        for page in response["results"]:
            props = page["properties"]
            habits.append({
                "id": page["id"],
                "nombre": props.get("Nombre", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                "frecuencia": props.get("Frecuencia", {}).get("select", {}).get("name", ""),
                "categoria": props.get("Categoría", {}).get("select", {}).get("name", ""),
                "prioridad": props.get("Prioridad", {}).get("select", {}).get("name", ""),
                "meta": props.get("Meta", {}).get("text", ""),
                "streak": props.get("Streak", {}).get("number", 0),
            })

        return habits
    except Exception as e:
        logging.error(f"Error querying habits: {e}")
        return []


# ===== API ENDPOINTS =====

@app.route("/api/tasks/top-q1", methods=["GET"])
def api_top_q1():
    """Get top 4 Q1 tasks"""
    tasks = get_top_q1_tasks(limit=4)
    return jsonify({
        "success": True,
        "data": tasks,
        "count": len(tasks)
    })


@app.route("/api/tasks/today", methods=["GET"])
def api_today_tasks():
    """Get today's tasks"""
    tasks = get_today_tasks()
    return jsonify({
        "success": True,
        "data": tasks,
        "count": len(tasks)
    })


@app.route("/api/tasks", methods=["GET"])
def api_all_tasks():
    """Get all tasks with optional filters"""
    filters = {}

    if request.args.get("flag_q"):
        filters["flag_q"] = request.args.get("flag_q")
    if request.args.get("estado"):
        filters["estado"] = request.args.get("estado")
    if request.args.get("fecha_programada"):
        filters["fecha_programada"] = request.args.get("fecha_programada")

    tasks = query_notion_tareas(filters if filters else None)
    return jsonify({
        "success": True,
        "data": tasks,
        "count": len(tasks)
    })


@app.route("/api/habits", methods=["GET"])
def api_habits():
    """Get all habits"""
    habits = get_habits()
    return jsonify({
        "success": True,
        "data": habits,
        "count": len(habits)
    })


@app.route("/api/nauta/briefing", methods=["GET"])
def api_nauta_briefing():
    """Get NAUTA morning briefing data"""
    try:
        top_q1 = get_top_q1_tasks(limit=3)
        today_tasks = get_today_tasks()
        habits = get_habits()

        # Calculate date
        today_date = datetime.now().strftime("%d %b").upper()

        return jsonify({
            "success": True,
            "data": {
                "fecha": today_date,
                "top_3_tareas": top_q1,
                "tareas_hoy": today_tasks,
                "habitos_esperados": habits[:5] if habits else [],
                "total_tareas_dia": len(today_tasks),
                "q1_pendientes": len([t for t in top_q1 if t["estado"] != "✓ Completada"]),
                "timestamp": datetime.now().isoformat()
            }
        })
    except Exception as e:
        logging.error(f"Error in NAUTA briefing: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "data": {}
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/", methods=["GET"])
def serve_dashboard():
    """Serve the main dashboard HTML"""
    try:
        return send_file("dashboard_v2.html")
    except Exception as e:
        logging.error(f"Error serving dashboard: {e}")
        return jsonify({"error": "Dashboard not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
