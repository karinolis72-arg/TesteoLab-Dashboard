# Auditoría Real del Dashboard — 12 Abril 2026
**Validado visualmente por la usuaria. Estado real vs esperado.**

---

## 🤖 MÓDULO NAUTA

### Panel "Estado de Hoy"
| Campo | Lo que se ve | Lo que debería ser | Estado |
|-------|-------------|-------------------|--------|
| Tareas Hoy | 3 ✅ | Tareas reales de Notion | ✅ OK |
| Completadas | 0 | Tareas marcadas como completadas | ⚠️ Hardcoded en 0 |
| Energía | 70% | Energía del último cierre | ❌ Hardcodeado en 70 |

### Botones principales
| Botón | Estado | Problema |
|-------|--------|---------|
| VER BRIEFING | ✅ Funciona | — |
| REGISTRAR CIERRE | ✅ Abre con checkboxes y tareas | — |
| GUARDAR CIERRE | ⚠️ Guarda pero no persiste | Se pierde al reiniciar servidor |
| VER ÚLTIMO CIERRE | ❌ No permanece | Sin persistencia en Notion |
| LLAMAR/CHAT NAUTA | ❌ No existe | **Prioridad alta — usuaria lo necesita** |

### Agente NAUTA (chat)
- **No existe aún**
- **Descripción de lo que se necesita**: Un agente que lee Notion (tareas, hábitos, Sobre Mí), mantiene conversación, actualiza información y da coaching personalizado
- Referencia: `framework-BLAST.md` → sección "Asistente Coach Cronometrado"

---

## 📓 MÓDULO NOTION
| Estado | Detalle |
|--------|---------|
| ❌ No carga nada | Spinner infinito o sin contenido visible |
| Causa probable | Endpoint `/api/tasks` puede estar fallando silenciosamente |

---

## 📊 MÓDULO TRACKER
| Estado | Detalle |
|--------|---------|
| ❌ Vacío | Solo texto "Módulo en construcción" en el código |
| En HTML | Existe el contenedor pero sin contenido |

---

## 🔍 M1 — Análisis de Ofertas
| Estado | Detalle |
|--------|---------|
| ❌ Vacío + error | Botón existe en sidebar, contenido vacío, da error |
| Definición | Ver `docs/planes/m1_especificacion.md` |

## 🛠️ M2 — (Sin definición clara en código)
| Estado | Detalle |
|--------|---------|
| ❌ Vacío + error | Botón existe, sin contenido |

## 📈 M3 — (Sin definición clara en código)
| Estado | Detalle |
|--------|---------|
| ❌ Vacío + error | Botón existe, sin contenido |

## ⚡ M4 — (Sin definición clara en código)
| Estado | Detalle |
|--------|---------|
| ❌ Vacío + error | Botón existe, sin contenido |

---

## ⚙️ SETTINGS
| Funcionalidad | Estado | Prioridad |
|--------------|--------|-----------|
| Configuración de perfil | ❌ No existe | Media |
| Foto de perfil | ❌ No existe | Baja |
| Cierre de sesión | ❌ No existe | No necesario ahora |
| Configuración NAUTA | ❌ No existe | Media |

---

## 📊 RESUMEN EJECUTIVO — ESTADO REAL HOY

```
NAUTA briefing:         ✅ Funciona (iframe)
NAUTA cierre (form):    ✅ Funciona (UI)
NAUTA cierre (persist): ❌ No persiste (sin Notion IDs)
NAUTA energía:          ❌ Hardcodeada (70%)
NAUTA chat/agente:      ❌ No existe (PRIORIDAD ALTA)
Módulo NOTION:          ❌ No carga
Módulo TRACKER:         ❌ Vacío
Módulos M1-M4:          ❌ Vacíos + errores
Settings:               ❌ Incompleto
```

---

## 🎯 ORDEN DE PRIORIDADES (acordado)

### TIER 1 — Desbloquea todo
1. Llenar "Sobre Mí" en Notion (usuaria)
2. Crear NAUTA Logs + Rueda de Vida en Notion (usuaria)
3. Agregar IDs al .env

### TIER 2 — Hace NAUTA funcional al 100%
4. **Agente NAUTA** (chat que lee Notion + coaching)
5. Persistencia cierres en Notion
6. Energía dinámica desde último cierre
7. Módulo NOTION funcionando

### TIER 3 — Completa la experiencia
8. Settings con perfil + foto
9. Módulo TRACKER
10. M1-M4 según especificación

---

*Auditado: 2026-04-12 | Método: validación visual usuaria + revisión código*
