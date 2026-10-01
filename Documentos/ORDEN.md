# ORDEN DE LECTURA — TesteoLab

> Cómo leer la documentación del proyecto. Empezá por arriba.

---

## 1. EMPEZÁ AQUÍ — Stack y estructura técnica
**`C:\apptesteo\CLAUDE.md`**
Qué hace el proyecto, qué archivos importan, qué endpoints existen, cómo correrlo.
→ Leer siempre antes de tocar código.

---

## 2. DEFINICIÓN COMPLETA DEL SISTEMA
**`C:\apptesteo\Documentos\SISTEMA_AGENTES_Y_MODULOS.md`**
Qué es cada agente (NAUTA, Espía, Crea, Creativo, Analista Meta), qué accesos tiene cada uno,
qué hace cada módulo (M1-M4), arquitectura general del producto.
→ Leer antes de trabajar en cualquier agente o módulo.

---

## 3. ROADMAP DE IMPLEMENTACIÓN
**`C:\apptesteo\Documentos\ROADMAP_IMPLEMENTACION.md`**
En qué orden construir las cosas. Tiers de prioridad. Dependencias entre módulos.
→ Leer antes de decidir qué construir a continuación.

---

## 4. ESTADO REAL DEL DASHBOARD (auditoría visual)
**`C:\apptesteo\docs\estado\AUDITORIA_DASHBOARD_REAL.md`**
Qué funciona hoy, qué no, qué está hardcodeado. Validado visualmente por la usuaria.
→ Leer antes de reportar cualquier "funciona" o "no funciona".

---

## 5. ESPECIFICACIONES DE MÓDULOS

### M1 — Espía (más completo)
**`C:\apptesteo\docs\planes\m1_especificacion.md`**
Flujo completo, wireframes en texto, scoring, integración con M2.

### NAUTA — Coach Agent
**`C:\apptesteo\docs\planes\NAUTA_PLAN_COMPLETO.md`**
Qué hace NAUTA, cómo se conecta a Notion, flujo del briefing y cierre.

---

## 6. METODOLOGÍA BASE (framework conceptual)
**`C:\apptesteo\DOCCOntextoBuild\framework-BLAST.md`**
BLAST framework. Context Engineering. Concepto de "Sobre Mí". Base para todo el diseño del sistema.
→ Leer si querés entender el "por qué" detrás de las decisiones.

---

## 7. DOCUMENTOS DE CONTEXTO DE NEGOCIO
**`C:\apptesteo\DOCCOntextoBuild\cLAUDE.MD`**
Reglas de trabajo para Claude dentro de este proyecto.

---

## CONVENCIONES DE ESTE PROYECTO

### Screenshots de validación
Los guardás en: `C:\apptesteo\testImage\`
Claude los lee antes de reportar estado de módulos.

### Documentos pre/post cambio
- **Antes de tocar código** → crear `Documentos\PRE_[nombre_cambio].md` con qué se va a cambiar y por qué
- **Después del cambio** → crear `Documentos\POST_[nombre_cambio].md` con qué se hizo, qué se probó, qué quedó pendiente

---

## ARCHIVOS QUE NO HAY QUE TOCAR SIN CONTEXTO
- `notion_api.py` — Flask app principal, cambios acá afectan todo
- `nauta_scheduler.py` — Scheduler activo en producción
- `.env` — Variables sensibles, nunca a git
- `Procfile` — Config de Render
