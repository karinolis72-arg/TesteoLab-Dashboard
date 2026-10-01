# 🤖 AUDITORÍA NAUTA - QUÉ FALTA

**Estado**: NAUTA está 50% funcional  
**Objetivo**: Hacerlo 100% antes de M1-M4

---

## ❌ FALTA EN NAUTA (Prioridad Alta)

### 1. **BRIEFING HTML - Vacío de datos reales**
- ✅ Estructura HTML existe
- ❌ Top 3 Tareas Q1 → Hardcoded, no conecta Notion Roadmap Master
- ❌ Tareas HOY → Hardcoded, no conecta /api/tasks/today
- ❌ Hábitos Esperados → No implementado
- ❌ Rueda de Vida → Hardcoded (60%, 40%, etc), no conecta datos reales
- **Solución**: nauta_scheduler.py línea 100+ necesita conectar a Notion

### 2. **CIERRE FORM - Tareas incompletas**
- ✅ Checkboxes se cargan desde /api/tasks/today
- ❌ Los datos vienen sin estructura (falta titulo, prioridad, etc)
- ❌ No hay validación: ¿qué si no checkea nada?
- ❌ Notas: textarea vacío, no hay ayuda/hints
- ❌ Energía: dropdown funciona pero sin contexto (¿por qué Baja/Media/Alta?)
- **Solución**: Mejorar estructura del formulario y validaciones

### 3. **GUARDADO EN NOTION**
- ✅ Se guarda en memoria (nauta_state dict)
- ❌ NO se guarda en Notion (tabla NAUTA Logs no existe)
- ❌ Cierres históricos se pierden al reiniciar servidor
- **Solución**: Crear tabla "NAUTA Logs" en Notion y conectar POST /api/nauta/save-cierre

### 4. **HÁBITOS NO INTEGRADOS**
- ❌ "✅ Hábitos Esperados" en briefing está vacío
- ❌ No conecta a base Hábitos en Notion
- ❌ No se trackean en cierre
- **Solución**: Conectar /api/habits en nauta_scheduler.py

### 5. **LLAMADA A NAUTA (Chat/IA)**
- ❌ Botón "📞 Llamar NAUTA" en briefing no hace nada
- ❌ No hay integración con ChatGPT/IA conversacional
- ❌ No existe "sesión NAUTA" de chat
- **Solución**: Crear endpoint /api/nauta/chat y integrar OpenAI

### 6. **MÓDULO DE NOTAS**
- ❌ No existe en sidebar (no está en data-module="notes")
- ❌ No hay contenedor #notes-container
- ❌ No hay acceso a historial de cierre
- **Solución**: Crear módulo NOTAS con historial de cierres + notas personales

### 7. **INTEGRACIÓN NOTION COMPLETA**
Faltan estas conexiones:
```
Notion Table          → API Endpoint           → NAUTA Función
─────────────────────────────────────────────────────────────
Roadmap Master        → /api/tasks/top-q1      → Top 3 Tareas (briefing)
Tareas               → /api/tasks/today       → Tareas del día (cierre)
Hábitos              → /api/habits            → Hábitos (briefing)
NAUTA Logs (CREAR)   → /api/nauta/save-cierre → Guardar cierres
Rueda de Vida (CREAR)→ /api/nauta/rueda       → Datos de balance
```

### 8. **RUEDA DE VIDA**
- ✅ Existe estructura HTML (8 áreas)
- ❌ Valores hardcoded: 60%, 40%, etc
- ❌ No conecta a tabla Notion
- **Solución**: Crear tabla "Rueda de Vida" en Notion

### 9. **RECOMENDACIÓN DIARIA**
- ❌ "💡 Recomendación" en briefing no existe
- ❌ Sería útil: recomendación basada en energía + hábitos pendientes
- **Solución**: Agregar lógica en generate_briefing_html()

### 10. **PRÓXIMO CIERRE (Predicción)**
- ❌ No hay predicción de cuándo será el próximo cierre
- ❌ No hay recordatorio visual
- **Solución**: Agregar contador regresivo en módulo NAUTA

---

## 🎯 PRIORIDAD DE FIXES

### TIER 1 (BLOQUEA VALIDACIÓN)
1. Conectar Roadmap Master → briefing Top 3 Q1
2. Conectar Tareas → cierre checkboxes
3. Crear tabla NAUTA Logs y guardar cierres en Notion
4. Conectar Hábitos → briefing

### TIER 2 (MEJORA EXPERIENCIA)
5. Módulo NOTAS con historial
6. Rueda de Vida datos reales
7. Recomendación diaria IA

### TIER 3 (NICE TO HAVE)
8. Chat con NAUTA (OpenAI)
9. Predicción próximo cierre
10. Metricas/analytics históricas

---

## 📊 CHECKER - ¿NAUTA LISTA PARA VALIDAR?

```
BRIEFING:
  [ ] Top 3 Q1 conectado a Notion ✅ o ❌
  [ ] Tareas hoy conectadas ✅ o ❌
  [ ] Hábitos mostrados ✅ o ❌
  [ ] Rueda de Vida con datos reales ✅ o ❌
  [ ] Recomendación visible ✅ o ❌

CIERRE:
  [ ] Checkboxes cargan tareas reales ✅ o ❌
  [ ] Notas se guardan en Notion ✅ o ❌
  [ ] Historial accesible ✅ o ❌
  [ ] Validaciones funcionan ✅ o ❌

SCHEDULER:
  [ ] 8:30 AM briefing automático ✅ o ❌
  [ ] 21:30 cierre automático ✅ o ❌
  [ ] Próximo horario visible ✅ o ❌

MÓDULOS:
  [ ] NOTAS módulo existe ✅ o ❌
  [ ] Historial de cierres visible ✅ o ❌
  [ ] Métricas semanales ✅ o ❌
```

---

## 🚀 PLAN PARA COMPLETAR NAUTA

### Fase 1: Conexiones Notion (Tier 1)
1. Leer datos reales de Roadmap Master
2. Leer datos reales de Tareas
3. Leer datos reales de Hábitos
4. Crear tabla NAUTA Logs
5. Guardar cierres en Notion

**Tiempo**: ~3-4 horas  
**Testing**: TODO_NAUTA_VALIDATION.txt

### Fase 2: Módulo NOTAS + Rueda Vida
1. Crear módulo NOTAS sidebar
2. Crear tabla Rueda de Vida en Notion
3. Conectar endpoint /api/nauta/rueda
4. Mostrar historial en NOTAS

**Tiempo**: ~2 horas

### Fase 3: IA Conversacional (Opcional)
1. Crear endpoint /api/nauta/chat
2. Integrar OpenAI API
3. Botón "Llamar NAUTA" funcional
4. Sesión conversacional

**Tiempo**: ~1-2 horas

---

## ✅ DESPUÉS: ENTONCES SÍ, M1-M4

Una vez NAUTA esté 100% validado:
- M1: Análisis de Ofertas (basado en Roadmap)
- M2: Seguimiento de ventas
- M3: Optimización de funnels
- M4: Métricas de ROI

---

**Conclusión**: NAUTA necesita ~4-5 horas de integración Notion  
**Sin eso**: Los datos vacíos harán M1-M4 inútiles  
**Recomendación**: Hagamos Fase 1 ahora, validemos, luego Fase 2, DESPUÉS M1-M4
