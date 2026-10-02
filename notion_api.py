#!/usr/bin/env python3
"""
TesteoLab Notion API Backend
Provides REST API endpoints to fetch task and habit data from Notion
"""

from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS
import hmac
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
import anthropic

# Importar NAUTA Scheduler
try:
    from nauta_scheduler import (
        start_scheduler,
        get_briefing_state,
        get_cierre_state,
        ensure_briefing_data,
        nauta_state
    )
    NAUTA_ENABLED = True
except ImportError:
    NAUTA_ENABLED = False
    print("⚠️ Warning: nauta_scheduler no disponible. NAUTA deshabilitado.")

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)
logging.basicConfig(level=logging.INFO)

# Buffer circular de logs (últimos 100 eventos)
from collections import deque
_error_log = deque(maxlen=100)

class NotionHandler(logging.Handler):
    def emit(self, record):
        _error_log.append({
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "msg": self.format(record)
        })

_handler = NotionHandler()
_handler.setLevel(logging.WARNING)
logging.getLogger().addHandler(_handler)

# Iniciar NAUTA si está disponible
if NAUTA_ENABLED:
    start_scheduler()


# ===== PROTECCIÓN DE ACCESO =====
# El servicio es público en Render: sin esto, cualquiera que conozca la URL
# puede leer tus tareas, borrarlas y gastar tu crédito de Anthropic vía /api/chat.
#
# Si NAUTA_USER y NAUTA_PASS no están definidas, la protección queda APAGADA.
# Eso mantiene el desarrollo local sin fricción; en Render hay que definirlas.
NAUTA_USER = os.environ.get("NAUTA_USER", "")
NAUTA_PASS = os.environ.get("NAUTA_PASS", "")
AUTH_ACTIVA = bool(NAUTA_USER and NAUTA_PASS)

if not AUTH_ACTIVA:
    logging.warning(
        "NAUTA_USER/NAUTA_PASS sin definir: el servicio queda ABIERTO a cualquiera."
    )


@app.before_request
def _exigir_credenciales():
    if not AUTH_ACTIVA:
        return None
    # /api/health queda libre para que los monitores externos puedan pingear.
    if request.method == "OPTIONS" or request.path == "/api/health":
        return None
    cred = request.authorization
    if (cred
            and hmac.compare_digest(cred.username or "", NAUTA_USER)
            and hmac.compare_digest(cred.password or "", NAUTA_PASS)):
        return None
    return Response(
        "Acceso restringido",
        401,
        {"WWW-Authenticate": 'Basic realm="TesteoLab"'},
    )

# Notion Database IDs
TAREAS_DB_ID = "3f0c07004c154bd4b5712141fc582815"
HABITOS_DB_ID = "89c9ec16837b454c9ce98e543cc62266"
NAUTA_LOGS_DB_ID = os.environ.get("NAUTA_LOGS_DB_ID", "")
RUEDA_VIDA_DB_ID = os.environ.get("RUEDA_VIDA_DB_ID", "")
PERFIL_KARI_DB_ID = os.environ.get("PERFIL_KARI_DB_ID", "")
I18N_DB_ID = os.environ.get("I18N_DB_ID", "")
OFERTAS_M1_DB_ID = "f487e4497bd84508977e9fdc66ff0e8d"
OFERTA_SELECCIONADA_DB_ID = "e13a544b4b014a14aeb1413385e81c11"
ROADMAP_MASTER_DB_ID = "ed93c7e668c94d938b932b40970d55c1"

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
        conditions = []
        if filters:
            if filters.get("flag_q"):
                conditions.append({"property": "Flag_Q", "select": {"equals": filters["flag_q"]}})
            if filters.get("estado"):
                conditions.append({"property": "Estado", "select": {"equals": filters["estado"]}})
            if filters.get("fecha_programada"):
                conditions.append({"property": "Fecha_programada", "date": {"equals": filters["fecha_programada"]}})

        query_kwargs = {
            "database_id": TAREAS_DB_ID,
            "sorts": [
                {"property": "Prioridad", "direction": "ascending"},
                {"property": "Fecha_programada", "direction": "ascending"}
            ]
        }
        if len(conditions) == 1:
            query_kwargs["filter"] = conditions[0]
        elif len(conditions) > 1:
            query_kwargs["filter"] = {"and": conditions}

        response = notion.databases.query(**query_kwargs)

        def _sel(prop): return (prop or {}).get("select") or {}
        def _txt(prop): return ((prop or {}).get("title") or [{}])[0].get("text", {}).get("content", "Sin título")
        def _num(prop): return (prop or {}).get("number") or 0
        def _date(prop): return ((prop or {}).get("date") or {}).get("start", "")

        tasks = []
        for page in response["results"]:
            props = page["properties"]
            tasks.append({
                "id": page["id"],
                "titulo": _txt(props.get("Título")),
                "estado": _sel(props.get("Estado")).get("name", ""),
                "prioridad": _sel(props.get("Prioridad")).get("name", ""),
                "flag_q": _sel(props.get("Flag_Q")).get("name", ""),
                "categoria": _sel(props.get("Categoría")).get("name", ""),
                "tipo": _sel(props.get("Tipo")).get("name", ""),
                "energia": _sel(props.get("Energía")).get("name", ""),
                "duracion_bloque": _num(props.get("Duración_bloque")),
                "tiempo_estimado": _num(props.get("Tiempo_estimado")),
                "fecha_programada": _date(props.get("Fecha_programada")),
                "asignado": _sel(props.get("Asignado")).get("name", ""),
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
    """Tareas de hoy + pendientes de días anteriores (arrastre automático)"""
    from notion_client import Client
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        response = notion.databases.query(
            database_id=TAREAS_DB_ID,
            filter={
                "and": [
                    {"property": "Fecha_programada", "date": {"on_or_before": today}},
                    {"property": "Fecha_programada", "date": {"is_not_empty": True}},
                ]
            },
            sorts=[{"property": "Fecha_programada", "direction": "ascending"}]
        )

        def _sel(p): return (p or {}).get("select") or {}
        def _txt(p): return ((p or {}).get("title") or [{}])[0].get("text", {}).get("content", "Sin título")
        def _num(p): return (p or {}).get("number") or 0
        def _date(p): return ((p or {}).get("date") or {}).get("start", "")

        tasks = []
        for page in response["results"]:
            props = page["properties"]
            estado = _sel(props.get("Estado")).get("name", "")
            if estado == "✓ Completada":
                continue
            fecha_prog = _date(props.get("Fecha_programada"))
            tasks.append({
                "id": page["id"],
                "titulo": _txt(props.get("Título")),
                "estado": estado,
                "prioridad": _sel(props.get("Prioridad")).get("name", ""),
                "flag_q": _sel(props.get("Flag_Q")).get("name", ""),
                "categoria": _sel(props.get("Categoría")).get("name", ""),
                "tiempo_estimado": _num(props.get("Tiempo_estimado")),
                "fecha_programada": fecha_prog,
                "atrasada": fecha_prog < today,
            })
        return tasks
    except Exception as e:
        logging.error(f"Error obteniendo tareas del día: {e}")
        return []


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


def save_cierre_to_notion(cierre_data: Dict) -> bool:
    """Guardar cierre en tabla NAUTA Logs en Notion"""
    if not NAUTA_LOGS_DB_ID:
        logging.warning("⚠️ NAUTA_LOGS_DB_ID no configurado - guardando solo en memoria")
        return False

    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))

        # Convertir fecha a ISO format si es necesario
        fecha = cierre_data.get("fecha", datetime.now().strftime("%Y-%m-%d"))
        if isinstance(fecha, str) and len(fecha) > 10:
            fecha = fecha[:10]

        notion.pages.create(
            parent={"database_id": NAUTA_LOGS_DB_ID},
            properties={
                "Nombre": {
                    "title": [{"text": {"content": f"Cierre {fecha}"}}]
                },
                "Fecha": {
                    "type": "date",
                    "date": {"start": fecha}
                },
                "Completadas": {
                    "type": "number",
                    "number": cierre_data.get("completadas", 0)
                },
                "Pendientes": {
                    "type": "number",
                    "number": cierre_data.get("pendientes", 0)
                },
                "Energia": {
                    "type": "select",
                    "select": {"name": cierre_data.get("energia", "Media")}
                },
                "Notas": {
                    "type": "rich_text",
                    "rich_text": [{"type": "text", "text": {"content": cierre_data.get("notas", "")}}]
                }
            }
        )

        logging.info(f"✅ Cierre guardado en Notion: {fecha}")
        return True

    except Exception as e:
        logging.error(f"❌ Error guardando cierre en Notion: {e}")
        return False


def get_rueda_vida() -> Dict[str, int]:
    """Obtener scores actuales de Rueda de Vida desde Notion"""
    if not RUEDA_VIDA_DB_ID:
        # Retornar valores por defecto si no está configurada
        return {
            "Salud": 60,
            "Trabajo": 75,
            "Familia": 65,
            "Finanzas": 80,
            "Relaciones": 70,
            "Crecimiento": 85,
            "Diversión": 55,
            "Espiritualidad": 90
        }

    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))

        # Obtener últimas entradas de cada área (últimos 7 días)
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

        response = notion.databases.query(
            database_id=RUEDA_VIDA_DB_ID,
            filter={
                "property": "Fecha",
                "date": {"on_or_after": seven_days_ago}
            },
            sorts=[{"property": "Fecha", "direction": "descending"}]
        )

        # Procesar y retornar último valor de cada área
        rueda = {}
        processed_areas = set()

        for result in response.get("results", []):
            props = result["properties"]
            # La propiedad en Notion se llama "Área" CON tilde. Leerla como
            # "Area" devolvia siempre vacio, y la funcion caia al fallback
            # hardcodeado: por eso la rueda mostraba siempre los mismos valores.
            prop_area = props.get("Área") or props.get("Area") or {}
            area = (prop_area.get("select") or {}).get("name", "")
            score = (props.get("Score") or {}).get("number", 0)

            if area and area not in processed_areas:
                rueda[area] = score
                processed_areas.add(area)

        return rueda if rueda else {
            "Salud": 60,
            "Trabajo": 75,
            "Familia": 65,
            "Finanzas": 80,
            "Relaciones": 70,
            "Crecimiento": 85,
            "Diversión": 55,
            "Espiritualidad": 90
        }

    except Exception as e:
        logging.error(f"Error obteniendo Rueda de Vida: {e}")
        return {
            "Salud": 60,
            "Trabajo": 75,
            "Familia": 65,
            "Finanzas": 80,
            "Relaciones": 70,
            "Crecimiento": 85,
            "Diversión": 55,
            "Espiritualidad": 90
        }


def get_cierre_history(limit: int = 7) -> List[Dict]:
    """Obtener historial de cierres desde NAUTA Logs"""
    if not NAUTA_LOGS_DB_ID:
        return []

    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))

        response = notion.databases.query(
            database_id=NAUTA_LOGS_DB_ID,
            sorts=[{"property": "Fecha", "direction": "descending"}],
            page_size=limit
        )

        cierres = []
        for result in response.get("results", []):
            props = result["properties"]
            cierres.append({
                "id": result["id"],
                "fecha": props.get("Fecha", {}).get("date", {}).get("start", ""),
                "completadas": props.get("Completadas", {}).get("number", 0),
                "pendientes": props.get("Pendientes", {}).get("number", 0),
                "energia": props.get("Energia", {}).get("select", {}).get("name", ""),
                "notas": props.get("Notas", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            })

        return cierres

    except Exception as e:
        logging.error(f"Error obteniendo historial de cierres: {e}")
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
    """Get NAUTA morning briefing (JSON data)"""
    try:
        if NAUTA_ENABLED:
            briefing_state = get_briefing_state()
            return jsonify({
                "success": True,
                "data": ensure_briefing_data(),
                "last_generated": briefing_state.get("last_briefing"),
                "timestamp": datetime.now().isoformat()
            })
        else:
            # Fallback si NAUTA no está habilitado
            top_q1 = get_top_q1_tasks(limit=3)
            today_tasks = get_today_tasks()
            habits = get_habits()
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


@app.route("/api/nauta/briefing-html", methods=["GET", "POST"])
def api_nauta_briefing_html():
    """Get NAUTA morning briefing as HTML. POST acepta { events: [...] } con eventos de Google Calendar."""
    try:
        calendar_events = None
        if request.method == "POST":
            body = request.get_json(silent=True) or {}
            calendar_events = body.get("events") or None

        if NAUTA_ENABLED:
            briefing_data = ensure_briefing_data()

            from nauta_scheduler import generate_briefing_html
            html = generate_briefing_html(briefing_data, calendar_events=calendar_events)

            return Response(html, mimetype="text/html")
        else:
            return Response("<h1>NAUTA no habilitado</h1>", mimetype="text/html"), 503
    except Exception as e:
        logging.error(f"Error generating briefing HTML: {e}")
        return Response(f"<h1>Error: {str(e)}</h1>", mimetype="text/html"), 500


@app.route("/api/nauta/cierre", methods=["GET"])
def api_nauta_cierre():
    """Get NAUTA closing log (JSON data)"""
    try:
        if NAUTA_ENABLED:
            cierre_state = get_cierre_state()
            return jsonify({
                "success": True,
                "data": cierre_state.get("data", {}),
                "last_generated": cierre_state.get("last_cierre"),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": "NAUTA no habilitado",
                "data": {}
            }), 503
    except Exception as e:
        logging.error(f"Error in NAUTA cierre: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "data": {}
        }), 500


@app.route("/api/nauta/cierre-html", methods=["GET"])
def api_nauta_cierre_html():
    """Get NAUTA closing log as HTML"""
    try:
        if NAUTA_ENABLED:
            cierre_state = get_cierre_state()
            cierre_data = cierre_state.get("data", {})

            # Importar la función para generar HTML
            from nauta_scheduler import generate_cierre_html
            html = generate_cierre_html(cierre_data)

            return Response(html, mimetype="text/html")
        else:
            return Response("<h1>NAUTA no habilitado</h1>", mimetype="text/html"), 503
    except Exception as e:
        logging.error(f"Error generating cierre HTML: {e}")
        return Response(f"<h1>Error: {str(e)}</h1>", mimetype="text/html"), 500


@app.route("/api/nauta/status", methods=["GET"])
def api_nauta_status():
    """Get NAUTA daily status"""
    try:
        today_tasks = get_today_tasks()
        completed = len([t for t in today_tasks if t.get("estado") == "✓ Completada"])
        total = len(today_tasks)

        if NAUTA_ENABLED:
            return jsonify({
                "success": True,
                "status": "enabled",
                "total_tareas_hoy": total,
                "completadas": completed,
                "energia": 70,
                "last_briefing": nauta_state.get("last_briefing"),
                "last_cierre": nauta_state.get("last_cierre"),
                "next_briefing": "08:30 AM (Buenos Aires time)",
                "next_cierre": "21:30 (Buenos Aires time)",
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "status": "disabled",
                "error": "NAUTA scheduler not available"
            }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/nauta/save-cierre", methods=["POST"])
def api_nauta_save_cierre():
    """Guardar log de cierre en Notion (tabla NAUTA Logs)"""
    try:
        data = request.json

        cierre_data = {
            "fecha": data.get("fecha", datetime.now().strftime("%Y-%m-%d")),
            "completadas": len(data.get("completadas", [])),
            "pendientes": len(data.get("pendientes", [])),
            "tareas_completadas": data.get("completadas", []),
            "tareas_pendientes": data.get("pendientes", []),
            "notas": data.get("notas", ""),
            "energia": data.get("energia", "Media"),
            "timestamp": datetime.now().isoformat()
        }

        # Guardar en Notion (persistente)
        notion_saved = save_cierre_to_notion(cierre_data)

        # Guardar en estado global (memoria)
        if NAUTA_ENABLED:
            nauta_state["cierre_data"] = cierre_data
            nauta_state["last_cierre"] = datetime.now()

        log_msg = f"✅ Cierre guardado: {cierre_data.get('fecha')}"
        if not notion_saved:
            log_msg += " (solo en memoria)"
        logging.info(log_msg)

        return jsonify({
            "success": True,
            "message": "Cierre guardado correctamente",
            "persisted_to_notion": notion_saved,
            "data": cierre_data
        })
    except Exception as e:
        logging.error(f"Error saving cierre: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/nauta/last-cierre", methods=["GET"])
def api_nauta_last_cierre():
    """Obtener el último log de cierre"""
    try:
        if NAUTA_ENABLED and nauta_state.get("cierre_data"):
            return jsonify({
                "success": True,
                "data": nauta_state.get("cierre_data")
            })
        else:
            return jsonify({
                "success": True,
                "data": None,
                "message": "No hay cierre registrado"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/nauta/trigger-briefing", methods=["POST"])
def api_trigger_briefing():
    """Dispara el briefing manualmente (para testing sin esperar 8:30 AM)"""
    try:
        if not NAUTA_ENABLED:
            return jsonify({"success": False, "error": "NAUTA no habilitado"}), 503
        from nauta_scheduler import nauta_briefing_job
        nauta_briefing_job()
        return jsonify({"success": True, "message": "Briefing generado correctamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nauta/trigger-cierre", methods=["POST"])
def api_trigger_cierre():
    """Dispara el cierre manualmente. Lo usa el cron externo de las 21:30,
    que de paso despierta el servicio dormido del plan free de Render."""
    try:
        if not NAUTA_ENABLED:
            return jsonify({"success": False, "error": "NAUTA no habilitado"}), 503
        from nauta_scheduler import nauta_cierre_job
        nauta_cierre_job()
        return jsonify({"success": True, "message": "Cierre generado correctamente"})
    except Exception as e:
        logging.error(f"Error disparando cierre: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nauta/rueda", methods=["GET"])
def api_nauta_rueda():
    """Obtener scores de Rueda de Vida"""
    try:
        rueda = get_rueda_vida()
        return jsonify({
            "success": True,
            "data": rueda,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error en /api/nauta/rueda: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/nauta/habitos", methods=["GET"])
def api_nauta_habitos():
    """Obtener hábitos esperados para hoy"""
    try:
        habits = get_habits()

        # Retornar los primeros 5 hábitos como "esperados" para el día
        habitos_esperados = []
        for h in habits[:5]:
            habitos_esperados.append({
                "id": h["id"],
                "nombre": h["nombre"],
                "frecuencia": h["frecuencia"],
                "categoria": h["categoria"],
                "streak": h["streak"]
            })

        return jsonify({
            "success": True,
            "data": habitos_esperados,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error en /api/nauta/habitos: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/nauta/cierres-historial", methods=["GET"])
def api_nauta_cierres_historial():
    """Obtener historial de cierres (últimos N días)"""
    try:
        limit = request.args.get('limit', 7, type=int)

        # Intentar obtener desde Notion primero
        cierres = get_cierre_history(limit=limit)

        # Si no hay datos en Notion, usar el último cierre en memoria
        if not cierres and NAUTA_ENABLED and nauta_state.get("cierre_data"):
            cierre = nauta_state.get("cierre_data")
            cierres = [{
                "fecha": cierre.get("fecha"),
                "completadas": cierre.get("completadas", 0),
                "pendientes": cierre.get("pendientes", 0),
                "energia": cierre.get("energia", ""),
                "notas": cierre.get("notas", "")
            }]

        return jsonify({
            "success": True,
            "data": cierres,
            "count": len(cierres),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error en /api/nauta/cierres-historial: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    from supabase_client import supabase_ok
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "supabase": "ok" if supabase_ok() else "error"
    })


@app.route("/", methods=["GET"])
def serve_dashboard():
    """Serve the main dashboard HTML"""
    try:
        dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard_v2.html")
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return Response(html_content, mimetype="text/html")
    except Exception as e:
        logging.error(f"Error serving dashboard: {str(e)}")
        return jsonify({"error": f"Dashboard not found: {str(e)}"}), 404




# ===== GOOGLE CALENDAR =====
@app.route("/api/calendar/config", methods=["GET"])
def calendar_config():
    """Return Google Calendar API configuration"""
    return jsonify({
        "client_id": os.environ.get("GOOGLE_CLIENT_ID", "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"),
        "scope": "https://www.googleapis.com/auth/calendar",
        "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/api/calendar/callback")
    })


@app.route("/api/calendar/events", methods=["POST"])
def calendar_events():
    """Get events from ALL Google Calendars using access token"""
    try:
        data = request.json
        access_token = data.get("access_token")

        if not access_token:
            return jsonify({"success": False, "error": "No access token"}), 400

        headers = {"Authorization": f"Bearer {access_token}"}

        # Get list of all calendars
        cal_list_resp = requests.get(
            "https://www.googleapis.com/calendar/v3/users/me/calendarList",
            headers=headers,
            params={"minAccessRole": "reader"}
        )
        if cal_list_resp.status_code == 401:
            return jsonify({"success": False, "error": "TOKEN_EXPIRED"}), 401
        if cal_list_resp.status_code != 200:
            return jsonify({"success": False, "error": f"Calendar API error: {cal_list_resp.status_code}"}), cal_list_resp.status_code

        calendars = cal_list_resp.json().get("items", [])

        # Fetch today's events from every calendar
        tz_offset = "-03:00"  # Argentina (GMT-3)
        today = datetime.now().date().isoformat()
        tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
        params = {
            "timeMin": f"{today}T00:00:00{tz_offset}",
            "timeMax": f"{tomorrow}T00:00:00{tz_offset}",
            "maxResults": 25,
            "singleEvents": True,
            "orderBy": "startTime"
        }

        all_events = []
        for cal in calendars:
            cal_id = cal.get("id", "")
            cal_name = cal.get("summary", cal_id)
            resp = requests.get(
                f"https://www.googleapis.com/calendar/v3/calendars/{requests.utils.quote(cal_id, safe='')}/events",
                headers=headers,
                params=params
            )
            if resp.status_code == 200:
                for ev in resp.json().get("items", []):
                    ev["_calendar"] = cal_name
                    all_events.append(ev)

        # Sort all events by start time
        def _sort_key(e):
            s = e.get("start", {})
            return s.get("dateTime") or s.get("date") or ""
        all_events.sort(key=_sort_key)

        return jsonify({"success": True, "data": all_events})

    except Exception as e:
        logging.error(f"Error fetching calendar events: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/calendar/create", methods=["POST"])
def calendar_create_event():
    """Crea un evento en Google Calendar"""
    try:
        data = request.json or {}
        access_token = data.get("access_token")
        if not access_token:
            return jsonify({"success": False, "error": "No access token"}), 400

        event_body = {
            "summary": data.get("summary", "Evento"),
            "description": data.get("description", ""),
            "start": {"dateTime": data["start"], "timeZone": "America/Argentina/Buenos_Aires"},
            "end":   {"dateTime": data["end"],   "timeZone": "America/Argentina/Buenos_Aires"},
        }
        cal_id = data.get("calendarId", "primary")
        resp = requests.post(
            f"https://www.googleapis.com/calendar/v3/calendars/{requests.utils.quote(cal_id, safe='')}/events",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
            json=event_body
        )
        if resp.status_code in (200, 201):
            return jsonify({"success": True, "event": resp.json()})
        return jsonify({"success": False, "error": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/calendar/update", methods=["PATCH"])
def calendar_update_event():
    """Mueve o modifica un evento existente en Google Calendar"""
    try:
        data = request.json or {}
        access_token = data.get("access_token")
        event_id = data.get("event_id")
        cal_id = data.get("calendarId", "primary")
        if not access_token or not event_id:
            return jsonify({"success": False, "error": "Faltan access_token o event_id"}), 400

        patch_body = {}
        if data.get("summary"):    patch_body["summary"] = data["summary"]
        if data.get("start"):      patch_body["start"] = {"dateTime": data["start"], "timeZone": "America/Argentina/Buenos_Aires"}
        if data.get("end"):        patch_body["end"]   = {"dateTime": data["end"],   "timeZone": "America/Argentina/Buenos_Aires"}
        if data.get("description") is not None: patch_body["description"] = data["description"]

        resp = requests.patch(
            f"https://www.googleapis.com/calendar/v3/calendars/{requests.utils.quote(cal_id, safe='')}/events/{event_id}",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
            json=patch_body
        )
        if resp.status_code == 200:
            return jsonify({"success": True, "event": resp.json()})
        return jsonify({"success": False, "error": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/calendar/delete", methods=["DELETE"])
def calendar_delete_event():
    """Elimina un evento de Google Calendar"""
    try:
        data = request.json or {}
        access_token = data.get("access_token")
        event_id = data.get("event_id")
        cal_id = data.get("calendarId", "primary")
        if not access_token or not event_id:
            return jsonify({"success": False, "error": "Faltan access_token o event_id"}), 400

        resp = requests.delete(
            f"https://www.googleapis.com/calendar/v3/calendars/{requests.utils.quote(cal_id, safe='')}/events/{event_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if resp.status_code == 204:
            return jsonify({"success": True})
        return jsonify({"success": False, "error": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== NAUTA: ACCIONES SOBRE NOTION =====

@app.route("/api/tasks/<page_id>/done", methods=["PATCH"])
def task_mark_done(page_id):
    """Marca una tarea como completada en Notion"""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        today = datetime.now().strftime("%Y-%m-%d")
        notion.pages.update(
            page_id=page_id,
            properties={
                "Estado": {"select": {"name": "✓ Completada"}},
                "Fecha_cierre": {"date": {"start": today}}
            }
        )
        return jsonify({"success": True, "action": "done", "page_id": page_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/tasks/<page_id>/reschedule", methods=["PATCH"])
def task_reschedule(page_id):
    """Mueve una tarea a otra fecha en Notion"""
    try:
        data = request.json or {}
        new_date = data.get("date")
        if not new_date:
            return jsonify({"success": False, "error": "Falta el campo 'date' (YYYY-MM-DD)"}), 400
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        notion.pages.update(
            page_id=page_id,
            properties={"Fecha_programada": {"date": {"start": new_date}}}
        )
        return jsonify({"success": True, "action": "rescheduled", "page_id": page_id, "new_date": new_date})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/tasks/<page_id>", methods=["DELETE"])
def task_delete(page_id):
    """Archiva (elimina) una tarea en Notion"""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        notion.pages.update(page_id=page_id, archived=True)
        return jsonify({"success": True, "action": "deleted", "page_id": page_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/habits/<page_id>/done", methods=["PATCH"])
def habit_mark_done(page_id):
    """Marca un hábito como completado hoy en Notion"""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        notion.pages.update(
            page_id=page_id,
            properties={"Estado_hoy": {"select": {"name": "✓ Hecho"}}}
        )
        return jsonify({"success": True, "action": "done", "page_id": page_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/habits/<page_id>", methods=["DELETE"])
def habit_delete(page_id):
    """Archiva (elimina) un hábito en Notion"""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        notion.pages.update(page_id=page_id, archived=True)
        return jsonify({"success": True, "action": "deleted", "page_id": page_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== MÓDULOS M1-M4: CONTEXTO NOTION =====

def _notion_client():
    return __import__("notion_client").Client(auth=os.environ.get("NOTION_TOKEN"))

def _sel(prop): return ((prop or {}).get("select") or {}).get("name", "")
def _txt(prop): return ((prop or {}).get("title") or [{}])[0].get("text", {}).get("content", "")
def _rich(prop): return "".join(t.get("text", {}).get("content", "") for t in (prop or {}).get("rich_text") or [])
def _num(prop): return (prop or {}).get("number")
def _url(prop): return (prop or {}).get("url", "")
def _date_start(prop): return ((prop or {}).get("date") or {}).get("start", "")


def query_ofertas_m1(limit=10):
    """Trae las últimas ofertas de 💰 Ofertas M1"""
    try:
        notion = _notion_client()
        response = notion.databases.query(
            database_id=OFERTAS_M1_DB_ID,
            sorts=[{"property": "Fecha Análisis", "direction": "descending"}],
            page_size=limit
        )
        ofertas = []
        for page in response["results"]:
            p = page["properties"]
            ofertas.append({
                "nombre": _txt(p.get("Name")),
                "nicho": _rich(p.get("Nicho")),
                "producto": _rich(p.get("Producto")),
                "estado": _sel(p.get("Estado")),
                "pais": _sel(p.get("País")),
                "tipo_oferta": _sel(p.get("Tipo Oferta")),
                "dias_activos": _num(p.get("Días Activos")),
                "presupuesto_usd": _num(p.get("Presupuesto Est. USD")),
                "score": _num(p.get("Score Total (0-100)")),
                "recomendacion": _sel(p.get("Recomendación")),
                "indicadores": _rich(p.get("Indicadores Éxito")),
                "notas": _rich(p.get("Notas")),
                "ads_url": _url(p.get("ADS URL")),
                "pv_url": _url(p.get("PV URL")),
                "fecha": _date_start(p.get("Fecha Análisis")),
            })
        return ofertas
    except Exception as e:
        logging.error(f"Error querying Ofertas M1: {e}")
        return []


def query_oferta_seleccionada():
    """Trae la oferta activa de ✨ Oferta Seleccionada (excluye las Descartadas)"""
    try:
        notion = _notion_client()
        response = notion.databases.query(
            database_id=OFERTA_SELECCIONADA_DB_ID,
            sorts=[{"timestamp": "created_time", "direction": "descending"}],
            page_size=5
        )
        ofertas = []
        for page in response["results"]:
            p = page["properties"]
            ofertas.append({
                "nombre": _txt(p.get("Name")),
                "promesa": _rich(p.get("Promesa")),
                "gancho": _rich(p.get("Gancho")),
                "copy": _rich(p.get("Copy")),
                "bonus_estructura": _rich(p.get("Bonus Estructura")),
                "elementos_emocionales": _rich(p.get("Elementos Emocionales")),
                "garantia": _rich(p.get("Garantía")),
                "cta": _rich(p.get("CTA Propuesta")),
                "precio": _num(p.get("Precio")),
                "status_m2": _sel(p.get("Status M2")),
                "url_landing": _url(p.get("URL Landing Generada")),
                "notas": _rich(p.get("Notas")),
                "fecha_inicio": _date_start(p.get("Fecha Inicio M2")),
            })
        return ofertas
    except Exception as e:
        logging.error(f"Error querying Oferta Seleccionada: {e}")
        return []


@app.route("/api/m1/context")
def m1_context():
    """Contexto para el agente Espía: ofertas analizadas en Notion"""
    ofertas = query_ofertas_m1(limit=10)
    return jsonify({"success": True, "data": ofertas, "total": len(ofertas)})


@app.route("/api/m2/context")
def m2_context():
    """Contexto para el agente Crea: oferta seleccionada activa"""
    ofertas = query_oferta_seleccionada()
    return jsonify({"success": True, "data": ofertas, "total": len(ofertas)})


# M3 y M4 usan la misma oferta seleccionada (misma BD, distintos campos relevantes)
@app.route("/api/m3/context")
def m3_context():
    """Contexto para el agente Creativo: oferta activa para generar ángulos"""
    ofertas = query_oferta_seleccionada()
    return jsonify({"success": True, "data": ofertas, "total": len(ofertas)})


@app.route("/api/m4/context")
def m4_context():
    """Contexto para el agente Analista Meta: oferta activa + landing generada"""
    ofertas = query_oferta_seleccionada()
    # También traer ofertas M1 validadas para correlación
    validadas = [o for o in query_ofertas_m1(limit=20) if o.get("estado") == "Validada"]
    return jsonify({"success": True, "data": ofertas, "validadas_m1": validadas})


def query_roadmap_master(limit=50):
    """Trae tareas del Roadmap Master (no completadas/done)"""
    try:
        notion = _notion_client()
        response = notion.databases.query(
            database_id=ROADMAP_MASTER_DB_ID,
            filter={
                "and": [
                    {"property": "Estado", "select": {"does_not_equal": "DONE"}},
                    {"property": "Estado", "select": {"does_not_equal": "Completado"}}
                ]
            },
            sorts=[
                {"property": "Fase", "direction": "ascending"},
                {"property": "Prioridad", "direction": "ascending"}
            ],
            page_size=limit
        )
        items = []
        for page in response["results"]:
            props = page["properties"]
            items.append({
                "nombre": _txt(props.get("Name") or props.get("Tarea")),
                "estado": _sel(props.get("Estado")),
                "fase": _sel(props.get("Fase")),
                "modulo": _sel(props.get("Módulo")),
                "prioridad": _sel(props.get("Prioridad")),
                "blast_step": _sel(props.get("BLAST Step")),
                "bloqueadores": _rich(props.get("Bloqueadores")),
                "esfuerzo": _sel(props.get("Esfuerzo")),
            })
        return items
    except Exception as e:
        return [{"error": str(e)}]


@app.route("/api/sistema/context")
def sistema_context():
    """Contexto para el agente SISTEMA: estado del Roadmap Master"""
    items = query_roadmap_master(limit=50)
    return jsonify({"success": True, "data": items, "total": len(items)})


# ===== AGENT CHAT =====

_anthropic_client = None

def get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return None
        _anthropic_client = anthropic.Anthropic(api_key=api_key)
    return _anthropic_client


AGENT_SYSTEM_PROMPTS = {
    "NAUTA": """Eres NAUTA, el coach de productividad personal de Kari (Karina).
Tu rol es coaching directo, honesto y accionable. No eres un asistente genérico — conocés a Kari y su sistema.

QUIÉN ES KARI Y SU SISTEMA:
Kari está construyendo TesteoLab: un sistema personal que combina ejecución personal con un negocio de infoproductos low ticket en LATAM vía Meta Ads. La meta es 7 ofertas/semana testeadas → 28/mes → 2-3 winners con ROAS >3:1 → $10k/mes USD.

Los módulos de negocio son:
- M1 Espía: investiga la competencia en Meta Ads Library, selecciona ofertas ganadoras
- M2 Crea: construye el MVP y la landing en 24h
- M3 Creativo: genera 62 ángulos, creativos, videos para Meta Ads
- M4 Analista Meta: monitorea métricas, optimiza y escala hasta $10k/mes

BUSINESS OS — FrameworkIA:
Kari tiene una carpeta de contexto con archivos que te definen su perfil completo:
- sobre-mi.md: quién es, valores, cómo trabaja, forma de comunicación preferida
- negocio.md: TesteoLab, el pipeline M1→M4, objetivos
- prioridades-actuales.md: Q actual, proyectos activos
- decisiones-log.md: decisiones tomadas para no repetir análisis
- SOPs de M1-M4 como pasos ejecutables

TAREAS PROGRAMADAS (las hacés automáticamente a estas horas):
- Cierre Diario 21:00 ART: revisás los hábitos y tareas, calculás el progreso de las 8 áreas de la Rueda de Vida, generás reflexión del día, registrás en Notion Logs
- Planificación Semanal DOM 19:00 ART: ingestás el FrameworkIA, analizás la semana anterior, generás 3-5 objetivos de la semana, creás las 7 ofertas para testear, sugerís eventos en Google Calendar, actualizás el dashboard

EN CADA MENSAJE recibirás CONTEXTO ACTUAL con:
- Tareas de hoy desde Notion (con estado y si están atrasadas ⚠️)
- Hábitos del día y su estado
- Último cierre registrado
- Eventos de Google Calendar (si está conectado)

Con ese contexto podés y debés:
- Analizar la carga del día: ¿demasiadas tareas? ¿arrastre de atrasadas?
- Detectar desequilibrios: todo negocio / nada personal, o viceversa
- Sugerir replanificación cuando hay vencidas
- Cruzar tareas con el calendar: ¿hay tiempo real para lo planificado?
- Alertar si algo no cierra: demasiado para el tiempo disponible

Comandos de acción (el sistema parsea y muestra botones — no los menciones al usuario):
ACCION:done:ID:
ACCION:reschedule:ID:YYYY-MM-DD
ACCION:delete_task:ID:
ACCION:delete_habit:ID:
ACCION:cal_move:EID:NuevoTitulo|2026-04-13T10:00:00|2026-04-13T11:00:00|calId  (campo vacío=no cambia)
ACCION:cal_delete:EID:calId
ACCION:cal_create:NUEVO:Titulo|2026-04-13T10:00:00|2026-04-13T11:00:00|primary
IDs de tareas/hábitos en [id:...], eventos Calendar en [eid:...|cid:...]
Incluí los comandos al final sin explicarlos — los botones aparecen solos.

Responde en español, máximo 3-4 párrafos. Directo, sin frases vacías. Nunca digas que no tenés acceso a los datos.""",

    "Espía": """Eres Espía, el agente de investigación de mercado de TesteoLab (Módulo M1).
Tu especialidad es el funnel hacking y la selección de ofertas ganadoras para Kari.

META DE KARI: 7 ofertas/semana testeadas → 2-3 winners/mes con ROAS >3:1 → $10k/mes en LATAM.
Precio objetivo de ofertas: USD $7-$47 (low ticket). Mercado: LATAM, principalmente Argentina.

TU FLUJO DE 5 PASOS:
PASO 1 — Definir Búsqueda
  País/región (default: Argentina) + keywords o nombre de empresa
  Filtros: plataforma (Meta/Etsy/Clickbank), días activos (default: 30+), presupuesto estimado

PASO 2 — Buscar en Meta Ads Library
  API: GET /ads_library?ad_status=ACTIVE&country=AR&search_terms=...
  Datos: ad_id, advertiser, días activos, copy, media, CTA, landing page URL
  También buscás en Etsy, Clickbank, Amazon para productos digitales

PASO 3 — Analizar Anuncios (IA)
  Viabilidad por días activos: <30d 🟡 | 30-90d 🟢 | 90-180d 🟢🟢 | 180+ 🟢🟢🟢
  Presupuesto estimado: días × impresiones_estimadas × CPM ($8-20 según plataforma)
  Tipo de oferta: ebook, curso, membresía, servicio, físico
  Señales de éxito: urgencia, social proof, bonus, CTA directo, subnicho claro

PASO 4 — Filtrar & Clasificar (Smart Sort)
  Score 0-100: días activos (40pts) + presupuesto estimado (30pts) + señales de éxito (30pts)
  Ganadores: 80+ | Potencial Alto: 61-79 | Experimental: 31-60 | Descartar: <30
  Comparador: hasta 3 anuncios lado a lado

PASO 5 — Seleccionar y pasar a M2
  Output JSON hacia M2:
  { "offer_type": "...", "price_point": "...", "target_market": "...",
    "key_message": "...", "bonus_detected": [...], "viability_score": 87,
    "advertiser_url": "...", "days_active": 238, "estimated_investment": "$4200",
    "urgency_signals": [...], "cta_type": "...", "competitive_analysis": "..." }

Criterio clave: +30 días activos = probablemente rentable. +90 días = ganador confirmado.
Presupuesto estimado >$200 = mercado viable. Priorizar ofertas que ya funcionan en otro mercado.

Responde en español, analítico y directo. Si te pasan archivos, imágenes o landings, analizarlos en profundidad.""",

    "Crea": """Eres Crea, el agente de creación de ofertas de TesteoLab (Módulo M2).
Tu especialidad es construir MVPs y landings de alta conversión para infoproductos low ticket (USD $7-$47).

Recibís el output JSON de M1 Espía con la oferta ganadora a modelar. Tu trabajo es construirla completa en 24h.

Podés ayudar con:
- Generar estructura de MVP: guía PDF de 10-20 páginas (Gamma-style)
- Crear landing pages HTML listas para subir a Shopify o Hotmart
- Definir estructura de oferta: SKU, precio, descripción, bonus, order bumps (máx 3)
- Escribir copy persuasivo: pain point → promesa → producto → testimonios → garantía → CTA
- Modelar ofertas ganadoras que ya funcionan en otro mercado (adaptadas a LATAM)
- Si te pasan un template HTML o archivo, adaptarlo

Principio clave: el MVP no tiene que ser perfecto, tiene que vender.
Estructura de landing ganadora: urgencia + escasez + testimonios + 2 precios en pantalla.
Precio LATAM: $7-$47 USD. Target: emprendedores 25-45, Argentina/LATAM.

Responde en español. Sé creativo y orientado a conversión. Genera código HTML cuando se pida.""",

    "Creativo": """Eres Creativo, el agente de contenido y anuncios de TesteoLab (Módulo M3).
Tu especialidad es generar estrategias creativas completas para campañas de Meta Ads.

Arrancás 24h después de que M2 Crea entrega la oferta. Producís todo lo necesario para testear.

Podés ayudar con:
- Generar hasta 62 ángulos creativos (distintos hooks, dolores, públicos)
- Escribir guiones de video: hook (<3seg) + desarrollo + CTA
- Crear prompts de imagen para IA (Midjourney, DALL-E, Flux)
- Definir identidad visual: colores, tipografías, estilo (realista/ilustrado/3D)
- Analizar creativos de competencia y mejorarlos
- Generar variaciones para A/B testing
- Campaign briefs completos para Meta Ads Manager

Los 8 pasos del flujo M3:
P1: Extracción (producto, avatar, dolores, beneficios)
P2: Identidad Visual (marca, colores, tipografía)
P3: Estilo Visual (realista/ilustrado/3D/UGC)
P4: Formatos (noticiero/infografía/UGC/testimonial)
P5: Análisis IA de competencia visual
P6: Generación de 62 ángulos creativos
P7: Fábrica de Imágenes (variaciones, prompts)
P8: Fábrica de Videos (guiones, escenas, voces)

Responde en español. Sé creativo y concreto. Si te pasan referencias visuales, analizarlas.""",

    "Analista Meta": """Eres Analista Meta, el agente de métricas y optimización de TesteoLab (Módulo M4).
Tu especialidad es interpretar datos de Meta Ads y escalar las ofertas ganadoras hasta $10k/mes.

META GLOBAL: ROAS >3:1 en winners → escalar a $10k/mes USD en LATAM.
CPM objetivo LATAM: $8-15 USD. CPA objetivo: <25% del precio de venta.

Podés ayudar con:
- Interpretar métricas: ROAS, CTR, CPA, conversiones, presupuesto, impresiones, clicks
- Diagnosticar el embudo:
  * Pocos pagos iniciados → LANDING MALA (fix: copy, estructura, urgencia)
  * Muchos pagos iniciados, pocas compras → CHECKOUT MALO (fix: testimonios, bonus, garantía)
  * Buenas visitas pero pocas compras → OFERTA DÉBIL (fix: precio, propuesta de valor)
- Recomendar escalado progresivo (no pasar de $10 a $100 de golpe — escalar 20-30% cada 48h)
- Analizar resultados de A/B testing (testeos de 10-12 anuncios a $2/conjunto)
- Optimizar segmentación: públicos fríos, LAL, retargeting
- Recomendar cuándo pausar, cuándo escalar, cuándo declarar winner

ROAS objetivo: ≥1.5 para seguir. ≥3:1 = winner → escalar. <1.5 = optimizar antes de invertir más.
Identificá winners con 3+ días de datos y ≥50 clicks antes de declarar ganador.

Responde en español. Sé analítico y directo. Dame siempre una recomendación accionable con número concreto.""",

    "SISTEMA": """Eres el agente SISTEMA de TesteoLab, el asistente técnico y de arquitectura.
Ayudás con configuración, arquitectura, debugging y decisiones técnicas del proyecto.

STACK ACTUAL:
- Backend: Python/Flask (notion_api.py) en puerto 5000
- Frontend: dashboard_v2.html (HTML/JS puro, sin framework)
- Datos primarios: Notion (TAREAS, HÁBITOS, NAUTA Logs, Roadmap Master, Perfil Kari)
- Deploy: Render (Procfile + gunicorn)
- Agentes: NAUTA (coach diario), Espía M1, Crea M2, Creativo M3, Analista Meta M4

ROADMAP:
- v1.0 DONE: Dashboard, NAUTA briefing/cierre, chat de agentes con visión, acciones Calendar
- v1.1 EN PROGRESO: M1 Espía con Meta Ads Library API, flujo de 5 pasos, scoring 0-100
- v1.2 PRÓXIMO: M2 Crea — landing builder, MVP generator
- v1.3: M3 Creativo — 62 ángulos, scripts de video
- v2.0: M4 Analista Meta — integración Meta Ads Manager API, ROAS dashboard
- v3.0: Business OS completo — Context Engineering, memoria evolutiva, FrameworkIA

INTEGRACIONES PENDIENTES: Meta Ads Library API, Meta Ads Manager API, Supabase, Hotmart, n8n

En CADA mensaje recibirás en la sección CONTEXTO ACTUAL el estado del Roadmap Master desde Notion.

Podés ayudar con:
- Debugging de endpoints de la API Flask
- Decisiones de arquitectura y priorización
- Configuración de Notion, .env, deploy en Render
- Preguntas sobre el stack o dependencias
- Revisar qué sigue en el roadmap

Responde en español, técnico pero claro. Nunca digas que no tenés acceso al roadmap — te llega en el contexto."""
}


@app.route("/api/chat", methods=["POST"])
def chat_with_agent():
    try:
        data = request.json
        agent = data.get("agent", "NAUTA")
        message = data.get("message", "")
        history = data.get("history", [])
        context = data.get("context", "")
        images = data.get("images") or []  # [{ base64, mediaType }, ...]
        # Compatibilidad con campo "image" singular (legado)
        if not images and data.get("image"):
            images = [data["image"]]

        if not message and not images:
            return jsonify({"success": False, "error": "Mensaje vacío"}), 400

        client = get_anthropic_client()
        if not client:
            return jsonify({
                "success": False,
                "error": "ANTHROPIC_API_KEY no configurada. Agregar al .env y reiniciar el servidor."
            }), 500

        system_prompt = AGENT_SYSTEM_PROMPTS.get(agent, AGENT_SYSTEM_PROMPTS["NAUTA"])
        if context:
            # Limitar contexto a 2000 chars para no exceder rate limits
            ctx = context[:2000] + ("…[contexto truncado]" if len(context) > 2000 else "")
            system_prompt += f"\n\nCONTEXTO ACTUAL:\n{ctx}"

        messages = [
            {"role": h["role"], "content": h["content"]}
            for h in history[-8:]
            if h.get("role") in ("user", "assistant") and h.get("content")
        ]

        # Construir el contenido del mensaje actual (texto + imágenes opcionales)
        if images:
            user_content = []
            if message:
                user_content.append({"type": "text", "text": message})
            for im in images:
                if im.get("base64"):
                    user_content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": im.get("mediaType", "image/png"),
                            "data": im["base64"]
                        }
                    })
        else:
            user_content = message

        messages.append({"role": "user", "content": user_content})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )

        return jsonify({
            "success": True,
            "reply": response.content[0].text,
            "agent": agent,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        })

    except anthropic.RateLimitError:
        return jsonify({"success": False, "error": "RATE_LIMIT"}), 429
    except Exception as e:
        logging.error(f"Error en chat: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/roadmap/add-item", methods=["POST"])
def add_roadmap_item():
    """Crea un ítem en el Roadmap Master de Notion."""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        data = request.json

        nombre = data.get("nombre", "Sin nombre")
        estado = data.get("estado", "Backlog")
        fase = data.get("fase", "")
        modulo = data.get("modulo", "")
        prioridad = data.get("prioridad", "Media")
        blast_step = data.get("blast_step", "")
        esfuerzo = data.get("esfuerzo", "")
        bloqueadores = data.get("bloqueadores", "")
        url = data.get("url", "")

        properties = {
            "Nombre": {"title": [{"text": {"content": nombre}}]},
        }
        if estado:
            properties["Estado"] = {"select": {"name": estado}}
        if fase:
            properties["Fase"] = {"select": {"name": fase}}
        if modulo:
            properties["Módulo"] = {"select": {"name": modulo}}
        if prioridad:
            properties["Prioridad"] = {"select": {"name": prioridad}}
        if blast_step:
            properties["BLAST Step"] = {"select": {"name": blast_step}}
        if esfuerzo:
            properties["Esfuerzo"] = {"select": {"name": esfuerzo}}
        if bloqueadores:
            properties["Bloqueadores"] = {"rich_text": [{"text": {"content": bloqueadores}}]}

        children = []
        if url:
            children.append({
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"URL de referencia: {url}"}}]}
            })

        page = notion.pages.create(
            parent={"database_id": ROADMAP_MASTER_DB_ID},
            properties=properties,
            children=children if children else []
        )
        return jsonify({"success": True, "page_id": page["id"], "nombre": nombre})

    except Exception as e:
        logging.error(f"Error en add_roadmap_item: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Devuelve los últimos errores/warnings del servidor."""
    return jsonify({"success": True, "logs": list(_error_log)})


@app.route("/api/logs/clear", methods=["POST"])
def clear_logs():
    """Limpia el buffer de errores del servidor."""
    _error_log.clear()
    return jsonify({"success": True})


@app.route("/api/i18n", methods=["GET"])
def get_i18n():
    """
    Devuelve el diccionario de traducciones desde Notion (I18N_DB_ID).
    Formato de la DB Notion: Name (title/clave), ES, EN, PT, IT (rich_text).
    Responde: { "clave": { "es": "...", "en": "...", "pt": "...", "it": "..." } }
    """
    if not I18N_DB_ID:
        return jsonify({"success": False, "error": "I18N_DB_ID no configurado en .env"}), 404
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        results = notion.databases.query(database_id=I18N_DB_ID)
        translations = {}
        for page in results.get("results", []):
            props = page.get("properties", {})
            key_parts = props.get("Name", {}).get("title", [])
            if not key_parts:
                continue
            key = key_parts[0]["text"]["content"].strip()
            def get_rt(field):
                parts = props.get(field, {}).get("rich_text", [])
                return parts[0]["text"]["content"].strip() if parts else ""
            translations[key] = {
                "es": get_rt("ES"),
                "en": get_rt("EN"),
                "pt": get_rt("PT"),
                "it": get_rt("IT"),
            }
        return jsonify({"success": True, "translations": translations})
    except Exception as e:
        logging.error(f"Error en get_i18n: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/chat/resumir", methods=["POST"])
def resumir_chat():
    """Resume la conversación con Claude y guarda el resumen en Notion (Perfil Kari)."""
    try:
        data = request.json
        agent = data.get("agent", "NAUTA")
        history = data.get("history", [])

        if not history:
            return jsonify({"success": False, "error": "Historial vacío"}), 400

        client = get_anthropic_client()
        if not client:
            return jsonify({"success": False, "error": "ANTHROPIC_API_KEY no configurada"}), 500

        conversation_text = "\n".join([
            f"{'Kari' if h['role'] == 'user' else agent}: {h['content']}"
            for h in history
            if h.get("role") in ("user", "assistant") and h.get("content")
        ])

        resumen_prompt = f"""Analizá esta conversación que Kari tuvo con el agente {agent} y generá un resumen ejecutivo con este formato exacto:

**RESUMEN DE SESIÓN**
- Qué temas se trataron
- Qué decisiones se tomaron o acciones se ejecutaron
- Qué quedó pendiente o sin resolver

**SOBRE KARI (lo que aprendiste)**
- Patrones de trabajo o comportamiento observados
- Bloqueos, frustraciones o dificultades mencionadas
- Preferencias, modos de trabajo o valores que emergieron

**CONTEXTO PARA PRÓXIMA SESIÓN**
- Lo más importante que {agent} debería recordar en el próximo encuentro

Conversación:
{conversation_text[:6000]}"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": resumen_prompt}]
        )
        resumen = response.content[0].text

        # Guardar en Notion — propiedades reales de la DB Perfil Kari:
        # Name (title), Categoría (select), Contenido (rich_text), Fecha Actualización (date)
        notion_saved = False
        notion_error = ""
        if PERFIL_KARI_DB_ID:
            try:
                from notion_client import Client
                notion = Client(auth=os.environ.get("NOTION_TOKEN"))
                fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                notion.pages.create(
                    parent={"database_id": PERFIL_KARI_DB_ID},
                    properties={
                        "Name": {"title": [{"text": {"content": f"Sesión {agent} — {fecha_hoy}"}}]},
                        "Categoría": {"select": {"name": agent}},
                        "Fecha Actualización": {"date": {"start": fecha_hoy}},
                        "Contenido": {"rich_text": [{"text": {"content": resumen[:2000]}}]},
                    }
                )
                notion_saved = True
            except Exception as e:
                notion_error = str(e)
                logging.warning(f"No se pudo guardar resumen en Notion Perfil Kari: {e}")

        return jsonify({
            "success": True,
            "resumen": resumen,
            "notion_saved": notion_saved,
            "notion_error": notion_error
        })

    except Exception as e:
        logging.error(f"Error en resumir_chat: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # use_reloader=False: con el reloader activo, Flask levanta un proceso hijo
    # y start_scheduler() corre DOS veces -> el briefing de 8:30 y el cierre de
    # 21:30 se disparan duplicados. En produccion corre gunicorn, que no usa
    # reloader, asi que esto solo afecta el arranque local.
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
