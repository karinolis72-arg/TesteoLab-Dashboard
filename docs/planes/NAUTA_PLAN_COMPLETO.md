# 🤖 NAUTA - PLAN COMPLETO DE VALIDACIÓN

**Documento**: Plan paso a paso para completar NAUTA  
**Audiencia**: Validación antes de M1-M4  
**Estado**: Listo para ejecutar

---

## 📋 TABLA DE CONTENIDOS

1. Situación actual
2. Qué falta (desglosado)
3. Plan de ejecución por fases
4. Archivos a crear/modificar
5. Validación checklist
6. Timeline estimado

---

## 1️⃣ SITUACIÓN ACTUAL

### Dashboard NAUTA - Estado Real

```
✅ FUNCIONA:
  - Módulo NAUTA visible en sidebar
  - 3 botones responden (VER BRIEFING, REGISTRAR CIERRE, VER ÚLTIMO CIERRE)
  - Modales abren/cierran correctamente
  - Formulario cierre: checkboxes, notas, energía
  - Estado de hoy muestra números (70% energía hardcoded)
  - Scheduler APScheduler corre en background
  - Endpoints API existen (/api/nauta/briefing, /api/nauta/save-cierre, etc)

❌ NO FUNCIONA:
  - Briefing HTML muestra DATOS FAKE (hardcoded)
  - Tareas cierre cargan pero SIN estructura real
  - Hábitos: NO APARECEN EN BRIEFING
  - Cierres guardados EN MEMORIA (se pierden al reiniciar)
  - Rueda de Vida: números hardcoded (60%, 40%)
  - Módulo NOTAS: NO EXISTE
  - Chat NAUTA: NO IMPLEMENTADO
  - Datos NO se guardan en Notion
```

### Conexión Notion - Actual

```
Notion Databases:
  ✅ Sobre Mí         → existe
  ✅ Roadmap Master   → existe + datos iniciales
  ✅ Hábitos          → existe
  ❌ NAUTA Logs       → NO EXISTE (necesario crear)
  ❌ Rueda de Vida    → NO EXISTE (necesario crear)
  ❌ Notas NAUTA      → NO EXISTE (opcional)

API Endpoints:
  ✅ /api/tasks/today              → funciona
  ✅ /api/tasks/top-q1             → funciona
  ✅ /api/habits                   → funciona pero no conectado a NAUTA
  ❌ /api/nauta/save-cierre        → guarda en memoria, no en Notion
  ❌ /api/nauta/rueda              → NO EXISTE
  ❌ /api/nauta/chat               → NO EXISTE
  ❌ /api/nauta/habitos            → NO EXISTE
```

---

## 2️⃣ QUÉ FALTA - DESGLOSADO

### A. BRIEFING - DATOS REALES

**Problema**: `/api/nauta/briefing-html` retorna HTML con datos hardcoded

**Archivo afectado**: `nauta_scheduler.py` líneas 90-180

**Función**: `generate_briefing_html(briefing_data)`

**Qué falta**:
```
generate_briefing_html() recibe:
{
    "fecha": "11 de Abril",
    "top_3_tareas": [  ← HARDCODED, debe venir de Notion
        {"titulo": "Tarea 1", "prioridad": "Alta", ...}
    ],
    "tareas_hoy": [    ← HARDCODED, debe venir de /api/tasks/today
        {"titulo": "Hacer X", ...}
    ],
    "habitos": [       ← NO EXISTE, debe venir de /api/habits
        {"nombre": "Meditación", "hecho": false}
    ],
    "rueda_vida": {    ← HARDCODED 60%/40%, debe venir de Notion
        "salud": 60,
        "trabajo": 40,
        ...
    },
    "recomendacion": "Enfócate en X" ← HARDCODED, debe generar IA
}
```

**Solución**:
1. Modificar `nauta_scheduler.py` función que genera briefing_data
2. Hacer queries a Notion para cada sección
3. Pasar datos reales a `generate_briefing_html()`

---

### B. TAREAS DEL DÍA - CIERRE

**Problema**: Checkboxes en modal cierre cargan `/api/tasks/today` pero datos incompletos

**Archivo afectado**: `dashboard_v2.html` línea 971

**Función**: `window.openCierreModal()`

**Qué falta**:
```javascript
// Actual (línea 971-985):
const res = await fetch('/api/tasks/today');
const data = await res.json();
data.data.forEach(tarea => {
    // Los datos vienen SIN estructura:
    // {id: "...", titulo: "...", prioridad: "..."}
    // Pero faltan: duración, categoría, bloque horario
});

// Necesita:
- Título completo
- Prioridad (Alta/Media/Baja)
- Categoría (Trabajo/Personal/etc)
- Duración estimada
- Bloque horario
- Estado actual
```

**Solución**:
1. Mejorar endpoint `/api/tasks/today` en `notion_api.py`
2. Retornar todos los campos de Notion
3. Mostrar más info en checkboxes del cierre

---

### C. HÁBITOS - INTEGRACIÓN BRIEFING

**Problema**: "✅ Hábitos Esperados" en briefing está VACÍO

**Archivo afectado**: `nauta_scheduler.py` línea 150 (en generate_briefing_html)

**Qué falta**:
```html
<!-- Actual (vacío o hardcoded):
<div>
    ✅ Meditación
    ❌ Ejercicio
    ✅ Lectura
</div>
-->

<!-- Necesita conectar a:
- GET /api/habits
- Mostrar hábitos de HOY
- Indicar si se completó (checkbox)
- Permitir marcar como hecho en cierre
-->
```

**Solución**:
1. Crear endpoint `/api/nauta/habitos` que retorne hábitos de hoy + estado
2. Inyectar en HTML del briefing
3. Permitir tracking en formulario cierre

---

### D. GUARDADO EN NOTION - CIERRES

**Problema**: `POST /api/nauta/save-cierre` guarda en memoria, datos se pierden

**Archivo afectado**: `notion_api.py` línea 377

**Qué falta**:
```python
# Actual (línea 395-396):
if NAUTA_ENABLED:
    nauta_state["cierre_data"] = cierre_data  # ← En memoria
    nauta_state["last_cierre"] = datetime.now()

# Necesita:
# 1. Crear tabla NAUTA Logs en Notion
# 2. INSERT row en Notion cuando se guarda cierre
# 3. Campos:
#    - Fecha
#    - Tareas completadas (count)
#    - Tareas pendientes (count)
#    - Notas (texto)
#    - Energía (select)
#    - Timestamp
#    - Lista de tareas completadas (relation a Roadmap Master)
```

**Solución**:
1. Crear tabla "NAUTA Logs" en Notion
2. Modificar POST /api/nauta/save-cierre para hacer INSERT en Notion
3. Guardar historial permanente

---

### E. RUEDA DE VIDA - DATOS REALES

**Problema**: 8 áreas muestran números hardcoded (60%, 40%, etc)

**Archivo afectado**: `nauta_scheduler.py` línea 160 (en generate_briefing_html)

**Qué falta**:
```
Rueda de Vida - 8 áreas:
1. Salud (60%) ← hardcoded
2. Trabajo (40%) ← hardcoded
3. Familia (50%) ← hardcoded
4. Finanzas (75%) ← hardcoded
5. Relaciones (55%) ← hardcoded
6. Crecimiento (70%) ← hardcoded
7. Diversión (45%) ← hardcoded
8. Espiritualidad (80%) ← hardcoded

Necesita tabla Notion con:
- Fecha
- Area (select)
- Score (0-100)
- Notas
- Última actualización

Y endpoint: GET /api/nauta/rueda → retorna scores actuales
```

**Solución**:
1. Crear tabla "Rueda de Vida" en Notion
2. Crear endpoint `/api/nauta/rueda`
3. Inyectar en HTML del briefing

---

### F. MÓDULO NOTAS - NO EXISTE

**Problema**: No hay módulo NOTAS en la sidebar

**Archivo afectado**: `dashboard_v2.html` sidebar (no existe)

**Qué falta**:
```
1. Agregar icon-label "NOTAS" en sidebar (línea 520+)
2. Crear contenedor #notes-container (línea 580+)
3. Funciones JavaScript:
   - loadNotes()
   - addNote(titulo, contenido)
   - deleteNote(id)
4. Mostrar:
   - Historial de últimos 7 cierres
   - Notas personales
   - Métricas resumidas
```

**Solución**:
1. Agregar módulo NOTAS en sidebar + HTML
2. Crear JavaScript functions
3. Conectar a historial de NAUTA Logs de Notion

---

### G. CHAT CON NAUTA - NO IMPLEMENTADO

**Problema**: Botón "📞 Llamar NAUTA" en briefing no hace nada

**Archivo afectado**: `nauta_scheduler.py` (no existe endpoint chat)

**Qué falta**:
```
1. Endpoint: POST /api/nauta/chat
   Input: { message: "user message" }
   Output: { response: "NAUTA response" }

2. Integración OpenAI:
   - Crear prompt system para NAUTA
   - Context: datos del usuario (energía, tareas, hábitos)
   - Tone: coach motivacional

3. UI Modal:
   - Chat window con mensajes
   - Input para escribir
   - Botón send
```

**Solución**:
1. Crear endpoint /api/nauta/chat en notion_api.py
2. Integrar OpenAI API
3. Crear modal chat en dashboard_v2.html

---

## 3️⃣ PLAN DE EJECUCIÓN - FASES

### FASE 1: Integración Notion Mínima (CRÍTICA)

**Objetivo**: Que NAUTA lea datos REALES de Notion  
**Duración**: ~3-4 horas  
**Bloqueador para**: TODO lo demás

#### Paso 1.1: Crear tabla NAUTA Logs en Notion
```
Tabla: "NAUTA Logs"
Propiedades:
  - Fecha (date) - fecha del cierre
  - Completadas (number) - cuántas tareas
  - Pendientes (number) - cuántas quedan
  - Energía (select) - Baja/Media/Alta
  - Notas (text) - notas personales
  - Tareas (relation to Roadmap Master) - qué se completó
  - Timestamp (created_time)
```

#### Paso 1.2: Modificar notion_api.py

**Archivo**: `C:\apptesteo\notion_api.py`

**Cambios**:
- Línea 377+: Modificar `api_nauta_save_cierre()`
  - Hacer INSERT en NAUTA Logs (además de memory)
  - Guardar permanentemente en Notion

**Código necesario**:
```python
def api_nauta_save_cierre():
    # ... código actual ...
    cierre_data = {...}
    
    # NUEVO: Guardar en Notion
    if NAUTA_ENABLED:
        try:
            notion = Client(auth=os.environ.get("NOTION_TOKEN"))
            notion.pages.create(
                parent={"database_id": NAUTA_LOGS_DB_ID},
                properties={
                    "Fecha": {"date": {"start": cierre_data['fecha']}},
                    "Completadas": {"number": cierre_data['completadas']},
                    "Pendientes": {"number": cierre_data['pendientes']},
                    "Energía": {"select": {"name": cierre_data['energia']}},
                    "Notas": {"rich_text": [{"text": {"content": cierre_data['notas']}}]}
                }
            )
        except Exception as e:
            logging.error(f"Error saving to Notion: {e}")
    
    return jsonify({"success": True, ...})
```

#### Paso 1.3: Crear tabla Rueda de Vida en Notion
```
Tabla: "Rueda de Vida"
Propiedades:
  - Fecha (date)
  - Área (select) - Salud, Trabajo, Familia, Finanzas, Relaciones, Crecimiento, Diversión, Espiritualidad
  - Score (number 0-100)
  - Notas (text)
```

#### Paso 1.4: Crear endpoint /api/nauta/rueda

**Archivo**: `notion_api.py` línea 430+

```python
@app.route("/api/nauta/rueda", methods=["GET"])
def api_nauta_rueda():
    """Get Rueda de Vida scores"""
    try:
        from notion_client import Client
        notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        
        # Query última entrada de cada área
        response = notion.databases.query(
            database_id="RUEDA_DE_VIDA_DB_ID",
            filter={
                "property": "Fecha",
                "date": {"on_or_after": (datetime.now() - timedelta(days=7)).isoformat()}
            }
        )
        
        # Procesar y retornar
        rueda = {}
        for result in response["results"]:
            area = result["properties"]["Área"]["select"]["name"]
            score = result["properties"]["Score"]["number"]
            rueda[area] = score
        
        return jsonify({
            "success": True,
            "data": rueda,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

#### Paso 1.5: Modificar nauta_scheduler.py

**Archivo**: `C:\apptesteo\nauta_scheduler.py`

**Cambios en función `generate_briefing_html()`**:
- Línea 100+: Conectar a /api/tasks/top-q1 en lugar de hardcoded
- Línea 120+: Conectar a /api/tasks/today en lugar de hardcoded
- Línea 140+: Agregar /api/habits en lugar de vacío
- Línea 160+: Conectar a /api/nauta/rueda en lugar de hardcoded

**Código necesario**:
```python
def generate_briefing_html(briefing_data):
    """Generate NAUTA briefing HTML with REAL data"""
    
    # briefing_data ahora viene con datos reales:
    top_3 = briefing_data.get("top_3_tareas", [])
    tareas_hoy = briefing_data.get("tareas_hoy", [])
    habitos = briefing_data.get("habitos", [])
    rueda = briefing_data.get("rueda_vida", {})
    
    # HTML dinámico basado en datos reales
    html = f"""
    <div class="briefing">
        <h2>Top 3 Tareas Q1</h2>
        {''.join([f'<div>{t["titulo"]}</div>' for t in top_3])}
        
        <h2>Hábitos Esperados</h2>
        {''.join([f'<div>{"✅" if h["hecho"] else "❌"} {h["nombre"]}</div>' for h in habitos])}
        
        <h2>Rueda de Vida</h2>
        {rueda}
    </div>
    """
    
    return html
```

---

### FASE 2: Módulo NOTAS + Historial (IMPORTANTE)

**Objetivo**: Acceso a historial de cierres + notas  
**Duración**: ~2 horas  
**Depende de**: Fase 1

#### Paso 2.1: Agregar módulo NOTAS en sidebar

**Archivo**: `dashboard_v2.html` línea 520+

```html
<!-- Agregar en sidebar-icons-top: -->
<div class="sidebar-icon" data-module="notas">
    <span class="icon-label">NOTAS</span>
    📝
</div>
```

#### Paso 2.2: Crear HTML container NOTAS

**Archivo**: `dashboard_v2.html` línea 580+ (nuevas líneas)

```html
<!-- MÓDULO: NOTAS -->
<div class="module" id="notas-container" data-module="notas">
    <h2>📝 Mis Notas & Cierre</h2>
    
    <!-- Últimos 7 cierres -->
    <div id="cierre-historial" style="max-height: 600px; overflow-y: auto;">
        <!-- Se carga con JS -->
    </div>
</div>
```

#### Paso 2.3: Crear funciones JavaScript

**Archivo**: `dashboard_v2.html` línea 1100+

```javascript
window.loadNotasHistorial = async function() {
    const container = document.getElementById("cierre-historial");
    
    try {
        const res = await fetch('/api/nauta/cierres-historial?limit=7');
        const data = await res.json();
        
        if (data.success && data.data.length > 0) {
            let html = '';
            data.data.forEach(cierre => {
                html += `
                    <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 6px;">
                        <h3>${cierre.fecha}</h3>
                        <p>✅ ${cierre.completadas} completadas / ❌ ${cierre.pendientes} pendientes</p>
                        <p>Energía: ${cierre.energia}</p>
                        <p>Notas: ${cierre.notas}</p>
                    </div>
                `;
            });
            container.innerHTML = html;
        } else {
            container.innerHTML = '<p>No hay cierres registrados</p>';
        }
    } catch (e) {
        container.innerHTML = `<p>Error: ${e.message}</p>`;
    }
};

// Cargar al switch a NOTAS
document.addEventListener('moduleSwitch', (e) => {
    if (e.detail.module === 'notas') {
        loadNotasHistorial();
    }
});
```

#### Paso 2.4: Crear endpoint /api/nauta/cierres-historial

**Archivo**: `notion_api.py` línea 450+

```python
@app.route("/api/nauta/cierres-historial", methods=["GET"])
def api_nauta_cierres_historial():
    """Get cierre history from Notion"""
    try:
        limit = request.args.get('limit', 7, type=int)
        
        # Query NAUTA Logs desde Notion
        # Retornar últimas N entradas
        
        return jsonify({
            "success": True,
            "data": cierres_list
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

---

### FASE 3: Chat NAUTA (OPCIONAL - DESPUÉS)

**Objetivo**: Chat conversacional con IA  
**Duración**: ~2 horas  
**Depende de**: Fase 1

*(Detalles en siguiente documento si procede)*

---

## 4️⃣ ARCHIVOS A CREAR/MODIFICAR

### CREAR:

1. **Tabla Notion**: NAUTA Logs
   - Acceso: https://notion.so
   - Propiedades: Fecha, Completadas, Pendientes, Energía, Notas

2. **Tabla Notion**: Rueda de Vida
   - Acceso: https://notion.so
   - Propiedades: Fecha, Área, Score, Notas

3. **Endpoints API nuevos** en notion_api.py:
   - POST /api/nauta/save-cierre (modificar)
   - GET /api/nauta/rueda (crear)
   - GET /api/nauta/cierres-historial (crear)
   - GET /api/nauta/habitos (crear)

### MODIFICAR:

1. **notion_api.py**:
   - Línea 377: api_nauta_save_cierre() - guardar en Notion
   - Línea 430+: Agregar endpoints nuevos
   - Variables globales: NAUTA_LOGS_DB_ID, RUEDA_VIDA_DB_ID

2. **nauta_scheduler.py**:
   - Función generate_briefing_html() - usar datos reales
   - Función que genera briefing_data - conectar a APIs
   - Importaciones: fetch de APIs dentro del scheduler

3. **dashboard_v2.html**:
   - Línea 520: Agregar módulo NOTAS en sidebar
   - Línea 580: Agregar HTML container NOTAS
   - Línea 1100: Agregar funciones JavaScript
   - Modificar switchModule() para trigger loadNotasHistorial()

---

## 5️⃣ VALIDACIÓN CHECKLIST

Antes de decir "NAUTA está listo":

```
BRIEFING:
  [ ] Top 3 Q1 carga datos reales de Notion (no hardcoded)
  [ ] Tareas HOY carga datos reales (no fake)
  [ ] Hábitos muestran (no vacío)
  [ ] Rueda de Vida muestra números reales (no 60%/40%)
  [ ] Fechas son actuales (hoy)

CIERRE:
  [ ] Checkboxes cargan tareas completas de Notion
  [ ] Se puede completar el formulario
  [ ] Guardar botón funciona sin errores
  [ ] Datos aparecen en "VER ÚLTIMO CIERRE" modal

GUARDADO:
  [ ] NAUTA Logs table existe en Notion
  [ ] Cierres se guardan en Notion (no solo memoria)
  [ ] Historial visible en módulo NOTAS
  [ ] Datos persisten al reiniciar servidor

MÓDULOS:
  [ ] NOTAS módulo existe en sidebar
  [ ] Historial de últimos 7 cierres visible
  [ ] Energía tracking funciona
  [ ] Rueda de Vida datos son reales

SCHEDULER:
  [ ] 8:30 AM briefing automático funciona
  [ ] 21:30 cierre automático funciona
  [ ] Log de scheduler muestra horarios correctos

CONSOLE:
  [ ] Sin errores rojos de JavaScript
  [ ] Sin errores API (404, 500)
  [ ] Conexión Notion validada
```

---

## 6️⃣ TIMELINE ESTIMADO

```
FASE 1 (Integración Notion):
  ├─ 1.1 Crear tablas Notion         30 min
  ├─ 1.2 Modificar notion_api.py     60 min
  ├─ 1.3 Modificar nauta_scheduler   60 min
  ├─ 1.4 Testing y debugging         60 min
  └─ TOTAL:                          3.5 horas

FASE 2 (Módulo NOTAS):
  ├─ 2.1-2.4 Implementación          90 min
  ├─ Testing                         30 min
  └─ TOTAL:                          2 horas

FASE 3 (Chat OpenAI):
  ├─ Endpoint + integración          90 min
  ├─ UI Modal                        30 min
  ├─ Testing                         30 min
  └─ TOTAL:                          2.5 horas

═════════════════════════════════════════
TOTAL PARA NAUTA 100%:              ~8 horas
═════════════════════════════════════════

Recomendación: Hacer Fase 1 + Fase 2 esta sesión (~5.5h)
              Fase 3 (Chat) después si hay tiempo/interés
```

---

## 🎯 PRÓXIMOS PASOS

### Opción A: Hacer todo ahora
1. Empezamos Fase 1 inmediatamente
2. Testing y validación
3. Si funciona, empezamos Fase 2
4. Luego decidimos Fase 3 (Chat)

### Opción B: Priorizar
1. Fase 1: CRÍTICA (sin esto NAUTA no tiene sentido)
2. Fase 2: IMPORTANTE (acceso a historial)
3. Fase 3: NICE-TO-HAVE (chat está lindo pero no es bloqueador)

### Opción C: Pausar y validar
1. Revisar estos documentos
2. Validar que la arquitectura tiene sentido
3. Luego ejecutar por fases

---

## 📝 NOTAS IMPORTANTES

### Sobre Notion IDs

Para ejecutar esto necesitamos:
```
TAREAS_DB_ID = "3f0c07004c154bd4b5712141fc582815"  # ✅ Ya existe
HABITOS_DB_ID = "89c9ec16837b454c9ce98e543cc62266"  # ✅ Ya existe
NAUTA_LOGS_DB_ID = "???"  # ❌ CREAR
RUEDA_VIDA_DB_ID = "???"  # ❌ CREAR
```

Cuando se crean las tablas en Notion, copiar los IDs al código.

### Sobre OpenAI API (Fase 3)

Para el chat NAUTA necesitaremos:
```
OPENAI_API_KEY = "sk-..."
NAUTA_SYSTEM_PROMPT = """Sos NAUTA, coach automático de Roxana...
```

Esto puede esperarse hasta tener Fase 1+2 validadas.

---

**Documento creado**: 2026-04-11  
**Estado**: Listo para ejecutar  
**Siguiente paso**: Confirmar si ejecutamos ahora o primero revisamos
