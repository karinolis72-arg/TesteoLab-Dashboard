# 🎯 TesteoLab - Sistema Completo v2.0
**Documento Maestro de Arquitectura, Agentes y Operaciones**

---

**Versión:** 2.0  
**Fecha:** 11 de Abril 2026  
**Usuario:** Roxana Karina Ordoqui (Karina/Kari)  
**Estado:** Framework + Especificación técnica integrada

---

## 📑 ÍNDICE

1. [Visión y Propósito](#visión)
2. [Framework BLAST Aplicado](#blast)
3. [Módulo "Sobre Mí" - Context Engineering](#sobre-mi)
4. [Sistema de Agentes](#agentes)
5. [Roadmap de Ofertas](#roadmap-ofertas)
6. [Dashboard NAUTA - Especificación Técnica](#nauta-tech)
7. [Flujo Operacional Diario](#flujo-operacional)
8. [Implementación Sprint by Sprint](#sprints)

---

## 🎯 VISIÓN Y PROPÓSITO {#visión}

### Declaración de Intención

**TesteoLab es un ecosistema personal de IA que integra:**

1. **Planificación Inteligente** (NAUTA) - Briefinings diarios basados en contexto personal
2. **Operación de Negocios Digitales** (Ofertas) - Análisis, creación y optimización de infoproductos
3. **Automatización Sistémica** (Sistema) - Procesos que corren sin intervención manual
4. **Desarrollo Personal Continuo** (Sobre Mí) - Base de datos viva del aprendizaje y evolución

### Objetivos Primarios

**Financiero:**
- Generar ingresos sostenibles mediante productos digitales (low ticket + mid ticket)
- Escalar oferta de análisis y asesoría (Ofertas module)
- Automatizar el 80% de procesos operacionales

**Intelectual:**
- Dominar metodologías de: marketing digital, trading, IA aplicada, desarrollo personal
- Crear frameworks propios que integren estos mundos
- Documentar aprendizajes en "Sobre Mí" para que agentes tengan contexto

**Personal:**
- Trabajar con creatividad, autonomía y constancia
- Tomar decisiones basadas en datos, no intuición
- Mantener equilibrio entre exploración y ejecución

---

## 🏗️ FRAMEWORK BLAST APLICADO {#blast}

### Paso 1: BOSQUEJO (Blueprint)

**North Star:**
"Quiero que el usuario pueda ejecutar su negocio digital desde un dashboard inteligente que entienda quién es, qué vende, y sugerir acciones diarias."

**Integraciones:**
- Notion (Base de datos principal)
- Google Calendar (Eventos y tareas)
- Google Sheets (Análisis de métricas)
- Meta Ads API (Campañas)
- Stripe/Hotmart (Pagos)
- OpenAI API (Procesamiento de IA)

**Source of Truth:**
- Notion workspace como base de datos primaria
- "Sobre Mí" folder como contexto de usuario
- Google Calendar como fuente de tiempo/eventos

**Delivery Payload:**
- Dashboard web responsivo (TesteoLab Dashboard)
- Módulos: NAUTA, Ofertas, Tracker, Habitos, Calendar, etc.
- Notificaciones inteligentes (coach mode)

**Behavior Rules:**
- NAUTA siempre responde en español, tono conversacional
- Los agentes respetan límites: no venden lo que el usuario marcó como "no vendo"
- Las tareas creadas automáticamente se marcan con origen "Agente"
- Las tareas manuales se marcan con origen "YO"

---

### Paso 2: LAZOS (Links) - Validación de Conexiones

**✅ Conexiones Validadas:**

| Sistema | Status | Token | Notas |
|---------|--------|-------|-------|
| Notion API | ✅ Activo | ntn_[REDACTADO] | TAREAS_DB, HABITOS_DB, etc. |
| Google Calendar | ✅ Activo | OAuth 2.0 | Leer eventos, crear eventos |
| Google Sheets | 🔄 Pendiente | Credenciales | Para análisis de métricas |
| Meta Ads | 🔄 Pendiente | App ID | Para automatizar campañas |
| OpenAI API | ✅ Activo | sk-proj... | Para procesamiento de prompts |

---

### Paso 3: ARQUITECTURA (Architecture)

**Tres Capas:**

#### Capa 1: SOPs (Standard Operating Procedures)
Documentos Markdown que definen cada función:
- `SOP_NAUTA_BRIEFING.md` - Cómo NAUTA genera briefings
- `SOP_OFERTAS_ANALYZER.md` - Cómo analizar ofertas
- `SOP_HABITTRACKER.md` - Cómo trackear hábitos

#### Capa 2: Navegación (Routing)
La IA razona entre SOPs:
- Si usuario pregunta por tareas → llama `/api/nauta/briefing`
- Si usuario pregunta por ofertas → llama `/api/ofertas/analyze`
- Si usuario pregunta por hábitos → llama `/api/habits/track`

#### Capa 3: Herramientas Determinísticas
Scripts Python atómicos:
- `notion_api.py` - Query Notion
- `calendar_sync.py` - Sincronizar Google Calendar
- `ofertas_analyzer.py` - Análisis de ofertas

---

### Paso 4: STILIZACIÓN (Stylize)

**Temas Disponibles:**
- ☀️ CLARA (Predeterminado)
- 🌙 DARK
- ⚪ MINIMAL
- 🎨 COLORFUL
- ⚡ ENERGY

**Componentes UI:**
- Dashboard principal con 8 módulos
- Notificaciones toast (esquina inferior derecha)
- Settings modal con preferencias
- Sidebar colapsable
- Keyboard shortcuts (Ctrl+Shift+S, ESC)

---

### Paso 5: TRANSFERENCIA (Trigger/Deploy)

**Desarrollo:**
- Local en `http://127.0.0.1:5000` (Flask)
- Hot reload con Ctrl+Shift+R

**Producción:**
- Será deployado en Render/Vercel cuando esté listo
- Variables de entorno en `.env`
- CI/CD con GitHub

---

## 🧠 MÓDULO "SOBRE MÍ" - CONTEXT ENGINEERING {#sobre-mi}

### Concepto Central

Cada agente tiene acceso a una base de datos viva que responde preguntas sobre ti:
- ¿Quién es este usuario?
- ¿Qué vende?
- ¿Cómo toma decisiones?
- ¿Cuál es su voz/tono?
- ¿Cuáles son sus límites?

### Estructura en Notion

```
📦 SOBRE MÍ (Database)
├── 📄 Perfil General
│   ├── Nombre completo
│   ├── Edad / Género
│   ├── Roles activos
│   ├── Objetivos 3-12 meses
│   ├── Métrica de éxito principal
│   └── Horarios preferidos
│
├── 👥 Personas Clave
│   ├── [Nombre]: [Relación, contexto, qué aprendo]
│   ├── [Nombre]: [...]
│   └── [...]
│
├── 💼 Proyectos & Productos
│   ├── [Proyecto]: Descripción, estado, metrics
│   ├── [Proyecto]: ...
│   └── [...]
│
├── 📢 Ofertas Activas
│   ├── [Oferta 1]: Descripción, precio, audiencia
│   ├── [Oferta 2]: ...
│   └── [...]
│
├── ⚙️ Metodología
│   ├── Cómo lanzo ofertas
│   ├── Cómo trackeo resultados
│   ├── Cómo decido qué vender
│   └── Frameworks que uso
│
├── 🚫 Límites & Valores
│   ├── "NO vendo X"
│   ├── "SÍ vendo X cuando..."
│   ├── Mi público ideal es...
│   └── Mis principios son...
│
└── 📈 Transcripciones & Notas
    ├── Charlas importantes
    ├── Notas diarias
    └── Aprendizajes clave
```

### Inyección de Contexto en Prompts

Cada vez que NAUTA o cualquier agente ejecuta:

```python
# En el backend (notion_api.py)
def get_user_context():
    """Obtiene todo el contexto de 'Sobre Mí'"""
    perfil = notion.query("SOBRE_MI/Perfil General")
    personas = notion.query("SOBRE_MI/Personas")
    proyectos = notion.query("SOBRE_MI/Proyectos")
    # ... etc
    
    return f"""
    # Contexto de Usuario
    
    {perfil}
    
    Personas clave: {personas}
    
    Proyectos activos: {proyectos}
    
    ...
    """

# En el prompt de NAUTA:
context = get_user_context()
prompt = f"""
{context}

Basado en este contexto, aquí están las tareas/sugerencias de hoy:
...
"""
```

---

## 🤖 SISTEMA DE AGENTES {#agentes}

### Definición de Agentes

Un **agente** es un módulo autónomo del sistema que ejecuta funciones específicas, tiene acceso a "Sobre Mí", y marca todo lo que genera con su nombre.

### Los 4 Agentes Principales

#### 1️⃣ YO (Manual)
**Rol:** Creador humano de tareas y decisiones  
**Origen:** Lo que tú escribes/creas manualmente  
**Permisos:** Lectura/escritura total en Notion  
**Marca en BD:** `Originado Por: YO`

**Ejemplos:**
- Tarea que creaste manualmente en Notion
- Nota diaria que escribiste
- Producto que definiste

---

#### 2️⃣ NAUTA
**Rol:** Asistente coach inteligente + briefing diario  
**Función:** 
- Ejecuta diariamente a las 9:00 AM
- Pregunta qué hiciste, qué necesitas, dónde estás trabado
- Sugiere next steps basado en tareas, hábitos, calendario
- Crea subtareas o ajusta prioridades

**Permisos:** 
- Lectura total de Notion + Calendar
- Escritura limitada (solo crea/actualiza tareas)

**Marca en BD:** `Originado Por: NAUTA`

**Prompt Base:**
```
Eres NAUTA, un coach inteligente para {user_name}.

Contexto sobre {user_name}:
{user_context}

Tu propósito es:
1. Preguntar sobre su día
2. Entender sus blockers
3. Sugerir acciones basado en su contexto

Hoy es {fecha}. El usuario debería estar trabajando en:
{tareas_programadas}

Responde en español, conversacional, empático pero directo.
```

---

#### 3️⃣ OFERTAS (Analyzer & Strategist)
**Rol:** Analiza, crea y optimiza productos/ofertas  
**Función:**
- Analiza ofertas de competidores
- Sugiere ángulos de subnicho
- Crea guiones/copy
- Calcula ROAS y métricas de venta

**Permisos:**
- Lectura de SOBRE_MI/Ofertas Activas
- Escritura en tabla de análisis

**Marca en BD:** `Originado Por: OFERTAS`

**Flujo (ver sección [Roadmap Ofertas](#roadmap-ofertas)):**
1. Validación de producto
2. Creación de MVP
3. Landing page
4. Anuncios
5. Testing & Optimización
6. Escala

---

#### 4️⃣ SISTEMA
**Rol:** Gestor de automatizaciones y Roadmap Master  
**Función:**
- Ejecuta cronjobs programados
- Sincroniza Notion ↔ Calendar
- Crea reportes de métricas
- Actualiza tableros de estado

**Permisos:**
- Full access (es el infraestructura)

**Marca en BD:** `Originado Por: SISTEMA`

**Tareas automatizadas:**
- 9:00 AM: Ejecutar NAUTA briefing
- 12:00 PM: Sincronizar Calendar
- 6:00 PM: Summarizar día y actualizar notas
- Cada 4h: Sincronizar Notion-Calendar

---

### Tabla de Campos "Originado Por"

**En Notion, cada tarea tiene este campo:**

| Originado Por | Ejemplo | Automation |
|---|---|---|
| **YO** | Crear producto nuevamente | Manual |
| **NAUTA** | Revisar métricas Q1 | Diario 9 AM |
| **OFERTAS** | Testear ángulo de subnicho | Cuando se crea oferta |
| **SISTEMA** | Sync Calendar events | Cada 4h |

---

## 📊 ROADMAP DE OFERTAS {#roadmap-ofertas}

### El Flujo Completo (Basado en documentación adjunta)

#### ETAPA 1: Investigación & Validación
**Objetivo:** Elegir un producto vendible con demanda real

**Actividades:**
1. Investigación de nicho (buscar en Facebook Ads Library, ETSY, Clickbank)
2. Selección de oferta (qué es lo que se está vendiendo bien)
3. Análisis de mercado (competidores, precios, ángulos)
4. Selección de subnicho (edad, experiencia, contexto específico)

**Criterios de Validación:**
- ✅ Alta demanda real
- ✅ Problema específico que resuelve
- ✅ Público que paga rápido
- ✅ Margen de ganancia viable

**Output:** Ficha de producto validado en Notion

---

#### ETAPA 2: MVP & Activos Publicitarios
**Objetivo:** Tener un ecosistema listo para vender

**Deliverables:**
1. MVP (Mínimo Viable Product)
   - Guía de 10-20 páginas
   - Herramientas: Gama App, Canva, AI
   - Tiempo: 2-3 días máximo
   
2. Activos publicitarios
   - Fanpage preparada
   - Perfil personal optimizado
   - Pixel de Meta instalado
   - Calentamiento de perfil (primeras interacciones)

**Plataforma de hosting:** Hotmart
**Razón:** Automatizaciones de email, pasarela, integraciones

---

#### ETAPA 3: Infraestructura & Contenido
**Objetivo:** Construir máquina de conversión optimizada

**Componentes:**

1. **Landing Page**
   - Estructura persuasiva (dolor → promesa → prueba → acción)
   - Ganchos: urgencia, escasez, testimonios
   - Herramienta: Divi en Hostinger ($7/mes) O Lovable/Gama

2. **Copywriting**
   - Guiones para anuncios (texto + audio)
   - Herramientas: Claude, ChatGPT, ElevenLabs
   - Prompts listos en Notion

3. **Creativos (Video/Imagen)**
   - Formato vertical (9x16 para stories)
   - UGC o IA-generated
   - Herramientas: Sora, Midjourney, Runway, clips de TikTok

4. **Pixel de Meta**
   - Instalado en landing + Hotmart
   - Tracking de: visitas, pagos iniciados, compras, upsells

---

#### ETAPA 4: Testeo & Validación
**Objetivo:** Validar anuncios ganadores

**Proceso:**
1. Crear 10-12 anuncios (variaciones)
2. Groupear en $2 test sets
3. Analizar métricas clave:
   - **CTR:** Click-through rate (% personas que hacen clic)
   - **CPA:** Cost per acquisition (cuánto cuesta una venta)
   - **ROAS:** Return on ad spend (dinero ganado / dinero invertido)
   
4. Criterio de éxito: **ROAS ≥ 1.5**
   - Si ROAS < 1.5: Mejorar copy, landing, oferta
   - Si ROAS ≥ 1.5: Pasar a escala

**Decisión Tree:**
```
¿Pocos pagos iniciados?
  → Landing page es mala
  
¿Muchos pagos iniciados, pocas compras?
  → Checkout/apariencia de pago es mala
  
¿Buenos pagos iniciados pero pocas compras?
  → Tu oferta no es lo suficientemente llamativa
```

---

#### ETAPA 5: Optimización & Escala
**Objetivo:** Aumentar ticket promedio y rentabilidad

**Estrategias:**

1. **Order Bumps** (Upsells)
   - Producto complementario que resuelve problema futuro
   - Ejemplo: Bajé de peso → ahora tengo estrías → cream antiestrias
   - Máximo 3 por página (evitar confusión)

2. **Campañas CBO** (Campaign Budget Optimization)
   - Dejar que Meta distribuya presupuesto automáticamente
   - Requiere ROAS ≥ 1.5

3. **Escala Progresiva**
   - Día 1: $10 test
   - Día 2: $20
   - Día 3: $40
   - Día 4: $50
   - ...hasta encontrar el límite (cuando Facebook no encuentra más clientes)

4. **Múltiples Productos**
   - No depender de uno solo
   - Tener 3-4 productos activos en paralelo
   - Rotar presupuesto según ROAS

---

#### ETAPA 6: Automatización & Reinversión
**Objetivo:** Sistema sostenible y escalable

**Automatizaciones:**
- Respuesta automática de comentarios (herramientas como Pancake)
- Upsells dentro del curso
- Email sequences automáticas
- Reporte de métricas diarias

**Reinversión:**
- Hotmart paga cada 15 días (o cada 2 días si facturación > $2,000)
- NO sacar el dinero → reinvertir en nuevos anuncios
- Diversificar: 70% anuncios, 20% nuevos productos, 10% desarrollo personal

---

### Estado Actual del Roadmap OFERTAS

**Productos en Desarrollo:**

| Producto | Etapa | ROAS | Status |
|----------|-------|------|--------|
| Rituales (Ofertas variadas) | Testing | TBD | 🔄 En validación |
| MenteEnOFF | Ideación | - | 📋 Planificación |
| Educación Financiera | Backlog | - | ⏳ Por empezar |
| Trading para +40 | Backlog | - | ⏳ Investigación |

---

## 🎯 DASHBOARD NAUTA - ESPECIFICACIÓN TÉCNICA {#nauta-tech}

### Módulo NAUTA: Briefing Inteligente Diario

**Ubicación en Dashboard:** Pestaña principal (primera)

**Componentes:**

#### 1. Saludo Personalizado
```
Hola Roxana 👋
Miércoles, 11 de Abril de 2026 | 9:00 AM

Tu energía hoy: [barra visual 0-100%]
```

#### 2. Preguntas Diarias (Coach Mode)
Si el usuario tiene "Modo Coach" activado en Settings:
```
¿Qué tal tu día de hoy?
¿Qué tareas prioritarias tenés?
¿Hay algo donde te sentís perdido?
¿Algún blocker o decisión pendiente?

[Input textarea]
[Botón: Procesar con NAUTA]
```

#### 3. Tareas de Hoy
```
TAREAS HOY (6)
└─ [Top 3 Q1] Integración Google Calendar a NAUTA ⭐⭐⭐
└─ [Top 3 Q1] Validación de producto Ofertas 1 ⭐⭐
└─ [Hoy] Responder emails del roadmap
└─ [Hoy] Análisis de métricas Meta Ads
└─ [Hábito] Pilates - 30min
└─ [Evento] Reunión con mentor - 4 PM
```

#### 4. Hábitos Esperados Hoy
```
HÁBITOS ESPERADOS (4)
├─ ✅/❌ Pilates (30 min)
├─ ✅/❌ Journaling (15 min)
├─ ✅/❌ Meditación (10 min)
└─ ✅/❌ Lectura Arcana (20 min)
```

#### 5. Próxima Acción Sugerida
```
🎯 NEXT STEP SUGERIDO
Basado en tus tareas y contexto:

"Debería empezar por terminar la integración de Google Calendar a NAUTA (es crítica para las otras 3 tareas de hoy)"

[Botón: Comenzar esta tarea]
```

#### 6. Rueda de Vida
```
RUEDA DE VIDA (8 áreas)
     Negocios ███████░ (7/10)
      Finanzas ██████░░ (6/10)
      Salud ████████░ (8/10)
   Relaciones ███████░ (7/10)
   Aprendizaje █████████ (9/10)
   Espiritualidad ███████░ (7/10)
     Creación ████████░ (8/10)
       Ocio ███░░░░░░ (3/10)
```

#### 7. Resumen de Métricas (si existe data)
```
MÉTRICAS SEMANA
├─ Tareas completadas: 23/28 (82%)
├─ Hábitos completados: 18/20 (90%)
├─ Ofertas analizadas: 5
└─ Ingresos: $156 (Meta Ads + Hotmart)
```

---

### Funcionamiento Técnico

#### Trigger: Ejecución Cronométrica

```python
# En /cron/nauta_briefing.py
import schedule
import time

def trigger_nauta_briefing():
    """Se ejecuta diariamente a las 9:00 AM"""
    
    # 1. Obtener contexto del usuario
    user_context = get_user_context()
    
    # 2. Consultar Notion: tareas, hábitos, calendario
    today_tasks = query_notion_tareas(fecha_hoy=today)
    today_habits = query_notion_habitos(fecha_hoy=today)
    today_events = get_calendar_events(fecha_hoy=today)
    
    # 3. Procesar con Claude
    response = call_claude_with_context(
        context=user_context,
        tasks=today_tasks,
        habits=today_habits,
        events=today_events
    )
    
    # 4. Actualizar dashboard
    update_dashboard_briefing(response)
    
    # 5. Enviar notificación
    send_notification("NAUTA: Tus tareas de hoy están listas")

# Scheduling
schedule.every().day.at("09:00").do(trigger_nauta_briefing)

# Ejecutar en loop
while True:
    schedule.run_pending()
    time.sleep(60)
```

#### Procesamiento del Response del Usuario

Cuando el usuario responde a las preguntas de NAUTA:

```python
def process_nauta_response(user_input: str):
    """
    User: "Hoy necesito acabar de validar la oferta de rituales,
    pero me estoy perdido con cuál ángulo elegir"
    """
    
    # 1. Extraer información con Claude
    extracted = extract_intent(user_input)
    # Output: {
    #   "tareas_nuevas": ["Validar ángulo de rituales"],
    #   "blockers": ["indecisión en ángulo de subnicho"],
    #   "necesita_ayuda": True
    # }
    
    # 2. Crear tareas automáticamente
    for tarea in extracted["tareas_nuevas"]:
        create_task_in_notion(
            titulo=tarea,
            originado_por="NAUTA",
            fecha=today,
            prioridad="Alta"
        )
    
    # 3. Si hay blocker, enviar análisis
    if extracted["blockers"]:
        analysis = call_ofertas_analyzer(
            blockers=extracted["blockers"],
            context=user_context
        )
        send_message_to_user(analysis)
    
    # 4. Actualizar briefing
    update_nauta_briefing(extracted)
```

---

## 📅 FLUJO OPERACIONAL DIARIO {#flujo-operacional}

### Timeline Diario Recomendado

```
⏰ 9:00 AM
├─ NAUTA ejecuta: "¿Qué tal tu día?"
├─ Usuario responde (5-10 min)
└─ Dashboard actualiza tareas/prioridades

⏰ 10:00 AM - 1:00 PM
├─ Usuario trabaja en tareas prioritarias
├─ NAUTA monitoea progreso (sin molestar)
└─ Sistema sincroniza Calendar cada 4h

⏰ 1:00 PM
├─ Pausa + Almuerzo
└─ Hábitos de mediodía (si los hay)

⏰ 2:00 PM - 5:00 PM
├─ Continua trabajo en tareas
├─ Análisis de métricas (si es momento de testing)
└─ Responder emails/comentarios (automático si es posible)

⏰ 6:00 PM
├─ SISTEMA: Resumen diario
├─ Actualizar Notas Diarias en "Sobre Mí"
├─ Reportar: tareas completadas, hábitos, métricas
└─ Usuario revisa briefing de mañana

⏰ 8:00 PM - 9:00 PM
├─ Tiempo de creación personal
├─ Journaling/reflexión
└─ Planeación discrecional
```

---

## 🚀 IMPLEMENTACIÓN SPRINT BY SPRINT {#sprints}

### Sprint 1 (Actual): NAUTA Básico + Integración Calendar
**Duración:** 2 semanas
**Estado:** 70% completado

- [x] Dashboard frontend (NAUTA módulo)
- [x] Notion API integration (TAREAS_DB, HABITOS_DB)
- [x] Google Calendar API integration
- [x] Settings panel (Idioma + Tema)
- [x] Notificaciones toast
- [ ] **PENDIENTE:** Cronometrado de NAUTA (9 AM ejecución)
- [ ] **PENDIENTE:** Procesamiento de respuestas del usuario
- [ ] **PENDIENTE:** Rueda de Vida (cálculo automático)

**Blocker actual:** Token de Notion inválido (RESUELTO 11/04)

---

### Sprint 2: Cronometrización de NAUTA
**Duración:** 1 semana

- [ ] Setup de scheduler (APScheduler o Celery)
- [ ] Implementar `trigger_nauta_briefing()`
- [ ] Persistencia de notas diarias
- [ ] Notificaciones desktop (Notification API)
- [ ] Testing de cronograma

---

### Sprint 3: Módulo OFERTAS
**Duración:** 2 semanas

- [ ] Crear tabla "Análisis de Ofertas" en Notion
- [ ] Endpoint `/api/ofertas/analyze`
- [ ] Prompt de análisis de nicho/subnicho
- [ ] Generador de guiones publicitarios
- [ ] Dashboard de métricas (ROAS, CPA, CTR)

---

### Sprint 4: Automatizaciones SISTEMA
**Duración:** 2 semanas

- [ ] Cronjobs: sincronización Calendar
- [ ] Reportes diarios automáticos
- [ ] Backup de Notion → GitHub
- [ ] Email digests
- [ ] Alertas de métricas

---

### Sprint 5: Perfeccionamiento & Deploy
**Duración:** 1 semana

- [ ] Testing E2E
- [ ] Optimización de velocidad
- [ ] Deploy a Render/Vercel
- [ ] Documentación de usuario
- [ ] Capacity para escalabilidad

---

## 📋 CAMPO "ORIGINADO POR" - ESPECIFICACIÓN

**Se agrega a TODAS las tablas de Notion que generen items:**

### Ubicación
```
Tabla: TAREAS
├─ Nombre (Title)
├─ Descripción
├─ Estado [TODO / IN PROGRESS / DONE]
├─ Fecha Programada
├─ Prioridad
├─ Flag_Q (Q1, Q2, etc.)
├─ Duración
├─ Asignado a (YO, NAUTA, OFERTAS, SISTEMA)
└─ ✨ Originado Por [NUEVO CAMPO]
    ├─ YO
    ├─ NAUTA
    ├─ OFERTAS
    └─ SISTEMA
```

### Lógica de Asignación

```javascript
// En notion_api.py, cuando se crea una tarea:

if (task.created_by === USER_ID) {
  task.originado_por = "YO"
} else if (task.created_by === NAUTA_AGENT_ID) {
  task.originado_por = "NAUTA"
} else if (task.created_by === OFERTAS_AGENT_ID) {
  task.originado_por = "OFERTAS"
} else if (task.created_by === SISTEMA_AGENT_ID) {
  task.originado_por = "SISTEMA"
}
```

---

## 🎓 CONCLUSIÓN: La Visión Unificada

**TesteoLab v2.0 integra:**

1. **Framework BLAST** para construcción de apps
2. **Context Engineering** ("Sobre Mí") para que la IA te entienda
3. **Sistema de Agentes** (YO, NAUTA, OFERTAS, SISTEMA)
4. **Roadmap Completo de Ofertas** (Investigación → Escala)
5. **Dashboard NAUTA** como interfaz unificada

**El resultado:** Un ecosistema donde:
- ✅ La IA sabe quién eres (Sobre Mí)
- ✅ Ella sugiere acciones inteligentes (NAUTA)
- ✅ Que se alinean con tu negocio (OFERTAS)
- ✅ Y se ejecutan automáticamente (SISTEMA)

**Métrica de éxito final:**
"El usuario puede trabajar 3 horas/día y generar los mismos resultados que antes con 8 horas/día, porque la IA hace el trabajo sistemático."

---

*Documento vivo. Se actualiza conforme a avances en cada sprint.*

**Próxima revisión:** Después de completar Sprint 1
