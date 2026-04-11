# MÓDULO 1: ESPIONAJE & SELECCIÓN 
## Especificación Completa - Funnel Hacking con Meta Ads Library

**Estado:** 100% Definido
**Basado en:** Meta Ads Library API + Funnel Hacking Framework

---

## 🎯 Objetivo Principal
**"Encontrar y modelar ofertas ganadoras analizando publicidades competidoras en Meta Ads Library"**

Output: Identificar qué está funcionando en el mercado y seleccionar la MEJOR OFERTA para modelar en M2.

---

## 📊 FLUJO COMPLETO (User Journey)

```
┌─────────────────────────────────────────────────────────────┐
│ PASO 1: DEFINIR BÚSQUEDA                                    │
│ (Parámetros iniciales)                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 2: BUSCAR EN META ADS LIBRARY                          │
│ (Encontrar anuncios competidores)                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 3: ANALIZAR ANUNCIOS                                   │
│ (Métricas, viabilidad, inversión estimada)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 4: FILTRAR & CLASIFICAR                                │
│ (Identificar "ganadores" según criterios)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 5: SELECCIONAR OFERTA A MODELAR                        │
│ ("Vamos con ESTA oferta")                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
OUTPUT → M2 (Creación de Oferta)
```

---

## 🔍 PASO 1: DEFINIR BÚSQUEDA

### Inputs (Obligatorios)
```
┌─────────────────────────────┐
│ 1. PAÍS/REGIÓN              │
│    Selecciona: [Argentina]  │
│    (Usa geolocalización del │
│     usuario como default)   │
└─────────────────────────────┘

┌─────────────────────────────┐
│ 2. PALABRAS CLAVE           │
│    Input: [busca...        │
│    Ejemplo: "curso online" │
│    "ebook gratis"          │
│    "membresía digital"     │
│    (Búsqueda por keywords) │
└─────────────────────────────┘

O ALTERNATIVA:

┌─────────────────────────────┐
│ 2b. NOMBRE DE EMPRESA       │
│    Input: [empresa...      │
│    (Búsqueda por anunciante│
│     directo)               │
└─────────────────────────────┘
```

### Filtros Iniciales
```
FILTROS APLICABLES:
├─ País: [Argentina ▼] (obligatorio)
├─ Plataforma: 
│  ☑ Instagram  ☑ Facebook  ☑ Messenger  ☑ Audience Network
├─ Tipo de Media:
│  ☑ Imagen  ☑ Video  ☑ Carousel  ☑ Colección  ☑ Todas
├─ Estado:
│  ☑ Activos  ☐ Inactivos
├─ Rango de Días Activos:
│  [Mínimo 7 días ▼] 
│  [Máximo 365 días ▼]
│  (Default: 30+ días = probable rentabilidad)
└─ Presupuesto Estimado:
   [Mín: $50 ▼] - [Máx: $50,000 ▼]
   (Hint: $200+ = mercado viable)
```

---

## 🔎 PASO 2: BUSCAR EN META ADS LIBRARY

### Cómo funciona la búsqueda
1. User ingresa país + keywords (o nombre empresa)
2. TesteoLab consulta Meta Ads Library API
3. Retorna TODOS los anuncios activos que coinciden
4. Aplica filtros (plataforma, media type, días activos)

### Data que retorna por cada anuncio
```json
{
  "ad_id": "12345678",
  "advertiser": "MiEmpresa SA",
  "advertiser_url": "https://miempresa.com",
  "ad_creative_bodies": [
    "Gana $5000/mes desde casa. Sin experiencia...",
    "Acceso exclusivo a membresía VIP..."
  ],
  "ad_creation_date": "2024-08-15",
  "ad_last_status_update": "2026-04-10",
  "days_active": 238,
  "media": {
    "type": "image/video/carousel",
    "url": "https://...",
    "thumbnail": "https://..."
  },
  "platform": "instagram",
  "call_to_action": "Visita sitio web / Regístrate",
  "landing_page": "https://minombredominio.com"
}
```

### UI de Resultados
```
RESULTADOS: 247 anuncios encontrados

┌──────────────────────────────────────┐
│ ANUNCIO 1                            │
├──────────────────────────────────────┤
│ [Thumbnail] Advertiser: CourseX SA  │
│ Días activos: 238 (✅ RENTABLE)      │
│ Plataforma: Instagram + Facebook    │
│ Tipo: Video (30seg)                 │
│ Copy: "Gana $5000/mes..."           │
│ CTA: "Regístrate gratis"            │
│ Landing: courseX.com/ebook          │
│                                      │
│ [Expandir] [Guardar] [Analizar]    │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ ANUNCIO 2                            │
│ [Similar structure]                 │
└──────────────────────────────────────┘

[Cargar más resultados] [Siguiente página]
```

---

## 📈 PASO 3: ANALIZAR ANUNCIOS (Inteligencia IA)

### Métricas Calculadas por cada anuncio

#### 1️⃣ **VIABILIDAD**
```
INDICADOR: Días Activos
├─ 7-30 días: 🟡 EXPERIMENTAL (testea pero no rentable aún)
├─ 30-90 días: 🟢 PROBABLE RENTABLE (buen signo)
├─ 90-180 días: 🟢🟢 MUY RENTABLE (ganador comprobado)
└─ 180+ días: 🟢🟢🟢 GANADOR CONFIRMADO (running 6+ meses)

REGLA DE ORO: Si corre 30+ días = probablemente gana dinero
```

#### 2️⃣ **PRESUPUESTO ESTIMADO INVERTIDO**
```
Cálculo (basado en Meta Ads research):
├─ CPM promedio por plataforma:
│  ├─ Instagram Feed: $8-15 (cold audience)
│  ├─ Instagram Stories: $6-12
│  ├─ Facebook Feed: $10-18
│  └─ Video (todos): $12-20
│
├─ Si ad tiene 238 días activos + 1,500 impresiones/día:
│  ├─ Total impresiones estimadas: 357,000
│  ├─ Costo estimado: 357k × $0.012 (CPM) = ~$4,284
│  │
│  VERDICT: "Este competidor invirtió aproximadamente $4,000-5,000"
│
└─ VIABILIDAD: ✅ $4k+ inversión = mercado viable para modelar
```

**NOTA IMPORTANTE:** Si presupuesto estimado > $200, el mercado es viable.

#### 3️⃣ **TIPO DE OFERTA** (Detección IA)
```
Análisis del copy + landing page → Tipo de oferta:
├─ Ebook + Bonus?     ✅ Detectado (copy menciona "acceso gratis + bonos")
├─ Curso Online?      ✅ Detectado (landing muestra módulos)
├─ Membresía?         ✅ Detectado (price point $49/mes)
├─ Producto físico?   ✅ Detectado (imágenes de producto)
├─ Servicio?          ✅ Detectado (mencionan consultoría)
└─ Híbrido (+ de 1)?  ✅ Detectado (ebook + curso)
```

#### 4️⃣ **INDICADORES DE ÉXITO**
```
SEÑALES POSITIVAS (por cada anuncio):
├─ ✅ Copy usa urgencia temporal ("Cierra el [fecha]")
├─ ✅ Copy menciona número ($5000, 50 cupos)
├─ ✅ Copy incluye pain point ("¿Cansado de...")
├─ ✅ Testimonios o prueba social visible
├─ ✅ Bonus o regalo incluido ("+ 3 bonos gratis")
├─ ✅ CTA es directo ("Obtén acceso", "Únete ahora")
├─ ✅ Múltiples variaciones del mismo anuncio (A/B testing)
└─ ✅ Corriendo en múltiples plataformas (escala probada)
```

#### 5️⃣ **SCORE DE POTENCIAL** (0-100)
```
Fórmula:
├─ Días activos: 30+ = +30 pts
├─ Presupuesto estimado: $200+ = +20 pts
├─ Tipo oferta identificable: +15 pts
├─ Señales de éxito (cantidad): +25 pts
├─ Competencia en el anuncio (menos es mejor): +10 pts
└─ TOTAL: Puntuación de potencial

Rangos:
├─ 0-30: 🔴 NO RECOMENDADO
├─ 31-60: 🟡 EXPERIMENTAL
├─ 61-80: 🟢 POTENCIAL ALTO
└─ 81-100: 🟢🟢 GANADOR CONFIRMADO
```

### UI de Análisis IA
```
┌────────────────────────────────────────────┐
│ ANÁLISIS DETALLADO - ANUNCIO #1            │
├────────────────────────────────────────────┤
│                                             │
│ VIABILIDAD: 🟢🟢 MUY RENTABLE (238 días)   │
│                                             │
│ PRESUPUESTO ESTIMADO: ~$4,284              │
│ Cálculo: 357k impresiones × $0.012 CPM    │
│ VERDICT: ✅ Mercado viable ($4k+ invertido)│
│                                             │
│ TIPO DE OFERTA DETECTADO: Curso Online     │
│ ├─ Precio: $97-297 (detectado en landing) │
│ ├─ Público: Emprendedores 25-45 años      │
│ ├─ Bonus: 3 bonos (ebooks + plantillas)   │
│ └─ Modalidad: Curso + Comunidad            │
│                                             │
│ SEÑALES DE ÉXITO: 8/10                     │
│ ✅ Urgencia temporal (Cierra 15 Abril)    │
│ ✅ Número específico ($5000/mes)          │
│ ✅ Pain point claro (cansado de empleo)   │
│ ✅ Testimonios (5 reviews 4.8/5)          │
│ ✅ Bonus incluido (3 bonos)                │
│ ✅ CTA directo (Obtén acceso)             │
│ ✅ A/B testing detectado (3 variaciones)  │
│ ⚠️  Competencia moderada (20 anuncios)    │
│                                             │
│ SCORE DE POTENCIAL: 78/100 🟢 ALTO         │
│                                             │
│ RECOMENDACIÓN:                             │
│ Este es un ganador comprobado. La oferta   │
│ está corriendo 238 días, con presupuesto   │
│ significativo ($4k+). Tipo de oferta:     │
│ Curso online con bonus. APTO PARA MODELAR.│
│                                             │
│ [Seleccionar esta oferta] [Ver más detalles]
│                                             │
└────────────────────────────────────────────┘
```

---

## 🏆 PASO 4: FILTRAR & CLASIFICAR (Smart Sorting)

### Vista de Grid Inteligente
```
MOSTRAR ORDENADO POR:
[Score de Potencial ▼] [Días Activos ▼] [Presupuesto ▼]

┌──────────────────────────────────────────┐
│ GANADORES (Score 80+)  [12 anuncios]     │
├──────────────────────────────────────────┤
│ 1. Curso Online - Score 87 - 238 días - $4.2k
│ 2. Membresía Digital - Score 84 - 156 días - $2.8k
│ 3. Ebook + Bonos - Score 81 - 145 días - $1.9k
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ POTENCIAL ALTO (Score 61-79)  [34 anuncios]
├──────────────────────────────────────────┤
│ 1. Servicio - Score 76 - 92 días - $800
│ 2. Producto Físico - Score 72 - 88 días - $1.2k
│ [...]
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ EXPERIMENTAL (Score 31-60)  [47 anuncios]
├──────────────────────────────────────────┤
│ 1. WebinAR - Score 55 - 42 días - $600
│ [...]
└──────────────────────────────────────────┘

[Comparar seleccionados] [Guardar esta búsqueda] [Siguiente]
```

### Comparador de Anuncios
```
Selecciona hasta 3 anuncios para comparar:

┌────────────┬────────────┬────────────┐
│ ANUNCIO 1  │ ANUNCIO 2  │ ANUNCIO 3  │
├────────────┼────────────┼────────────┤
│ Curso      │ Membresía  │ Ebook      │
│ $97-297    │ $49/mes    │ Gratis+$47 │
│ 238 días   │ 156 días   │ 145 días   │
│ $4.2k inv. │ $2.8k inv. │ $1.9k inv. │
│ Score: 87  │ Score: 84  │ Score: 81  │
│            │            │            │
│ GANADOR    │ MUY BUENO  │ BUENO      │
└────────────┴────────────┴────────────┘
```

---

## ✅ PASO 5: SELECCIONAR OFERTA A MODELAR

### Decisión Final
```
┌────────────────────────────────────────────┐
│ HAS ELEGIDO:                               │
│                                             │
│ OFERTA: Curso Online "Gana $5000/Mes"     │
│ TIPO: Educación Digital + Comunidad        │
│ PRECIO: $97-297 (según paquete)            │
│ TIEMPO ACTIVO: 238 días (GANADOR)          │
│ PRESUPUESTO ESTIMADO: $4,200+              │
│ SCORE POTENCIAL: 87/100                    │
│                                             │
│ ✅ APTO PARA MODELAR                       │
│                                             │
│ [Guardar esta selección] [Ir a M2]        │
└────────────────────────────────────────────┘
```

### Output → M2
```
DATOS ENVIADOS A MÓDULO 2 (Creación de Oferta):

{
  "m1_reference_id": "ad_12345678",
  "offer_type": "online_course",
  "estimated_price_point": "$97-297",
  "target_market": "Emprendedores 25-45 años",
  "key_message": "Gana $5000/mes desde casa",
  "bonus_detected": ["Ebook 1", "Plantillas", "Plantilla Excel"],
  "viability_score": 87,
  "advertiser_url": "https://mioferta.com",
  "days_active": 238,
  "estimated_investment": "$4200",
  "competitive_analysis": {
    "similar_offers_count": 45,
    "top_ctas": ["Obtén acceso", "Únete ahora"],
    "common_urgencies": ["Limited spots", "Cierra [fecha]"]
  }
}
```

---

## 🎛️ INTERFAZ AVANZADA (Smart Tips & Helpers)

### Tips Automáticos mientras buscas
```
💡 TIP 1: "Estás buscando 'curso online'. Hay 156 resultados
          que corren +30 días. Eso significa probablemente 
          generan ingresos. Buen nicho."

💡 TIP 2: "Competencia: MODERADA. Hay 45 variaciones del 
          mismo anuncio = A/B testing probado. Buena señal."

💡 TIP 3: "Presupuesto: Este competidor invirtió ~$4,200 
          en Meta. Eso indica $X/mes potencial."

⚠️  ADVERTENCIA: "Ads con <7 días pueden no ser decisivos.
              Enfócate en los de 30+ días."
```

### Búsquedas Guardadas
```
MIS BÚSQUEDAS:
├─ [Curso online] - 12 resultados - Guardada hace 2 días
├─ [Membresía digital] - 8 resultados - Guardada hace 1 día
├─ [Ebook gratis] - 23 resultados - Nueva
└─ [Por empresa: CourseX SA] - 5 anuncios - Nueva
```

### Historial & Seguimiento
```
ÚLTIMAS SELECCIONES:
├─ 10 Abril: Seleccioné "Curso Online 238d" → Score 87
├─ 8 Abril: Seleccioné "Membresía 156d" → Score 84
└─ 5 Abril: Seleccioné "Ebook 145d" → Score 81

[Replicar búsqueda anterior] [Descargar reporte]
```

---

## 🔧 INTEGRACIÓN CON OTROS MÓDULOS

### Entrada de M1
- Búsquedas iniciales (keywords, empresa)
- Meta Ads Library API (datos de anuncios)

### Salida de M1 → Entrada M2
- Offer reference (tipo, precio, mercado)
- Análisis de viabilidad (score, inversión estimada)
- Insights competitivos (CTAs, urgencias, bonus)

### Relación con M9 (IDEAS)
- M9 propone ideas/nichos
- M1 valida si hay competencia activa en esos nichos
- Feedback loop: "Hay 156 competidores activos en este nicho"

---

## 📊 TECNOLOGÍA & APIs

### Meta Ads Library API
- Endpoint: `GET /ads_library?ad_status=ACTIVE`
- Parámetros: country, keywords, advertiser_name, media_type
- Rate limit: 50 requests/min
- Respuesta: JSON con ads + metadata

### Agentes Involucrados
- **Agente Marketing**: Análisis de copy, detección de tipo oferta
- **Agente Leads**: Cálculo de presupuesto estimado, scoring
- **Asistente Guía**: Guía user a través del flujo

### Base de Datos (Supabase)
- Tabla: `competitor_accounts`
- Tabla: `competitor_ads`
- Tabla: `ad_metrics`
- Tabla: `ad_analysis` (análisis IA por ad)

---

## ✨ RESUMEN DE CARACTERÍSTICAS

```
✅ Búsqueda por keywords + advertiser name
✅ Filtros avanzados (país, plataforma, días, presupuesto)
✅ Análisis IA de viabilidad (días activos = rentabilidad)
✅ Cálculo de presupuesto invertido (CPM-based)
✅ Detección automática de tipo oferta
✅ Scoring 0-100 de potencial
✅ Identificación de señales de éxito
✅ Comparador de anuncios
✅ Tips automáticos inteligentes
✅ Historial & búsquedas guardadas
✅ Output limpio hacia M2
✅ Integración con M9 (Ideas)
```

