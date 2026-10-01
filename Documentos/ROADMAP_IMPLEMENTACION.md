# Roadmap de Implementación — TesteoLab
**Última actualización: 2026-04-16**

---

## ESTADO ACTUAL (punto de partida)

```
NAUTA briefing:         ✅ Funciona (datos reales de Notion) — bug unhashable dict corregido 2026-04-16
NAUTA cierre form:      ✅ UI funciona (sin persistencia)
NAUTA persistencia:     ⏳ En progreso — NAUTA_LOGS_DB_ID configurado, pendiente validar endpoint
NAUTA chat/agente:      ⏳ En progreso — ANTHROPIC_API_KEY en .env, pendiente implementar
Google Calendar:        ✅ Integrado (OAuth + events + briefing HTML)
Rueda de Vida:          ⏳ Tabla creada en Notion (RUEDA_VIDA_DB_ID en .env), sin datos aún
Módulo TRACKER:         ❌ Placeholder vacío
M1 Espía:               ❌ Botón existe, sin contenido
M2 Crea:                ❌ Botón existe, sin contenido
M3 Creativo:            ❌ Botón existe, sin contenido
M4 Analista Meta:       ❌ Botón existe, sin contenido
Settings:               ❌ No existe
```

---

## TIER 0 — Pre-requisitos (la usuaria hace esto)

Estas tareas las hace la usuaria en Notion. Sin ellas, el sistema no puede persistir.

| Tarea | Quién | Estado |
|-------|-------|--------|
| Llenar "Sobre Mí" en Notion | Usuaria | ⏳ Pendiente |
| Crear tabla NAUTA Logs en Notion | Dev | ✅ Completado 2026-04-16 |
| Crear tabla Rueda de Vida en Notion | Dev | ✅ Completado 2026-04-16 |
| Agregar `NAUTA_LOGS_DB_ID` al `.env` | Dev | ✅ Completado 2026-04-16 |
| Agregar `RUEDA_VIDA_DB_ID` al `.env` | Dev | ✅ Completado 2026-04-16 |
| Crear tabla ROADMAP MASTER en Notion | Usuaria | ✅ Ya existía |

Guía para crear las tablas: `docs/planes/NAUTA_SETUP_NOTIO_TABLES.md`

---

## TIER 1 — Chats de agentes (desbloquea conversaciones con M1-M4)

**Objetivo:** Que la usuaria pueda chatear con cada módulo para ir definiendo su lógica.

| Tarea | Archivo afectado | Prioridad |
|-------|-----------------|-----------|
| Botón "Chat con Espía" en M1 | dashboard_v2.html | 🔴 Alta |
| Botón "Chat con Crea" en M2 | dashboard_v2.html | 🔴 Alta |
| Botón "Chat con Creativo" en M3 | dashboard_v2.html | 🔴 Alta |
| Botón "Chat con Analista Meta" en M4 | dashboard_v2.html | 🔴 Alta |
| Chat de NAUTA en módulo NAUTA | dashboard_v2.html + notion_api.py | 🔴 Alta |
| Interface de chat genérica (modal o panel) | dashboard_v2.html | 🔴 Alta |

**Decisión pendiente:** ¿Chat real (Claude API) o placeholder? → Ver preguntas al final.

---

## TIER 2 — NAUTA funcional al 100%

**Objetivo:** NAUTA como coach diario completamente funcional.

| Tarea | Depende de | Archivo |
|-------|-----------|---------|
| Persistencia cierres en Notion | `NAUTA_LOGS_DB_ID` en .env | notion_api.py |
| Energía dinámica desde último cierre | Persistencia funcionando | notion_api.py + dashboard_v2.html |
| Chat con NAUTA (lee Notion + coaching) | Claude API key | notion_api.py + dashboard_v2.html |
| NAUTA lee "Sobre Mí" | Sobre Mí en Notion | nauta_scheduler.py |
| NAUTA lee Google Calendar | Google Calendar API | notion_api.py |
| Tareas completadas dinámicas (no hardcoded 0) | / | notion_api.py |

---

## TIER 3 — Módulos de negocio (M1 primero)

**Objetivo:** M1 Espía funcional, luego M2-M4 en secuencia.

### M1 — Espía (más avanzado, tiene spec completa)
Spec: `docs/planes/m1_especificacion.md`

| Fase | Tarea |
|------|-------|
| 1 | UI básica: formulario de búsqueda (país + keywords) |
| 2 | Integración Meta Ads Library API |
| 3 | Análisis de viabilidad (días activos, scoring) |
| 4 | Grid de resultados con score de potencial |
| 5 | Comparador de anuncios |
| 6 | Output hacia M2 |

### M2 — Crea
| Fase | Tarea |
|------|-------|
| 1 | Recibe output de M1 |
| 2 | MVP generator (Gamma-style) |
| 3 | Landing HTML builder |
| 4 | Estructura de producto + order bumps |
| 5 | Mockups básicos |

### M3 — Creativo
| Fase | Tarea |
|------|-------|
| 1 | P1-P2: Extracción + identidad visual |
| 2 | P6: Generador de 62 ángulos |
| 3 | P7-P8: Fábrica de imágenes/videos |

### M4 — Analista Meta
| Fase | Tarea |
|------|-------|
| 1 | Integración Meta Ads Manager API |
| 2 | Dashboard de métricas en tiempo real |
| 3 | Diagnóstico automático del embudo |
| 4 | A/B testing y escalado |

---

## TIER 4 — Infraestructura técnica

| Tarea | Para qué sirve |
|-------|---------------|
| Migrar a Supabase como DB principal | Persistencia confiable vs in-memory |
| Integrar n8n | Automatizaciones entre módulos |
| Settings: perfil + foto | Personalización |
| Módulo TRACKER | Métricas personales |

---

## ORDEN DE BUILD RECOMENDADO

```
Semana 1:
├── Tier 0: Usuaria crea tablas en Notion + agrega IDs
├── Tier 1: Botones de chat en M1-M4 + interface chat básica
└── Tier 2: Chat NAUTA funcional (Claude API)

Semana 2:
├── Tier 2: Persistencia cierres en Notion
├── Tier 2: Energía dinámica
└── Tier 3: M1 Espía — UI + Meta Ads Library API

Semana 3-4:
└── Tier 3: M2 + M3 según definición en chats

Mes 2:
└── Tier 3: M4 + Tier 4: Supabase, n8n
```

---

## DEPENDENCIAS CLAVE

```
Chat NAUTA ──────────────────────── requiere Claude API key
Persistencia cierres ────────────── requiere NAUTA_LOGS_DB_ID
Energía dinámica ────────────────── requiere persistencia funcionando
NAUTA lee Sobre Mí ──────────────── requiere Sobre Mí en Notion
M1 búsqueda ─────────────────────── requiere Meta Ads Library API key
M4 métricas ─────────────────────── requiere Meta Ads Manager API
M2-M3-M4 chat ──────────────────── requiere Claude API key
```

---

## PREGUNTAS ABIERTAS (decisiones pendientes)

1. **Chat de agentes**: ¿Chat real con Claude API o placeholder con mensaje "Próximamente"?
   - Si es real: ¿Hay API key de Claude (Anthropic) disponible en .env?
   - Si es placeholder: ¿Qué mensaje mostrar?

2. **Notion tasks de roadmap**: ¿Creo las tareas del TIER 0-1 en la base TAREAS existente (`3f0c07004c154bd4b5712141fc582815`) o en una nueva base "ROADMAP MASTER" separada?

3. **Google Calendar**: ¿Integrar ahora (Tier 2) o dejar para más adelante?

4. **"Sobre Mí" en Notion**: ¿Ya tiene ID de página o base de datos? Si sí, podemos conectarlo ya.

---

*Documento vivo — actualizar con cada sprint completado*
