# ✅ CHECKLIST: Completar Setup Notion

**Estado**: En progreso | **Fecha**: 2026-04-11 | **Responsable**: SISTEMA

---

## 📋 FASE 1: Validación de Estructura Roadmap Master

### Columnas Requeridas
```
✓ = Existe | ✗ = Falta | ⚠ = Tipo incorrecto
```

| Columna | Tipo Esperado | Estado | Acción |
|---------|---------------|--------|--------|
| **Name** | Title | ✓ | OK |
| **Módulo** | Select | ✓ | OK |
| **Asignado a** | Select | ✓ | OK |
| **BLAST Step** | Select | ✓ | OK |
| **Estado** | Select | ✓ | OK |
| **Originado Por** | Select | ? | 🔍 VERIFICAR |
| **Bloqueadores** | Rich Text | ? | 🔍 VERIFICAR |
| **Dependencias** | Relation | ? | 🔍 VERIFICAR |
| **Esfuerzo** | Select | ? | 🔍 VERIFICAR |
| **Prioridad** | Select | ? | 🔍 VERIFICAR |
| **KPI** | Rich Text | ? | 🔍 VERIFICAR |
| **Chat Agente** | Button | ✗ | ⚠️ AGREGAR |
| **Timeline FASE** | Select | ? | 🔍 VERIFICAR |
| **Última Actualización** | Date | ? | 🔍 VERIFICAR |
| **Owner** | Person | ? | 🔍 VERIFICAR |

### Acciones Requeridas

```
1. ABRIR Notion → Roadmap Master
2. VER panel "+" (agregar propiedad)
3. SI FALTA "Originado Por":
   ├─ Nombre: Originado Por
   ├─ Tipo: Select
   └─ Valores: YO, NAUTA, M1 Espía, M2 Crea, M3 Creativo, M4 Meta, SISTEMA
4. SI FALTA "Chat Agente":
   ├─ Nombre: Chat Agente
   ├─ Tipo: Button
   └─ Configurar: [PENDIENTE - ver FASE 2]
```

---

## 🎯 FASE 2: Crear Vistas en Roadmap Master

### Vista 1: "Roadmap por Fase"

```
TIPO: Grouped
GROUPED BY: Timeline FASE
MOSTRAR: Name, Estado, Asignado a, Esfuerzo

INSTRUCCIONES:
1. Click "+" junto a vista actual
2. Nuevo nombre: "Roadmap por Fase"
3. Tipo: Grouped
4. Group property: Timeline FASE
5. Sort by: Timeline FASE ASC
6. Mostrar columnas: Name, Estado, Asignado a, Esfuerzo, KPI
```

### Vista 2: "Kanban por Estado"

```
TIPO: Kanban
BY: Estado
MOSTRAR: Name, Módulo, KPI, Esfuerzo

INSTRUCCIONES:
1. Click "+"
2. Nombre: "Kanban por Estado"
3. Tipo: Kanban
4. Kanban by: Estado
5. Mostrar: Name, Módulo, KPI, Esfuerzo
```

### Vista 3: "Bloqueadores"

```
TIPO: Table
FILTER: Estado = BLOCKED
MOSTRAR: Name, Bloqueadores, Dependencias, Chat Agente

INSTRUCCIONES:
1. Click "+"
2. Nombre: "Bloqueadores"
3. Tipo: Table
4. Agregar FILTER: Estado = BLOCKED
5. Sort by: Prioridad DESC
```

### Vista 4: "Mis Tareas (YO)"

```
TIPO: Table
FILTER: Asignado a = YO
MOSTRAR: Name, Estado, Prioridad, KPI

INSTRUCCIONES:
1. Click "+"
2. Nombre: "Mis Tareas"
3. Tipo: Table
4. FILTER: Asignado a = YO
5. Sort by: Prioridad DESC, Timeline FASE ASC
```

---

## 📝 FASE 3: Cargar Datos FASE 0

### Tareas a Crear

```
OFERTA: Framework BLAST + Context Engineering Setup

TAREA 1:
├─ Name: "Documentar framework BLAST + Context Engineering"
├─ Módulo: GENERAL
├─ Asignado a: SISTEMA
├─ BLAST Step: Blueprint
├─ Estado: DONE
├─ Originado Por: YO
├─ Prioridad: Crítica
├─ Timeline FASE: FASE 0
├─ KPI: "v2.0 documentación completa"
└─ Owner: [Tu nombre]

TAREA 2:
├─ Name: "Crear base de datos 'Sobre Mí'"
├─ Módulo: SISTEMA
├─ Asignado a: SISTEMA
├─ BLAST Step: Architecture
├─ Estado: DONE
├─ Originado Por: SISTEMA
├─ Prioridad: Alta
├─ Timeline FASE: FASE 0
├─ Esfuerzo: M
├─ KPI: "Todas las categorías pobladas"
└─ Owner: [Tu nombre]

TAREA 3:
├─ Name: "Configurar Roadmap Master"
├─ Módulo: SISTEMA
├─ Asignado a: SISTEMA
├─ BLAST Step: Architecture
├─ Estado: IN PROGRESS
├─ Originado Por: SISTEMA
├─ Prioridad: Alta
├─ Timeline FASE: FASE 0
├─ Esfuerzo: M
├─ KPI: "Todas las propiedades, 4+ vistas"
├─ Bloqueadores: "Agregar columna Chat Agente"
└─ Owner: [Tu nombre]

TAREA 4:
├─ Name: "Setup cronométrico NAUTA (8:30 AM briefing)"
├─ Módulo: NAUTA
├─ Asignado a: NAUTA
├─ BLAST Step: Architecture
├─ Estado: TODO
├─ Originado Por: SISTEMA
├─ Prioridad: Crítica
├─ Timeline FASE: FASE 0
├─ Esfuerzo: L
├─ KPI: "Briefing automático cada mañana"
├─ Dependencias: [Integración Google Calendar API]
└─ Owner: [Tu nombre]

TAREA 5:
├─ Name: "Setup cronométrico NAUTA (21:30 log cierre)"
├─ Módulo: NAUTA
├─ Asignado a: NAUTA
├─ BLAST Step: Architecture
├─ Estado: TODO
├─ Originado Por: SISTEMA
├─ Prioridad: Crítica
├─ Timeline FASE: FASE 0
├─ Esfuerzo: M
├─ KPI: "Log de cierre automático cada noche"
├─ Dependencias: [Setup cronométrico NAUTA (8:30 AM briefing)]
└─ Owner: [Tu nombre]
```

### Instrucciones de Carga

```
1. Abrir Notion → Roadmap Master
2. Click "Add a page" (o +" inferior)
3. Para cada tarea:
   ├─ Llenar campos según la tabla arriba
   ├─ Asegurarse de que Timeline FASE = FASE 0
   ├─ Establecer dependencias si corresponde
   └─ Press Enter
4. Verificar que aparecen en vista "Roadmap por Fase"
```

---

## 🔗 FASE 4: Configurar Botones [Chat con Agente]

### Estructura de Botones

```
UBICACIÓN: Columna "Chat Agente" en Roadmap Master

PARA CADA TAREA M1-M4:
├─ Si Asignado a = M1 Espía
│  └─ URL: https://claude.ai/chat?agent=M1-Espía&task={task_id}
├─ Si Asignado a = M2 Crea
│  └─ URL: https://claude.ai/chat?agent=M2-Crea&task={task_id}
├─ Si Asignado a = M3 Creativo
│  └─ URL: https://claude.ai/chat?agent=M3-Creativo&task={task_id}
├─ Si Asignado a = M4 Meta
│  └─ URL: https://claude.ai/chat?agent=M4-Meta&task={task_id}
└─ Si Asignado a = NAUTA o SISTEMA
   └─ Botón inactivo (no aplica)
```

### Instrucciones

```
1. NOTION PROPERTIES:
   ├─ En Roadmap Master, propiedades
   ├─ Buscar/crear "Chat Agente" (Button)
   ├─ Configurar tipos de botón
   
2. POR CADA FILA:
   ├─ Si es M1/M2/M3/M4
   └─ Configurar URL del botón
```

---

## 📊 FASE 5: Crear Tabla Análisis de Ofertas (OPCIONAL)

```
TABLA: "Análisis de Ofertas" (nueva)

CAMPOS:
├─ Name (Title): "Nombre de la oferta"
├─ Estado (Select): Ideación, Investigación, MVP, Creativos, Testing, Escalando
├─ Avatar (Rich Text): Descripción del público ideal
├─ Pain Point (Rich Text): Principal problema que resuelve
├─ Precio (Number): Ticket de venta
├─ M1 Status (Select): TODO, IN PROGRESS, DONE
├─ M2 Status (Select): TODO, IN PROGRESS, DONE
├─ M3 Status (Select): TODO, IN PROGRESS, DONE
├─ M4 Status (Select): TODO, IN PROGRESS, DONE
├─ Roadmap Tasks (Relation): Link a Roadmap Master (M1-M4)
├─ ROI (Formula): [Cálculo básico]
└─ Última Actualización (Date)
```

---

## ✅ CHECKLIST FINAL

```
□ Validar todas las columnas en Roadmap Master
□ Agregar "Originado Por" si falta
□ Agregar "Chat Agente" (Button)
□ Crear vista "Roadmap por Fase"
□ Crear vista "Kanban por Estado"
□ Crear vista "Bloqueadores"
□ Crear vista "Mis Tareas"
□ Cargar 5 tareas FASE 0
□ Configurar botones [Chat con Agente]
□ Verificar que NAUTA tiene acceso a lectura
□ Crear tabla "Análisis de Ofertas" (opcional)
□ Testear flujo completo (click botón → chat)
□ Documentar resultado
```

---

## 🚀 Estado: LISTO PARA EJECUTAR

**Próximo paso**: Seguir checklist FASE 1-5 en orden.  
**Tiempo estimado**: 30-45 minutos (manual en Notion).  
**Responsable**: [TÚ - en Notion UI]

