# 🤖 NAUTA: Arquitectura Final Integrada

**Estado**: Implementación completa | **Fecha**: 2026-04-11 | **Version**: 2.1

---

## 📋 OVERVIEW

NAUTA es ahora un **módulo integrado dentro del dashboard** (no una página separada).

```
DASHBOARD (dashboard_v2.html)
    │
    ├─ NAUTA Module (Panel principal)
    │  ├─ Estado del día (tareas, completadas, energía)
    │  ├─ Botón [VER BRIEFING]
    │  ├─ Botón [REGISTRAR CIERRE]
    │  └─ Botón [VER ÚLTIMO CIERRE]
    │
    ├─ Modales (overlays)
    │  ├─ Modal Briefing (8:30 AM)
    │  ├─ Modal Cierre (21:30)
    │  └─ Modal Último Cierre (readonly)
    │
    └─ Otros módulos (NOTION, M1-M4, etc.)
```

---

## 🎯 FLUJO DE USUARIO

### Escenario 1: Ver Briefing (8:30 AM)

```
1. User abre dashboard
   │
2. Ve módulo NAUTA con:
   ├─ 3 Tareas Hoy
   ├─ 2 Completadas
   ├─ 70% Energía
   └─ 3 Botones de acción
   │
3. Click [VER BRIEFING]
   │
4. Modal se abre con:
   ├─ 🤖 NAUTA BRIEFING
   ├─ Tareas de hoy (de Notion real)
   ├─ Hábitos esperados
   ├─ Rueda de Vida (balance)
   └─ Recomendación personal
   │
5. Click [X] o ESC
   │
6. Vuelve al dashboard
```

### Escenario 2: Registrar Cierre (21:30)

```
1. User clickea [REGISTRAR CIERRE]
   │
2. Modal se abre con formulario:
   ├─ ✅ ¿Qué completaste?
   │  └─ Checkboxes de todas las tareas del día
   ├─ 💬 Notas Personales
   │  └─ Textarea libre
   └─ ⚡ Energía para mañana
      └─ Select: Baja, Media, Alta
   │
3. User completa el formulario:
   ├─ Checkea tareas completadas
   ├─ Escribe notas
   └─ Selecciona energía
   │
4. Click [GUARDAR CIERRE]
   │
5. POST /api/nauta/save-cierre
   ├─ Guarda en memoria (próximo: Notion)
   ├─ Actualiza módulo NAUTA
   └─ Cierra modal
   │
6. Dashboard se actualiza
   └─ Score completado: 50%
```

### Escenario 3: Ver Último Cierre

```
1. Click [VER ÚLTIMO CIERRE]
   │
2. Modal se abre (readonly):
   ├─ Fecha del cierre
   ├─ Score: X completadas / Y tareas
   ├─ Notas registradas
   └─ Energía registrada
   │
3. Click [X] o ESC
   └─ Vuelve al dashboard
```

---

## 🔌 ARQUITECTURA TÉCNICA

### Frontend (dashboard_v2.html)

```html
<!-- Módulo NAUTA en el dashboard -->
<div id="nauta-container">
    <!-- Estado del día -->
    <div class="stat-box">
        <div id="tareas-count">3</div> Tareas Hoy
    </div>
    
    <!-- Botones -->
    <button onclick="openBriefingModal()">VER BRIEFING</button>
    <button onclick="openCierreModal()">REGISTRAR CIERRE</button>
    <button onclick="openLastCierre()">VER ÚLTIMO CIERRE</button>
</div>

<!-- Modales -->
<div id="nauta-briefing-modal">...</div>
<div id="nauta-cierre-modal">...</div>
<div id="nauta-last-cierre-modal">...</div>

<!-- Funciones JavaScript -->
<script>
openBriefingModal() → fetch(/api/nauta/briefing-html)
openCierreModal() → fetch(/api/tasks/today)
guardarCierre() → POST /api/nauta/save-cierre
openLastCierre() → fetch(/api/nauta/last-cierre)
</script>
```

### Backend (notion_api.py)

```python
@app.route("/api/nauta/status", methods=["GET"])
# Retorna: total_tareas_hoy, completadas, energia

@app.route("/api/nauta/save-cierre", methods=["POST"])
# Body: {completadas, pendientes, notas, energia, fecha}
# Guarda en memoria + próximo: Notion

@app.route("/api/nauta/last-cierre", methods=["GET"])
# Retorna: {fecha, completadas, pendientes, notas, energia}

@app.route("/api/nauta/briefing-html", methods=["GET"])
# Retorna: HTML del briefing (ya existía)

@app.route("/api/nauta/cierre-html", methods=["GET"])
# Retorna: HTML del cierre (ya existía)
```

### Scheduler (nauta_scheduler.py)

```python
@scheduler.scheduled_job('cron', hour=8, minute=30)
def nauta_briefing_job():
    # Ejecuta a las 8:30 AM
    # Genera datos de briefing
    # Guarda en nauta_state

@scheduler.scheduled_job('cron', hour=21, minute=30)
def nauta_cierre_job():
    # Ejecuta a las 21:30
    # Genera template de cierre
    # Guarda en nauta_state
```

---

## 📊 FLUJO DE DATOS

### Datos que se usan

```
Notion Roadmap Master
    ├─ Tareas del día (get_today_tasks)
    └─ Top Q1 (get_top_q1_tasks)

Notion Hábitos
    ├─ Lista de hábitos
    └─ Frecuencia

Datos de ejemplo
    ├─ Rueda de Vida (hardcoded por ahora)
    └─ Recomendaciones personalizadas

Estado en memoria (nauta_state)
    ├─ last_briefing
    ├─ briefing_data
    ├─ last_cierre
    └─ cierre_data
```

### Guardar en Notion (Próximo paso)

```
Crear tabla "NAUTA Logs" en Notion
    ├─ Date
    ├─ Tareas Completadas (Relation)
    ├─ Tareas Pendientes (Relation)
    ├─ Score (Formula)
    ├─ Notas (Rich Text)
    ├─ Energía (Select)
    └─ Timestamp (Date)

Endpoint POST /api/nauta/save-cierre
    └─ Guarda en tabla "NAUTA Logs"
```

---

## 🎨 UI/UX

### Módulo NAUTA en Dashboard

```
┌─────────────────────────────────────────┐
│ 🤖 NAUTA - Coach Automático             │
├─────────────────────────────────────────┤
│                                         │
│  📊 Estado de Hoy                      │
│  ┌──────────┬──────────┬──────────┐   │
│  │    3     │    2     │    70%   │   │
│  │ Tareas   │Completas │ Energía  │   │
│  └──────────┴──────────┴──────────┘   │
│                                         │
│  [📖 VER BRIEFING]                    │
│  [🌙 REGISTRAR CIERRE]                │
│  [📊 VER ÚLTIMO CIERRE]               │
│                                         │
│  ⚠️ Último cierre: Ayer a las 21:30   │
│     ✅ 2 completadas | ❌ 3 pendientes│
│                                         │
└─────────────────────────────────────────┘
```

### Modal Briefing

```
┌─────────────────────────────────────────┐
│ 🤖 NAUTA BRIEFING                  [X]  │
│ 11 de April de 2026                     │
├─────────────────────────────────────────┤
│                                         │
│ 💡 Recomendación: Hoy tienes 3        │
│    tareas. Comienza por la prioritaria│
│                                         │
│ 📋 Top 4 Tareas de Hoy                │
│ 1. Investigar ofertas (M1)             │
│ 2. Crear MVP (M2)                      │
│ 3. Ángulos (M3)                        │
│ 4. Testing Meta (M4)                   │
│                                         │
│ ✅ Hábitos Esperados                   │
│ □ Meditación 10 min                    │
│ □ Lectura 30 min                       │
│                                         │
│ ⚖️ Rueda de Vida: [Gráfico 8 áreas]   │
│                                         │
└─────────────────────────────────────────┘
```

### Modal Cierre

```
┌─────────────────────────────────────────┐
│ 🌙 Registra tu Cierre              [X]  │
├─────────────────────────────────────────┤
│                                         │
│ ✅ ¿Qué completaste hoy?               │
│ ☑ Investigar ofertas (M1)              │
│ ☑ 50% Crear MVP (M2)                  │
│ ☐ Ángulos (M3)                         │
│ ☐ Testing Meta (M4)                    │
│                                         │
│ 💬 Notas Personales                    │
│ [Textarea: Hoy fue bueno. M1 rápido...] │
│                                         │
│ ⚡ Energía para mañana                  │
│ ○ Baja  ○ Media  ● Alta               │
│                                         │
│ [✅ GUARDAR CIERRE] [Cancelar]         │
│                                         │
└─────────────────────────────────────────┘
```

---

## ✅ CHECKLIST IMPLEMENTADO

```
✓ Módulo NAUTA integrado en dashboard
✓ Botones [VER BRIEFING], [REGISTRAR CIERRE], [VER ÚLTIMO CIERRE]
✓ Modal Briefing con HTML del scheduler
✓ Modal Cierre con formulario
✓ Modal Último Cierre (readonly)
✓ Estado del día (tareas, completadas, energía)
✓ Funciones JavaScript:
  ├─ openBriefingModal()
  ├─ openCierreModal()
  ├─ gardarCierre()
  ├─ openLastCierre()
  ├─ closeBriefingModal()
  ├─ closeCierreModal()
  ├─ closeLastCierreModal()
  └─ loadNautaStatus()
✓ Endpoints API:
  ├─ GET /api/nauta/status
  ├─ POST /api/nauta/save-cierre
  └─ GET /api/nauta/last-cierre
✓ Cerrar modales con ESC o click afuera
✓ Loading spinners mientras carga
✓ Integración con tareas reales (get_today_tasks)
```

---

## 🚀 TESTING AHORA

### 1. Inicia el backend

```bash
cd C:\apptesteo
python notion_api.py
```

### 2. Abre el dashboard

```
http://localhost:5000
```

### 3. Prueba NAUTA

- Verifica que ves el módulo NAUTA en el dashboard
- Click [📖 VER BRIEFING] → Debe abrir modal con briefing
- Click [🌙 REGISTRAR CIERRE] → Debe mostrar tareas de hoy para checkear
- Completa un cierre y click [GUARDAR]
- Click [📊 VER ÚLTIMO CIERRE] → Debe mostrar el cierre que acabas de guardar

---

## 📝 PRÓXIMOS PASOS

### Fase 1: Validación (HOY)
```
☐ Testear todos los botones del módulo NAUTA
☐ Verificar que los modales abren/cierran correctamente
☐ Completar un cierre y guardar
☐ Verificar que se muestra el último cierre
```

### Fase 2: Integración Notion (Esta semana)
```
☐ Crear tabla "NAUTA Logs" en Notion
☐ Conectar POST /api/nauta/save-cierre con Notion
☐ Cargar últimos cierres desde Notion
☐ Crear dashboard de histórico de cierres
```

### Fase 3: Datos Reales (Próxima semana)
```
☐ Conectar Rueda de Vida con datos reales de Notion
☐ Conectar Hábitos con datos reales
☐ Agregar recomendaciones personalizadas basadas en histórico
☐ Metricas y analytics
```

---

## 🎯 ESTADO FINAL

```
DASHBOARD ORIGINAL:   Mostrar tareas + botones
NAUTA SCHEDULER:      ✓ Cronometría 8:30 y 21:30
NAUTA MÓDULO:        ✓ Integrado en dashboard
MODALES:             ✓ Briefing + Cierre + Último Cierre
API ENDPOINTS:       ✓ Status + SaveCierre + LastCierre
GUARDAR DATOS:       ⏳ Próximo (Notion)
HISTÓRICO:           ⏳ Próximo (Dashboard de cierres)
```

---

**Implementación completada**: 2026-04-11  
**Próxima acción**: Testing del módulo NAUTA en dashboard  
**Responsable**: SISTEMA + Usuario

