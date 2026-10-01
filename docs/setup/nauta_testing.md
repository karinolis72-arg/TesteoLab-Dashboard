# 🧪 NAUTA TESTING - Verificación del Sistema Cronométrico

**Estado**: Listo para testing | **Fecha**: 2026-04-11 | **Responsable**: SISTEMA

---

## ✅ VERIFICACIÓN PRE-DEPLOYMENT

### 1. Dependencias Instaladas
```bash
pip install APScheduler==3.10.4 --break-system-packages
pip install -r requirements.txt --break-system-packages
```

**Verificación:**
```python
python3 -c "from apscheduler.schedulers.background import BackgroundScheduler; print('✓ APScheduler instalado')"
```

---

## 🚀 INICIAR NAUTA

### Opción 1: Testing Local (Recomendado)

```bash
cd C:\apptesteo

# Terminal 1: Inicia backend Flask + NAUTA Scheduler
python notion_api.py

# Terminal 2: Testing de endpoints
curl http://localhost:5000/api/nauta/status
curl http://localhost:5000/api/nauta/briefing
curl http://localhost:5000/api/nauta/cierre
```

### Opción 2: Testing Directo del Scheduler

```bash
cd C:\apptesteo
python nauta_scheduler.py
```

Esto ejecutará:
1. Briefing inmediatamente (8:30 AM no espera)
2. Cierre inmediatamente (21:30 no espera)
3. Continuará corriendo con el scheduler

---

## 📊 ENDPOINTS PARA TESTING

### 1. Status NAUTA
```bash
GET /api/nauta/status

Respuesta esperada:
{
  "success": true,
  "status": "enabled",
  "last_briefing": "2026-04-11T08:30:00",
  "last_cierre": "2026-04-11T21:30:00",
  "next_briefing": "08:30 AM (Buenos Aires time)",
  "next_cierre": "21:30 (Buenos Aires time)",
  "timestamp": "2026-04-11T14:25:00..."
}
```

### 2. Briefing Data (JSON)
```bash
GET /api/nauta/briefing

Respuesta esperada:
{
  "success": true,
  "data": {
    "fecha": "11 de April de 2026",
    "hora_generado": "08:30",
    "total_tareas_hoy": 3,
    "top_3_q1": [...],
    "tareas_pendientes": [...],
    "habitos_esperados": [...],
    "rueda_vida_balance": {...}
  },
  "last_generated": "2026-04-11T08:30:00",
  "timestamp": "2026-04-11T14:25:00..."
}
```

### 3. Briefing HTML
```bash
GET /api/nauta/briefing-html

Retorna: HTML renderizable directamente en navegador
```

Abre en navegador:
```
http://localhost:5000/api/nauta/briefing-html
```

### 4. Cierre Data (JSON)
```bash
GET /api/nauta/cierre

Respuesta esperada:
{
  "success": true,
  "data": {
    "fecha": "11 de April de 2026",
    "hora_cierre": "21:30",
    "completadas": 2,
    "pendientes": 2,
    "tareas_completadas": [...],
    "tareas_pendientes": [...],
    "notas": "..."
  },
  "last_generated": "2026-04-11T21:30:00",
  "timestamp": "2026-04-11T21:45:00..."
}
```

### 5. Cierre HTML
```bash
GET /api/nauta/cierre-html

Retorna: HTML renderizable directamente en navegador
```

Abre en navegador:
```
http://localhost:5000/api/nauta/cierre-html
```

---

## 🧪 TEST CASES

### Test 1: Verificar que el scheduler inicia
```python
# Archivo: test_nauta.py
from nauta_scheduler import start_scheduler, get_briefing_state, get_cierre_state

start_scheduler()
print("✓ Scheduler iniciado")

# Verificar estado
print(get_briefing_state())
print(get_cierre_state())
```

**Ejecutar:**
```bash
python test_nauta.py
```

### Test 2: Verificar endpoints API
```bash
# Terminal con Flask ejecutándose en :5000

# Status
curl http://localhost:5000/api/nauta/status | jq

# Briefing JSON
curl http://localhost:5000/api/nauta/briefing | jq

# Cierre JSON
curl http://localhost:5000/api/nauta/cierre | jq

# Briefing HTML (abre en navegador)
open http://localhost:5000/api/nauta/briefing-html

# Cierre HTML (abre en navegador)
open http://localhost:5000/api/nauta/cierre-html
```

### Test 3: Cronograma (sin esperar 8:30 AM o 21:30)
```python
# En nauta_scheduler.py, comenta las líneas del decorador @scheduler
# y ejecuta manualmente:

from nauta_scheduler import nauta_briefing_job, nauta_cierre_job

print("Ejecutando briefing...")
nauta_briefing_job()

print("Ejecutando cierre...")
nauta_cierre_job()
```

---

## 📈 MÉTRICAS A VALIDAR

### Briefing (8:30 AM)
```
✓ Se ejecuta a las 8:30 AM exactas
✓ Lee contexto de "Sobre Mí"
✓ Obtiene top 3 tareas Q1
✓ Obtiene tareas del día
✓ Obtiene hábitos
✓ Genera HTML renderizable
✓ Guarda log en Notion (próximo paso)
✓ Timestamp correcto (UTC-3)
```

### Cierre (21:30)
```
✓ Se ejecuta a las 21:30 exactas
✓ Solicita qué se completó
✓ Solicita qué falta
✓ Calcula porcentaje completado
✓ Genera HTML renderizable
✓ Guarda log en Notion (próximo paso)
✓ Timestamp correcto (UTC-3)
```

---

## 🔍 DEBUGGING

### Si el scheduler no inicia
```python
# Ver logs
tail -f /tmp/nauta_scheduler.log

# Verificar que APScheduler está instalado
python3 -c "import apscheduler; print(apscheduler.__version__)"

# Verificar que el módulo se importa
python3 -c "from nauta_scheduler import start_scheduler; print('OK')"
```

### Si los endpoints no responden
```bash
# Verificar que Flask está corriendo
curl http://localhost:5000/api/health

# Verificar que NAUTA está enabled
curl http://localhost:5000/api/nauta/status

# Ver logs de Flask
python notion_api.py  # Sin --debug para ver todos los logs
```

### Si las horas no son correctas
```bash
# Verificar timezone del sistema
date
TZ=America/Argentina/Buenos_Aires date

# Los jobs están configurados para America/Argentina/Buenos_Aires
# Si tu sistema está en otra zona horaria, los jobs se ejecutarán
# en horarios convertidos
```

---

## ✅ CHECKLIST DE VALIDACIÓN

```
□ APScheduler instalado correctamente
□ nauta_scheduler.py importa sin errores
□ notion_api.py inicia con NAUTA habilitado
□ GET /api/nauta/status retorna "enabled"
□ GET /api/nauta/briefing-html carga HTML (abre en navegador)
□ GET /api/nauta/cierre-html carga HTML (abre en navegador)
□ Los horarios mostrados son 08:30 AM y 21:30 (Buenos Aires)
□ El HTML se ve correctamente formateado
□ El HTML muestra datos de ejemplo (tareas, hábitos, rueda de vida)
□ El scheduler está corriendo en background
□ Los logs muestran "NAUTA Scheduler iniciado"
```

---

## 📱 INTEGRACIÓN CON DASHBOARD

Una vez validado el backend, integrar con dashboard_v2.html:

```html
<!-- En dashboard_v2.html -->

<div id="nauta-module">
  <h2>🤖 NAUTA Coach</h2>
  
  <div class="briefing-section">
    <button onclick="loadBriefing()">📋 Cargar Briefing (8:30 AM)</button>
    <div id="briefing-content"></div>
  </div>
  
  <div class="cierre-section">
    <button onclick="loadCierre()">📊 Cargar Log Cierre (21:30)</button>
    <div id="cierre-content"></div>
  </div>
</div>

<script>
async function loadBriefing() {
  const res = await fetch('/api/nauta/briefing-html');
  const html = await res.text();
  document.getElementById('briefing-content').innerHTML = html;
}

async function loadCierre() {
  const res = await fetch('/api/nauta/cierre-html');
  const html = await res.text();
  document.getElementById('cierre-content').innerHTML = html;
}
</script>
```

---

## 🎯 PRÓXIMOS PASOS

Una vez que NAUTA está validado:

1. ✅ Testing local (ahora)
2. ⏳ Integración con dashboard HTML
3. ⏳ Integración con Notion (guardar logs)
4. ⏳ Configurar alertas/notificaciones
5. ⏳ Deploy a Render

---

## 📌 NOTAS

- **Timezone**: America/Argentina/Buenos_Aires (UTC-3)
- **Horarios**: 8:30 AM (briefing), 21:30 (cierre)
- **Jobs**: Se ejecutan en background, no bloquean la API
- **Errores**: Se registran en logs (ver section Debugging)
- **HTML**: Se genera con inline CSS (no requiere archivos externos)

---

**Testing iniciado**: 2026-04-11  
**Próxima revisión**: Cuando hayas ejecutado todos los tests  
**Responsable**: SISTEMA + TÚ

