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

El sistema tiene **4 agentes principales** que trabajan en conjunto:

---

### 1️⃣ AGENTE COACH (NAUTA) — Tu Sistema Personal
**Rol:** Ejecución personal, seguimiento diario y retrospectiva nocturna  
**Marca en BD:** `Originado Por: NAUTA`

**Funciones Clave:**

```
⏰ MAÑANA (9:00 AM)
├─ Lee: Google Calendar de hoy
├─ Genera: Briefing diario (tareas, hábitos, eventos)
├─ Crea: Top 4 tareas prioritarias para el día
├─ Valida: Contra Rueda de Vida (para no descuidar áreas)
└─ Output: Dashboard NAUTA listo para ejecutar

💼 DURANTE EL DÍA
├─ Seguimiento en tiempo real
├─ Alertas si hay bloqueos
├─ Replanificación automática si es necesario
└─ Tracking de hábitos (Pilates, Journaling, etc.)

🌙 NOCHE (6:00 PM)
├─ Lee: Tareas completadas vs. programadas
├─ Genera: "Log de Cierre" (retrospectiva del día)
├─ Analiza: ¿Qué salió bien? ¿Qué no?
├─ Valida: Estado de la Rueda de Vida
├─ Identifica: Áreas con poco foco
├─ Crea: Notas en "Sobre Mí" (decisiones, aprendizajes)
└─ Prepara: Top 4 tareas para MAÑANA
```

**Permisos:**
- Lectura total: Notion + Google Calendar + "Sobre Mí"
- Escritura: Tareas, Hábitos, Notas Diarias

**Inspiración:** Video 1 sobre Context Engineering

---

### 2️⃣ AGENTE BUILDER (OFERTAS) — Tu Sistema de Negocio
**Rol:** Automatizar el flujo completo de creación y escala de ofertas  
**Marca en BD:** `Originado Por: OFERTAS`

**Estructura: 4 Módulos secuenciales**

#### **M1: ESPIONAJE & SELECCIÓN — Agente "Espía"**
```
Pregunta: "¿Qué oferta modelar?"

AGENTE: M1 Espía

Funciones:
├─ Web scraping automático
│  ├─ Facebook Ads Library (por país + keywords)
│  ├─ Etsy (trending products)
│  └─ Clickbank (bestsellers)
├─ Análisis de competencia
│  ├─ ¿Cuántos competidores?
│  ├─ ¿Cuál es el precio?
│  └─ ¿Cuál es el angle de venta?
├─ Detección de tendencias
└─ Output: "Vamos con ESTA oferta"

Tarea en Notion: "Investigar + Validar Oferta [X]"
KPIs: Ofertas identificadas, % Validación demanda

🔗 ACCESO DIRECTO: [Chat con M1 Espía]
```

#### **M2: CREACIÓN DE OFERTA — Agente "Crea"**
```
Pregunta: "¿Cómo armo la oferta?"

AGENTE: M2 Crea

Funciones:
├─ Landing HTML Builder
│  ├─ Estructura persuasiva automática
│  ├─ Copy generado (Shopify-ready)
│  └─ Bloques de conversión pre-diseñados
├─ Estructura de productos (SKU, precio, descripción)
├─ Bonus generator (qué incluir, orden, presentación)
├─ Mockups generator (visuales de la oferta)
└─ Output: Oferta completa lista para vender

Tarea en Notion: "Crear MVP + Landing [Oferta X]"
KPIs: MVP completado (%), Landing CTR esperado

🔗 ACCESO DIRECTO: [Chat con M2 Crea]
```

#### **M3: CREATIVO — Agente "Creativo"**
```
Pregunta: "¿Cómo vendo esto?"

AGENTE: M3 Creativo

Proceso (Guiado):
├─ P1: Extracción de insights
│  ├─ Producto
│  ├─ Avatar (público ideal)
│  ├─ Dolores (pain points)
│  └─ Beneficios
├─ P2: Identidad Visual (marca)
├─ P3: Estilo Visual (realista/ilustrado/3D/etc)
├─ P4: Formatos Creativos (noticiero/infografía/etc)
├─ P5: Análisis IA de competencia visual
├─ P6: Generación de ~62 ángulos de venta
├─ P7: Fábrica de Imágenes
│  ├─ Variaciones automáticas
│  ├─ Edición IA
│  └─ Descarga de creativos
├─ P8: Fábrica de Videos
│  ├─ Guiones con hooks
│  ├─ Escenas generadas (IA o stock)
│  ├─ Voces en off (ElevenLabs)
│  └─ Secuencias editadas
└─ Output: 62+ creativos listos para testear

Tarea en Notion: "Generar 62 ángulos de venta [Oferta X]"
KPIs: Ángulos generados (X/62), Creativos listos (img/video)

🔗 ACCESO DIRECTO: [Chat con M3 Creativo]
```

#### **M4: ANALISTA META — Agente "Meta"**
```
Pregunta: "¿Cómo va en Meta?"

AGENTE: M4 Meta

Funciones:
├─ Integración automática con Meta Ads Manager
├─ Upload de creativos
├─ Dashboard en tiempo real
│  ├─ Métricas: ROAS, CAC, conversiones, presupuesto
│  ├─ A/B testing automático
│  ├─ Recomendaciones de optimización
│  └─ Análisis de rendimiento por ángulo
├─ Decisiones automáticas:
│  ├─ "Tu ROAS es < 1.5, pausa este creativo"
│  ├─ "Este ángulo tiene 60% mejor CTR, aumenta presupuesto"
│  └─ "Encontré 3 segmentos nuevos para testear"
└─ Output: "Tu problema es [landing/oferta/creativo]"

Tarea en Notion: "Testing + Optimización Campaña [Oferta X]"
KPIs: ROAS actual, CTR, CPA

🔗 ACCESO DIRECTO: [Chat con M4 Meta]
```

**Flujo Completo:**
```
M1 (Validar) → M2 (Crear) → M3 (Creativos) → M4 (Meta) → Escala
```

---

### 3️⃣ AGENTE CREATIVO (CONTENIDO)
**Rol:** Generación de assets creativos y contenido  
**Marca en BD:** `Originado Por: CREATIVO`

**Funciones:**
- Generador de hooks y ángulos
- Fábrica de imágenes (variaciones, estilos)
- Fábrica de videos (guiones, secuencias, voces)
- Generador de copy persuasivo
- Análisis visual de competencia

**Integración:** Trabaja bajo las órdenes de M3

---

### 4️⃣ AGENTE ANALISTA (MÉTRICAS)
**Rol:** Interpretación de datos y decisiones  
**Marca en BD:** `Originado Por: SISTEMA`

**Funciones:**
- Dashboard unificado (Vida + Negocio)
- Análisis de ROAS, CTR, CPA
- Recomendaciones de optimización
- Detección de patrones
- Sugerencias de reescalado

**Métricas que trackea:**
```
PERSONAL:
├─ Execution Score (% tareas completadas)
├─ Q1 Score (progreso Q1)
├─ Rueda de Vida (8 áreas)
└─ Hábitos completados

NEGOCIO:
├─ ROAS (Return on Ad Spend)
├─ CTR (Click-through rate)
├─ CPA (Cost per acquisition)
├─ Conversiones
└─ Ingresos por oferta
```

---

### Tabla de Campos "Originado Por"

**En Notion Roadmap Master, cada tarea tiene este campo:**

| Originado Por | Ejemplo | Tipo | Automation |
|---|---|---|---|
| **YO** | Investigar nuevo nicho | Manual | - |
| **NAUTA** | Top 4 tareas de mañana | Sistema | Diario 9 AM + 6 PM |
| **OFERTAS-M1** | Espiar ofertas tendencia | Builder | Cuando se inicia oferta |
| **OFERTAS-M2** | Crear MVP + Landing | Builder | Después de M1 validado |
| **OFERTAS-M3** | Generar 62 ángulos | Creativo | Después de M2 listo |
| **OFERTAS-M4** | Testing en Meta | Analista | Después de creativos listos |
| **SISTEMA** | Sync Notion-Calendar | Automática | Cada 4h |

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

### Ejecución del Sistema Completo

#### 🌅 MAÑANA: NAUTA Briefing (9:00 AM)

```
NAUTA ejecuta automáticamente:

1️⃣ LECTURA DE CONTEXTO
   ├─ Leer: Google Calendar (eventos hoy)
   ├─ Leer: Notas de ayer (Log de Cierre)
   ├─ Leer: Estado Rueda de Vida
   └─ Leer: "Sobre Mí" (proyectos, personas, metodología)

2️⃣ GENERACIÓN DE BRIEFING
   ├─ Crear: Top 4 tareas prioritarias
   ├─ Mapear: A qué área de Rueda de Vida corresponden
   ├─ Incluir: Hábitos esperados hoy
   ├─ Detectar: Áreas con poco foco
   └─ Alertar: Si hay conflictos de horario

3️⃣ PRESENTACIÓN AL USUARIO
   Dashboard muestra:
   ├─ Saludo personalizado
   ├─ Top 4 tareas (con contexto)
   ├─ Hábitos de hoy
   ├─ Próxima acción sugerida
   └─ Rueda de Vida visual

⏱️ Tiempo: 5-10 min para usuario revisar
```

#### 💼 DÍA: Ejecución & Tracking (10 AM - 6 PM)

```
Usuario trabaja en tareas (Top 4 prioridades)

NAUTA en segundo plano:
├─ Trackea progreso en tiempo real
├─ Notifica si hay bloqueadores
├─ Puede sugerir replanificación si es necesario
├─ Ejecuta sincronización Calendar (cada 4h)
└─ No molesta, solo soporta

Agentes OFERTAS pueden estar activos si:
├─ Usuario está en fase M1 (espiar)
├─ Usuario está en fase M2 (crear)
├─ Usuario está en fase M3 (creativos)
├─ Usuario está en fase M4 (testing)
└─ Estos generan tareas en Notion automáticamente
```

#### 🌙 NOCHE: Log de Cierre & Planeación (6:00 PM)

```
NAUTA ejecuta automáticamente:

1️⃣ RETROSPECTIVA DEL DÍA
   ├─ ¿Completaste el Top 4?
   ├─ ¿Cuáles sí, cuáles no?
   ├─ ¿Por qué no completaste los que faltaron?
   └─ ¿Qué aprendiste?

2️⃣ VALIDACIÓN DE RUEDA DE VIDA
   ├─ ¿Tocaste hoy todas las áreas importantes?
   ├─ ¿Hay áreas que están siendo descuidadas?
   ├─ Sugerencia: "Hace 4 días no haces meditación"
   └─ Ajuste automático: "Mañana incluyo meditación en Top 4"

3️⃣ CREACIÓN DE LOG DE CIERRE
   Nota automática en "Sobre Mí":
   ```
   # Log de Cierre - 11/04/2026
   
   TOP 4 COMPROMETIDO:
   ✅ Integrar Google Calendar
   ✅ Validar producto Ofertas
   ❌ Responder emails
   ⏳ Análisis Meta (75% completo)
   
   BLOQUEADORES:
   - Falta código de Calendar API
   
   APRENDIZAJES:
   - El módulo M3 demora más de lo estimado
   
   RUEDA DE VIDA (hoy):
   - Negocios: ✅ (Google Calendar)
   - Salud: ✅ (Pilates 30min)
   - Espiritualidad: ❌ (sin meditación)
   
   MAÑANA INCLUIR: Meditación 10min
   ```

4️⃣ PLANEACIÓN DEL PRÓXIMO DÍA
   ├─ Leer objetivos Q1
   ├─ Revisar tareas pendientes
   ├─ Balancear Rueda de Vida
   ├─ Crear Top 4 tentativo
   └─ Notificar al usuario: "Tus tareas de mañana están listas"

⏱️ Tiempo: Automático (sin intervención del usuario)
```

#### 🎯 Timeline Semanal Adicional

```
CADA LUNES 9:00 AM
├─ NAUTA genera resumen semanal
├─ Métricas de ejecución
├─ Estado de proyectos
└─ Replanificación semanal si es necesario

CADA VIERNES 6:00 PM
├─ ANALISTA genera reporte semanal
├─ Métrica Q1 Score actualizado
├─ Sugerencias de reinversión (si hay ingresos)
└─ Preparación para nueva semana
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

---

## 🗺️ MAPEO A NOTION: ROADMAP MASTER {#mapeo-notion}

### Cómo la Arquitectura de Agentes se Refleja en Tareas

Tu **Roadmap Master** en Notion es el documento central que contiene TODAS las tareas del proyecto TesteoLab. Cada tarea pertenece a un agente y sigue una estructura específica.

#### Estructura de Columnas (Modelo Base)

```
ROADMAP MASTER Database:
├─ Name (Título de tarea)
├─ Asignado a (Persona/Agente)
├─ BLAST Step (Blueprint/Links/Architecture/Stylize/Transfer)
├─ Originado Por (YO / NAUTA / OFERTAS-M1 / OFERTAS-M2 / OFERTAS-M3 / OFERTAS-M4 / CREATIVO / SISTEMA)
├─ Estado (TODO / IN PROGRESS / DONE)
├─ Bloqueadores (Lista de qué impide progreso)
├─ Dependencias (Qué tareas debe completar antes)
├─ Esfuerzo (S / M / L / XL)
└─ Timeline FASE (FASE 0 / FASE 1 / FASE 2)
```

#### Ejemplo: Cómo se ve una Secuencia de Tareas (OFERTAS Workflow)

```
OFERTA: "Rituales para Cierre de Relaciones"

├─ M1: ESPIONAJE & SELECCIÓN
│  ├─ Tarea: "Investigar ofertas de rituales en Facebook Ads"
│  │  ├─ Originado Por: OFERTAS-M1 (SISTEMA crea automáticamente)
│  │  ├─ Asignado a: M1 Analyzer (tú)
│  │  └─ Estado: IN PROGRESS
│  │
│  └─ Tarea: "Validar demanda real para subnicho 'cierre relaciones'"
│     ├─ Originado Por: OFERTAS-M1
│     ├─ Bloqueadores: Ninguno
│     └─ Dependencias: Investigar ofertas (arriba)
│
├─ M2: CREACIÓN DE OFERTA
│  ├─ Tarea: "Crear MVP (Guía 15 páginas)"
│  │  ├─ Originado Por: OFERTAS-M2
│  │  ├─ Asignado a: Builder Agent
│  │  └─ Bloqueadores: Validación de M1
│  │
│  └─ Tarea: "Generar Landing Page HTML"
│     ├─ Originado Por: OFERTAS-M2
│     └─ Dependencias: MVP completado
│
├─ M3: CREATIVO
│  └─ Tarea: "Generar 62 ángulos de venta + creativos"
│     ├─ Originado Por: OFERTAS-M3 (CREATIVO agent)
│     ├─ Subtareas:
│     │  ├─ P1: Extracción de insights
│     │  ├─ P2: Identidad Visual
│     │  ├─ P3: Estilo Visual
│     │  ├─ P4: Formatos Creativos
│     │  ├─ P5: Análisis competencia visual
│     │  ├─ P6: Generación ~62 ángulos
│     │  ├─ P7: Fábrica de imágenes
│     │  └─ P8: Fábrica de videos
│     └─ Bloqueadores: Landing completada
│
└─ M4: ANALISTA META
   ├─ Tarea: "Setup Meta Ads Campaign"
   │  ├─ Originado Por: OFERTAS-M4
   │  └─ Dependencias: Creativos listos
   │
   └─ Tarea: "Testing + Optimización"
      ├─ Originado Por: OFERTAS-M4 (ANALISTA)
      ├─ Métrica: ROAS >= 1.5 para escala
      └─ Próximo: Escala progresiva
```

#### Ejemplo: Cómo se ve una Secuencia NAUTA

```
SISTEMA PERSONAL (Diario)

├─ CADA MAÑANA (9:00 AM)
│  └─ Tarea: "[RECURRENTE] NAUTA Briefing - Top 4 Tareas Hoy"
│     ├─ Originado Por: NAUTA
│     ├─ Asignado a: Sistema Automático
│     ├─ Recurrencia: Diaria
│     └─ Output: Dashboard actualizado + Notificación
│
├─ [Tareas generadas automáticamente por NAUTA para hoy]
│  ├─ "Integración Google Calendar" (Top 1)
│  ├─ "Validar producto Ofertas" (Top 2)
│  ├─ "Pilates 30min" (Hábito)
│  └─ "Reunion mentor 4PM" (Evento Calendar)
│
└─ CADA NOCHE (6:00 PM)
   └─ Tarea: "[RECURRENTE] Log de Cierre - Retrospectiva Día"
      ├─ Originado Por: NAUTA
      ├─ Asignado a: Sistema Automático
      ├─ Output: Nota en "Sobre Mí" + Top 4 mañana
      └─ Detecta: Áreas poco desarrolladas en Rueda de Vida
```

#### Ejemplo: Cómo se ve el Roadmap Master Completo

```
ROADMAP MASTER - Vista Kanban por Estado:

TODO (20 tasks):
├─ [M1] Espiar ofertas rituales
├─ [M2] Crear MVP ebook
├─ [M3] Generar 62 ángulos
├─ [M4] Setup Meta campaign
├─ [NAUTA] Testing autom. briefing
├─ [SISTEMA] Setup cronométrica 9 AM
├─ [Dashboard] Implementar Rueda de Vida
└─ ...

IN PROGRESS (5 tasks):
├─ [Sprint 1] Integración Google Calendar → 70%
├─ [Dashboard] NAUTA módulo básico → 80%
├─ [M3] P6: Generación ángulos → 30%
├─ [Notion] Agregar campo "Originado Por"
└─ [API] notion_api.py mejoras

DONE (15 tasks):
├─ [Framework] Documentar BLAST + Context Engineering ✅
├─ [Spec] TesteoLab v2.0 completo ✅
├─ [Settings] Idioma + Tema selector ✅
├─ ...
```

#### Campos Esenciales en el Roadmap Master

**"Originado Por" valores esperados:**

```
VALOR: YO
├─ Significado: Creaste manualmente
├─ Ejemplo: "Investigar nuevo nicho"
└─ Automation: Ninguna

VALOR: NAUTA
├─ Significado: Top 4 diarios o sugerencia coach
├─ Ejemplo: "Top 4 de mañana"
└─ Automation: Cada mañana 9 AM + noche 6 PM

VALOR: OFERTAS-M1
├─ Significado: Fase de investigación
├─ Ejemplo: "Espiar ofertas de rituales"
└─ Automation: Al iniciar oferta nueva

VALOR: OFERTAS-M2
├─ Significado: Creación de MVP + Landing
├─ Ejemplo: "Crear MVP 15 páginas"
└─ Automation: Cuando M1 validado

VALOR: OFERTAS-M3
├─ Significado: Generación de creativos
├─ Ejemplo: "Generar 62 ángulos"
└─ Automation: Cuando M2 listo

VALOR: OFERTAS-M4
├─ Significado: Testing en Meta
├─ Ejemplo: "Testing + Optimización campaña"
└─ Automation: Cuando creativos listos

VALOR: CREATIVO
├─ Significado: Assets creativos puros
├─ Ejemplo: "Editar videos anuncios"
└─ Automation: Bajo órdenes de M3

VALOR: SISTEMA
├─ Significado: Automatizaciones
├─ Ejemplo: "Sync Notion-Calendar cada 4h"
└─ Automation: Cron jobs programados
```

---

*Documento vivo. Se actualiza conforme a avances en cada sprint.*

**Próxima revisión:** Después de completar Sprint 1

**Última actualización:** 11 de Abril 2026 - Versión 2.0 (Agentes + Módulos OFERTAS M1-M4 + NAUTA Completo)
