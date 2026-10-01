# 🔧 LISTA DE ARREGLOS DE CÓDIGO - Sprint 1 v2

**Archivo Principal**: `dashboard_v2.html`  
**Archivo Secundario**: `notion_api.py`  

---

## ✨ ARREGLO #1: NOTIFICACIONES - Pausar con Opciones 
**Prioridad**: 🔴 ALTA  
**Esfuerzo**: 1-2 horas  
**Archivos**: `dashboard_v2.html`

### ¿Qué hacer?
Cambiar el botón ⏸ para que muestre un **dropdown con opciones de pausar**

### Cambios Específicos:

#### 1. Actualizar HTML de notificación
**Ubicación**: Función `showNotification()` alrededor de línea 520

**Cambiar esto**:
```html
<div class="notification-close">✕</div>
```

**Por esto**:
```html
<div class="notification-actions">
  <button class="notification-pause-btn" data-id="${Date.now()}">⏸</button>
  <button class="notification-close-btn">✕</button>
</div>
<div class="notification-pause-menu" style="display: none;">
  <div class="pause-option" data-minutes="1">1 min</div>
  <div class="pause-option" data-minutes="5">5 min</div>
  <div class="pause-option" data-minutes="15">15 min</div>
  <div class="pause-option" data-hours="1">1 hora</div>
  <div class="pause-option" data-days="1">1 día</div>
  <div class="pause-option" data-weeks="1">1 semana</div>
  <div class="pause-option" data-indefinite="true">Pausa indefinida</div>
</div>
```

#### 2. Agregar CSS para el dropdown
**Ubicación**: Sección `<style>` alrededor de línea 400

```css
.notification-pause-menu {
  position: absolute;
  top: 40px;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  min-width: 120px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 10;
}

.pause-option {
  padding: 10px 15px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s;
}

.pause-option:hover {
  background: #f5f5f5;
}

.notification-actions {
  display: flex;
  gap: 5px;
}

.notification-pause-btn,
.notification-close-btn {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.notification-pause-btn:hover {
  background: #667eea;
  color: white;
}

.notification-close-btn:hover {
  background: #f44336;
  color: white;
}
```

#### 3. Agregar JavaScript para lógica de pausar
**Ubicación**: Sección `<script>` alrededor de línea 900, dentro de `showNotification()`

```javascript
// AGREGAR esto DESPUÉS de crear la notificación:

const pauseBtn = notification.querySelector('.notification-pause-btn');
const closeBtn = notification.querySelector('.notification-close-btn');
const pauseMenu = notification.querySelector('.notification-pause-menu');
const notificationId = `notification-${Date.now()}`;

// Toggle pause menu
pauseBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  pauseMenu.style.display = 
    pauseMenu.style.display === 'none' ? 'block' : 'none';
});

// Handle pause options
notification.querySelectorAll('.pause-option').forEach(option => {
  option.addEventListener('click', () => {
    const minutes = option.dataset.minutes || 0;
    const hours = option.dataset.hours || 0;
    const days = option.dataset.days || 0;
    const weeks = option.dataset.weeks || 0;
    const indefinite = option.dataset.indefinite === 'true';

    // Calcular tiempo de pausa
    let pauseUntil = Date.now();
    if (indefinite) {
      pauseUntil = 'indefinite';
    } else {
      const totalMs = 
        (parseInt(minutes) * 60 * 1000) +
        (parseInt(hours) * 60 * 60 * 1000) +
        (parseInt(days) * 24 * 60 * 60 * 1000) +
        (parseInt(weeks) * 7 * 24 * 60 * 60 * 1000);
      pauseUntil = Date.now() + totalMs;
    }

    // Guardar en localStorage
    localStorage.setItem(`${notificationId}-paused-until`, pauseUntil);
    
    // Cerrar visualmente
    notification.style.opacity = '0.5';
    notification.style.pointerEvents = 'none';
    pauseBtn.textContent = '⏱️'; // Cambiar icono
    pauseMenu.style.display = 'none';

    showNotification(`⏸ Notificación pausada`, 'info');
  });
});

// Cerrar PERMANENTEMENTE
closeBtn.addEventListener('click', () => {
  localStorage.setItem(`${notificationId}-dismissed`, 'true');
  notification.style.opacity = '0';
  setTimeout(() => notification.remove(), 300);
});
```

---

## ✨ ARREGLO #2: NOTIFICACIONES - Cerrar Permanente
**Prioridad**: 🔴 ALTA  
**Esfuerzo**: 30 minutos  
**Archivos**: `dashboard_v2.html`

### ¿Qué hacer?
Cuando usuario hace click en ✕, guardar en localStorage para que NO reaparezca al recargar

### Cambios Específicos:

**Ubicación**: Función `showNotification()` alrededor de línea 520

```javascript
// ACTUALIZAR el manejador de close:

// Opción A: Si usas closeBtn (recomendado)
closeBtn.addEventListener('click', () => {
  // Guardar en localStorage que fue cerrada
  const notificationId = `notification-${Date.now()}`;
  localStorage.setItem(`${notificationId}-dismissed`, 'true');
  
  // Animar y remover
  notification.style.opacity = '0';
  notification.style.transform = 'translateX(400px)';
  setTimeout(() => notification.remove(), 300);
});

// Opción B: Si mantienes la antigua estructura
notification.querySelector(".notification-close").addEventListener("click", () => {
  const id = Date.now();
  localStorage.setItem(`notification-${id}-dismissed`, 'true');
  notification.remove();
});
```

**Agregar verificación al mostrar notificaciones**:

```javascript
// ANTES de crear nueva notificación, verificar:
function shouldShowNotification(type, message) {
  const hash = `${type}-${message}`.replace(/\s/g, '');
  const isDismissed = localStorage.getItem(`notification-${hash}-dismissed`);
  return !isDismissed; // true = mostrar, false = saltar
}

// EN showNotification(), al inicio:
if (!shouldShowNotification(type, message)) {
  return; // No mostrar si fue cerrada antes
}
```

---

## ✨ ARREGLO #3: Settings - Agregar TEMA Selector
**Prioridad**: 🟡 MEDIA  
**Esfuerzo**: 1.5 horas  
**Archivos**: `dashboard_v2.html`

### ¿Qué hacer?
Agregar dropdown para elegir tema (CLARA, DARK, MINIMAL, COLORFUL, ENERGY)

### Cambios Específicos:

#### 1. Actualizar HTML del Settings Modal
**Ubicación**: Settings Modal alrededor de línea 300

**Agregar esto DESPUÉS del campo de idioma CREATIVES**:

```html
<div class="form-group">
  <label for="theme-selector">🎨 TEMA (Diseño)</label>
  <select id="theme-selector">
    <option value="clara">CLARA - Recomendado (Blanco/Azul)</option>
    <option value="dark">DARK - Modo Oscuro (Negro/Gris)</option>
    <option value="minimal">MINIMAL - Minimalista (Gris/Blanco)</option>
    <option value="colorful">COLORFUL - Colorido (Multicolor)</option>
    <option value="energy">ENERGY - High Energy (Neon)</option>
  </select>
</div>
```

#### 2. Agregar CSS para cada tema
**Ubicación**: Sección `<style>` al final alrededor de línea 400

```css
/* TEMA: CLARA (Default) */
body.theme-clara {
  --primary: #667eea;
  --secondary: #764ba2;
  --background: #ffffff;
  --sidebar: #1E4682;
  --text: #333;
  --accent: #FFD700;
}

/* TEMA: DARK */
body.theme-dark {
  --primary: #667eea;
  --secondary: #764ba2;
  --background: #1a1a1a;
  --sidebar: #0d0d0d;
  --text: #e0e0e0;
  --accent: #FFD700;
  filter: invert(0.95);
}

/* TEMA: MINIMAL */
body.theme-minimal {
  --primary: #666666;
  --secondary: #999999;
  --background: #f5f5f5;
  --sidebar: #333333;
  --text: #333;
  --accent: #000000;
}

/* TEMA: COLORFUL */
body.theme-colorful {
  --primary: #FF6B6B;
  --secondary: #4ECDC4;
  --background: #FFF8F3;
  --sidebar: #2D3436;
  --text: #2D3436;
  --accent: #FFE66D;
}

/* TEMA: ENERGY */
body.theme-energy {
  --primary: #00FF41;
  --secondary: #FF006E;
  --background: #0a0e27;
  --sidebar: #0d0a14;
  --text: #00FF41;
  --accent: #FF006E;
  font-weight: bold;
}

/* Aplicar variables a elementos */
body {
  background: var(--background);
  color: var(--text);
}

.sidebar {
  background: var(--sidebar);
}

.sidebar-icon.active {
  border-color: var(--accent);
}

/* etc... */
```

#### 3. Agregar JavaScript para cambiar tema
**Ubicación**: Función `loadLanguageSettings()` alrededor de línea 920

**Reemplazar con**:

```javascript
function loadThemeAndLanguageSettings() {
  // Cargar tema
  const theme = localStorage.getItem("theme") || "clara";
  document.getElementById("theme-selector").value = theme;
  document.body.className = `theme-${theme}`;

  // Cargar idiomas
  const frontLang = localStorage.getItem("lang-front") || "es";
  const creativesLang = localStorage.getItem("lang-creatives") || "es";
  document.getElementById("lang-front").value = frontLang;
  document.getElementById("lang-creatives").value = creativesLang;
}

function saveSettings() {
  const theme = document.getElementById("theme-selector").value;
  const frontLang = document.getElementById("lang-front").value;
  const creativesLang = document.getElementById("lang-creatives").value;

  localStorage.setItem("theme", theme);
  localStorage.setItem("lang-front", frontLang);
  localStorage.setItem("lang-creatives", creativesLang);

  // Aplicar tema inmediatamente
  document.body.className = `theme-${theme}`;

  showNotification("Configuración guardada ✓", "success");
  document.getElementById("settings-modal").classList.remove("active");
}
```

**Cambiar el call inicial de** `loadLanguageSettings()` **a** `loadThemeAndLanguageSettings()`

---

## ✨ ARREGLO #5: NAUTA - Leer Datos Reales de Notion
**Prioridad**: 🔴 CRÍTICA  
**Esfuerzo**: 2-3 horas  
**Archivos**: `dashboard_v2.html` + `notion_api.py`

### ¿Qué hacer?
NAUTA debe mostrar datos REALES del API en lugar de estar hardcoded

### Cambios Específicos:

#### En `dashboard_v2.html`:

**Reemplazar TODA la función `loadNautuaBriefing()`** (líneas ~800-900) con:

```javascript
async function loadNautuaBriefing() {
  const container = document.getElementById("nauta-container");
  
  try {
    // 1. Fetch del briefing del API
    const result = await apiCall("/nauta/briefing");

    if (!result.success || !result.data) {
      container.innerHTML = '<p style="color: #999; text-align: center;">Error cargando briefing. Revisa la conexión al API.</p>';
      return;
    }

    const data = result.data;
    const now = new Date().toLocaleTimeString("es-ES", { 
      hour: "2-digit", 
      minute: "2-digit" 
    });

    let html = `
      <div class="nauta-briefing">
        <div class="nauta-greeting">
          Hola Roxana 👋<br>
          <small style="font-size: 14px; color: #888; font-weight: 400;">
            HOY ${data.fecha} • ${now}
          </small>
        </div>

        <div style="margin-bottom: 25px;">
          <h3 style="color: #667eea; font-size: 14px; font-weight: 600; margin-bottom: 15px;">
            🎯 TOP 3 TAREAS Q1
          </h3>
    `;

    // 2. Mostrar Top 3 Q1
    if (data.top_3_tareas && data.top_3_tareas.length > 0) {
      data.top_3_tareas.forEach((task, idx) => {
        const estilo_color = 
          task.prioridad === "Alta" ? "badge-alta" :
          task.prioridad === "Media" ? "badge-media" : "badge-baja";

        html += `
          <div class="task-card">
            <div class="task-info">
              <div class="task-title">${idx + 1}. ${task.titulo}</div>
              <div class="task-meta">
                <span class="task-badge ${estilo_color}">${task.prioridad}</span>
                <span class="task-badge" style="background: #f0f0f0; color: #666;">
                  ${task.categoria || "—"}
                </span>
                ${task.duracion_bloque ? 
                  `<span class="task-badge" style="background: #e3f2fd; color: #1976d2;">
                    ${task.duracion_bloque}min
                  </span>` : ''}
              </div>
            </div>
            <div class="task-actions">
              <button class="btn-small" title="Marcar completada">✓</button>
              <button class="btn-small" title="Editar">✎</button>
            </div>
          </div>
        `;
      });
    } else {
      html += '<p style="color: #999; text-align: center; padding: 20px;">No hay tareas Q1 pendientes</p>';
    }

    html += `
        </div>

        <div style="margin-bottom: 25px;">
          <h3 style="color: #667eea; font-size: 14px; font-weight: 600; margin-bottom: 10px;">
            📋 TAREAS HOY (${data.tareas_hoy.length})
          </h3>
          <p style="color: #888; font-size: 12px; margin-bottom: 10px;">
            ${data.q1_pendientes} Q1 pendientes • ${data.total_tareas_dia} total
          </p>
          
          ${data.tareas_hoy && data.tareas_hoy.length > 0 ? `
            <div style="max-height: 200px; overflow-y: auto;">
              ${data.tareas_hoy.slice(0, 5).map((task, idx) => `
                <div class="task-card" style="margin-bottom: 10px; font-size: 12px;">
                  <div class="task-info">
                    <div class="task-title">${task.titulo}</div>
                    <div class="task-meta">${task.tipo} • ${task.categoria}</div>
                  </div>
                </div>
              `).join('')}
              ${data.tareas_hoy.length > 5 ? 
                `<p style="color: #999; text-align: center; font-size: 11px;">
                  +${data.tareas_hoy.length - 5} más
                </p>` : ''}
            </div>
          ` : `
            <p style="color: #999; text-align: center; padding: 10px;">
              No hay tareas programadas hoy
            </p>
          `}
        </div>

        <div style="margin-top: 20px;">
          <button class="btn-small" style="width: auto; padding: 10px 16px; background: #667eea; color: white; border: none;">
            📞 Llamar NAUTA Ahora
          </button>
          <button class="btn-small" style="width: auto; padding: 10px 16px; margin-left: 10px; background: white; color: #667eea;">
            📋 Ver Log Cierres
          </button>
        </div>
      </div>
    `;

    container.innerHTML = html;

    // 3. Event listeners para botones
    container.querySelectorAll('.btn-small').forEach(btn => {
      btn.addEventListener('click', handleTaskAction);
    });

  } catch (error) {
    console.error('Error en NAUTA:', error);
    container.innerHTML = '<p style="color: #f44336; text-align: center;">Error cargando NAUTA briefing</p>';
  }
}

function handleTaskAction(e) {
  const action = e.currentTarget.textContent.trim();
  if (action === '✓') {
    showNotification('Tarea marcada como completada ✓', 'success');
  } else if (action === '✎') {
    showNotification('Función de edición en desarrollo', 'info');
  }
}
```

#### En `notion_api.py`:

**Actualizar la función `/api/nauta/briefing`** (líneas ~180-220) para que retorne datos completos:

```python
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
```

---

## 📋 RESUMEN DE CAMBIOS

| # | Función | Lineas HTML | Lineas JS | Lineas CSS | Lineas Python | Total |
|----|---------|------------|-----------|-----------|---------------|-------|
| 1 | Pausar notificaciones | 20 | 80 | 40 | - | 140 |
| 2 | Cerrar permanente | - | 30 | - | - | 30 |
| 3 | TEMA selector | 15 | 50 | 80 | - | 145 |
| 5 | NAUTA datos reales | 100 | 150 | - | 50 | 300 |
| **TOTAL** | | **135** | **310** | **120** | **50** | **615** |

---

## 🎯 ORDEN RECOMENDADO

**Si tienes 2-3 horas**:
1. Arreglo #5 (NAUTA) - CRÍTICO
2. Arreglo #1 (Pausar notificaciones)
3. Arreglo #2 (Cerrar permanente)

**Si tienes 3-4 horas**:
1. Arreglo #5 (NAUTA)
2. Arreglo #1 (Pausar)
3. Arreglo #2 (Cerrar)
4. Arreglo #3 (TEMA)

**Si tienes <2 horas**:
- Solo Arreglo #5 (NAUTA) - lo más crítico

---

## ✅ TESTING CHECKLIST

Después de cada arreglo, verificar:

**Arreglo #1 (Pausar)**:
- [ ] Click en ⏸ muestra dropdown
- [ ] Seleccionar opción pausa la notificación
- [ ] Icono cambia a ⏱️
- [ ] Permanece pausada al recargar página

**Arreglo #2 (Cerrar)**:
- [ ] Click en ✕ cierra notificación
- [ ] NO reaparece al F5 (refresh)
- [ ] localStorage guarda dismissed state

**Arreglo #3 (TEMA)**:
- [ ] Dropdown muestra 5 opciones
- [ ] Cambiar tema aplica CSS inmediatamente
- [ ] Se guarda en localStorage
- [ ] Persiste al recargar

**Arreglo #5 (NAUTA)**:
- [ ] Muestra Top 3 Q1 CON datos reales
- [ ] Muestra tareas de hoy con datos reales
- [ ] Muestra counts correctos
- [ ] API conectado (revisar console)
- [ ] Si API falla, muestra error amigable

---

**Estado**: ⏳ Esperando revisión y aprobación de qué arreglos hacer
