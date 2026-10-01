# Sistema Completo — Agentes y Módulos
**Definido: 2026-04-12 | Fuente: transcripciones de la usuaria + decisiones de sesión**

---

## VISIÓN GENERAL DEL PRODUCTO

TesteoLab es una web app con agentes IA que integra:
- **Ejecución personal** (NAUTA Coach) — organiza la vida personal y profesional
- **Generación de negocio** (M1-M4 Builder) — sistema automático de low ticket digital
- **Memoria contextual** (Context Engineering) — conocimiento acumulado que mejora con el tiempo

> No es solo un organizador. Genera ingresos de forma sistemática.

---

## ARQUITECTURA DE MÓDULOS

```
Dashboard (Home)
│
├── NAUTA — Coach Personal
├── M1 — Espía (investigación)
├── M2 — Crea (oferta + MVP)
├── M3 — Creativo (ads + contenido)
└── M4 — Meta (métricas + optimización)
```

---

## AGENTE 1 — NAUTA (Coach Personal)

**Nombre del agente:** NAUTA
**Función:** Sistema coach diario. Planifica, sigue, presiona, replantea.

### Lo que hace
- Briefing matutino (8:30 AM automático o manual)
- Seguimiento de Top 4 tareas del día
- Registro de cierre nocturno (21:30 o manual)
- Coaching personalizado basado en contexto
- Replanificación automática cuando hay arrastre de tareas

### Accesos de NAUTA

**Lee:**
- Notion → TAREAS (top 4, hoy, arrastre)
- Notion → HÁBITOS (Franco, gym, etc.)
- Notion → Roadmap Master (contexto de proyectos)
- Notion → "Sobre Mí" (contexto personal completo)
- Google Calendar → eventos del día
- Rueda de Vida → visualización de estado personal

**Escribe:**
- Notion → Tareas (crear / actualizar Top 4)
- Notion → NAUTA Logs / Notas Diarias (log de cierre)
- Notion → Hábitos (actualizar estado)

### Context Engineering — Memoria viva
NAUTA aprende cómo trabaja la usuaria:
- Qué hora del día es más productiva
- Qué tipo de tareas se arrastran y por qué
- Cuánto duran realmente las tareas
- Decisiones históricas, proyectos pasados, personas clave

Estructura de memoria:
```
/sobre-mi
/personas       ← pareja, mentores, equipo
/proyectos      ← historial de proyectos
/transcripciones← cómo habla, qué valora
/notas-diarias  ← log día a día
```

### Estado actual (2026-04-12)
```
Briefing HTML:        ✅ Funciona (datos reales de Notion)
Cierre form:          ✅ UI funciona
Persistencia Notion:  ⏳ Requiere NAUTA_LOGS_DB_ID
Chat/Agente:          ❌ No existe — PRIORIDAD ALTA
Google Calendar:      ❌ No integrado aún
Rueda de Vida:        ⏳ Requiere RUEDA_VIDA_DB_ID
```

---

## AGENTE 2 — ESPÍA (M1)

**Nombre del agente:** Espía
**Nombre técnico en app:** M1 Analyzer
**Módulo:** M1 — Análisis de Ofertas
**Función:** Investigar y seleccionar ofertas ganadoras para modelar.

### Flujo M1
```
Buscar en Meta Biblioteca (país + keywords)
    ↓
Ver anuncios de competencia activos
    ↓
Analizar viabilidad (días activos, presupuesto estimado, tipo oferta)
    ↓
Score de potencial (0-100)
    ↓
Filtrar y clasificar ganadores
    ↓
Output: "Vamos con ESTA oferta" → pasa a M2
```

### Tareas tipo del agente
- Búsqueda en Meta Ads Library (país + keywords o nombre empresa)
- Búsqueda en Etsy, Clickbank, Amazon (productos digitales)
- Detección de tipo de oferta (ebook, curso, membresía, servicio)
- Cálculo de presupuesto estimado invertido (CPM-based)
- Scoring de potencial con señales de éxito
- Comparador de anuncios (hasta 3)
- Historial de búsquedas guardadas

### Output a M2
```json
{
  "offer_type": "online_course",
  "price_point": "$97-297",
  "target_market": "Emprendedores 25-45",
  "key_message": "...",
  "bonus_detected": ["Ebook 1", "Plantillas"],
  "viability_score": 87,
  "advertiser_url": "...",
  "days_active": 238,
  "estimated_investment": "$4200"
}
```

### Spec completa
Ver `docs/planes/m1_especificacion.md`

---

## AGENTE 3 — CREA (M2)

**Nombre del agente:** Crea
**Nombre técnico en app:** M2 Builder
**Módulo:** M2 — Creación de Oferta
**Función:** Construir la oferta completa lista para vender.

### Flujo M2
```
Recibe output de M1 (oferta a modelar)
    ↓
Landing HTML builder (Shopify-ready)
    ↓
Estructura de producto (SKU, precio, descripción)
    ↓
Bonus (qué incluir, orden, presentación)
    ↓
Mockups generator (visuales de la oferta)
    ↓
Output: Oferta completa lista para ir a mercado → pasa a M3
```

### Tareas tipo del agente
- MVP generator (guía 10-20 páginas con Gamma-style)
- Landing HTML con estructura persuasiva (puntos de dolor, testimonios, bonus, garantía, CTA)
- Apariencia de pago (checkout optimizado)
- Estructura de productos con order bumps (máx 3)
- Mockups de producto
- Integración con Hotmart (subida del producto)

### KPIs del módulo
- MVP completado (%)
- Landing CTR esperado
- Elementos persuasivos implementados (checklist)

---

## AGENTE 4 — CREATIVO (M3)

**Nombre del agente:** Creativo
**Nombre técnico en app:** M3 Creative
**Módulo:** M3 — Creative Lab
**Función:** Crear estrategia completa de ads y contenido.

### Flujo M3 (8 pasos)
```
P1: Extracción      → producto, avatar, dolores, beneficios
P2: Identidad Visual → marca, colores, tipografía
P3: Estilo Visual   → realista / ilustrado / 3D / etc.
P4: Formatos        → noticiero / infografía / UGC / etc.
P5: Análisis IA     → competencia visual
P6: Ángulos (~62)   → generación de 62 ángulos creativos
P7: Fábrica Imágenes → variaciones, edición, descarga
P8: Fábrica Videos  → guiones, escenas, voces, secuencias
```

### Tareas tipo del agente
- Extracción de puntos de dolor y beneficios del avatar
- Generación de ~62 ángulos creativos
- Scripts para anuncios (con hook, desarrollo, CTA)
- Generación de audios con IA (Eleven Labs, etc.)
- Producción de videos (Sora, clips TikTok, UGC sintético)
- Imágenes con prompts optimizados
- "Modo creativo guiado" — fuerza a testear 10 anuncios

### KPIs del módulo
- Ángulos generados (X/62)
- Creativos listos (imágenes/videos)
- CTR objetivo por formato

---

## AGENTE 5 — ANALISTA META (M4)

**Nombre del agente:** Analista Meta
**Nombre técnico en app:** M4 Metrics
**Módulo:** M4 — Métricas y Optimización
**Función:** Monitorear campañas en Meta Ads y tomar decisiones de optimización.

### Flujo M4
```
Sube creativos a Meta Ads Manager
    ↓
Dashboard en tiempo real (ROAS, CAC, conversiones, presupuesto)
    ↓
Análisis de embudos:
  - Pocos pagos iniciados → landing mala
  - Muchos pagos iniciados, pocas compras → checkout malo
  - Pocas compras totales → oferta débil
    ↓
Optimización: segmentación, pausar / escalar
    ↓
A/B testing automático
    ↓
Reporting + decisiones
```

### Tareas tipo del agente
- Integración con Meta Ads Manager API
- Dashboard de métricas en tiempo real
- Diagnóstico automático del embudo (landing / checkout / oferta)
- Recomendaciones de escalado progresivo
- A/B testing (testeo de 10-12 anuncios con conjuntos de $2)
- Reinversión automática sugerida (cuando ROAS ≥ 1.5)
- Tracking de múltiples productos simultáneos

### KPIs del módulo
- ROAS actual (objetivo: ≥ 1.5)
- CTR por anuncio
- CPA (costo por adquisición)
- Pagos iniciados vs compras
- Presupuesto diario invertido

---

## ROADMAP MASTER (Notion — base compartida)

El Roadmap Master es la base de datos de Notion donde converge todo:

| Quién escribe | Qué agrega |
|--------------|------------|
| BUILDER (sistema) | Crea estructura, gestiona |
| Usuaria | Crea tareas manuales |
| NAUTA | Agrega Top 4 diarios |
| M1-M4 | Agrega tareas automáticas por fase |

Todos pueden leer. BUILDER es el "guardián" pero no el dueño exclusivo.

---

## IDEAS DESEABLES (alto valor, fase futura)

### Producto
- "Modo ejecución" — solo 1 tarea visible (modo focus)
- "Modo guerra" — bloquea distracciones
- Auto-replan semanal automático

### Negocio
- Clonador de ofertas (modelado automático en 48hs)
- Generador de landings en 1 click
- Testeo automático de anuncios

### IA
- Pre-prompt automático (usuario habla, se genera el prompt)
- Memoria evolutiva (mejora sola con el tiempo)
- Agente que hace preguntas proactivas (clave de Context Engineering)

### Escala
- Multi-producto tracking
- Sugerencia de nuevos nichos
- Reinversión automática sugerida

---

## INTEGRACIONES REQUERIDAS

| Integración | Quién la usa | Estado |
|-------------|-------------|--------|
| Notion | NAUTA + todos | ✅ Conectado (parcial) |
| Google Calendar | NAUTA | ❌ No integrado |
| Meta Ads Library | M1 Espía | ❌ No integrado |
| Meta Ads Manager | M4 Analista Meta | ❌ No integrado |
| Hotmart | M2 Crea | ❌ No integrado |
| Supabase | Base de datos central | ❌ No integrado |
| n8n | Automatizaciones | ❌ No integrado |
| Eleven Labs | M3 Creativo (audio) | ❌ No integrado |
| Gamma App | M2 Crea (MVP PDF) | ❌ No integrado |

---

*Última actualización: 2026-04-12*
*Fuente: Transcripciones de la usuaria + decisiones de sesión de diseño*
