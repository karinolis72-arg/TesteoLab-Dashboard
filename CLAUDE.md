# TesteoLab — CLAUDE.md

## Stack
- **Backend**: Python/Flask (`notion_api.py`) — API REST en puerto 5000
- **Scheduler**: APScheduler (`nauta_scheduler.py`) — 8:30 AM briefing / 21:30 cierre
- **Frontend**: HTML/JS (`dashboard_v2.html`) — Dashboard en puerto 9000
- **Datos**: Notion (TAREAS + HÁBITOS + NAUTA Logs + Rueda de Vida)
- **Deploy**: Render (`Procfile` + gunicorn)

## Estructura del proyecto
```
apptesteo/
├── notion_api.py          ← Flask app principal (no mover, Render lo busca acá)
├── nauta_scheduler.py     ← Scheduler APScheduler (importado por notion_api)
├── dashboard_v2.html      ← Frontend servido por Flask en GET /
├── dashboard.html         ← Versión anterior (deprecada)
├── start_testeolab.py     ← Inicio local (levanta Flask + servidor estático)
├── run_dashboard.py       ← Servidor estático solo (puerto 9000)
├── Procfile               ← gunicorn web: para Render
├── requirements.txt
├── runtime.txt
├── .env                   ← Variables de entorno (NO en git)
│
├── tests/
│   └── test_nauta_endpoints.py    ← python tests/test_nauta_endpoints.py
│
├── scripts/
│   ├── setup_nauta_tables.py      ← Crea tablas NAUTA Logs + Rueda de Vida en Notion
│   ├── load_tasks.py
│   ├── inicio.bat
│   ├── fix_git_push.ps1
│   └── reparar_git.ps1
│
└── docs/
    ├── AUDITORIA_NAUTA_PENDIENTE.md
    ├── indice_maestro.md
    ├── estado/            ← Snapshots del estado actual
    ├── planes/            ← Planes, roadmaps, especificaciones
    ├── setup/             ← Guías de configuración y deploy
    ├── historial/         ← Changelogs y registros de cambios
    ├── arquitectura/      ← Diagramas y decisiones de arquitectura
    ├── producto/          ← PRDs, wireframes, .xlsx de producto
    └── framework/         ← FrameworkIA y excels de contexto
```

## Variables de entorno (.env)
```
NOTION_TOKEN=secret_...
FLASK_PORT=5000
FLASK_ENV=development
FRONT_LANGUAGE=es
CREATIVES_LANGUAGE=es

# Pendiente configurar (crear tablas en Notion primero):
# NAUTA_LOGS_DB_ID=...
# RUEDA_VIDA_DB_ID=...
```

## Notion DB IDs
| Base | ID | Conecta a |
|------|-----|-----------|
| TAREAS | `3f0c07004c154bd4b5712141fc582815` | `/api/tasks/*` |
| HÁBITOS | `89c9ec16837b454c9ce98e543cc62266` | `/api/habits` |
| NAUTA Logs | `NAUTA_LOGS_DB_ID` en .env | `/api/nauta/save-cierre` |
| Rueda de Vida | `RUEDA_VIDA_DB_ID` en .env | `/api/nauta/rueda` |
| 💰 Ofertas M1 | `f487e4497bd84508977e9fdc66ff0e8d` | `/api/m1/context` |
| ✨ Oferta Seleccionada | `e13a544b4b014a14aeb1413385e81c11` | `/api/m2/context`, `/api/m3/context`, `/api/m4/context` |
| 🗺️ Roadmap Master | `ed93c7e668c94d938b932b40970d55c1` | `/api/sistema/context` |
| 🧠 Perfil Kari | `PERFIL_KARI_DB_ID` en .env | `/api/chat/resumir` |

## API Endpoints
| Endpoint | Método | Estado | Descripción |
|----------|--------|--------|-------------|
| `/api/tasks/top-q1` | GET | ✅ | Top 4 tareas Q1 |
| `/api/tasks/today` | GET | ✅ | Tareas de hoy + arrastre días anteriores |
| `/api/habits` | GET | ✅ | Todos los hábitos |
| `/api/nauta/briefing` | GET | ✅ | Briefing matutino (JSON) |
| `/api/nauta/briefing-html` | GET | ✅ | Briefing matutino (HTML para iframe) |
| `/api/nauta/trigger-briefing` | POST | ✅ | Dispara briefing manualmente |
| `/api/nauta/save-cierre` | POST | ✅ | Guarda cierre (Notion si hay ID, sino memoria) |
| `/api/nauta/last-cierre` | GET | ✅ | Último cierre registrado |
| `/api/nauta/status` | GET | ⚠️ | Estado del día (energía hardcodeada) |
| `/api/nauta/rueda` | GET | ⚠️ | Rueda de Vida (requiere RUEDA_VIDA_DB_ID) |
| `/api/nauta/habitos` | GET | ✅ | Hábitos del día |
| `/api/nauta/cierres-historial` | GET | ⚠️ | Historial cierres (requiere NAUTA_LOGS_DB_ID) |
| `/api/health` | GET | ✅ | Health check |
| `/api/m1/context` | GET | ✅ | Ofertas M1 de Notion (para Espía) |
| `/api/m2/context` | GET | ✅ | Oferta Seleccionada de Notion (para Crea) |
| `/api/m3/context` | GET | ✅ | Oferta Seleccionada de Notion (para Creativo) |
| `/api/m4/context` | GET | ✅ | Oferta Seleccionada + Validadas M1 (para Analista Meta) |
| `/api/sistema/context` | GET | ✅ | Roadmap Master desde Notion (para SISTEMA) |
| `/api/chat/resumir` | POST | ✅ | Resume sesión de chat y guarda en Perfil Kari |

## Inicio local
```bash
python start_testeolab.py     # levanta Flask (:5000) + estático (:9000)
# o por separado:
python notion_api.py          # API en :5000 (también sirve el dashboard)
python run_dashboard.py       # UI estática en :9000
```

## Tests
```bash
python tests/test_nauta_endpoints.py    # valida 10+ endpoints
```

## Agentes del sistema
| Agente | Módulo | Nombre en app | Función |
|--------|--------|--------------|---------|
| NAUTA | Coach | NAUTA | Coach diario: briefing, cierre, tareas, hábitos |
| Espía | M1 | M1 Analyzer | Investiga y selecciona ofertas ganadoras |
| Crea | M2 | M2 Builder | Construye MVP, landing y oferta completa |
| Creativo | M3 | M3 Creative | 62 ángulos, creativos, imágenes, videos |
| Analista Meta | M4 | M4 Metrics | Dashboard métricas, ROAS, CTR, CPA, optimización |

Definición completa: `Documentos/SISTEMA_AGENTES_Y_MODULOS.md`

## Estado actual de NAUTA
```
Briefing HTML:      ✅ Funciona, datos reales (tareas + hábitos)
Cierre form:        ✅ Funciona, guarda en memoria
Google Calendar:    ✅ Integrado (OAuth + events + briefing HTML)
NAUTA_LOGS_DB_ID:   ✅ ca5d1d618c3145dca9a86901b635e11e (tabla creada 2026-04-16)
RUEDA_VIDA_DB_ID:   ✅ d2ee4684f0f64311b487ec1e782d86c0 (tabla creada 2026-04-16)
Persistencia Notion:⏳ NAUTA_LOGS_DB_ID configurado, pendiente validar endpoint
Chat NAUTA:         ⏳ ANTHROPIC_API_KEY en .env, pendiente implementar — PRIORIDAD MÁXIMA
```

## Próximos pasos (ver ROADMAP completo en Documentos/)
1. [Dev] Validar /api/nauta/save-cierre persiste en tabla NAUTA Logs
2. [Dev] Chat NAUTA real (Claude API) — PRIORIDAD ALTA
3. [Dev] Energía dinámica desde último cierre
4. [Dev] Botones de chat en cada módulo (M1-M4)
5. [Usuaria] Llenar "Sobre Mí" en Notion

Roadmap completo: `Documentos/ROADMAP_IMPLEMENTACION.md`


---

@blueprint.md
