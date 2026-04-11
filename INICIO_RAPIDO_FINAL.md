# 🚀 TESTEOLAB - INICIO RÁPIDO FINAL

**Estado General**: ✅ 95% Completado  
**Fecha**: 11 Abril 2026  
**Próximo Paso**: Ejecutar script PowerShell + Deploy en Render

---

## ✅ QUÉ YA ESTÁ LISTO

### Código Sprint 1 v2.0
- ✅ Arreglo #1: Pausar notificaciones con 6 opciones de tiempo
- ✅ Arreglo #2: Cerrar notificaciones permanentemente
- ✅ Arreglo #3: Selector de tema (CLARA/DARK/MINIMAL/COLORFUL/ENERGY)
- ✅ Arreglo #5: NAUTA con datos reales de Notion

### Configuración Render
- ✅ Procfile configurado
- ✅ requirements.txt con gunicorn
- ✅ runtime.txt con Python 3.11.7
- ✅ .gitignore configurado (no sube .env)
- ✅ Dashboard responsive listo

### Documentación
- ✅ NOTION_TOKEN reemplazado con placeholder en todos los archivos
- ✅ Guías paso a paso creadas
- ✅ Script PowerShell de reparación listo

---

## 🎯 PRÓXIMOS 3 PASOS (15 MINUTOS)

### PASO 1: Ejecutar Script PowerShell (2 min)
```powershell
# Abre PowerShell como Administrador
cd C:\apptesteo

# Ejecuta el script:
.\FIX_GIT_AND_PUSH.ps1
```

**Qué hace**:
- Limpia el repositorio .git corrupto
- Crea nuevo repositorio Git
- Hace commit de todos los archivos
- Hace push a GitHub automáticamente
- Te pide credenciales de GitHub (PAT - Personal Access Token)

**Si pide credenciales**:
- Username: tu-usuario-github
- Password: [Personal Access Token]
  - Si no tienes PAT, crea uno en: https://github.com/settings/tokens

---

### PASO 2: Crear Web Service en Render (3 min)
1. Ve a: https://render.com/dashboard
2. Click "New +" → "Web Service"
3. **Conectar repositorio**: Selecciona "TesteoLab-Dashboard"
4. **Configuración básica**:
   - Name: `testeolab-dashboard`
   - Region: `Oregon` (us-west)
   - Runtime: `Python 3`
5. **Comandos**:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn notion_api:app --bind 0.0.0.0:$PORT`
6. **Environment Variables** (Agregar en la sección "Environment"):
   ```
   NOTION_TOKEN=[TU_NOTION_TOKEN_AQUI]
   FLASK_ENV=production
   FRONT_LANGUAGE=es
   CREATIVES_LANGUAGE=es
   ```
   ⚠️ Reemplaza `[TU_NOTION_TOKEN_AQUI]` con tu token real de Notion
7. Click "Create Web Service"

**Esperar**: Render iniciará build automáticamente (2-3 minutos)

---

### PASO 3: Verificar Deploy en Render (1 min)
1. Ir a https://render.com/dashboard
2. Buscar "testeolab-dashboard"
3. Esperar a que estado cambie de "Building..." → "Live"
4. Cuando sea "Live", copiar URL (ej: https://testeolab-dashboard.onrender.com)
5. **Prueba desde PC**: Abre URL en navegador
6. **Prueba desde Celular**: Abre URL en navegador del celular

**Verificar que funcione**:
- ✅ Dashboard carga sin errores
- ✅ Aparecen datos de Notion (tareas, hábitos)
- ✅ Interfaz es responsive (se ve bien en celular)
- ✅ Todos los botones funcionan

---

## 📍 URLS IMPORTANTES

| Recurso | URL |
|---------|-----|
| Script reparación | C:\apptesteo\FIX_GIT_AND_PUSH.ps1 |
| GitHub repo | https://github.com/karinolis/TesteoLab-Dashboard |
| Render dashboard | https://render.com/dashboard |
| Tu dashboard | https://testeolab-dashboard.onrender.com |
| Notion token | Guardado en Render env vars |

---

## 🔐 SEGURIDAD

✅ **Token Notion**:
- NO está en archivos de GitHub (está en Render env vars)
- NO está en documentación pública
- Almacenado seguro en Render

✅ **.env local**:
- No está en git (ignorado por .gitignore)
- No se sube a GitHub

---

## ❓ TROUBLESHOOTING RÁPIDO

| Problema | Solución |
|----------|----------|
| "Git not recognized" | Reinicia PowerShell o instala Git |
| "403 Forbidden" en push | Verifica credenciales GitHub (usa PAT, no password) |
| "Build failed" en Render | Ver Logs en Render dashboard. Verificar requirements.txt |
| Dashboard se ve blanco | F12 → Console. Ver si hay errores CORS |
| Notion no carga datos | Verificar NOTION_TOKEN en Render env vars es exacto |

---

## 📅 PRÓXIMAS FASES (Después de Deploy)

### Fase 2: Calendar Integration (Sprint 2)
- Conectar Google Calendar API
- Sincronizar eventos ↔ Notion
- Mostrar disponibilidad en NAUTA

### Fase 3: Dominio Personalizado
- Comprar dominio (ej: dashboard.menteenoff.net)
- Apuntar DNS a Render
- SSL automático con Let's Encrypt

### Fase 4: Optimizaciones
- Caché de Notion
- CDN para assets
- Monitoreo de uptime

---

## 📚 ARCHIVOS DE REFERENCIA

```
C:\apptesteo\
├── FIX_GIT_AND_PUSH.ps1          ← EJECUTA ESTO
├── QUICK_START_RENDER.md          ← Guía rápida
├── DEPLOYMENT_RENDER.md           ← Guía detallada
├── README_INICIO.md               ← Instrucciones en español
├── dashboard_v2.html              ← Frontend listo
├── notion_api.py                  ← Backend listo
├── requirements.txt               ← Dependencias
├── Procfile                       ← Config Render
├── runtime.txt                    ← Versión Python
├── .gitignore                     ← Archivos ignorados
└── SPRINT1_V2_CAMBIOS_COMPLETADOS.md  ← Documentación cambios
```

---

## ✨ RESUMEN

**Antes**: TesteoLab era local en PC, sin acceso desde celular, con arreglos pendientes.

**Después**: 
- ✅ TesteoLab en producción (Render)
- ✅ Accesible desde PC y celular
- ✅ Datos reales de Notion
- ✅ Notificaciones pausables
- ✅ Cierre permanente de notificaciones
- ✅ 5 temas disponibles
- ✅ Seguro (token no expuesto)

**Tiempo total**: ~15 minutos

---

**¡Listo para deploy! 🎉**

Ejecuta `.\FIX_GIT_AND_PUSH.ps1` cuando estés en C:\apptesteo.
