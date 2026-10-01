# 📅 SPRINT 2: Calendar Integration - Plan Detallado
**Versión**: 0.1 - Draft  
**Fecha**: 11 Abril 2026  
**Duración Estimada**: 48 horas (2 días)  
**Estado**: 🔵 En Planificación

---

## 🎯 OBJETIVO PRINCIPAL

Integrar **Google Calendar API** para que NAUTA importe eventos del calendario y optimice la gestión diaria automática de tareas.

**Flujo Final**:
```
Google Calendar (Eventos)
        ↓
    API Sync
        ↓
Flask Backend (notion_api.py)
        ↓
Notion (Tareas + Horarios)
        ↓
Dashboard NAUTA (Muestra eventos + tareas)
```

---

## 📋 REQUISITOS FUNCIONALES

### RF1: Lectura de Google Calendar
- [x] Usuario conecta su Google Calendar
- [x] Sistema sincroniza eventos automáticamente cada 30 min
- [x] Muestra eventos en NAUTA briefing
- [x] Detecta conflictos entre tareas y eventos

### RF2: Creación de Eventos desde Notion
- [ ] Al marcar tarea como "En curso", se crea evento en Calendar
- [ ] Al completar tarea, se cierra evento en Calendar
- [ ] Duración del evento = duracion_bloque de la tarea

### RF3: Análisis de Disponibilidad
- [ ] Calcula tiempo libre entre eventos
- [ ] Sugiere "ventanas de trabajo" óptimas
- [ ] Notifica si hay conflictos de horarios

---

## 🏗️ ARQUITECTURA TÉCNICA

### Backend (Flask - notion_api.py)

#### Nuevos Endpoints:

**1. GET /api/calendar/events**
```python
Response:
{
  "success": True,
  "data": [
    {
      "id": "google_event_id",
      "title": "Reunión Q1 Planning",
      "start": "2026-04-11T10:00:00",
      "end": "2026-04-11T11:00:00",
      "location": "Zoom",
      "description": "Q1 planning session",
      "busy": True
    }
  ]
}
```

**2. POST /api/calendar/sync**
```python
# Sincroniza Notion tareas ↔ Google Calendar
Body: {
  "sync_direction": "both|notion_to_calendar|calendar_to_notion"
}

Response: {
  "success": True,
  "synced_tasks": 5,
  "synced_events": 3,
  "conflicts": []
}
```

**3. GET /api/calendar/availability**
```python
# Retorna franjas libres en el día
Body: {
  "date": "2026-04-11",
  "min_duration_minutes": 60
}

Response: {
  "success": True,
  "data": [
    {
      "start": "09:00",
      "end": "10:30",
      "duration_minutes": 90,
      "energy_level": "Alta"  # Sugerir tareas Alta antes de 12:30
    }
  ]
}
```

**4. POST /api/calendar/create-event**
```python
Body: {
  "task_id": "notion_task_id",
  "title": "Tarea X",
  "start": "2026-04-11T14:00:00",
  "duration_minutes": 45
}

Response: {
  "success": True,
  "calendar_event_id": "google_event_id"
}
```

---

### Dependencias Python Nuevas

```txt
google-auth-oauthlib==1.0.0
google-auth-httplib2==0.2.0
google-api-python-client==2.97.0
```

---

### Frontend (dashboard_v2.html)

#### Nuevo Módulo: CALENDAR

```html
<div class="module" data-module="calendar">
  <div class="module-title">📅 CALENDAR - Eventos & Disponibilidad</div>
  
  <div id="calendar-container">
    <!-- Secciones:
         1. Google Calendar Status (conectado/no)
         2. Eventos de hoy
         3. Próximas 48 horas timeline
         4. Franjas libres (recomendaciones)
         5. Botón "Sincronizar Ahora"
    -->
  </div>
</div>
```

#### Componentes UI:

**1. Status Google Calendar**
- Verde: Conectado ✓
- Rojo: No conectado
- Botón: "Conectar Google Calendar"

**2. Timeline Eventos**
- Vista tipo agenda (hora por hora)
- Eventos en colores
- Tareas en colores diferentes
- Franjas libres en gris

**3. Recomendaciones**
```
🟢 FRANJA LIBRE: 14:00-15:30 (90 min)
   ✓ Óptimo para: Tarea Alta
   Sugerencia: "Revisar análisis Q1"
```

---

## 🔐 AUTENTICACIÓN GOOGLE

### Setup Inicial:

1. **Crear OAuth 2.0 Credentials** en Google Cloud Console
   - Application type: Web Application
   - Authorized redirect URIs: `http://localhost:5000/api/calendar/auth/callback`

2. **Guardar en .env**:
```env
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxx
GOOGLE_REDIRECT_URI=http://localhost:5000/api/calendar/auth/callback
```

3. **Flow OAuth**:
```
User Click "Conectar"
    ↓
Redirect a Google OAuth
    ↓
User da permiso
    ↓
Google → Callback a Flask
    ↓
Guardamos access_token en localStorage
    ↓
Futuras llamadas usan token
```

---

## 📊 FLUJO DE SINCRONIZACIÓN

### Sincronización Notion → Google Calendar

```
Tarea en Notion (Estado: "En curso")
    ↓
    Trigger: POST /api/calendar/create-event
    ↓
    Crea evento en Google Calendar
    ↓
    Relaciona: task_id ↔ calendar_event_id (en Notion)
    ↓
    Evento aparece en Calendar
```

### Sincronización Google Calendar → Notion

```
Evento en Google Calendar
    ↓
    Sistema detecta vía /api/calendar/sync
    ↓
    ¿Existe tarea relacionada?
    ├─ SÍ: Actualiza horario en Notion
    └─ NO: Crea "bloqueo de tiempo" (tarea tipo "Evento")
```

---

## ⚙️ CONFIGURACIÓN EN NOTION

### Nueva Propiedad en TAREAS:

```
"Calendar_Event_ID": {
  "type": "text",
  "description": "ID del evento en Google Calendar"
}
```

### Estados Sincronizados:

| Notion Estado | → | Calendar Estado |
|---|---|---|
| Pendiente | | (Sin evento) |
| En curso | → | Evento activo |
| Completada | → | Evento finalizado |

---

## 🧪 CASOS DE USO

### Caso 1: Usuario tiene evento en Calendar
```
1. Evento: "Reunión con CEO" 15:00-16:00
2. Sistema detecta → Crea "bloqueo" en Notion
3. NAUTA muestra: "⚠️ Bloqueado 15:00-16:00"
4. Sugiere tareas en franjas libres
```

### Caso 2: Usuario marca tarea como "En curso"
```
1. Tarea: "Analizar datos Q1" (45 min)
2. Usuario: Click "En curso" a las 14:00
3. Sistema: Crea evento en Calendar 14:00-14:45
4. Calendar: Muestra "Analizar datos Q1" ocupado
```

### Caso 3: Conflicto de horarios
```
1. Evento: "Reunión Imprevista" 10:00-11:00
2. Tarea: "Tarea Q1 Alta" 10:30-11:30
3. Sistema: Detecta conflicto
4. NAUTA: Notifica "⚠️ CONFLICTO: Tarea solapada con evento"
5. Sugiere: Reprogramar a franja libre 14:00-15:30
```

---

## 📅 TIMELINE SPRINT 2

### Día 1 (4 horas)
- [ ] Setup Google OAuth + credenciales
- [ ] Implementar /api/calendar/events endpoint
- [ ] Implementar /api/calendar/availability endpoint
- [ ] Testing OAuth flow

### Día 2 (4 horas)
- [ ] Implementar /api/calendar/sync endpoint
- [ ] Agregar módulo CALENDAR en dashboard
- [ ] Implementar UI de timeline y franjas libres
- [ ] Testing de sincronización bidireccional

---

## 🎨 UI MOCKUP (Dashboard)

```
[📅 CALENDAR - Eventos & Disponibilidad]

┌─ ESTADO ──────────────────────┐
│ ✅ Conectado a Google Calendar │
│ Última sync: hace 5 min        │
│ [🔄 Sincronizar Ahora]         │
└────────────────────────────────┘

┌─ EVENTOS HOY (11 Abril) ──────┐
│ 10:00-11:00  Reunión CEO      │ 🔴 Ocupado
│ 14:00-14:45  Tarea Q1 Alta    │ 🔵 Por hacer
│ 15:00-15:30  ☕ Break         │ ⚪ Otra tarea
└────────────────────────────────┘

┌─ FRANJAS LIBRES ──────────────┐
│ 🟢 11:00-14:00 (180 min)       │
│    Óptimo para: Tareas Alta    │
│    Sugerencia: "Analizar datos"│
│                                │
│ 🟢 15:30-17:00 (90 min)        │
│    Óptimo para: Tareas Media   │
│    Sugerencia: "Email follow-up"
└────────────────────────────────┘
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

### Funcionalidad:
- [x] User puede conectar Google Calendar
- [x] Eventos se sincronizan cada 30 min automáticamente
- [x] NAUTA muestra eventos + tareas integrados
- [x] Sistema detecta conflictos de horarios
- [x] Sugerencias de franjas libres correctas

### Performance:
- [x] Sync completa en < 2 segundos
- [x] API responde en < 500ms
- [x] No bloquea UI durante sync

### Confiabilidad:
- [x] Error handling si Calendar API falla
- [x] Fallback a Notion-only si sin conexión
- [x] Logging de todas las sincronizaciones

---

## 📚 REFERENCIAS & RECURSOS

- **Google Calendar API Docs**: https://developers.google.com/calendar/api
- **OAuth 2.0 Flow**: https://developers.google.com/identity/protocols/oauth2
- **Python google-api-client**: https://github.com/googleapis/google-api-python-client

---

## 💡 NOTAS ADICIONALES

1. **Consideración de Zonas Horarias**: 
   - Usar pytz para manejar múltiples zonas
   - Mostrar en zona horaria del usuario (de Notion)

2. **Rate Limiting**:
   - Google Calendar API: 1000 requests/día free tier
   - Implementar caché para evitar queries innecesarias

3. **Privacidad**:
   - No guardar eventos completos en Notion
   - Solo guardar: ID, título, horario, busy/free status

4. **Próximas Fases (Post-Sprint 2)**:
   - Integración con otras calendarios (Outlook, iCal)
   - Asistente IA que sugiera horarios basado en patrones
   - Notificaciones push antes de eventos/tareas

---

**Estado**: 🔵 Listo para comenzar  
**Próximo**: Aprobación de arquitectura + Setup de Google OAuth credentials

