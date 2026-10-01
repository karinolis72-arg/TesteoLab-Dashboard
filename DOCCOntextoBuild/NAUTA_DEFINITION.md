# NAUTA — Definición Completa del Sistema
**Fuente: Transcripciones + SISTEMA_AGENTES_Y_MODULOS.md + framework-BLAST.md**
**Última actualización: 2026-04-12**

---

## QUIÉN ES KARI (Karina)

Karina está construyendo TesteoLab: un sistema que combina ejecución personal con un negocio de infoproductos low ticket en LATAM vía Meta Ads.

**Objetivo del negocio:** 7 ofertas/semana testeadas → 28/mes → 2-3 winners con ROAS >3:1 → $10k/mes USD  
**Mercado:** LATAM, principalmente Argentina  
**Precio objetivo de ofertas:** USD $7-$47 (low ticket)  
**CPM estimado LATAM:** $8-15 USD

---

## QUÉ ES NAUTA

NAUTA es el coach de productividad personal de Kari. No es un asistente genérico — es su sistema operativo diario.

**Función core:**
- Briefing matutino (8:30 AM automático o manual)
- Seguimiento de Top 4 tareas del día
- Registro de cierre nocturno (21:30 o manual)
- Coaching personalizado basado en contexto real (Notion + Calendar)
- Replanificación automática cuando hay arrastre de tareas

---

## TAREAS PROGRAMADAS (Scheduled Tasks)

### Cierre Diario — 21:00 ART
1. Lee Rueda de Vida desde Notion (8 áreas de vida)
2. Calcula scores de cada área
3. Genera reflexión del día: qué funcionó, qué no, qué aprendió
4. Registra en Notion NAUTA Logs (requiere NAUTA_LOGS_DB_ID)
5. Notificación opcional al usuario

### Planificación Semanal — Domingos 19:00 ART
1. Ingesta FrameworkIA (3 archivos Excel de contexto)
2. Analiza la semana anterior (qué se completó, qué se arrastró)
3. Genera 3-5 objetivos de la semana siguiente
4. Crea las 7 ofertas a testear en la semana
5. Sugiere eventos en Google Calendar
6. Actualiza el dashboard de TesteoLab

---

## BUSINESS OS — FrameworkIA

Carpeta de contexto que NAUTA lee para conocer a Kari profundamente:

```
FrameworkIA/
├── sobre-mi.md          ← quién es Kari, valores, cómo trabaja, comunicación preferida
├── negocio.md           ← TesteoLab, pipeline M1→M4, objetivos, métricas
├── prioridades-actuales.md ← Q actual, proyectos activos, deadlines
├── decisiones-log.md    ← decisiones tomadas para no repetir análisis
└── SOPs/
    ├── m1-espy.md       ← paso a paso M1 como ejecutable
    ├── m2-crea.md       ← paso a paso M2
    ├── m3-creativo.md   ← paso a paso M3
    └── m4-meta.md       ← paso a paso M4
```

---

## PIPELINE DE NEGOCIO (M1 → M4)

```
M1 ESPÍA         M2 CREA          M3 CREATIVO      M4 ANALISTA META
──────────────   ──────────────   ──────────────   ──────────────
Investiga Meta   Construye MVP    62 ángulos       ROAS dashboard
Ads Library  →   + landing    →   + creativos   →  Optimiza hasta
Selecciona       en 24h           para Meta Ads    $10k/mes
oferta ganadora
```

### M1 — Flujo de 5 pasos

**PASO 1:** Definir Búsqueda (país + keywords + filtros)  
**PASO 2:** Buscar en Meta Ads Library (GET /ads_library)  
**PASO 3:** Analizar (días activos, CPM, tipo oferta, señales de éxito)  
**PASO 4:** Filtrar & Clasificar (score 0-100, comparador hasta 3)  
**PASO 5:** Seleccionar → Output JSON hacia M2

**Scoring:**
- Días activos: `<30d`=🟡 `30-90d`=🟢 `90-180d`=🟢🟢 `180+`=🟢🟢🟢
- Puntos: días activos (40pts) + presupuesto estimado (30pts) + señales de éxito (30pts)
- Ganadores: 80+ | Potencial Alto: 61-79 | Experimental: 31-60 | Descartar: <30

**Output JSON a M2:**
```json
{
  "offer_type": "online_course",
  "price_point": "$17-47",
  "target_market": "Emprendedores 25-45 LATAM",
  "key_message": "...",
  "bonus_detected": ["Ebook", "Plantillas"],
  "viability_score": 87,
  "days_active": 238,
  "estimated_investment": "$4200",
  "urgency_signals": ["Tiempo limitado", "Plazas"],
  "cta_type": "Comprar ahora"
}
```

### M2 — Crea (24h desde M1)
- Recibe JSON de M1
- MVP: guía PDF 10-20 páginas (Gamma-style)
- Landing HTML Shopify/Hotmart-ready
- Estructura: SKU, precio, descripción, bonus, order bumps (máx 3)
- Copy: pain point → promesa → producto → testimonios → garantía → CTA

### M3 — Creativo (24h desde M2)
- 62 ángulos creativos (hooks, dolores, públicos distintos)
- Scripts de video: hook <3seg + desarrollo + CTA
- Prompts de imagen para Midjourney/DALL-E/Flux
- Campaign briefs completos para Meta Ads Manager
- Variaciones para A/B testing

### M4 — Analista Meta
- ROAS objetivo: ≥1.5 para seguir | ≥3:1 = winner → escalar
- Diagnóstico embudo: landing / checkout / oferta
- A/B testing: 10-12 anuncios a $2/conjunto
- Winner: 3+ días de datos + 50+ clicks
- Escalado: 20-30% cada 48h (nunca saltos bruscos)
- Meta final: $10k/mes USD

---

## ACCESOS DE NAUTA

**Lee:**
- Notion → TAREAS (top 4, hoy, arrastre)
- Notion → HÁBITOS (estado del día)
- Notion → Roadmap Master (contexto de proyectos)
- Notion → Perfil Kari (resúmenes de sesiones guardados)
- Google Calendar → eventos del día
- Rueda de Vida → 8 áreas de vida

**Escribe:**
- Notion → Tareas (crear / actualizar / marcar hecha)
- Notion → NAUTA Logs (log de cierre diario)
- Notion → Hábitos (actualizar estado)
- Google Calendar → crear / mover / eliminar eventos

---

## COMANDOS DE ACCIÓN (formato ACCION)

El sistema parsea estos comandos y muestra botones de confirmación — NAUTA los incluye sin explicarlos:

```
ACCION:done:ID:
ACCION:reschedule:ID:YYYY-MM-DD
ACCION:delete_task:ID:
ACCION:delete_habit:ID:
ACCION:cal_move:EID:NuevoTitulo|start|end|calId   (campo vacío = no cambia)
ACCION:cal_delete:EID:calId
ACCION:cal_create:NUEVO:Titulo|start|end|primary
```

IDs de tareas/hábitos → `[id:...]`  
IDs de eventos Calendar → `[eid:...|cid:...]`

---

## ESTADO ACTUAL DEL SISTEMA (2026-04-12)

| Feature | Estado |
|---------|--------|
| Briefing HTML | ✅ Funciona (datos reales de Notion) |
| Cierre form | ✅ UI funciona |
| Chat de agentes (NAUTA + M1-M4 + SISTEMA) | ✅ Funciona con Claude API |
| Visión múltiple (múltiples imágenes) | ✅ Funciona |
| Resumir sesión → Notion Perfil Kari | ✅ Funciona (requiere PERFIL_KARI_DB_ID) |
| Acciones Calendar (mover/crear/eliminar) | ✅ Funciona |
| Persistencia NAUTA Logs en Notion | ⏳ Requiere NAUTA_LOGS_DB_ID |
| Rueda de Vida real | ⏳ Requiere RUEDA_VIDA_DB_ID |
| Cierre Diario 21:00 ART automático | ❌ Pendiente |
| Planificación Semanal DOM 19:00 ART | ❌ Pendiente |
| M1 Meta Ads Library API | ❌ Pendiente (v1.1) |
| M4 Meta Ads Manager API | ❌ Pendiente (v2.0) |
| Business OS / Context Engineering | ❌ Pendiente (v3.0) |

---

## ROADMAP

| Fase | Contenido | Estado |
|------|-----------|--------|
| v1.0 | Dashboard + NAUTA + chat agentes + Calendar | ✅ DONE |
| v1.1 | M1 Espía — Meta Ads Library + scoring + comparador | 🔄 EN PROGRESO |
| v1.2 | M2 Crea — landing builder + MVP generator | ⏳ Backlog |
| v1.3 | M3 Creativo — 62 ángulos + scripts video | ⏳ Backlog |
| v2.0 | M4 Analista Meta — ROAS dashboard + A/B | ⏳ Backlog |
| v3.0 | Business OS — Context Engineering + memoria evolutiva | ⏳ Backlog |

---

## CARACTERÍSTICAS DESEADAS DEL SISTEMA (checklist de producto)

### Core
- [x] Dashboard personal con módulos M1-M4
- [x] NAUTA como coach diario con datos reales
- [x] Chat con todos los agentes con historial
- [x] Acciones sobre tareas/hábitos/calendar desde el chat
- [ ] Cierre diario automatizado a las 21:00
- [ ] Planificación semanal automatizada los domingos

### Negocio
- [ ] M1: Búsqueda en Meta Ads Library
- [ ] M1: Scoring 0-100 con CPM
- [ ] M1: Comparador de ofertas
- [ ] M2: Landing HTML builder
- [ ] M2: MVP generator (Gamma)
- [ ] M3: 62 ángulos creativos
- [ ] M3: Scripts de video para Meta Ads
- [ ] M4: Dashboard ROAS en tiempo real
- [ ] M4: A/B testing automatizado

### Memoria y Context Engineering
- [ ] Perfil Kari en Notion (resúmenes de sesiones)
- [ ] Carpeta FrameworkIA / Business OS
- [ ] Memoria evolutiva que mejora sola
- [ ] Agente que hace preguntas proactivas

---

*Este documento es la fuente de verdad para el desarrollo de NAUTA y TesteoLab.*
*Actualizar cuando cambien decisiones arquitectónicas o de producto.*
