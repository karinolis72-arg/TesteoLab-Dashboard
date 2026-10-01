# 🤖 NAUTA - Setup Notion Databases (Fase 1)

**Estado**: Endpoints backend están listos. Faltan: crear tablas en Notion y poblar IDs.

---

## 📌 Qué necesitas hacer

### Paso 1: Crear tabla **NAUTA Logs** en Notion

Esta tabla guardará todos tus cierres diarios.

#### Instrucciones:

1. Ve a https://notion.so
2. **Nuevo** → **Database** (o agrega a una página existente)
3. Nombre: **"NAUTA Logs"**
4. Elimina la columna "Name" por defecto
5. Crea las siguientes propiedades:

| Nombre | Tipo | Opciones |
|--------|------|----------|
| **Fecha** | Date | - |
| **Completadas** | Number | formato: número |
| **Pendientes** | Number | formato: número |
| **Energía** | Select | Baja (red), Media (yellow), Alta (green) |
| **Notas** | Text | - |
| **Timestamp** | Created time | - |

#### Cómo copiar el ID:

1. Una vez creada la tabla, abre su URL
2. La URL se ve así: `https://www.notion.so/YOUR_WORKSPACE/[database_id]?v=...`
3. Copia `[database_id]` (es una cadena larga de números)
4. **Ejemplo**: `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o`

---

### Paso 2: Crear tabla **Rueda de Vida** en Notion

Esta tabla trackea el balance de las 8 áreas de tu vida.

#### Instrucciones:

1. Ve a https://notion.so
2. **Nuevo** → **Database**
3. Nombre: **"Rueda de Vida"**
4. Elimina la columna "Name"
5. Crea las siguientes propiedades:

| Nombre | Tipo | Opciones |
|--------|------|----------|
| **Fecha** | Date | - |
| **Área** | Select | Salud (red), Trabajo (blue), Familia (pink), Finanzas (green), Relaciones (purple), Crecimiento (orange), Diversión (yellow), Espiritualidad (gray) |
| **Score** | Number | formato: número (0-100) |
| **Notas** | Text | - |
| **Timestamp** | Created time | - |

#### Cómo copiar el ID:

1. Mismo proceso que NAUTA Logs
2. Copia el `[database_id]` de la URL

---

### Paso 3: Agregar los IDs a .env

Abre `C:\apptesteo\.env` y agrega:

```
NAUTA_LOGS_DB_ID=paste_aqui_el_id_de_nauta_logs
RUEDA_VIDA_DB_ID=paste_aqui_el_id_de_rueda_vida
```

**Ejemplo completo:**

```
NOTION_TOKEN=secret_abc123xyz789...
FLASK_PORT=5000
FLASK_ENV=development
NAUTA_LOGS_DB_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o
RUEDA_VIDA_DB_ID=5z9y8x7w6v5u4t3s2r1q0p9o8n7m6l
```

---

### Paso 4: Copiar algunos datos iniciales (Opcional)

Si quieres que la Rueda de Vida tenga datos iniciales:

1. Abre tabla Rueda de Vida en Notion
2. Agrega 8 filas (una por área):

| Fecha | Área | Score | Notas |
|-------|------|-------|-------|
| Hoy | Salud | 75 | Ejercicio y descanso |
| Hoy | Trabajo | 80 | Productivo |
| Hoy | Familia | 70 | Llamé a mamá |
| Hoy | Finanzas | 85 | Buenas ganancias |
| Hoy | Relaciones | 65 | Necesito más tiempo |
| Hoy | Crecimiento | 90 | Estudiando mucho |
| Hoy | Diversión | 50 | Poco tiempo libre |
| Hoy | Espiritualidad | 88 | Meditación diaria |

---

## ✅ Validación Checklist

Una vez hayas creado las tablas:

```
CREAR TABLAS:
  [ ] NAUTA Logs creada con 6 propiedades
  [ ] Rueda de Vida creada con 5 propiedades
  [ ] .env actualizado con ambos IDs

VERIFICAR CÓDIGO:
  [ ] /notion_api.py tiene ambos NAUTA_LOGS_DB_ID y RUEDA_VIDA_DB_ID
  [ ] /nauta_scheduler.py importa get_rueda_vida()
  [ ] Endpoints nuevos: /api/nauta/rueda, /api/nauta/habitos, /api/nauta/cierres-historial

PROBAR ENDPOINTS:
  [ ] GET /api/nauta/rueda → retorna scores
  [ ] GET /api/nauta/habitos → retorna hábitos
  [ ] GET /api/nauta/cierres-historial → retorna historial (vacío al inicio)
  [ ] POST /api/nauta/save-cierre → guarda en Notion (no solo memoria)
```

---

## 🚀 Próximos pasos después del setup:

1. **Generar briefing automático** (8:30 AM)
   - Dirígete a http://localhost:9000 → NAUTA → VER BRIEFING
   - Debería mostrar datos reales de Notion

2. **Registrar cierre** (21:30)
   - Click en REGISTRAR CIERRE
   - Completa el formulario
   - Guardar → datos van a Notion (tabla NAUTA Logs)

3. **Ver historial**
   - Crear módulo NOTAS en sidebar (Fase 2)
   - Mostrará últimos 7 cierres

---

## ⚠️ Troubleshooting

### "NAUTA_LOGS_DB_ID no configurado"
- ✅ Solución: Verificar que .env tiene el ID
- ✅ Reiniciar servidor Flask: `python notion_api.py`

### "Error guardando cierre en Notion"
- ✅ Verificar que el token de Notion es válido
- ✅ Verificar que los database IDs están correctos (sin espacios)
- ✅ Ver console de Flask: `/api/nauta/save-cierre` debe retornar `"persisted_to_notion": true`

### "Rueda de Vida muestra valores por defecto"
- Esto es normal si:
  - No hay datos en tabla Rueda de Vida en Notion
  - El RUEDA_VIDA_DB_ID está vacío o incorrecto
- ✅ Agregar datos iniciales a la tabla (ver paso 4 arriba)

---

## 📋 Quick Reference

**Base de Datos IDs Existentes:**
```
TAREAS: 3f0c07004c154bd4b5712141fc582815 ← YA EXISTE
HÁBITOS: 89c9ec16837b454c9ce98e543cc62266 ← YA EXISTE
```

**Endpoints Nuevos:**
```
GET  /api/nauta/rueda                    ← Lee Rueda de Vida
GET  /api/nauta/habitos                  ← Lee Hábitos para hoy
GET  /api/nauta/cierres-historial        ← Lee historial de cierres
POST /api/nauta/save-cierre (MODIFICADO) ← Ahora guarda en Notion
```

---

**Documento**: NAUTA Setup Notion - Fase 1  
**Autor**: Coaching Automation System  
**Fecha**: 2026-04-12
