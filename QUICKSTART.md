# TesteoLab - Quick Start (5 Minutes)

## 🎯 What You've Got

A complete personal operating system combining:
- **Notion** as your data source (TAREAS + HÁBITOS)
- **Python API** to fetch & organize your data
- **Dashboard** to visualize & interact with everything
- **NAUTA** AI assistant for daily briefings

## ⚡ Get Running in 3 Steps

### Step 1: Configure Notion (2 min)

1. Go to https://www.notion.com/my-integrations
2. Click "Create new integration"
3. Name it `TesteoLab`, select your workspace
4. Copy the token

Create `C:\apptesteo\.env` file:
```env
NOTION_TOKEN=secret_xxxxx_your_token_here
FLASK_PORT=5000
FLASK_ENV=development
FRONT_LANGUAGE=es
CREATIVES_LANGUAGE=es
```

5. In Notion, go to "🎯 TesteoLab TAREAS" → ⋯ menu → Connections → Add TesteoLab
6. Repeat for "📚 TesteoLab HÁBITOS"

### Step 2: Install Python Packages (1 min)

```bash
cd C:\apptesteo
pip install -r requirements.txt
```

### Step 3: Start TesteoLab (1 min)

```bash
python start_testeolab.py
```

✅ Dashboard opens automatically at http://localhost:9000

---

## 📱 What You See

### NAUTA Briefing (Default Screen)
- **Today's date & time**
- **Top 3 Q1 tasks** with priority badges
- **Quick action buttons** (✓ mark done, ✎ edit)
- **Today's task count** and Q1 pending count

### Available Modules (Click sidebar icons)
- 🧭 **NAUTA** - Daily AI assistant briefing
- 📓 **NOTION** - View all tasks
- 📊 **TRACKER** - Habit tracking (coming next sprint)
- 🔍 **M1/M2/M3/M4** - Module-specific views
- 📖 **SISTEMA** - Documentation
- ⚙️ **SETTINGS** - Configure language (Ctrl+Shift+S)

---

## 📊 Your Notion Structure

### TAREAS (Tasks)
20 properties for complete task management:
- **Status**: 7 states (Pendiente, En curso, Bloqueada, Vencida, Reprogramada, Backlog, Completada)
- **Priority**: Alta, Media, Baja
- **Quarter**: Q1, Q2, Q3, Q4
- **Category**: M1, M2, M3, M4, Framework, NAUTA, Personal
- **Type**: Deep Work, Admin, Creativo, Clase, Personal
- **Energy**: Alta, Media, Baja
- **Dates**: Fecha_programada, Fecha_vencimiento, Fecha_cierre
- **Time**: Duración_bloque, Tiempo_estimado, Tiempo_real
- **Relations**: Bloqueadores, Dependencias

### HÁBITOS (15 Habits)
Pre-loaded habits tracked daily:
- **Salud**: Gimnasio, Caminata, Pilates, Sol, Agua, Descanso
- **Crecimiento**: Lectura, Meditación, Gratitud, Imaginación, Cierre
- **Productividad**: Landing, Áreas review
- **Relaciones**: Paseo Franco

---

## 🎮 How to Use

### Add a Task
1. Go to Notion → 🎯 TesteoLab TAREAS
2. Click "New" at bottom
3. Fill in: Título, Estado, Flag_Q, Fecha_programada, Duración_bloque
4. Dashboard updates in 30 seconds

### Check Your Briefing
1. Dashboard automatically shows Top 3 Q1 tasks
2. Quick buttons to mark complete (✓) or edit (✎)
3. Notif if tasks overdue (⏰) or blocked (⊠)

### Track a Habit
1. Open Notion → 📚 TesteoLab HÁBITOS
2. Add today's completion
3. Streak counter updates automatically

### Change Settings
- Press `Ctrl+Shift+S` or click ⚙️ icon
- Choose FRONT language (UI)
- Choose CREATIVES language (generated content)
- Save

---

## 🔗 API Endpoints (For developers)

All running on `http://localhost:5000/api`:

```bash
# Get today's tasks
curl http://localhost:5000/api/tasks/today

# Get top 4 Q1 tasks
curl http://localhost:5000/api/tasks/top-q1

# Get all habits
curl http://localhost:5000/api/habits

# Get NAUTA briefing
curl http://localhost:5000/api/nauta/briefing

# Health check
curl http://localhost:5000/api/health
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` | Open Settings |
| `ESC` | Close modals |
| Click sidebar icons | Switch modules |

---

## 🔄 Timeline

Your 6-sprint plan:

| Sprint | Days | Focus |
|--------|------|-------|
| **1** ✅ | Sat-Sun | Dashboard + TAREAS + HÁBITOS (DONE) |
| **2** | Mon-Tue | Calendar sync (Notion ↔ Google) |
| **3** | Wed-Thu | Metrics + Alerts system |
| **4** | Fri-Sat | NAUTA AI automation |
| **5-6** | Sun-Tue | Mobile + Voice + Polish |

---

## 🐛 Troubleshooting

### Dashboard shows loading spinner forever
```
✓ Check API: http://localhost:5000/api/health
✓ If 404: Start notion_api.py in new terminal
✓ Check NOTION_TOKEN in .env file
✓ Verify Notion integration connected to databases
```

### Settings button not appearing
```
✓ It's in bottom-left of sidebar (⚙️)
✓ Or press Ctrl+Shift+S
✓ Refresh page if still hidden
```

### No tasks showing in briefing
```
✓ Create a task in Notion with Flag_Q = Q1
✓ Set Fecha_programada to today or later
✓ Set Estado to something other than Completada
✓ Wait 30 seconds for API refresh
✓ Check browser console (F12) for errors
```

---

## 📚 Full Documentation

For comprehensive setup, troubleshooting, and API docs:
→ See **SETUP.md** (200+ lines)

For detailed sprint progress:
→ See **STATUS_SPRINT_1.md** (300+ lines)

---

## 🎬 Next: Sprint 2

Once comfortable with the dashboard:

1. **Calendar Sync Setup** (30 min)
   - Connect Google Calendar
   - Enable auto-sync from Notion
   - View tasks in Google Calendar alongside dashboard

2. **Test Full Workflow**
   - Create task in Notion
   - See it in dashboard
   - See it in Google Calendar
   - Mark complete → updates everywhere

3. **Plan Sprint 3+**
   - Metrics system (Execution Score, Q1 Score, etc.)
   - Alert system (Q1 at risk, overload, low execution, etc.)
   - NAUTA morning briefing automation

---

## 💡 Pro Tips

**Daily Routine**:
1. Open dashboard (http://localhost:9000)
2. Check NAUTA briefing
3. Click tasks to mark complete or reschedule
4. Evening: Check 5 Objetivos Cierre habit

**Weekly Check-in**:
1. Review Rueda de Vida (8 life areas)
2. Update Q1/Q2/Q3/Q4 flags
3. Clean up BACKLOG

**Productivity Tips**:
- Use **Flag_Q = Q1** for quarterly focus
- Set **Energía = Alta** for morning (before 12:30pm)
- Use **Tipo = Deep Work** for focus blocks
- Link **Dependencias** for task sequences
- Track **Tiempo_real** vs **Tiempo_estimado** for accuracy

---

## 🚀 You're Ready!

TesteoLab is now running. Your next step:

```bash
# If stopped, restart with:
python start_testeolab.py

# Dashboard: http://localhost:9000
# API: http://localhost:5000
```

Create your first task in Notion and watch it appear in the dashboard! 🎯

---

**Questions?** Check SETUP.md or STATUS_SPRINT_1.md  
**Issues?** Look at browser console (F12) for detailed error messages  
**Ready for Sprint 2?** Let's implement Google Calendar sync! 📅
