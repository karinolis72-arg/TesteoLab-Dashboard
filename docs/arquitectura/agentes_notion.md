# 🔗 LLAMADAS A AGENTES EN NOTION
**Especificación: Cómo integrar botones "Chat con [Agente]" en Roadmap Master**

---

## 📋 ESTRUCTURA EN NOTION ROADMAP MASTER

Cada módulo (M1-M4) tendrá una columna o sección que permite acceso directo al agente.

### Opción 1: Botones en la Base de Datos (RECOMENDADO)

```
ROADMAP MASTER - Agregamos nueva columna:

Nombre de Columna: "Chat Agente"
Tipo: Button (Botón)
Configuración:
├─ Nombre del botón: "[Chat con Agente]"
├─ Icono: 💬 (chat bubble)
└─ Acción: URL externa

URLs por módulo:
├─ M1: claude://chat/M1-Espía
├─ M2: claude://chat/M2-Crea
├─ M3: claude://chat/M3-Creativo
└─ M4: claude://chat/M4-Meta
```

### Opción 2: Relaciones Directas en Notion (ALTERNATIVA)

```
Crear una tabla "AGENTES" en Notion:

Tabla: AGENTES
├─ Nombre: M1 Espía
├─ Rol: Investigación de ofertas
├─ Chat URL: [Link directo a chat]
├─ Status: Activo
└─ Última actualización: [fecha]

Luego, en ROADMAP MASTER:
├─ Agregar relación: "Agente Asignado" → AGENTES tabla
└─ El botón llama automáticamente al chat del agente relacionado
```

---

## 🎯 FLUJO DE USO: Tú → Botón → Chat con Agente

### Escenario 1: M1 Espía (Investigar oferta)

```
1. ABRES Notion Roadmap Master
2. VES tarea: "Investigar + Validar Oferta [Rituales]"
3. HACES CLIC: [Chat con M1 Espía]
4. SE ABRE: Chat con M1 Espía (en nueva ventana/tab)
5. ESCRIBES: "Necesito espiar ofertas de rituales en Facebook"
6. M1 RESPONDE: 
   - Scrapea Facebook Ads Library
   - Te muestra 5 ofertas similares
   - Te propone: "¿Vamos con ESTA? (x razones)"
7. TÚ CONFIRMAS: "Sí, vamos con esta"
8. M1 ACTUALIZA: 
   - Crea tarea siguiente: "Crear MVP"
   - Marca M1 como DONE
   - Crea nueva tarea para M2
```

### Escenario 2: M2 Crea (Armar oferta)

```
1. ABRES Notion (ahora hay nueva tarea de M2)
2. VES tarea: "Crear MVP + Landing [Rituales]"
3. HACES CLIC: [Chat con M2 Crea]
4. SE ABRE: Chat con M2 Crea
5. ESCRIBES: "Necesito crear un MVP sobre rituales de cierre"
6. M2 RESPONDE:
   - Te pregunta sobre la estructura
   - Propone: guía 15 pág, 3 bonos, testimonio
   - Genera landing HTML preview
7. TÚ APRUEBAS: "Dale, crea el MVP"
8. M2 ACTUALIZA:
   - Genera documento (PDF/DOCX)
   - Sube a Notion
   - Pasa a M3
```

### Escenario 3: M3 Creativo (Generar ángulos)

```
1. ABRES Notion (nueva tarea de M3)
2. VES tarea: "Generar 62 ángulos [Rituales]"
3. HACES CLIC: [Chat con M3 Creativo]
4. SE ABRE: Chat con M3 Creativo
5. ESCRIBES: "Genera ángulos para vender rituales de cierre"
6. M3 RESPONDE:
   - "Necesito algunos detalles. ¿Cuál es el avatar?"
   - "¿Cuál es el main pain point?"
   - "¿Precio low ticket?"
7. RESPONDES sus preguntas
8. M3 CREA:
   - ~62 ángulos diferentes
   - Sugerencias de creativos (imagen/video)
   - Mockups visuales
```

### Escenario 4: M4 Meta (Testing en Meta)

```
1. ABRES Notion (nueva tarea de M4)
2. VES tarea: "Testing + Optimización [Rituales]"
3. HACES CLIC: [Chat con M4 Meta]
4. SE ABRE: Chat con M4 Meta
5. ESCRIBES: "Necesito hacer testing de la campaña en Meta"
6. M4 RESPONDE:
   - "¿Creativos listos?"
   - "¿Presupuesto de test?"
   - "¿Target audience?"
7. RESPONDES
8. M4 CONFIGURA:
   - Sube creativos a Meta Ads Manager
   - Configura A/B tests
   - Genera dashboard en tiempo real
   - "Aquí van tus métricas: [dashboard]"
```

---

## 📊 TAREAS REFLEJADAS EN ROADMAP MASTER

Cada módulo genera automáticamente sus tareas:

```
OFERTA: "Rituales para Cierre de Relaciones"

┌─ M1 Espía (PENDIENTE)
│  Tarea: "Investigar + Validar Oferta Rituales"
│  [Chat con M1 Espía] ← HACES CLIC ACÁ
│  Status: TODO → IN PROGRESS → DONE
│
├─ M2 Crea (BLOQUEADO - espera M1)
│  Tarea: "Crear MVP + Landing Rituales"
│  [Chat con M2 Crea] ← Disponible cuando M1 DONE
│  Status: TODO
│
├─ M3 Creativo (BLOQUEADO - espera M2)
│  Tarea: "Generar 62 ángulos Rituales"
│  [Chat con M3 Creativo]
│  Status: TODO
│
└─ M4 Meta (BLOQUEADO - espera M3)
   Tarea: "Testing + Optimización Rituales"
   [Chat con M4 Meta]
   Status: TODO
```

---

## 🔄 INTEGRACIÓN CON ROADMAP MASTER

### Columnas Esperadas en Notion:

```
ROADMAP MASTER Database Structure:

├─ Name (Título)
├─ Asignado a (Agente/Persona)
├─ Módulo (M1 / M2 / M3 / M4 / NAUTA / SISTEMA)
├─ Estado (TODO / IN PROGRESS / DONE)
├─ Originado Por (Espía / Crea / Creativo / Meta / YO / NAUTA)
├─ Bloqueadores (Si hay algo que impide)
├─ Dependencias (Qué debe estar completo antes)
├─ Chat Agente (BOTÓN) ← ACÁ VAS A HACER CLIC
│  ├─ M1 Espía → [Chat con M1 Espía]
│  ├─ M2 Crea → [Chat con M2 Crea]
│  ├─ M3 Creativo → [Chat con M3 Creativo]
│  └─ M4 Meta → [Chat con M4 Meta]
├─ KPI (Métrica clave del módulo)
└─ Última actualización (fecha)
```

---

## 🚀 CÓMO FUNCIONA TÉCNICAMENTE

### Backend (Notion API):

```python
# Cuando tú haces clic en [Chat con M1 Espía]
def handle_agent_click(agent_name, task_id):
    # 1. Obtén contexto de la tarea
    task = notion.get_page(task_id)
    
    # 2. Obtén contexto del usuario ("Sobre Mí")
    user_context = get_user_context()
    
    # 3. Prepara prompt para el agente
    prompt = f"""
    AGENTE: {agent_name}
    TAREA: {task.name}
    CONTEXTO USUARIO: {user_context}
    
    ¿Qué necesitas hacer?
    """
    
    # 4. Inicia chat con el agente
    open_chat_with_agent(agent_name, prompt)
```

### URL Schema:

```
claude://chat/M1-Espía
claude://chat/M2-Crea
claude://chat/M3-Creativo
claude://chat/M4-Meta
```

O si usas integración web:

```
https://claude.ai/chat?agent=M1-Espía&context=task_[task_id]
```

---

## ✅ SETUP EN NOTION (Paso a Paso)

### 1. Crear columna "Chat Agente"

```
En ROADMAP MASTER:
├─ Click en "+"
├─ Selecciona "Button"
├─ Nombre: "Chat Agente"
├─ Icono: 💬
└─ Crear
```

### 2. Configurar URLs

```
Para cada fila con módulo:

Si es M1:
├─ Click en botón
├─ Configure
├─ URL: claude://chat/M1-Espía?task={task_id}

Si es M2:
├─ URL: claude://chat/M2-Crea?task={task_id}

Etc...
```

### 3. Alternativa: Usar Relaciones

```
Nueva tabla en Notion: AGENTES

├─ M1 Espía
│  ├─ Chat URL: [link directo]
│  └─ Rol: Investigación
│
├─ M2 Crea
│  ├─ Chat URL: [link directo]
│  └─ Rol: Creación
│
├─ M3 Creativo
│  ├─ Chat URL: [link directo]
│  └─ Rol: Creativos
│
└─ M4 Meta
   ├─ Chat URL: [link directo]
   └─ Rol: Métricas

Luego en ROADMAP MASTER:
├─ Agregar columna "Agente Asignado" (relación)
├─ Selecciona agente de la tabla AGENTES
└─ El botón lee la relación y abre el chat
```

---

## 🎯 RESUMEN: TÚ → NOTION → BOTÓN → CHAT → AGENTE

```
Workflow esperado:

1. Abres Notion Roadmap Master
2. Ves tarea: "Investigar ofertas de rituales"
3. Haces clic: [Chat con M1 Espía]
4. Se abre chat con el agente
5. Charlas directamente con el agente
6. El agente crea tareas automáticamente
7. Vuelves a Notion → ves nuevas tareas
8. Repites para M2, M3, M4
9. Al final: Oferta completa + landing + creativos + testing en Meta
```

**VENTAJA:** No saltas entre herramientas. Todo en Notion → Todo integrado.

---

*Especificación lista para implementar. ¿Empezamos con M1 Espía?*
