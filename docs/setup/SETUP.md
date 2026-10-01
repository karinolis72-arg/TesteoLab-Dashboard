# TesteoLab Control Center - Setup Guide

## ⚙️ System Architecture

TesteoLab is built on a modern architecture:

```
┌─────────────────┐
│  Dashboard UI   │ (browser: localhost:9000)
│  (HTML/JS)      │
└────────┬────────┘
         │
         │ HTTP Requests
         ↓
┌─────────────────────────┐
│  Notion API Backend     │ (Flask: localhost:5000)
│  - Data fetching        │
│  - Aggregation          │
│  - Real-time sync       │
└────────┬────────────────┘
         │
         │ Notion API
         ↓
┌─────────────────────────┐
│  Notion Workspace       │
│  - TAREAS DB            │
│  - HÁBITOS DB           │
│  - Other databases      │
└─────────────────────────┘
```

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Notion account with workspace access
- Modern web browser

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
cd C:\apptesteo
pip install -r requirements.txt
```

### 2. Configure Notion Integration

1. Go to: https://www.notion.com/my-integrations
2. Click "Create new integration"
3. Name it: `TesteoLab`
4. Select your workspace
5. Click "Submit"
6. Copy the "Internal Integration Token"
7. Create `.env` file in C:\apptesteo with:

```env
NOTION_TOKEN=your_token_here
FLASK_PORT=5000
FLASK_ENV=development
FRONT_LANGUAGE=es
CREATIVES_LANGUAGE=es
```

### 3. Share Notion Databases with Integration

1. In Notion, go to "🎯 TesteoLab TAREAS" database
2. Click the "⋯" menu (top right)
3. Select "Connections"
4. Search for your "TesteoLab" integration
5. Click to connect
6. Repeat for "📚 TesteoLab HÁBITOS" database

### 4. Start TesteoLab

**Option A: Using startup script (recommended)**

```bash
python start_testeolab.py
```

This will:
- Check dependencies
- Verify Notion configuration
- Start API backend (port 5000)
- Start Dashboard (port 9000)
- Auto-open browser

**Option B: Manual startup**

Terminal 1 - API Backend:
```bash
python notion_api.py
```

Terminal 2 - Dashboard:
```bash
python run_dashboard.py
```

Then open browser to: http://localhost:9000

## 📚 Notion Database Structure

### TAREAS Database

**Purpose**: Central task management with 7 states

**Properties**:
- `Título` (Title) - Task name
- `Estado` (Select) - ◯ Pendiente, ◔ En curso, ⊠ Bloqueada, ⏰ Vencida, ↻ Reprogramada, ∞ Backlog, ✓ Completada
- `Prioridad` (Select) - Alta, Media, Baja
- `Flag_Q` (Select) - Q1, Q2, Q3, Q4
- `Categoría` (Select) - M1, M2, M3, M4, Framework, NAUTA, Personal
- `Tipo` (Select) - Deep Work, Admin, Creativo, Clase, Personal
- `Energía` (Select) - Alta, Media, Baja
- `Fecha_programada` (Date) - When to execute
- `Fecha_vencimiento` (Date) - Deadline
- `Duración_bloque` (Number) - Minutes needed
- `Tiempo_estimado` (Number) - Estimated hours
- `Tiempo_real` (Number) - Actual hours spent
- `Asignado` (Select) - Usuario, NAUTA
- `Origen` (Select) - NanoPlan, Manual, Automatización
- `Bloqueadores` (Text) - What's blocking this task
- `Notas` (Text) - Additional notes

**Views**:
- `📅 HOY` - Today's tasks (Fecha_programada = today)
- `🔥 BACKLOG` - All backlog items
- `⚠️ REPROGRAMADAS` - Rescheduled tasks
- `🚨 BLOQUEADAS` - Blocked tasks
- `🎯 Q1 FOCO` - Q1 tasks (focus/priority)

### HÁBITOS Database

**Purpose**: Track 15 daily/weekly habits

**Properties**:
- `Nombre` (Title) - Habit name with emoji
- `Frecuencia` (Select) - Diario, Lun-Vie, Sab-Dom, Mar-Jue, Personalizado
- `Horario_ideal` (Text) - Suggested time
- `Métrica` (Select) - Sí/No or Cantidad
- `Meta` (Text) - Target (e.g., "8000 pasos")
- `Categoría` (Select) - Salud, Crec.Personal, Productividad, Relaciones
- `Energía` (Select) - Alta, Media, Baja
- `Prioridad` (Select) - Alta, Media, Baja
- `Origen` (Select) - Manual, Automatización
- `Streak` (Number) - Current consecutive days

**15 Pre-loaded Habits**:
1. 💪 Gimnasio (Lun-Vie)
2. 🚶 Caminata 8000 pasos (Sab-Dom)
3. 🧘 Pilates (Mar-Jue)
4. ☀️ 15min Sol (Diario)
5. 💧 2.5L Agua (Diario)
6. 😴 Descanso Horario (Diario)
7. 📖 Lectura 10pág (Diario)
8. 🧠 Meditación 10-15min (Diario)
9. 🙏 Agradecer+Metas (Diario)
10. 🎯 Imaginar Vida (Diario)
11. 5️⃣ 5 Objetivos Cierre (Diario)
12. 🍎 Comer Fruta (Diario)
13. 🚀 Accionar Landing (Lun-Vie)
14. 📊 Repasar Áreas (Diario)
15. 👯 Paseo Franco 3x (Personalizado)

## 🔌 API Endpoints

### Tasks Endpoints

```bash
# Get top 4 Q1 tasks
GET /api/tasks/top-q1

# Get today's tasks
GET /api/tasks/today

# Get all tasks with optional filters
GET /api/tasks?flag_q=Q1&estado=Pendiente&fecha_programada=2026-04-11
```

### Habits Endpoints

```bash
# Get all habits
GET /api/habits
```

### NAUTA Briefing

```bash
# Get morning briefing data
GET /api/nauta/briefing
```

Response includes:
- Top 3 Q1 tasks
- Today's tasks
- Expected habits
- Statistics

## 🎨 Dashboard Modules

### 🧭 NAUTA (Active Module)
AI assistant for daily planning
- Morning briefing (07:00)
- Top Q1 tasks display
- Quick task actions
- Evening closing (21:00)

### 📓 NOTION
Direct Notion database view
- All tasks with filters
- Status management
- Drag-to-prioritize

### 📊 TRACKER
Habit tracking interface
- Daily/weekly tracker
- Streak visualization
- Category breakdowns
- Rueda de Vida (wheel of life)

### 🔍 M1, 🛠️ M2, 📈 M3, ⚡ M4
Module-specific views for each project area

### 📖 SISTEMA
System documentation and guidelines

### ⚙️ SETTINGS
Configuration panel
- FRONT language (ES/EN/PT-BR/IT)
- CREATIVES language
- Theme preferences
- API configuration

## ⌨️ Keyboard Shortcuts

- `Ctrl+Shift+S` - Open Settings
- `ESC` - Close modals
- `1-8` - Quick module switch (future)

## 📊 Next Steps (Sprint 1-6)

### Sprint 1 (Sat-Sun): Dashboard + NAUTA
- ✅ Create TAREAS database
- ✅ Create HÁBITOS database
- ✅ Build API backend
- ✅ Create v2 dashboard
- [ ] Test end-to-end flow

### Sprint 2 (Mon-Tue): Calendar Integration
- [ ] Implement Notion → Google Calendar sync
- [ ] Auto-schedule tasks
- [ ] Calendar event updates

### Sprint 3 (Wed-Thu): Automation + Analytics
- [ ] Build metrics system (7 metrics)
- [ ] Implement alert system (7 alerts)
- [ ] NAUTA automation engine

### Sprint 4-6: Advanced Features
- [ ] Habit tracking with daily checkins
- [ ] Rueda de Vida visualization
- [ ] Voice/microphone commands
- [ ] Mobile responsive optimization
- [ ] Offline support

## 🐛 Troubleshooting

### Error: "NOTION_TOKEN not set"
```
→ Check .env file has NOTION_TOKEN
→ Verify token format (should start with "secret_")
→ Re-create integration if token is invalid
```

### Error: "Database not found"
```
→ Verify databases exist in Notion
→ Check integration is connected to databases
→ Confirm database IDs in code match Notion
```

### Error: "CORS error" or "Cannot fetch"
```
→ Verify both servers running (API + Dashboard)
→ Check ports: 5000 (API), 9000 (Dashboard)
→ Clear browser cache
→ Check browser console for detailed errors
```

### Dashboard won't load data
```
→ Check API is running: http://localhost:5000/api/health
→ Check Notion integration permissions
→ Look at browser console (F12) for errors
→ Check network tab to see API calls
```

## 📞 Support

For issues or questions:
1. Check the SISTEMA module in dashboard
2. Review Notion database structure
3. Check API logs (terminal where notion_api.py runs)
4. Verify Notion integration permissions

## 📝 Notes

- **Data Source of Truth**: Notion TAREAS database
- **Execution Layer**: Google Calendar (tasks with date + duration)
- **Daily Interface**: Dashboard (localhost:9000)
- **Jornada Start**: 06:00 AM local time
- **Sprint Duration**: 2 days
- **Total Timeline**: 6 sprints (~12 days)
