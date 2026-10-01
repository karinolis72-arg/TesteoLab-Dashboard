# 🗂️ NOTION SETUP SPECIFICATION
**Estructura completa: "Sobre Mí" + "Roadmap Master"**

---

## 📋 TABLA 1: SOBRE MÍ

### Ubicación
```
Workspace TesteoLab
└─ "Sobre Mí" (Database)
```

### Propósito
Base de datos de contexto personal. Los agentes la consultan para entender quién eres, qué haces, cómo trabajas.

### Campos (Propiedades)

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| **Name** | Title | Título de la entrada | "Perfil General" |
| **Categoría** | Select | Tipo de contenido | Perfil, Personas, Proyectos, Ofertas, Metodología, Límites |
| **Contenido** | Rich Text | Información detallada | [Texto largo con formato] |
| **Última Actualización** | Date | Cuándo se actualizó | 2026-04-11 |
| **Relevancia** | Select | Prioridad para agentes | Alta, Media, Baja |
| **Tags** | Multi-select | Palabras clave | "contexto", "decisión", "aprendizaje" |

### Estructura de Categorías

```
SOBRE MÍ Database → Vista "Categorized"

├─ PERFIL GENERAL
│  └─ Nombre completo
│  └─ Edad / Género
│  └─ Roles activos
│  └─ Objetivos 3-12 meses
│  └─ Métrica de éxito principal
│  └─ Horarios preferidos
│
├─ PERSONAS CLAVE
│  └─ [Nombre Persona 1]
│     └─ Relación
│     └─ Contexto (qué aprendo, cómo interactúo)
│  └─ [Nombre Persona 2]
│  └─ ...
│
├─ PROYECTOS & PRODUCTOS
│  └─ [Proyecto 1]
│     └─ Descripción
│     └─ Estado (Activo, Pausa, Completo)
│     └─ Métricas
│  └─ ...
│
├─ OFERTAS ACTIVAS
│  └─ [Oferta 1]
│     └─ Descripción
│     └─ Precio
│     └─ Audiencia
│  └─ ...
│
├─ METODOLOGÍA
│  └─ Cómo lanzo ofertas
│  └─ Cómo trackeo resultados
│  └─ Cómo decido qué vender
│  └─ Frameworks que uso
│
├─ LÍMITES & VALORES
│  └─ "NO vendo X"
│  └─ "SÍ vendo X cuando..."
│  └─ Público ideal es...
│  └─ Mis principios son...
│
└─ TRANSCRIPCIONES & NOTAS
   └─ Charlas importantes
   └─ Notas diarias
   └─ Aprendizajes clave
```

### Configuración Recomendada

**Vistas:**
```
1. "Database" - Vista default (todas las propiedades)
2. "Categorized" - Vista grouped by "Categoría"
3. "Timeline" - Vista por fecha (última actualización)
4. "Tags" - Vista grouped by "Tags"
```

---

## 📊 TABLA 2: ROADMAP MASTER

### Ubicación
```
Workspace TesteoLab
└─ "Roadmap Master" (Database)
```

### Propósito
Plan maestro del proyecto TesteoLab. Todas las tareas, fases, módulos, agentes.

### Campos (Propiedades)

| Campo | Tipo | Descripción | Valores |
|-------|------|-------------|---------|
| **Name** | Title | Título de la tarea | "Integración Google Calendar" |
| **Módulo** | Select | Qué módulo/fase | M0, M1, M2, M3, M4, NAUTA, SISTEMA, GENERAL |
| **Asignado a** | Select | Persona/Agente | YO, M1 Espía, M2 Crea, M3 Creativo, M4 Meta, NAUTA, SISTEMA |
| **BLAST Step** | Select | Fase del framework | Blueprint, Links, Architecture, Stylize, Transfer |
| **Estado** | Select | Progreso | TODO, IN PROGRESS, BLOCKED, DONE |
| **Originado Por** | Select | Quién creó | YO, NAUTA, M1 Espía, M2 Crea, M3 Creativo, M4 Meta, SISTEMA |
| **Bloqueadores** | Text | Qué impide avanzar | [Lista de obstáculos] |
| **Dependencias** | Relation | Tareas que deben completarse primero | [Links a otras tareas] |
| **Esfuerzo** | Select | Complejidad | XS, S, M, L, XL |
| **Prioridad** | Select | Urgencia | Baja, Media, Alta, Crítica |
| **KPI** | Text | Métrica de éxito | "ROAS >= 1.5" |
| **Chat Agente** | Button | Acceso a agente | [Link a chat] |
| **Timeline FASE** | Select | Sprint o fase | FASE 0, FASE 1, FASE 2, etc. |
| **Última Actualización** | Date | Cuándo se modificó | [Auto] |
| **Owner** | Person | Responsable | [Usuario] |

### Estructura de Módulos

```
ROADMAP MASTER → Vista "Timeline FASE"

FASE 0: SETUP & PLANNING
├─ [ ] Documentar framework BLAST
├─ [ ] Crear "Sobre Mí" en Notion
├─ [ ] Setup Roadmap Master
└─ [ ] Integración Google Calendar

FASE 1: NAUTA BASICS
├─ [ ] Dashboard NAUTA módulo
├─ [ ] Briefing 8:30 AM
├─ [ ] Log Cierre 21:30
├─ [ ] Rueda de Vida visual
└─ [ ] Tracking de hábitos

FASE 2: OFERTAS M1-M4
├─ M1 ESPÍA
│  ├─ [ ] Web scraping Meta Ads Library
│  ├─ [ ] Análisis de competencia
│  └─ [ ] Validación de demanda
├─ M2 CREA
│  ├─ [ ] MVP Generator
│  ├─ [ ] Landing Builder
│  └─ [ ] Mockups Generator
├─ M3 CREATIVO
│  ├─ [ ] 62 ángulos generator
│  ├─ [ ] Fábrica de imágenes
│  └─ [ ] Fábrica de videos
└─ M4 META
   ├─ [ ] Dashboard Meta Ads
   ├─ [ ] A/B Testing automático
   └─ [ ] Reporting & análisis

FASE 3: AUTOMATIZACIÓN
├─ [ ] Cronjobs (8:30 AM, 21:30, etc.)
├─ [ ] Sync Notion-Calendar
├─ [ ] Email digests
└─ [ ] Alerts de métricas
```

### Configuración Recomendada

**Vistas:**
```
1. "Default view" - Tabla con todas las propiedades
2. "Roadmap por Fase" - Grouped by "Timeline FASE"
3. "Kanban por Estado" - Kanban grouped by "Estado"
4. "Timeline FASE 0" - Filtered para FASE 0 actual
5. "Mis Tareas" - Filtered por "Owner" = YO
6. "Bloqueadores" - Filtered "Estado" = BLOCKED
```

---

## 🔗 RELACIONES ENTRE TABLAS

### "Sobre Mí" ↔ "Roadmap Master"

```
SOBRE MÍ (Database)
    ↓
    └─ Relaciona a "Roadmap Master"
       └─ Campo "Contexto Asociado"
          └─ Permite filtrar tareas por contexto personal

ROADMAP Master (Database)
    ↓
    └─ Relaciona a "Sobre Mí"
       └─ Campo "Referencia Personal"
          └─ Vincula tareas con contexto de "Sobre Mí"
```

### "Roadmap Master" ↔ "Sobre Mí" (AGENTES)

```
ROADMAP Master
    ↓
    └─ "Asignado a" (Select)
       ├─ YO
       ├─ M1 Espía
       ├─ M2 Crea
       ├─ M3 Creativo
       ├─ M4 Meta
       ├─ NAUTA
       └─ SISTEMA

Nota: Los agentes se consultan a "Sobre Mí" automáticamente
Sin relación explícita (la ley consumen vía API/query)
```

---

## 📱 ESTRUCTURA DE VISTAS

### Vista 1: "Default view" (Tabla)

```
Mostrar columnas:
├─ Name (Title)
├─ Módulo
├─ Asignado a
├─ Estado
├─ Originado Por
├─ Esfuerzo
├─ KPI
├─ Chat Agente [BOTÓN]
└─ Última Actualización

Orden: Por "Timeline FASE" + "Prioridad DESC"
```

### Vista 2: "Roadmap por Fase" (Grouped)

```
Grouped by: "Timeline FASE"
├─ FASE 0 (expandible)
├─ FASE 1 (expandible)
├─ FASE 2 (expandible)
└─ FASE 3 (expandible)

Dentro de cada fase: Kanban por "Estado"
```

### Vista 3: "Kanban por Estado" (Kanban)

```
Kanban by: "Estado"
├─ TODO (columna izquierda)
├─ IN PROGRESS (columna)
├─ BLOCKED (columna)
└─ DONE (columna derecha)

Mostrar: Name, Módulo, KPI, Esfuerzo
```

### Vista 4: "Mi Timeline" (Gantt/Timeline)

```
Timeline by: "Última Actualización" (o fecha de creación)
Mostrar: Name, Estado, Módulo
Filter: "Timeline FASE" = FASE 0 (actual)
```

### Vista 5: "Bloqueadores" (Tabla Filtrada)

```
Filter: "Estado" = "BLOCKED"
Mostrar: Name, Bloqueadores, Dependencias, Chat Agente
Ordenar por: "Prioridad DESC"
```

---

## 🚀 PASO A PASO: CREAR EN NOTION

### 1. Crear Base de Datos "Sobre Mí"

```
1. Abre Notion
2. Click "+" → "Database"
3. Nombre: "Sobre Mí"
4. Tipo: "Table"
5. Agregar propiedades:
   ├─ Name (Title) ✓ [Default]
   ├─ Categoría (Select)
   │  └─ Valores: Perfil, Personas, Proyectos, Ofertas, Metodología, Límites
   ├─ Contenido (Rich Text)
   ├─ Última Actualización (Date)
   ├─ Relevancia (Select)
   │  └─ Valores: Alta, Media, Baja
   └─ Tags (Multi-select)
6. Crear 2-3 entradas de prueba
```

### 2. Crear Base de Datos "Roadmap Master"

```
1. Click "+" → "Database"
2. Nombre: "Roadmap Master"
3. Tipo: "Table"
4. Agregar propiedades:
   ├─ Name (Title) ✓ [Default]
   ├─ Módulo (Select)
   │  └─ Valores: M0, M1, M2, M3, M4, NAUTA, SISTEMA, GENERAL
   ├─ Asignado a (Select)
   │  └─ Valores: YO, M1 Espía, M2 Crea, M3 Creativo, M4 Meta, NAUTA, SISTEMA
   ├─ BLAST Step (Select)
   │  └─ Valores: Blueprint, Links, Architecture, Stylize, Transfer
   ├─ Estado (Select)
   │  └─ Valores: TODO, IN PROGRESS, BLOCKED, DONE
   ├─ Originado Por (Select)
   │  └─ Valores: YO, NAUTA, M1 Espía, M2 Crea, M3 Creativo, M4 Meta, SISTEMA
   ├─ Bloqueadores (Text)
   ├─ Dependencias (Relation → link to Roadmap Master)
   ├─ Esfuerzo (Select)
   │  └─ Valores: XS, S, M, L, XL
   ├─ Prioridad (Select)
   │  └─ Valores: Baja, Media, Alta, Crítica
   ├─ KPI (Text)
   ├─ Chat Agente (Button) [Opcional por ahora]
   ├─ Timeline FASE (Select)
   │  └─ Valores: FASE 0, FASE 1, FASE 2, FASE 3
   ├─ Última Actualización (Date)
   └─ Owner (Person)
5. Crear tareas de prueba para FASE 0
```

### 3. Crear Vistas

```
En "Roadmap Master":

1. Vista "Roadmap por Fase"
   ├─ Tipo: Grouped
   ├─ Grouped by: "Timeline FASE"
   └─ Show: Name, Estado, Asignado a

2. Vista "Kanban por Estado"
   ├─ Tipo: Kanban
   ├─ By: "Estado"
   └─ Show: Name, Módulo, KPI

3. Vista "Bloqueadores"
   ├─ Tipo: Table
   ├─ Filter: Estado = BLOCKED
   └─ Show: Name, Bloqueadores, Chat Agente
```

---

## 🎯 DATOS INICIALES (FASE 0)

### Tareas FASE 0 a crear:

```
1. Título: "Documentar framework BLAST + Context Engineering"
   Módulo: GENERAL
   Asignado a: SISTEMA
   Originado Por: YO
   Estado: DONE
   KPI: "v2.0 completo"

2. Título: "Crear base de datos 'Sobre Mí'"
   Módulo: SISTEMA
   Asignado a: SISTEMA
   Originado Por: SISTEMA
   Estado: IN PROGRESS
   KPI: "Todas las categorías pobladas"

3. Título: "Configurar Roadmap Master"
   Módulo: SISTEMA
   Asignado a: SISTEMA
   Originado Por: SISTEMA
   Estado: IN PROGRESS
   KPI: "Todas las propiedades, 2+ vistas"

4. Título: "Integración Google Calendar API"
   Módulo: M0
   Asignado a: SISTEMA
   Originado Por: SISTEMA
   Estado: IN PROGRESS
   BLAST Step: Architecture
   Esfuerzo: M
   KPI: "Calendar eventos visibles en NAUTA"
   Bloqueadores: "Credenciales Google OAuth"

5. Título: "Setup cronométrico NAUTA (8:30 AM)"
   Módulo: NAUTA
   Asignado a: NAUTA
   Originado Por: SISTEMA
   Estado: TODO
   BLAST Step: Architecture
   Esfuerzo: L
   KPI: "Briefing automático cada mañana"
   Dependencias: [Integración Google Calendar API]
```

---

## 💡 NOTAS IMPORTANTES

### Acceso de Agentes
```
NAUTA Lee:
├─ "Sobre Mí" (contexto)
├─ "Roadmap Master" (tareas)
├─ Google Calendar (eventos)
└─ Rueda de Vida (validación)

OFERTAS Agentes (M1-M4) Leen/Escriben:
├─ "Roadmap Master" (crean tareas automáticamente)
├─ "Sobre Mí" (consultan preferencias)
└─ Tablas de ofertas específicas (si existen)

SISTEMA Lee/Escribe:
├─ Todo (es la infraestructura)
└─ Ejecuta automatizaciones
```

### Sincronización
```
Cada 4 horas:
├─ Notion → Google Calendar
└─ Google Calendar → Notion

Cada mañana 8:30 AM:
└─ NAUTA actualiza "Roadmap Master" con Top 4

Cada noche 21:30:
└─ NAUTA crea Log de Cierre en "Sobre Mí"
```

---

*Especificación lista para implementar en Notion. Seguir paso a paso.*
