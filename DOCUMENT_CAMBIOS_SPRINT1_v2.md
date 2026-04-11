# 📋 CAMBIOS IDENTIFICADOS - Sprint 1 v2.0
**Fecha**: 11 de Abril 2026  
**Estado**: Documento de cambios en revisión  
**Autor**: Claude + Karina Ordoqui  

---

## 🔴 PROBLEMAS ENCONTRADOS & SOLUCIONES

### PROBLEMA #1: Notificaciones - Lógica de Pausar/Cerrar
**Severidad**: ALTA  
**Ubicación**: `dashboard_v2.html` (líneas ~500-550)

**Comportamiento Actual**:
- ✕ (Cerrar): Cierra pero **reaparece al recargar página** ❌
- ⏸ (Pausar): No muestra opciones de periodicidad ❌

**Comportamiento Requerido**:
- ✕ (Cerrar): Cierra **PERMANENTEMENTE** (no reaparece al recargar) ✓
- ⏸ (Pausar): Muestra **dropdown con opciones**:
  - 1 minuto
  - 5 minutos
  - 15 minutos
  - 1 hora
  - 1 día
  - 1 semana
  - Pausa indefinida
No solo horas estimadas, sino:

15 / 30 / 60 / 90 min

✔ Esto permite a NAUTA  encastrar automático.
**Cambios Técnicos**:
```javascript
// Antes: Solo cierra visualmente
notification.remove()

// Después: localStorage para persistencia + dropdown de pausar
localStorage.setItem(`notification-${id}-dismissed`, true)
localStorage.setItem(`notification-${id}-paused-until`, timestamp)
```

---

### PROBLEMA #2: Settings - Falta Selector TEMA
**Severidad**: MEDIA  
**Ubicación**: `dashboard_v2.html` Settings Modal (líneas ~300-350)

**Actual**:
```html
<div class="form-group">
  <label for="lang-front">Idioma FRONT (UI)</label>
  <select id="lang-front">...</select>
</div>
<div class="form-group">
  <label for="lang-creatives">Idioma CREATIVES (Contenido)</label>
  <select id="lang-creatives">...</select>
</div>
<!-- FALTA: Selector TEMA -->
```

**Requerido**:
```html
<div class="form-group">
  <label for="theme-selector">🎨 TEMA (Diseño)</label>
  <select id="theme-selector">
    <option value="clara">CLARA - Recomendado (Blanco/Azul)</option>
    <option value="dark">DARK - Modo Oscuro (Negro/Gris)</option>
    <option value="minimal">MINIMAL - Minimalista (Gris/Blanco)</option>
    <option value="colorful">COLORFUL - Colorido (Multicolor)</option>
    <option value="energy">ENERGY - High Energy (Neon/Vibrante)</option>
  </select>
</div>
```

**Funcionalidad**:
- Guardar en localStorage: `localStorage.setItem('theme', value)`
- Aplicar CSS classes al `<body>`: `body.className = 'theme-clara'`
- Crear archivo CSS con variables para cada tema

---

### PROBLEMA #3: Panel de Preferencias - Incompleto
**Severidad**: MEDIA  
**Ubicación**: Nueva sección en Settings (después de TEMA)

**Campos a Agregar**:
```
🔔 NOTIFICACIONES
├─ [Toggle] Sonar notificaciones
├─ [Toggle] Mostrar desktop alerts
├─ [Slider] Volumen (0-100%)
└─ [Select] Tipo de sonido (Beep, Ding, Chime, Custom)

📊 DASHBOARD
├─ [Toggle] Mostrar Rueda de Vida
├─ [Toggle] Mostrar métricas en tiempo real
├─ [Select] Frecuencia refresh (30s, 1min, 5min)
└─ [Toggle] Expandir módulos por default

⌨️ ATAJOS
├─ [Text] Custom shortcut para Settings
├─ [Text] Custom shortcut para NAUTA
└─ [Button] Restaurar defaults

🤖 NAUTA AI
├─ [Toggle] Modo coach (insistente)
├─ [Toggle] Sugerencias automáticas
├─ [Select] Nivel de detalle (Breve, Normal, Completo)
└─ [Toggle] Notificar cambios en Notion
```

---

### PROBLEMA #4: NAUTA - No Lee Datos Reales de Notion
**Severidad**: CRÍTICA  
**Ubicación**: `dashboard_v2.html` función `loadNautuaBriefing()` (líneas ~800-900)

**Problema Actual**:
```javascript
// Carga el HTML pero no pide datos al API
container.innerHTML = `
    <div class="nauta-briefing">
        <div class="nauta-greeting">
            Hola Roxana 👋
            ...
            // HARDCODED - No trae datos reales
```

**Requerido**:
```javascript
async function loadNautuaBriefing() {
    // 1. Fetch datos del API
    const result = await apiCall("/nauta/briefing")
    
    // 2. Si éxito:
    // - Mostrar Top 3 Q1 tasks CON DATOS REALES
    // - Mostrar count de tareas HOY
    // - Mostrar hábitos esperados de HÁBITOS DB
    // - Mostrar Rueda de Vida si existe
    
    // 3. Si falla:
    // - Mostrar error amigable
    // - Ofrecimiento de retry
}
```

**Datos que NAUTA debe mostrar**:
- ✅ Top 3 Q1 tareas (de TAREAS con Flag_Q=Q1)
- ✅ Tareas para hoy (de TAREAS con Fecha_programada=hoy)
- ✅ Hábitos esperados (de HÁBITOS para hoy)
- ✅ Rueda de Vida (8 áreas)
- ✅ Próxima ejecución (siguiente tarea)
- ✅ Métrica Q1 Score (X% completado)

---

### PROBLEMA #5: Conectar Calendar para que NAUTA lo lea
**Severidad**: ALTA (SPRINT 2 pero necesita preparación)  
**Ubicación**: `notion_api.py` + Calendar API integration

**Requiere**:
- [ ] Google Calendar API authentication
- [ ] Sincronización bidireccional (Notion ↔ Calendar)
- [ ] NAUTA leyendo eventos del calendar como tareas
- [ ] Actualizar `/api/nauta/briefing` con datos del calendar

**Conexión necesaria**:
```python
# En notion_api.py
def get_calendar_events(date):
    # Conectar a Google Calendar API
    # Filtrar por fecha
    # Retornar lista de eventos
    
def get_nauta_briefing():
    # Combinar:
    # - Top Q1 de TAREAS
    # - Tareas de hoy
    # - HÁBITOS esperados
    # - EVENTOS del calendar  ← NUEVO
```

---

## 📝 CAMBIOS DE DOCUMENTACIÓN NECESARIOS

### PDF `TesteoLab_Sistema_Completo_v1.0.pdf`
Actualizar secciones:

1. **Arquitectura del Sistema**
   - Agregar Calendar como nueva capa
   - Mostrar flujo: Notion → API → Calendar ↔ Dashboard

2. **Módulos del Dashboard**
   - NAUTA: Actualizar con datos reales en briefing
   - TRACKER: Documentar las 15 hábitos
   - Agregar módulo CALENDAR

3. **Settings & Preferencias**
   - Documentar TEMA selector
   - Panel de Preferencias completo
   - Atajos de teclado customizables

4. **Notificaciones**
   - Pausar con opciones de periodicidad
   - Cerrar permanente vs temporal
   - Persistencia con localStorage

5. **Sprint 2 Roadmap**
   - Calendar integration en detalle
   - Sincronización Notion ↔ Calendar
   - NAUTA leyendo ambas fuentes

---

## ✅ CAMBIOS CONFIRMADOS (Ya en código)

### Dashboard v2
- ✅ 8 módulos en sidebar
- ✅ NAUTA module con estructura
- ✅ Settings modal con idiomas
- ✅ Conectado a API backend
- ✅ Notificaciones toast
- ✅ Responsive design
- ✅ Keyboard shortcuts (Ctrl+Shift+S, ESC)

### Backend
- ✅ 7 endpoints funcionando
- ✅ Notion API integration
- ✅ TAREAS database queries
- ✅ HÁBITOS database queries
- ✅ NAUTA briefing endpoint (estructura)

---

## 🎯 PENDIENTE DE CÓDIGO

| ID | Función | Prioridad | Archivos |
|-----|---------|-----------|----------|
| #1 | Pausar notificaciones con dropdown | ALTA | dashboard_v2.html |
| #2 | Cerrar notificaciones permanente | ALTA | dashboard_v2.html |
| #3 | Agregar TEMA selector | MEDIA | dashboard_v2.html |
| #4 | Panel de preferencias | MEDIA | dashboard_v2.html |
| #5 | NAUTA leyendo datos reales | CRÍTICA | dashboard_v2.html |
| #6 | Calendar API setup | ALTA | notion_api.py |

---

## 💡 DUDAS/DECISIONES PENDIENTES

### ¿TEMA por defecto?
**Opciones**:
- [X ] CLARA (Recomendado - lo que ves ahora)
- [ ] DARK (Oscuro para noches)
- [ ] MINIMAL (Limpio)

**Decisión**: CLARA es default, user puede cambiar

### ¿Pausar notificaciones - guardar en?
**Opciones**:
- [X ] localStorage (no persiste entre navegadores)
- [X ] Base de datos Notion
- [ ] Backend (notion_api.py)

**Recomendación**: localStorage + opción de sincronizar a Notion

### ¿Rueda de Vida - cómo se calcula?
**Opciones**:
- [ ] Manual (user ingresa score)
- [ ] Automático (basado en hábitos completados)
- [X ] Hybrid (user puede editar, sugerencia automática)

**Recomendación**: Hybrid

### ¿Calendar - qué información mostrar en NAUTA?
**Opciones**:
- [ ] Solo eventos de TesteoLab (sincronizados desde Notion)
- [ X] Todos los eventos del calendar
- [X ] Filtrados por tipo/categoría

**Recomendación**: Solo eventos de TesteoLab

---

## 📊 LÍNEA DE TIEMPO

**Ahora (antes de 2hrs)**: 
- [ ] Tú revisas este documento
- [ ] Agregás comentarios
- [ ] Me decís qué arreglos hacer primero

**Próximas 2 horas**:
- [ ] Arreglo #1: Notificaciones (pausar + cerrar)
- [ ] Arreglo #5: NAUTA leyendo datos reales
- [ ] Arreglo #3: TEMA selector

**Después de tú revisar**:
- [ ] Arreglos restantes
- [ ] Actualizar PDF documentación
- [ ] Testing

---

## 🔗 REFERENCIAS

**Archivos involucrados**:
- `C:\apptesteo\dashboard_v2.html` - Frontend
- `C:\apptesteo\notion_api.py` - Backend
- `C:\apptesteo\Documentos\TesteoLab_Sistema_Completo_v1.0.pdf` - Docs

**Tareas en Notion** que necesito:
- Ver estructura actual de TAREAS
- Ver estructura actual de HÁBITOS
- Confirmar campos disponibles para Rueda de Vida

---

**Estado**: ⏳ Esperando revisión de usuario
