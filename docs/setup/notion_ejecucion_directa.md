# 🚀 NOTION: Ejecución Directa Paso a Paso

**Estado**: Listo para ejecutar | **Tiempo**: 45 minutos | **Responsable**: TÚ

---

## 📍 PASO 1: Agregar Columnas Faltantes (5 min)

### 1.1 Abrir Roadmap Master

```
1. Abre Notion
2. Workspace: TesteoLab
3. Click: "Roadmap Master"
```

### 1.2 Agregar Columna: "Originado Por"

```
1. Click en el "+" a la derecha de la última columna
2. Nombre: "Originado Por"
3. Tipo: Select
4. Valores (agregar uno a uno):
   ├─ YO (color rojo)
   ├─ NAUTA (color azul)
   ├─ M1 Espía (color verde)
   ├─ M2 Crea (color naranja)
   ├─ M3 Creativo (color púrpura)
   ├─ M4 Meta (color rosa)
   └─ SISTEMA (color gris)
5. Click "Done"
```

### 1.3 Agregar Columna: "Chat Agente"

```
1. Click en el "+"
2. Nombre: "Chat Agente"
3. Tipo: Button
4. Click "Done"
   (Configuraremos las URLs después)
```

### 1.4 Agregar Columna: "Esfuerzo" (si no existe)

```
1. Nombre: "Esfuerzo"
2. Tipo: Select
3. Valores: XS, S, M, L, XL
4. Click "Done"
```

### 1.5 Agregar Columna: "Prioridad" (si no existe)

```
1. Nombre: "Prioridad"
2. Tipo: Select
3. Valores: 
   ├─ Baja
   ├─ Media
   ├─ Alta (color rojo)
   └─ Crítica (color rojo oscuro)
4. Click "Done"
```

---

## 📊 PASO 2: Crear Vistas (10 min)

### 2.1 Vista "Roadmap por Fase"

```
1. En Roadmap Master, busca el selector de vista (arriba, donde dice "Database" o el nombre actual)
2. Click en "+" (Add a view)
3. Nombre: "Roadmap por Fase"
4. Tipo: Grouped
5. Group property: "Timeline FASE"
6. Click "Create"
7. Resultado esperado: Verás 4 grupos (FASE 0, FASE 1, FASE 2, FASE 3)
```

### 2.2 Vista "Kanban por Estado"

```
1. Click "+" (Add a view)
2. Nombre: "Kanban por Estado"
3. Tipo: Kanban
4. Kanban by: "Estado"
5. Click "Create"
6. Resultado esperado: 4 columnas (TODO, IN PROGRESS, BLOCKED, DONE)
```

### 2.3 Vista "Bloqueadores"

```
1. Click "+"
2. Nombre: "Bloqueadores"
3. Tipo: Table
4. Click "Create"
5. Una vez creada:
   ├─ Click en el nombre de la vista → "Edit"
   ├─ Busca "Filter" o ícono de filtro
   ├─ Click "Add a filter"
   ├─ Selecciona: "Estado" "is" "BLOCKED"
   ├─ Click "Done"
6. Resultado: Solo mostrarán tareas bloqueadas
```

### 2.4 Vista "Mis Tareas"

```
1. Click "+"
2. Nombre: "Mis Tareas"
3. Tipo: Table
4. Click "Create"
5. Agregar filter: "Asignado a" "is" "YO"
6. Sort by: Prioridad DESC
```

---

## 📝 PASO 3: Cargar Datos FASE 0 (20 min)

### 3.1 Primera Tarea

```
Título: "Documentar framework BLAST + Context Engineering"

En la nueva fila, llenar:
├─ Name: Documentar framework BLAST + Context Engineering
├─ Módulo: GENERAL
├─ Asignado a: SISTEMA
├─ BLAST Step: Blueprint
├─ Estado: DONE
├─ Originado Por: YO
├─ Bloqueadores: (dejar vacío)
├─ Dependencias: (dejar vacío)
├─ Esfuerzo: S
├─ Prioridad: Crítica
├─ KPI: "v2.0 documentación completa"
├─ Timeline FASE: FASE 0
├─ Owner: [Tu nombre]
└─ Chat Agente: (dejar vacío - no aplica)

Press ENTER para guardar
```

### 3.2 Segunda Tarea

```
Título: "Crear base de datos 'Sobre Mí'"

├─ Name: Crear base de datos 'Sobre Mí'
├─ Módulo: SISTEMA
├─ Asignado a: SISTEMA
├─ BLAST Step: Architecture
├─ Estado: DONE
├─ Originado Por: SISTEMA
├─ Esfuerzo: M
├─ Prioridad: Alta
├─ KPI: "Todas las categorías pobladas"
├─ Timeline FASE: FASE 0
└─ Owner: [Tu nombre]

Press ENTER
```

### 3.3 Tercera Tarea

```
Título: "Configurar Roadmap Master"

├─ Name: Configurar Roadmap Master
├─ Módulo: SISTEMA
├─ Asignado a: SISTEMA
├─ BLAST Step: Architecture
├─ Estado: IN PROGRESS
├─ Originado Por: SISTEMA
├─ Bloqueadores: "Agregar columna Chat Agente + Vistas"
├─ Esfuerzo: M
├─ Prioridad: Alta
├─ KPI: "Todas las propiedades, 4 vistas funcionales"
├─ Timeline FASE: FASE 0
└─ Owner: [Tu nombre]

Press ENTER
```

### 3.4 Cuarta Tarea

```
Título: "Setup cronométrico NAUTA (8:30 AM briefing)"

├─ Name: Setup cronométrico NAUTA (8:30 AM briefing)
├─ Módulo: NAUTA
├─ Asignado a: NAUTA
├─ BLAST Step: Architecture
├─ Estado: TODO
├─ Originado Por: SISTEMA
├─ Esfuerzo: L
├─ Prioridad: Crítica
├─ KPI: "Briefing automático cada mañana a las 8:30"
├─ Timeline FASE: FASE 0
└─ Owner: [Tu nombre]

Press ENTER
```

### 3.5 Quinta Tarea

```
Título: "Setup cronométrico NAUTA (21:30 log cierre)"

├─ Name: Setup cronométrico NAUTA (21:30 log cierre)
├─ Módulo: NAUTA
├─ Asignado a: NAUTA
├─ BLAST Step: Architecture
├─ Estado: TODO
├─ Originado Por: SISTEMA
├─ Esfuerzo: M
├─ Prioridad: Crítica
├─ KPI: "Log de cierre automático cada noche a las 21:30"
├─ Timeline FASE: FASE 0
└─ Owner: [Tu nombre]

Press ENTER
```

---

## 🔗 PASO 4: Configurar Botones [Chat con Agente] (10 min)

### Concepto

Para tareas asignadas a M1, M2, M3, M4, agregaremos botones que linkean a chats con esos agentes.

### Instrucciones

Cuando crees tareas de ofertas (M1-M4), en la columna "Chat Agente":

```
1. Si Asignado a = M1 Espía:
   Click botón → Configure → URL:
   https://claude.ai/chat?agent=M1-Espía&context=offering

2. Si Asignado a = M2 Crea:
   https://claude.ai/chat?agent=M2-Crea&context=offering

3. Si Asignado a = M3 Creativo:
   https://claude.ai/chat?agent=M3-Creativo&context=offering

4. Si Asignado a = M4 Meta:
   https://claude.ai/chat?agent=M4-Meta&context=offering
```

⚠️ **POR AHORA**: No necesitas configurar esto todavía. Lo haremos cuando agregues las ofertas.

---

## ✅ VERIFICACIÓN: Pasos Completados

Una vez que hayas hecho TODO lo anterior, verifica:

```
□ Columna "Originado Por" existe con 7 opciones
□ Columna "Chat Agente" existe
□ Columna "Esfuerzo" existe con XS, S, M, L, XL
□ Columna "Prioridad" existe con Baja, Media, Alta, Crítica

□ Vista "Roadmap por Fase" creada (muestra FASE 0, FASE 1, FASE 2, FASE 3)
□ Vista "Kanban por Estado" creada (TODO, IN PROGRESS, BLOCKED, DONE)
□ Vista "Bloqueadores" creada (solo tareas con Estado = BLOCKED)
□ Vista "Mis Tareas" creada (solo tareas con Asignado a = YO)

□ 5 tareas FASE 0 cargadas
   ├─ Documentar framework BLAST (DONE)
   ├─ Crear 'Sobre Mí' (DONE)
   ├─ Configurar Roadmap Master (IN PROGRESS)
   ├─ Setup NAUTA 8:30 AM (TODO)
   └─ Setup NAUTA 21:30 (TODO)

□ Todas las tareas tienen:
   ├─ Módulo asignado
   ├─ Asignado a (SISTEMA o NAUTA)
   ├─ Estado asignado
   ├─ Originado Por asignado
   ├─ Timeline FASE = FASE 0
   └─ KPI o descripción clara
```

---

## 🎯 Resultado Final

Una vez completado, tu Notion debería verse así:

```
ROADMAP MASTER

┌─ Vista: Database (default table)
│  └─ Muestra todas las propiedades
│
├─ Vista: Roadmap por Fase
│  ├─ FASE 0 (5 tareas)
│  │  ├─ [DONE] Documentar framework BLAST
│  │  ├─ [DONE] Crear 'Sobre Mí'
│  │  ├─ [IN PROGRESS] Configurar Roadmap Master
│  │  ├─ [TODO] Setup NAUTA 8:30 AM
│  │  └─ [TODO] Setup NAUTA 21:30
│  ├─ FASE 1 (vacía)
│  ├─ FASE 2 (vacía)
│  └─ FASE 3 (vacía)
│
├─ Vista: Kanban por Estado
│  ├─ TODO (2 tareas)
│  ├─ IN PROGRESS (1 tarea)
│  ├─ BLOCKED (0 tareas)
│  └─ DONE (2 tareas)
│
├─ Vista: Bloqueadores
│  └─ (vacía - no hay bloqueadores por ahora)
│
└─ Vista: Mis Tareas
   └─ (vacía - solo si Asignado a = YO)
```

---

## 🚀 Próximo Paso

Una vez que completes esto:

→ **Setup cronométrico de NAUTA**
  - 8:30 AM: Briefing automático
  - 21:30: Log de cierre automático

Vamos a configurar esto en el dashboard/API para que se ejecute automáticamente.

---

## ⏱️ Timeline

- **Total time**: ~45 minutos (todo manual en Notion)
- **FASE 1** (Agregar columnas): 5 min
- **FASE 2** (Crear vistas): 10 min
- **FASE 3** (Cargar tareas): 20 min
- **FASE 4** (Configurar botones): 10 min después

