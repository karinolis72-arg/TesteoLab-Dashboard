# ⏰ NAUTA: Setup Cronométrico Automático

**Estado**: Listo para implementar | **Responsable**: SISTEMA | **Fecha**: 2026-04-11

---

## 🎯 Objetivo

Configurar NAUTA para que ejecute automáticamente:
- **8:30 AM** → Briefing matutino (lee tareas, hábitos, calendario)
- **21:30 (9:30 PM)** → Log de cierre (registra qué se hizo, qué falta)

---

## 📋 ARQUITECTURA

```
TRIGGER (Hora del Sistema)
    ↓
┌─ 08:30 AM
│  └─ NAUTA.briefing()
│     ├─ Lee "Sobre Mí" (contexto)
│     ├─ Lee Roadmap Master (Top 4 tareas HOY)
│     ├─ Lee Google Calendar (eventos de hoy)
│     ├─ Lee Rueda de Vida (balance actual)
│     └─ Genera BRIEFING en Notion + Dashboard
│
└─ 21:30 (9:30 PM)
   └─ NAUTA.log_cierre()
      ├─ Pregunta qué se hizo
      ├─ Pregunta qué falta
      ├─ Registra en "Sobre Mí" (Log de Cierre)
      ├─ Actualiza estado de tareas
      └─ Genera REPORTE de cierre
```

---

## 🔧 IMPLEMENTACIÓN

### Opción 1: Usando Google Cloud Scheduler (RECOMENDADO)

**Ventaja**: No necesita servidor corriendo 24/7  
**Desventaja**: Requiere Google Cloud

#### Pasos:

```
1. Google Cloud Console → Cloud Scheduler
2. Crear Job 1: NAUTA Briefing
   ├─ Nombre: nauta-briefing-830
   ├─ Frecuencia: 0 8 * * * (8:30 AM diario)
   ├─ Tipo: HTTP POST
   ├─ URL: https://[tu-dominio-render]/api/nauta/briefing
   └─ Headers: Authorization: Bearer [TOKEN]

3. Crear Job 2: NAUTA Log Cierre
   ├─ Nombre: nauta-cierre-2130
   ├─ Frecuencia: 0 21 * * * (21:30 diario)
   ├─ Tipo: HTTP POST
   ├─ URL: https://[tu-dominio-render]/api/nauta/log-cierre
   └─ Headers: Authorization: Bearer [TOKEN]
```

### Opción 2: Usando APScheduler en Python (ALTERNATIVA)

**Ventaja**: Todo en Python, más control  
**Desventaja**: Requiere servidor corriendo

#### Implementación en `notion_api.py`:

```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

# Job 1: NAUTA Briefing 8:30 AM
@scheduler.scheduled_job('cron', hour=8, minute=30)
def nauta_briefing_job():
    """Ejecuta briefing de NAUTA cada mañana a las 8:30"""
    try:
        context = get_user_context()
        tasks_today = get_top_tasks_today()
        calendar_events = get_calendar_events_today()
        vida_wheel = get_vida_wheel()
        
        briefing_text = generate_briefing(
            context,
            tasks_today,
            calendar_events,
            vida_wheel
        )
        
        # Guardar en Notion (Log)
        save_briefing_log(briefing_text)
        print(f"✓ NAUTA Briefing ejecutado: {datetime.now()}")
    except Exception as e:
        print(f"✗ Error en NAUTA Briefing: {e}")

# Job 2: NAUTA Log Cierre 21:30
@scheduler.scheduled_job('cron', hour=21, minute=30)
def nauta_cierre_job():
    """Ejecuta log de cierre cada noche a las 21:30"""
    try:
        completed_tasks = get_completed_tasks_today()
        pending_tasks = get_pending_tasks()
        
        cierre_text = generate_cierre_log(
            completed_tasks,
            pending_tasks
        )
        
        # Guardar en Notion
        save_cierre_log(cierre_text)
        print(f"✓ NAUTA Cierre ejecutado: {datetime.now()}")
    except Exception as e:
        print(f"✗ Error en NAUTA Cierre: {e}")

# Iniciar scheduler
scheduler.start()
```

---

## 📊 CONTENIDO: BRIEFING (8:30 AM)

### Estructura

```
NAUTA BRIEFING - [DATE] a las 8:30

════════════════════════════════════════
🎯 TU CONTEXTO HOY
════════════════════════════════════════

Nombre: [Tu nombre]
Rol Activo: [Ej: Emprendedora Digital]
Objetivo Hoy: [Del dashboard o último log]

════════════════════════════════════════
📅 TUS EVENTOS HOY (Google Calendar)
════════════════════════════════════════

08:30 - 09:00  | Briefing NAUTA
10:00 - 11:30  | Reunión con [Persona]
14:00 - 15:00  | Focus Time - Copywriting
18:00 - 19:00  | Análisis de ofertas M1

════════════════════════════════════════
📋 TOP 4 TAREAS DE HOY
════════════════════════════════════════

1. [PRIORIDAD] Investigar ofertas competencia (M1 Espía)
   Estado: TODO
   Tiempo estimado: 2h
   
2. [ALTA] Crear MVP landing page (M2 Crea)
   Estado: IN PROGRESS
   Tiempo estimado: 3h
   
3. [MEDIA] Generar 62 ángulos de venta (M3 Creativo)
   Estado: TODO
   Tiempo estimado: 4h
   
4. [BAJA] Documentar processo de testing (SISTEMA)
   Estado: BLOCKED
   Razón: Esperando salida de M2

════════════════════════════════════════
⚖️ RUEDA DE VIDA (Balance)
════════════════════════════════════════

Salud         ████░ 40%
Familia       ██░░░ 20%
Amigos        ███░░ 30%
Romance       ██░░░ 20%
Finanzas      ███░░ 60%
Negocios      █████ 90%
Personal Dev  ████░ 80%
Diversión     ██░░░ 20%

Enfoque hoy: Balancear "Familia" y "Diversión"

════════════════════════════════════════
💡 RECOMENDACIÓN NAUTA
════════════════════════════════════════

"Hoy tienes mucha carga de trabajo (M1-M3 en paralelo).
Sugiero: 15min de meditación antes de empezar.
¿Quieres hacer una pausa de 10min cada 90min?"

════════════════════════════════════════

[EMPEZAR TRABAJO]  [MODIFICAR TAREAS]  [VER CALENDARIO]
```

---

## 📊 CONTENIDO: LOG DE CIERRE (21:30)

### Estructura

```
NAUTA LOG DE CIERRE - [DATE] 21:30

════════════════════════════════════════
✅ ¿QUÉ COMPLETASTE HOY?
════════════════════════════════════════

[CHECKBOX] Investigar ofertas competencia (M1)
[CHECKBOX] 50% MVP landing page (M2)
[ ] Generar 62 ángulos (M3) - POSPUESTO
[ ] Documentar proceso testing - BLOQUEADO

SCORE: 2.5 / 4 completado (62.5%)

════════════════════════════════════════
❌ ¿QUÉ TE FALTA?
════════════════════════════════════════

URGENTE (mañana primero):
├─ Terminar MVP landing (M2) - 3h pendientes
└─ Generar ángulos (M3) - 4h pendientes

NORMAL (resto de semana):
├─ Documentar proceso testing
└─ Revisar métricas Meta Ads

════════════════════════════════════════
📊 MÉTRICAS DEL DÍA
════════════════════════════════════════

Horas productivas: 6.5 / 8 proyectadas
Interrupciones: 3
Energía final: Media (3/5)
Satisfacción: Alta (4/5)

════════════════════════════════════════
💬 NOTA PERSONAL
════════════════════════════════════════

[Área de texto libre para que escribas qué tal el día]

Ej: "Hoy fue bueno. La sesión de M1 fue rápida.
Pero M2 se complicó más de lo esperado. 
Mañana necesito empezar antes con M3."

════════════════════════════════════════
🎯 OBJETIVOS MAÑANA
════════════════════════════════════════

1. Terminar MVP landing (M2) - URGENTE
2. Iniciar ángulos (M3)
3. [Tú completas]

════════════════════════════════════════
⚖️ ENERGÍA MAÑANA (Predicción)
════════════════════════════════════════

Energía esperada: ░░░░░ (basada en hoy)
Recomendación: "Quizás comienza con tarea fácil de M3 (0.5h)
para tomar momentum, luego M2 completo"

════════════════════════════════════════

[GUARDAR LOG]  [VER RESUMEN SEMANA]  [AJUSTAR TAREAS]
```

---

## 🔌 ENDPOINTS API REQUERIDOS

```
GET /api/nauta/briefing
├─ Lee: Sobre Mí, Roadmap Master, Calendar, Rueda de Vida
├─ Genera: HTML briefing
├─ Guarda: Log en Notion
└─ Retorna: JSON con briefing generado

POST /api/nauta/log-cierre
├─ Body: {tareas_completadas, tareas_pendientes, notas}
├─ Guarda: En Notion "Sobre Mí"
├─ Actualiza: Estados en Roadmap Master
└─ Retorna: JSON con confirmación

GET /api/nauta/dashboard
├─ Retorna: Briefing + Cierre del día + Proyecciones
└─ Usa: Dashboard NAUTA
```

---

## 📱 INTEGRACIÓN CON DASHBOARD

En `dashboard_v2.html`, agregar módulo NAUTA:

```html
<div id="nauta-module">
  <h2>🤖 NAUTA Coach</h2>
  
  <div class="briefing-section">
    <button onclick="loadBriefing()">Cargar Briefing (8:30 AM)</button>
    <div id="briefing-content"></div>
  </div>
  
  <div class="cierre-section">
    <button onclick="loadCierre()">Cargar Log Cierre (21:30)</button>
    <div id="cierre-content"></div>
  </div>
  
  <div class="stats">
    <span>Tareas completadas: <strong id="completed-count">0</strong></span>
    <span>Energía: <strong id="energy-level">--</strong></span>
  </div>
</div>

<script>
async function loadBriefing() {
  const res = await fetch('/api/nauta/briefing');
  const data = await res.json();
  document.getElementById('briefing-content').innerHTML = data.html;
}

async function loadCierre() {
  const res = await fetch('/api/nauta/log-cierre');
  const data = await res.json();
  document.getElementById('cierre-content').innerHTML = data.html;
}
</script>
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

```
□ Instalar APScheduler: pip install apscheduler
□ Agregar jobs en notion_api.py
□ Crear funciones get_briefing(), generate_briefing()
□ Crear funciones get_cierre(), generate_cierre()
□ Crear endpoints /api/nauta/briefing y /api/nauta/log-cierre
□ Agregar módulo NAUTA en dashboard
□ Testear ejecución manual (sin esperar a 8:30)
□ Verificar que logs se guardan en Notion
□ Configurar alertas si hay errores
□ Documentar en CHANGELOG
```

---

## 🚀 PRÓXIMO PASO

Una vez completado el setup cronométrico:

→ **Crear tabla "Análisis de Ofertas"** en Notion  
→ **Configurar M1-M4 agents** con acceso a Roadmap Master  
→ **Testear flujo completo**: Crear oferta → M1 investiga → M2 crea → M3 genera ángulos → M4 testa

---

## 📌 NOTAS

- **Timezone**: América/Buenos Aires (ART, UTC-3)
- **Google Calendar**: Sincronizar cada 4 horas
- **Notion**: Actualizar campos automáticamente
- **Errores**: Guardar logs en /logs/nauta-{date}.log

