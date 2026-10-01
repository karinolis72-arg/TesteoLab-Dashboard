# El Framework BLAST para Construir Apps Full Stack con IA

## ¿Qué es el Framework BLAST?

BLAST es un sistema de cinco pasos diseñado para construir aplicaciones full stack con herramientas de IA generativa de forma ordenada, sin cometer errores costosos y con resultados predecibles. El nombre es un acrónimo donde cada letra representa una etapa del proceso:

| Letra | Inglés | Español |
|-------|--------|---------|
| **B** | Blueprint | Bosquejo |
| **L** | Links | Lazos |
| **A** | Architecture | Arquitectura |
| **S** | Stylize | Stilización |
| **T** | Trigger / Deploy | Transferencia al cloud |

La idea central del framework es separar responsabilidades: antes de escribir una sola línea de código, se define exactamente qué se quiere construir, a qué se va a conectar, cómo va a funcionar por dentro, cómo va a verse y dónde va a vivir en producción.

---

## Por qué importa este framework

La mayoría de las apps construidas con IA generativa fallan por tres razones: se ven mal, no funcionan, o no resuelven un problema real. El framework BLAST ataca estos tres problemas en orden. Además, trabaja sobre una arquitectura de tres capas que separa:

1. **Los SOPs técnicos** (documentos en markdown que definen metas, inputs, lógica y casos borde)
2. **La capa de razonamiento** (navegación entre herramientas, sin ejecutar lógica compleja directamente)
3. **Los scripts determinísticos** (código Python atómico y testeable, con variables de entorno en `.env`)

El principio fundamental es que los LLMs son probabilísticos —si hacés la misma pregunta 100 veces obtenés 100 respuestas distintas— pero la lógica de negocio de una app tiene que ser determinística. Separar estas capas resuelve ese problema.

---

## Paso 1 — B: Bosquejo (Blueprint)

### ¿Qué es?

Es la etapa de definición lógica. Acá le explicás a la IA en lenguaje natural exactamente qué querés construir, sin tocar código todavía. Es el paso más importante del proceso porque **el problema que resolvés importa más que cómo lo resolvés**.

### Las cinco preguntas que tenés que responder antes de arrancar

Antes de darle cualquier instrucción a la IA, necesitás tener claras estas cinco cosas:

**1. Estrella del norte (North Star)**
¿Cuál es el resultado deseado? ¿Qué querés que haga la app? Formulalo como "quiero que el usuario pueda hacer X". Si no está claro, la IA va a pedir preguntas de clarificación.

**2. Servicios externos (Integraciones)**
¿Con qué sistemas externos se va a conectar? Listá todas las integraciones: bases de datos, APIs, servicios de terceros, herramientas de automatización. Ejemplo: Reddit para scraping, Supabase como base de datos, Notion para notas, YouTube para métricas.

**3. Fuente de verdad (Source of Truth)**
¿Dónde vive el dato primario? Tiene que haber un solo lugar donde los datos son la verdad oficial. En la mayoría de los casos esto es la base de datos principal (por ejemplo, Supabase).

**4. Entrega (Delivery Payload)**
¿Cómo y dónde se entrega el resultado final? ¿Es un dashboard? ¿Una interfaz de chat? ¿Tabs específicas? Cuanto más concreto seas acá, mejor va a ser el output.

**5. Reglas de comportamiento (Behavior Rules)**
¿Cómo tiene que comportarse el sistema? Restricciones lógicas, límites, casos especiales. Por ejemplo: "si el artículo ya fue guardado, no lo dupliques" o "siempre respondé en el tono de marca X".

### Herramientas usadas en este paso

- **La IA generativa (IDE con IA):** recibe el prompt del bosquejo y genera la estructura de archivos del proyecto
- **Modo planificación (Planning Mode):** activarlo antes de mandar el prompt garantiza que la IA planifique antes de ejecutar
- **Modelo de IA:** siempre usar el modelo más potente disponible para esta etapa
- **Carpeta de inspiración de diseño:** imágenes de referencia visual que se le pasan a la IA como contexto (de sitios como Dribbble o similares)

---

## Paso 2 — L: Lazos (Links)

### ¿Qué es?

Lazos es la etapa de conectividad. La IA valida que puede conectarse y comunicarse con todos los servicios externos antes de construir nada. Básicamente es un "handshake" con todas las integraciones: verificar credenciales, testear conexiones y confirmar que los endpoints responden.

### ¿Qué es el MCP y por qué importa acá?

MCP significa **Model Context Protocol** (Protocolo de Contexto de Modelo). Es el mecanismo que le permite a la IA conectarse a herramientas y servicios externos como si fueran sus propias manos. Cuando la IA tiene un MCP de Notion configurado, puede crear páginas, editarlas y borrarlas directamente. Lo mismo con Supabase, GitHub, Vercel, etc.

La primera pregunta ante cualquier integración es: **¿tiene MCP disponible?** Si lo tiene, la integración es trivial. Si no lo tiene, se puede obtener el código de configuración preguntándoselo a cualquier otro LLM con la consulta: "¿cuál es la configuración MCP para [servicio]?"

### Cómo conectar un servicio con MCP

El proceso siempre es el mismo:

1. Ir al panel de MCPs del IDE
2. Buscar el servicio en el store integrado
3. Configurar el token de acceso (generarlo desde la cuenta del servicio)
4. Verificar que aparece como activo en el listado de servidores MCP

Un tip importante: no conviene tener más de 50 herramientas MCP activas simultáneamente porque afecta la ventana de contexto del modelo.

### Cómo conectar una API cuando no hay MCP

Cuando un servicio no tiene MCP disponible, se usa su API directamente. El proceso es:

1. Obtener la URL del endpoint (generalmente un `POST`)
2. Obtener el preview del cuerpo del request (request body preview)
3. Pasarle ambas cosas a la IA junto con las credenciales
4. La IA valida que puede comunicarse con el endpoint antes de seguir

### Herramientas usadas en este paso

- **Store de MCPs del IDE:** punto de acceso a las integraciones nativas disponibles
- **Supabase MCP:** para conectar y operar la base de datos (crear tablas, consultar, guardar datos)
- **Notion MCP:** para crear páginas, actualizar bases de datos, agregar ítems a listas
- **Vercel MCP:** para gestionar deployments y variables de entorno
- **APIs externas (ej. Poppy AI):** cuando no hay MCP, se usa el endpoint de la API directamente
- **Otro LLM (ej. Gemini):** para obtener configuraciones MCP de servicios menos conocidos

---

## Paso 3 — A: Arquitectura (Architecture)

### ¿Qué es?

Arquitectura es la etapa de construcción. La IA tiene todo lo que necesita: sabe qué construir (Bosquejo) y puede conectarse a todo (Lazos). Ahora construye la aplicación real, lista para producción.

Esta etapa sigue la arquitectura de tres capas mencionada al inicio:

- **Capa de SOPs:** documentos markdown que definen cada función del sistema, sus inputs, su lógica y sus casos borde. Regla de oro: si la lógica cambia, primero se actualiza el SOP, después el código.
- **Capa de navegación:** la IA razona y enruta entre los SOPs y las herramientas. No ejecuta lógica compleja por su cuenta.
- **Capa de herramientas:** scripts Python determinísticos, atómicos y testeables. Las credenciales sensibles nunca están en el código, siempre en variables de entorno (`.env`).

### El concepto de "context rot" (degradación de contexto)

A medida que la conversación con la IA se extiende, la calidad de las respuestas baja. Esto ocurre porque la ventana de contexto se llena: los primeros tokens son los más efectivos, los últimos mucho menos. Cuando la IA termina una tarea grande, conviene abrir una nueva ventana de chat para la siguiente fase. Esto evita errores y resultados inconsistentes.

### Herramientas usadas en este paso

- **La IA generativa:** construye toda la estructura de archivos, componentes y lógica del backend
- **Supabase:** base de datos principal (tablas, storage de archivos como imágenes, queries SQL)
- **Scripts Python:** lógica determinística para tareas específicas (scrapers, procesadores de datos)
- **Variables de entorno (.env):** almacenamiento seguro de credenciales y tokens
- **Servidor local (localhost):** para previsualizar la app mientras se construye

---

## Paso 4 — S: Stilización (Stylize)

### ¿Qué es?

Stilización es la etapa de diseño. Acá se transforma el front end de funcional a bello. La app ya funciona; ahora tiene que verse como un producto profesional.

La técnica principal se llama **UI sniping**: ir a librerías de componentes y sitios de referencia, encontrar elementos visuales que te gusten, y pedirle a la IA que los replique o adapte en tu app.

### De dónde sacar inspiración y componentes

Hay varios lugares útiles:

- **Dribbble:** para capturar referencias visuales de dashboards y apps (buscar "dark mode dashboard", "glassmorphism UI", etc.)
- **Librerías de componentes (ej. 21st.dev):** componentes listos para usar —borders, chats, navbars, footers, etc.— de los que podés copiar el código directamente
- **CodePen:** para encontrar implementaciones específicas de UIs interactivas o animaciones

### Cómo funciona el UI sniping en la práctica

1. Navegar una librería de componentes y encontrar algo que te guste
2. Copiar el código del componente
3. Pedirle a la IA que lo integre en la app, indicando exactamente dónde y cómo
4. Repetir paso a paso para cada elemento que querés mejorar

No hace falta reinventar nada: la mayoría de las interfaces web de alta calidad usan componentes existentes que alguien más ya construyó y probó.

### Herramientas usadas en este paso

- **Dribbble:** fuente de inspiración visual
- **21st.dev y similares:** librerías de componentes React/Tailwind listos para copiar
- **CodePen:** referencia para UIs interactivas y efectos específicos
- **La IA generativa:** integra los componentes, ajusta colores, tipografías y layout según las instrucciones y la referencia visual cargada en el paso de Bosquejo

---

## Paso 5 — T: Transferencia al cloud (Trigger / Deploy)

### ¿Qué es?

Transferencia al cloud es la etapa de despliegue y automatización. Acá resolvemos dos cosas distintas pero relacionadas:

1. **Automatizaciones:** hacer que ciertas tareas corran solas en segundo plano (por ejemplo, un scraper que se ejecuta todos los días a las 8am aunque la laptop esté apagada)
2. **Publicación online:** hacer que la app esté disponible en una URL pública, accesible para vos, tu equipo o tus clientes

### Cuándo necesitás deployar y cuándo no

Si la app es solo para uso personal y la corrés desde tu propia máquina, no necesitás deployar. Pero si querés que otros puedan accederla, o si querés que las automatizaciones corran sin que tu computadora esté encendida, necesitás un deploy.

### Automatizaciones en la nube

Para que scripts corran automáticamente (cronjobs en la nube), se usa **Modal**. El proceso es:

1. Pedirle a la IA que escriba el script del proceso que querés automatizar (ej. el scraper de Reddit)
2. Configurar Modal para que ejecute ese script en el horario que quieras
3. Decirle a la IA que guarde los resultados en Supabase para no repetir trabajo ya hecho
4. Definir reglas de deduplicación (si el artículo ya existe, no lo agregues de nuevo)

### Publicación de la app

El flujo estándar para publicar una app online tiene tres pasos:

**GitHub → Vercel → Dominio propio**

1. **GitHub:** repositorio donde vive el código. Es simplemente un lugar donde se guardan los archivos del proyecto. La IA puede hacer el commit y push directamente usando el MCP de GitHub o las credenciales configuradas.

2. **Vercel:** plataforma de hosting que toma el código de GitHub y lo publica en internet. Cada vez que el código en GitHub se actualiza, Vercel refleja los cambios automáticamente. Acá también se configuran las **variables de entorno** de producción (las claves de API, tokens de Supabase, etc.) para que no queden expuestas en el código.

3. **Dominio propio:** desde el dashboard de Vercel se puede comprar un dominio personalizado y asociarlo al proyecto en minutos.

### Variables de entorno: por qué son críticas

Una variable de entorno es una credencial (token, API key, URL de base de datos) que vive fuera del código. Nunca se hardcodea en el proyecto. Esto importa por dos razones:

- **Seguridad:** nadie que vea el código puede acceder a tus servicios
- **Portabilidad:** podés cambiar una credencial sin tocar el código

En Vercel, las variables de entorno se configuran desde el panel del proyecto antes de hacer el deploy.

### Herramientas usadas en este paso

- **Modal:** plataforma para correr scripts automatizados en la nube (scrapers, jobs periódicos)
- **GitHub:** repositorio del código fuente del proyecto
- **Vercel:** hosting del front end y back end de la app; sincronización automática con GitHub
- **Vercel MCP:** le permite a la IA configurar variables de entorno y hacer deployments directamente
- **Supabase:** base de datos donde se persisten los resultados de las automatizaciones

---

## Resumen del framework

```
B — Bosquejo       →  Definir qué construir, integraciones, fuente de verdad y reglas
L — Lazos          →  Validar todas las conexiones con MCPs y APIs antes de construir
A — Arquitectura   →  Construir la app en tres capas: SOPs, navegación y herramientas
S — Stilización    →  Transformar el front end con UI sniping de librerías de componentes
T — Transferencia  →  Automatizar tareas y publicar la app en producción vía GitHub + Vercel
```

El orden no es negociable. Cada paso depende del anterior. Saltarse el Bosquejo genera apps que nadie quiere usar. Saltarse los Lazos genera apps que se rompen en producción. Saltarse la Stilización genera apps que nadie quiere pagar. Y sin la Transferencia, la app solo vive en tu laptop.

---

## EXTENSIÓN CRÍTICA: Context Engineering & Módulo "Sobre Mí"

### ¿Por qué Context Engineering es fundamental?

El BLAST define QUÉ construir. Pero hay un paso previo (casi invisible) que determina QUÉ tan bien lo construirá la IA: el **contexto del usuario**.

Ejemplo: Si le pides a Claude "crea una app de infoproductos", obtendrás una app genérica. Pero si Claude tiene acceso a:
- Tu historial de productos vendidos
- Tus personas clave (mentores, clientes, socios)
- Tu metodología personal
- Tus transcripciones de cómo hablas
- Tus notas diarias de decisiones

Entonces Claude creará una app que suena *como tú*, que funciona *como tú quieres*, optimizada para *tu mercado específico*.

### Estructura: La Base de Datos "Sobre Mí"

Esta base de datos vive en:
- **Obsidian** (recomendado para Context Engineering)
- **Notion** (alternativa)
- **Sistema de carpetas en GitHub** (backup)

**Estructura de carpetas requerida:**

```
📦 Sobre Mí/
├── 📄 mi-perfil.md (Quién eres, roles, objetivos)
├── 📁 Personas/ (Mentores, clientes, socios, amigos)
│   ├── 📄 [Nombre Mentor 1]
│   ├── 📄 [Nombre Cliente Tipo]
│   └── 📄 [Mi Pareja / Familia]
├── 📁 Proyectos/ (Historial de lo que has creado)
│   ├── 📄 [Proyecto 1 - Lecciones aprendidas]
│   ├── 📄 [Proyecto 2 - Métricas]
│   └── 📄 [Proyecto 3 - ROI]
├── 📁 Transcripciones/ (Cómo hablas, tus patrones mentales)
│   ├── 📄 charla-sobre-mi
│   ├── 📄 video-entrevista
│   └── 📄 podcast-ep01
├── 📁 Notas Diarias/ (Decisiones, reflexiones, aprendizajes)
│   ├── 📄 2026-04-11.md
│   ├── 📄 2026-04-10.md
│   └── 📄 2026-04-09.md
├── 📁 Methodologías/ (Cómo trabajas, procesos, frameworks)
│   ├── 📄 proceso-lanzamiento-oferta.md
│   ├── 📄 estructura-funnel.md
│   └── 📄 decisiones-tecnicas.md
└── 📁 Ideología/ (Principios, valores, límites)
    ├── 📄 que-vendo-y-que-no.md
    ├── 📄 publico-ideal.md
    └── 📄 rojo-límites.md
```

### El Asistente Coach Cronometrado (NAUTA)

El concepto más poderoso: **Un agente de IA que se ejecuta automáticamente cada mañana a una hora específica y te hace preguntas sobre tu día.**

**Implementación:**

```
⏰ Trigger: Todos los días a las 9:00 AM
📝 Acción: NAUTA ejecuta script que pregunta:

"Buenos días, [Nombre] 👋

¿Qué tal tu día de hoy?
¿Qué tareas prioritarias tenés?
¿Hay algo donde te sentís perdido o necesites ayuda?
¿Algún blockers o decisiones pendientes?"

✅ El usuario responde en el chat
🤖 NAUTA procesa la respuesta y:
   1. Extrae tareas nuevas
   2. Las mapea a proyectos existentes
   3. Actualiza el dashboard
   4. Sugiere next steps basado en "Sobre Mí"
```

**Esto requiere:**
- Cron job (ejecución cronométrica)
- Acceso a la base de datos "Sobre Mí"
- Integración con Notion/Dashboard para persistencia
- Context inyectado en cada ejecución

---

*Framework BLAST + Context Engineering: El combo que hace que la IA entienda no solo QUÉ construir, sino CÓMO construirlo para que sea una extensión natural de quién eres.*
