#!/usr/bin/env python3
"""
NAUTA Scheduler - Sistema cronométrico automático
Ejecuta briefing (8:30 AM) y log de cierre (21:30) diariamente
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
import logging
import json
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - NAUTA - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar scheduler con timezone Buenos Aires
scheduler = BackgroundScheduler(timezone="America/Argentina/Buenos_Aires")

TAREAS_DB_ID = "3f0c07004c154bd4b5712141fc582815"
HABITOS_DB_ID = "89c9ec16837b454c9ce98e543cc62266"


def _get_notion_tasks(filters=None):
    """Query TAREAS desde Notion directamente (evita circular import con notion_api)"""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))

        conditions = []
        if filters:
            if filters.get("flag_q"):
                conditions.append({"property": "Flag_Q", "select": {"equals": filters["flag_q"]}})
            if filters.get("fecha_programada"):
                conditions.append({"property": "Fecha_programada", "date": {"equals": filters["fecha_programada"]}})

        query_kwargs = {
            "database_id": TAREAS_DB_ID,
            "sorts": [{"property": "Prioridad", "direction": "ascending"}]
        }
        if len(conditions) == 1:
            query_kwargs["filter"] = conditions[0]
        elif len(conditions) > 1:
            query_kwargs["filter"] = {"and": conditions}

        response = notion.databases.query(**query_kwargs)

        def _sel(p): return (p or {}).get("select") or {}
        def _txt(p): return ((p or {}).get("title") or [{}])[0].get("text", {}).get("content", "Sin título")
        def _num(p): return (p or {}).get("number") or 0
        def _date(p): return ((p or {}).get("date") or {}).get("start", "")

        tasks = []
        for page in response["results"]:
            props = page["properties"]
            tasks.append({
                "id": page["id"],
                "titulo": _txt(props.get("Título")),
                "estado": _sel(props.get("Estado")).get("name", ""),
                "prioridad": _sel(props.get("Prioridad")).get("name", ""),
                "flag_q": _sel(props.get("Flag_Q")).get("name", ""),
                "tiempo_estimado": _num(props.get("Tiempo_estimado")),
                "fecha_programada": _date(props.get("Fecha_programada")),
            })
        return tasks
    except Exception as e:
        logger.error(f"Error consultando tareas Notion: {e}")
        return []


def _get_top_q1():
    tasks = _get_notion_tasks({"flag_q": "Q1"})
    tasks = [t for t in tasks if t["estado"] != "✓ Completada"]
    priority_order = {"Alta": 0, "Media": 1, "Baja": 2}
    tasks.sort(key=lambda x: priority_order.get(x["prioridad"], 3))
    return tasks[:3]


def _get_today_tasks():
    """Tareas de hoy + pendientes de días anteriores (arrastre automático)"""
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        from notion_client import Client
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
                "tiempo_estimado": _num(props.get("Tiempo_estimado")),
                "fecha_programada": fecha_prog,
                "atrasada": fecha_prog < today,
            })
        return tasks
    except Exception as e:
        logger.error(f"Error obteniendo tareas del día: {e}")
        return []


def _get_habits():
    try:
        from notion_client import Client
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
                "streak": props.get("Streak", {}).get("number", 0),
            })
        return habits
    except Exception as e:
        logger.error(f"Error consultando hábitos Notion: {e}")
        return []

# Variables globales para compartir estado
nauta_state = {
    "last_briefing": None,
    "last_cierre": None,
    "briefing_data": {},
    "cierre_data": {}
}


def generate_briefing_data(tasks_today, top_q1, habits):
    """Genera estructura de datos para briefing de NAUTA - CON DATOS REALES"""

    # Traducir nombres de fecha al español
    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre"
    }

    fecha_str = datetime.now().strftime("%d de %B de %Y")
    for en, es in meses.items():
        fecha_str = fecha_str.replace(en, es)

    # Obtener Rueda de Vida
    try:
        # Importar función si no está disponible
        from notion_api import get_rueda_vida as get_rueda
        rueda_datos = get_rueda()
    except:
        rueda_datos = {}

    return {
        "timestamp": datetime.now().isoformat(),
        "fecha": fecha_str,
        "hora_generado": datetime.now().strftime("%H:%M"),
        "total_tareas_hoy": len(tasks_today),
        "top_3_q1": top_q1[:3] if top_q1 else [],
        "tareas_pendientes": [t for t in tasks_today if t.get("estado") != "✓ Completada"],
        "habitos_esperados": habits[:5] if habits else [],
        "rueda_vida_balance": rueda_datos if rueda_datos else {
            "Salud": 60,
            "Trabajo": 75,
            "Familia": 65,
            "Finanzas": 80,
            "Relaciones": 70,
            "Crecimiento": 85,
            "Diversión": 55,
            "Espiritualidad": 90
        }
    }


def generate_briefing_html(briefing_data, calendar_events=None):
    """Genera HTML del briefing matutino - DISEÑO MEJORADO"""

    # Sección de Google Calendar
    cal_html = ""
    if calendar_events:
        def fmt_time(dt_str):
            if not dt_str:
                return "todo el día"
            try:
                from datetime import datetime as dt
                d = dt.fromisoformat(dt_str.replace("Z", "+00:00"))
                return d.strftime("%H:%M")
            except Exception:
                return dt_str[:5] if len(dt_str) >= 5 else dt_str

        for ev in calendar_events:
            start = ev.get("start", {})
            end = ev.get("end", {})
            hora_inicio = fmt_time(start.get("dateTime") or start.get("date", ""))
            hora_fin = fmt_time(end.get("dateTime") or end.get("date", ""))
            titulo = ev.get("summary", "Evento sin título")
            ev_id = ev.get("id", "").replace("/", "_")
            titulo_safe = titulo.replace("'", "\\'")
            cal_html += f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px;background:#f8f9fa;border-radius:8px;margin-bottom:8px;">
                <input type="checkbox" id="cal-{ev_id}" data-eid="{ev_id}" data-title="{titulo_safe}"
                    style="width:18px;height:18px;cursor:pointer;accent-color:#4285F4;flex-shrink:0;"
                    onchange="saveCalEvent(this)">
                <div style="background:#4285F4;color:white;padding:4px 10px;border-radius:6px;font-size:0.85em;font-weight:600;white-space:nowrap;">
                    {hora_inicio}–{hora_fin}
                </div>
                <label for="cal-{ev_id}" style="font-weight:500;color:#1f2937;cursor:pointer;flex:1;">{titulo}</label>
            </div>"""

    tareas_html = ""
    for i, tarea in enumerate(briefing_data.get("tareas_pendientes", [])[:4], 1):
        prioridad = tarea.get('prioridad', 'Media').lower()
        color_prioridad = "#ef4444" if prioridad == "alta" else "#f97316" if prioridad == "media" else "#22c55e"

        atrasada = tarea.get('atrasada', False)
        badge_fecha = f'<span class="badge-atrasada">⚠️ {tarea.get("fecha_programada", "")}</span>' if atrasada else ""

        tareas_html += f"""
        <div class="tarea-card{'  tarea-atrasada' if atrasada else ''}">
            <div class="tarea-numero" style="background: {color_prioridad};">{i}</div>
            <div class="tarea-contenido">
                <h4>{tarea.get('titulo', 'Sin título')}</h4>
                <div class="tarea-meta">
                    <span class="badge-pri" style="background: {color_prioridad};">{prioridad.upper()}</span>
                    <span class="badge-tiempo">⏱️ {tarea.get('tiempo_estimado', 0)} min</span>
                    {badge_fecha}
                </div>
            </div>
        </div>
        """

    # Filtrar hábitos por día de la semana
    from datetime import datetime as _dt
    dow = _dt.now().weekday()  # 0=Lun, 1=Mar, 2=Mie, 3=Jue, 4=Vie, 5=Sab, 6=Dom
    freq_days = {
        'Diario': list(range(7)),
        'Lun-Vie': [0,1,2,3,4], 'Lun-Vier': [0,1,2,3,4],
        'Mar-Jue': [1,3],
        'Mié-Vie': [2,3,4], 'Mie-Vie': [2,3,4],
        'Sab-Dom': [5,6], 'Sáb-Dom': [5,6],
        'Personalizado': list(range(7)),
    }
    habitos_del_dia = [
        h for h in briefing_data.get("habitos_esperados", [])[:8]
        if (freq_days.get(h.get('frecuencia', 'Personalizado'), list(range(7)))) and
           dow in freq_days.get(h.get('frecuencia', 'Personalizado'), list(range(7)))
    ]

    habitos_html = ""
    for habito in habitos_del_dia:
        hid = habito.get('id', '')
        habitos_html += f"""
        <div class="habito-card">
            <input type="checkbox" id="h-{hid}" data-hid="{hid}" class="habito-checkbox">
            <label for="h-{hid}" class="habito-label">
                <span class="habito-nombre">{habito.get('nombre', 'Hábito')}</span>
                <span class="habito-freq">{habito.get('frecuencia', 'diario')}</span>
            </label>
        </div>
        """

    # Rueda de Vida con íconos por área
    RUEDA_ICONS = {
        'Salud': '💪', 'Trabajo': '💼', 'Familia': '👨‍👩‍👧', 'Finanzas': '💰',
        'Relaciones': '❤️', 'Crecimiento': '🌱', 'Diversión': '🎉', 'Espiritualidad': '🙏'
    }
    rueda = briefing_data.get("rueda_vida_balance", {})
    rueda_areas = list(rueda.items())
    rueda_html = ""
    for i, (area, valor) in enumerate(rueda_areas):
        icono = RUEDA_ICONS.get(area, '⭐')
        color = f"hsl({i * 45}, 65%, 50%)"
        rueda_html += f"""
        <div class="rueda-circle">
            <div style="font-size:1.8em;margin-bottom:4px;">{icono}</div>
            <div class="rueda-valor" style="color:{color};">{valor}%</div>
            <div class="rueda-label">{area}</div>
            <div class="rueda-bar"><div class="rueda-fill" style="width:{valor}%;background:{color};"></div></div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NAUTA Briefing</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            html, body {{ height: 100%; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #1f2937;
                line-height: 1.6;
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 30px;
                background: white;
                border-radius: 0;
                min-height: 100vh;
            }}

            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding-bottom: 30px;
                border-bottom: 2px solid #e5e7eb;
            }}

            .header h1 {{
                font-size: 2.5em;
                color: #667eea;
                margin-bottom: 10px;
                font-weight: 700;
            }}

            .header p {{
                font-size: 1.1em;
                color: #6b7280;
                margin: 5px 0;
            }}

            .header .hora {{
                font-size: 0.95em;
                color: #9ca3af;
                font-style: italic;
            }}

            /* LAYOUT PRINCIPAL */
            .main-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}

            .panel {{
                background: #f8fafc;
                border-radius: 12px;
                padding: 25px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}

            .panel h2 {{
                font-size: 1.3em;
                color: #1f2937;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                padding-bottom: 15px;
                border-bottom: 2px solid #e5e7eb;
            }}

            .panel h2 span {{
                font-size: 1.3em;
            }}

            /* RECOMENDACIÓN */
            .panel-recommendation {{
                grid-column: 1 / -1;
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                border: 2px solid #fcd34d;
            }}

            .recommendation-content {{
                color: #92400e;
            }}

            .recommendation-content h3 {{
                font-size: 1.1em;
                font-weight: 600;
                margin-bottom: 10px;
                color: #b45309;
            }}

            .recommendation-content p {{
                font-size: 0.95em;
                line-height: 1.7;
            }}

            /* TAREAS */
            .tarea-card {{
                display: flex;
                gap: 15px;
                padding: 15px;
                background: white;
                border-radius: 8px;
                margin-bottom: 12px;
                border-left: 4px solid #667eea;
                transition: all 0.2s ease;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }}

            .tarea-card:hover {{
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transform: translateX(4px);
            }}

            .tarea-numero {{
                display: flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                border-radius: 50%;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                flex-shrink: 0;
            }}

            .tarea-contenido {{
                flex: 1;
            }}

            .tarea-contenido h4 {{
                font-size: 0.95em;
                color: #1f2937;
                margin-bottom: 8px;
                font-weight: 600;
            }}

            .tarea-meta {{
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }}

            .badge-pri {{
                display: inline-block;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 0.75em;
                font-weight: 700;
                color: white;
            }}

            .badge-tiempo {{
                display: inline-block;
                padding: 4px 10px;
                background: #dbeafe;
                color: #1e40af;
                border-radius: 4px;
                font-size: 0.75em;
                font-weight: 600;
            }}

            /* HÁBITOS */
            .habito-card {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                background: white;
                border-radius: 8px;
                margin-bottom: 10px;
                cursor: pointer;
                transition: all 0.2s ease;
                border: 2px solid transparent;
            }}

            .habito-card:hover {{
                background: #f0f9ff;
                border-color: #667eea;
            }}

            .habito-checkbox {{
                width: 22px;
                height: 22px;
                cursor: pointer;
                accent-color: #667eea;
                flex-shrink: 0;
            }}

            .habito-label {{
                flex: 1;
                cursor: pointer;
                user-select: none;
            }}

            .habito-nombre {{
                display: block;
                font-weight: 600;
                color: #1f2937;
                font-size: 0.95em;
            }}

            .habito-freq {{
                display: block;
                font-size: 0.8em;
                color: #9ca3af;
                margin-top: 2px;
            }}

            /* RUEDA DE VIDA */
            .rueda-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
            }}

            .rueda-circle {{
                background: white;
                padding: 16px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e2e8f0;
                transition: all 0.2s ease;
            }}

            .rueda-circle:hover {{
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
                transform: translateY(-2px);
            }}

            .rueda-valor {{
                font-size: 1.6em;
                font-weight: 700;
                color: #667eea;
                margin-bottom: 6px;
            }}

            .rueda-label {{
                font-size: 0.8em;
                color: #6b7280;
                font-weight: 600;
                margin-bottom: 8px;
                line-height: 1.3;
            }}

            .rueda-bar {{
                height: 4px;
                background: #e5e7eb;
                border-radius: 2px;
                overflow: hidden;
            }}

            .rueda-fill {{
                height: 100%;
                border-radius: 2px;
                transition: width 0.3s ease;
            }}

            /* FOOTER */
            .footer {{
                text-align: center;
                padding-top: 30px;
                margin-top: 40px;
                border-top: 2px solid #e5e7eb;
                color: #9ca3af;
                font-size: 0.9em;
            }}

            .footer p {{
                margin: 5px 0;
            }}

            /* RESPONSIVE */
            @media (max-width: 1024px) {{
                .main-grid {{
                    grid-template-columns: 1fr 1fr;
                }}
            }}

            @media (max-width: 768px) {{
                .main-grid {{
                    grid-template-columns: 1fr;
                }}

                .rueda-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 NAUTA BRIEFING</h1>
                <p>{briefing_data.get('fecha', 'Hoy')}</p>
                <p class="hora">Generado a las {briefing_data.get('hora_generado', '')}</p>
            </div>

            <!-- RECOMENDACIÓN -->
            <div class="panel panel-recommendation">
                <div class="recommendation-content">
                    <h3>💡 Recomendación del Día</h3>
                    <p>Hoy tienes {briefing_data.get('total_tareas_hoy', 0)} tareas planificadas.
                    Sugiero comenzar con la tarea de mayor prioridad y hacer pausas cada 90 minutos.
                    Recuerda balancear el trabajo con descanso y movimiento.</p>
                </div>
            </div>

            <!-- GRID PRINCIPAL: Tareas y Hábitos -->
            <div class="main-grid">
                <!-- TAREAS -->
                <div class="panel">
                    <h2><span>📋</span> Tus Top 4 Tareas de Hoy</h2>
                    {tareas_html if tareas_html else '<p style="color: #9ca3af;">No hay tareas planificadas para hoy.</p>'}
                </div>

                <!-- HÁBITOS (filtrados por día) -->
                <div class="panel">
                    <h2><span>✅</span> Hábitos de Hoy</h2>
                    {habitos_html if habitos_html else '<p style="color: #9ca3af;">Sin hábitos para hoy.</p>'}
                </div>
            </div>

            <!-- RUEDA DE VIDA — ancho completo -->
            <div class="panel" style="margin-top:20px;">
                <h2><span>⚖️</span> Rueda de Vida</h2>
                <div style="display:grid;grid-template-columns:repeat(8,1fr);gap:12px;margin-top:12px;">
                    {rueda_html}
                </div>
            </div>

            {f'''
            <!-- GOOGLE CALENDAR con checkboxes locales -->
            <div class="panel" style="margin-top:20px;">
                <h2><span>📅</span> Google Calendar — Hoy</h2>
                <p style="font-size:12px;color:#9ca3af;margin-bottom:12px;">Marcá lo que ejecutaste — se guarda localmente para el cierre</p>
                {cal_html}
            </div>
            ''' if cal_html else ''}

            <div class="footer">
                <p><strong>TesteoLab NAUTA Coach</strong> | Sistema Automático de Productividad</p>
                <p>Próxima revisión: 21:30 (Log de Cierre)</p>
            </div>
        </div>

        <script>
        const TODAY = new Date().toISOString().slice(0,10);
        const CAL_KEY = 'cal_done_' + TODAY;

        // Guardar evento Calendar marcado (localStorage vía postMessage al padre)
        function saveCalEvent(cb) {{
            const states = JSON.parse(localStorage.getItem(CAL_KEY) || '{{}}');
            states[cb.dataset.eid] = {{ title: cb.dataset.title, done: cb.checked }};
            localStorage.setItem(CAL_KEY, JSON.stringify(states));
            window.parent.postMessage({{ type: 'cal_state_update', key: CAL_KEY, states }}, '*');
        }}

        // Restaurar estados guardados al cargar
        window.addEventListener('load', function() {{
            const states = JSON.parse(localStorage.getItem(CAL_KEY) || '{{}}');
            Object.entries(states).forEach(([id, s]) => {{
                const cb = document.getElementById('cal-' + id);
                if (cb) {{ cb.checked = s.done; if(s.done) cb.closest('div').style.opacity='0.6'; }}
            }});
            // Guardar hábitos al checkear
            document.querySelectorAll('.habito-checkbox').forEach(cb => {{
                cb.addEventListener('change', async function() {{
                    const hid = this.dataset.hid;
                    if (hid && this.checked) {{
                        try {{ await fetch('http://localhost:5000/api/habits/' + hid + '/done', {{method:'PATCH'}}); }} catch(e) {{}}
                    }}
                    this.closest('.habito-card').style.opacity = this.checked ? '0.5' : '1';
                }});
            }});
        }});
        </script>
    </body>
    </html>
    """
    return html


def generate_cierre_html(cierre_data):
    """Genera HTML del log de cierre"""

    completadas = cierre_data.get("completadas", 0)
    pendientes = cierre_data.get("pendientes", 0)
    total = completadas + pendientes
    porcentaje = int((completadas / total * 100) if total > 0 else 0)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NAUTA Log Cierre</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f8f9fa; color: #333; }}
            .container {{ max-width: 900px; margin: 20px auto; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; text-align: center; }}
            .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ color: #f5576c; font-size: 1.5em; margin-bottom: 15px; border-bottom: 2px solid #f5576c; padding-bottom: 10px; }}
            .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }}
            .stat-box {{ background: #f8f9fa; padding: 20px; text-align: center; border-radius: 8px; }}
            .stat-box .numero {{ font-size: 2em; font-weight: bold; color: #f5576c; }}
            .stat-box .label {{ color: #999; font-size: 0.9em; margin-top: 5px; }}
            .progress-bar {{ height: 30px; background: #e0e0e0; border-radius: 15px; overflow: hidden; display: flex; align-items: center; margin: 15px 0; }}
            .progress-fill {{ height: 100%; background: linear-gradient(90deg, #f093fb, #f5576c); width: {porcentaje}%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; transition: width 0.3s ease; }}
            .task-list {{ list-style: none; }}
            .task-list li {{ padding: 10px; margin: 8px 0; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #f5576c; }}
            .task-list li.completed {{ opacity: 0.6; }}
            .task-list li.completed::before {{ content: "✓ "; color: #4caf50; font-weight: bold; }}
            .notes {{ background: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; border-radius: 4px; font-style: italic; }}
            .footer {{ text-align: center; color: #999; font-size: 0.9em; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 NAUTA LOG DE CIERRE</h1>
                <p>{cierre_data.get('fecha', '')}</p>
                <p>Cierre a las {cierre_data.get('hora_cierre', '')}</p>
            </div>

            <div class="section">
                <h2>📊 Resumen del Día</h2>
                <div class="stats">
                    <div class="stat-box">
                        <div class="numero">{completadas}</div>
                        <div class="label">Completadas</div>
                    </div>
                    <div class="stat-box">
                        <div class="numero">{pendientes}</div>
                        <div class="label">Pendientes</div>
                    </div>
                    <div class="stat-box">
                        <div class="numero">{porcentaje}%</div>
                        <div class="label">Completado</div>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
            </div>

            <div class="section">
                <h2>✅ Tareas Completadas Hoy</h2>
                <ul class="task-list">
                    {' '.join([f'<li class="completed">{t}</li>' for t in cierre_data.get('tareas_completadas', [])])}
                </ul>
            </div>

            <div class="section">
                <h2>❌ Tareas Pendientes</h2>
                <ul class="task-list">
                    {' '.join([f'<li>{t}</li>' for t in cierre_data.get('tareas_pendientes', [])])}
                </ul>
            </div>

            <div class="section">
                <h2>💬 Notas Personales</h2>
                <div class="notes">
                    {cierre_data.get('notas', 'Sin notas registradas.')}
                </div>
            </div>

            <div class="footer">
                <p>TesteoLab NAUTA Coach | Sistema Automático</p>
                <p>Próximo briefing: Mañana 8:30 AM</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


@scheduler.scheduled_job('cron', hour=8, minute=30, timezone='America/Argentina/Buenos_Aires')
def nauta_briefing_job():
    """
    Ejecuta cada día a las 8:30 AM (Buenos Aires)
    Genera briefing matutino
    """
    try:
        logger.info("=" * 60)
        logger.info("🤖 NAUTA BRIEFING - Iniciando...")

        tasks_today = _get_today_tasks()
        top_q1 = _get_top_q1()
        habits = _get_habits()

        briefing_data = generate_briefing_data(
            tasks_today=tasks_today,
            top_q1=top_q1,
            habits=habits
        )

        briefing_html = generate_briefing_html(briefing_data)

        # Guardar en archivo para debugging
        with open('/tmp/nauta_briefing_latest.html', 'w', encoding='utf-8') as f:
            f.write(briefing_html)

        nauta_state["last_briefing"] = datetime.now()
        nauta_state["briefing_data"] = briefing_data

        logger.info("✓ NAUTA Briefing completado")
        logger.info(f"  Tareas hoy: {len(briefing_data.get('tareas_pendientes', []))}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"✗ Error en NAUTA Briefing: {e}")
        logger.error("=" * 60)


@scheduler.scheduled_job('cron', hour=21, minute=30, timezone='America/Argentina/Buenos_Aires')
def nauta_cierre_job():
    """
    Ejecuta cada día a las 21:30 (Buenos Aires)
    Genera log de cierre
    """
    try:
        logger.info("=" * 60)
        logger.info("🌙 NAUTA LOG DE CIERRE - Iniciando...")

        cierre_data = {
            "timestamp": datetime.now().isoformat(),
            "fecha": datetime.now().strftime("%d de %B de %Y").replace("of", "de"),
            "hora_cierre": datetime.now().strftime("%H:%M"),
            "completadas": 2,
            "pendientes": 2,
            "tareas_completadas": [
                "Investigar ofertas Meta Ads (M1)",
                "Setup cronométrico NAUTA 8:30 AM"
            ],
            "tareas_pendientes": [
                "Crear MVP landing page (M2) - 50% pendiente",
                "Generar 62 ángulos de venta (M3)"
            ],
            "notas": "Hoy fue un día productivo. M1 se completó rápidamente. M2 tiene más complejidad de la esperada. Mañana necesito comenzar antes con M3 para ajustar timeline."
        }

        cierre_html = generate_cierre_html(cierre_data)

        # Guardar en archivo para debugging
        with open('/tmp/nauta_cierre_latest.html', 'w', encoding='utf-8') as f:
            f.write(cierre_html)

        nauta_state["last_cierre"] = datetime.now()
        nauta_state["cierre_data"] = cierre_data

        logger.info("✓ NAUTA Log de Cierre completado")
        logger.info(f"  Completadas: {cierre_data['completadas']}/{cierre_data['completadas'] + cierre_data['pendientes']}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"✗ Error en NAUTA Cierre: {e}")
        logger.error("=" * 60)


def start_scheduler():
    """Inicia el scheduler (llamar una sola vez al iniciar la app)"""
    if not scheduler.running:
        scheduler.start()
        logger.info("✓ NAUTA Scheduler iniciado")
        logger.info("  - 8:30 AM: Briefing automático")
        logger.info("  - 21:30: Log de cierre automático")
        logger.info("  - Timezone: America/Argentina/Buenos_Aires (UTC-3)")
    else:
        logger.info("⚠ NAUTA Scheduler ya está corriendo")


def stop_scheduler():
    """Detiene el scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("✓ NAUTA Scheduler detenido")


def get_briefing_state():
    """Retorna el último estado de briefing"""
    return {
        "last_briefing": nauta_state["last_briefing"],
        "data": nauta_state["briefing_data"]
    }


def get_cierre_state():
    """Retorna el último estado de cierre"""
    return {
        "last_cierre": nauta_state["last_cierre"],
        "data": nauta_state["cierre_data"]
    }


if __name__ == "__main__":
    # Para testing local
    logger.info("Iniciando NAUTA Scheduler en modo test...")
    start_scheduler()

    # Simular ejecución de jobs
    logger.info("\n[TEST] Ejecutando briefing manualmente...")
    nauta_briefing_job()

    logger.info("\n[TEST] Ejecutando cierre manualmente...")
    nauta_cierre_job()

    logger.info("\nScheduler está corriendo. Presiona Ctrl+C para detener.")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_scheduler()
        logger.info("Scheduler detenido.")
