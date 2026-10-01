# DEPLOYMENT TESTEOLAB EN RENDER.COM

**Fecha de Deployment:** 11 Abril 2026
**Usuario:** Karina (menteenoff.net)
**Estado:** Listo para Push a GitHub y Deploy en Render

## 1. ARCHIVOS PREPARADOS

Los siguientes archivos han sido configurados para Render:

```
✅ Procfile                 - Configuración de comando web para Render
✅ requirements.txt         - Dependencias Python (incluye gunicorn)
✅ runtime.txt             - Versión Python 3.11.7
✅ .gitignore              - Archivos a ignorar en git
✅ notion_api.py           - Backend Flask (sin cambios)
✅ dashboard_v2.html       - Frontend responsive (sin cambios)
✅ .env.example            - Template de variables de entorno
```

## 2. PASOS PARA COMPLETAR DEPLOYMENT

### PASO 1: CREAR REPOSITORIO EN GITHUB
1. Ir a https://github.com/new
2. Nombre del repo: `TesteoLab-Dashboard`
3. Descripción: "TesteoLab - Dashboard responsivo con integración Notion"
4. Tipo: **Public** (necesario para Render)
5. Crear repositorio

### PASO 2: PUSH A GITHUB
```bash
cd C:\apptesteo
git remote add origin https://github.com/tu-usuario/TesteoLab-Dashboard.git
git branch -M main
git push -u origin main
```

**NOTA:** Reemplaza `tu-usuario` con tu usuario de GitHub

### PASO 3: CREAR DEPLOYMENT EN RENDER.COM
1. Ir a https://render.com
2. Sign up / Sign in con GitHub
3. Click "New +" → "Web Service"
4. Conectar repositorio: `TesteoLab-Dashboard`
5. Configurar:
   - **Name:** `testeolab-dashboard`
   - **Region:** `Oregon` (us-west)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn notion_api:app --bind 0.0.0.0:$PORT`

### PASO 4: VARIABLES DE ENTORNO EN RENDER
En la sección "Environment" de Render, agregar:

```
NOTION_TOKEN=[TU_NOTION_TOKEN_AQUI]
FLASK_ENV=production
FRONT_LANGUAGE=es
CREATIVES_LANGUAGE=es
```

**IMPORTANTE:** NO incluir .env con el token en GitHub (está en .gitignore)

### PASO 5: DEPLOY
- Click "Create Web Service"
- Render iniciará build automáticamente
- Esperar a que aparezca URL (ej: https://testeolab-dashboard.onrender.com)

## 3. URL Y ACCESO

Una vez deployado:
- **URL Pública:** `https://testeolab-dashboard.onrender.com`
- **Acceso desde Celular:** URL directa en navegador (es responsive)
- **Acceso desde PC:** URL directa en navegador (Chrome, Firefox, Edge)

## 4. TESTING CHECKLIST

Después de deployar, verificar:

- [ ] Dashboard carga sin errores en navegador
- [ ] Datos de Notion se cargan correctamente
- [ ] Interfaz es responsive en celular (landscape y portrait)
- [ ] Colores y estilos cargan correctamente
- [ ] API endpoints responden (ej: /api/tareas, /api/habitos)
- [ ] No hay errores en consola del navegador (F12)
- [ ] No hay errores en logs de Render

## 5. MONITOREO EN RENDER

Una vez deployado:
- Dashboard de Render muestra logs en tiempo real
- Si hay errores, aparecerán en la sección "Logs"
- Para reiniciar: Click "Manual Deploy" en dashboard de Render

## 6. PRÓXIMOS PASOS

### Fase 2: Dominio Personalizado
```
1. Comprar dominio (Cloudflare, GoDaddy, etc.)
2. En Render, agregar dominio personalizado
3. Apuntar DNS al servidor de Render
4. Certificado SSL automático (Let's Encrypt)
```

### Fase 3: Optimizaciones
```
1. Caché de Notion (evitar rate limiting)
2. CDN para assets (dashboard_v2.html, CSS)
3. Compresión de responses
4. Monitoreo de uptime
```

## 7. SOLUCIÓN DE PROBLEMAS

### "Build Failed"
- Verificar requirements.txt está completo
- Verificar Procfile tiene sintaxis correcta
- Ver logs en Render para detalles

### "Port already in use"
- Render automáticamente asigna PORT
- Procfile ya tiene `--bind 0.0.0.0:$PORT`
- No cambiar configuración

### "Module not found"
- Verificar todas las dependencias en requirements.txt
- Render ejecuta: `pip install -r requirements.txt`

### "Notion API Error"
- Verificar NOTION_TOKEN en variables de entorno
- Token debe ser exacto (sin espacios)
- Token debe tener permisos en Notion workspace

## 8. ARCHIVOS CRÍTICOS

```
/sessions/keen-magical-feynman/mnt/apptesteo/
├── notion_api.py           ← Backend Flask (NO MODIFICAR)
├── dashboard_v2.html       ← Frontend (NO MODIFICAR)
├── requirements.txt        ← Dependencias (ACTUALIZAR si necesario)
├── Procfile               ← Configuración Render
├── runtime.txt            ← Versión Python
├── .gitignore             ← Archivos ignorados en git
├── .env.example           ← Template de env
└── .git/                  ← Repositorio Git
```

## 9. GIT STATUS

```
Rama: main
Commits: 1 (Initial commit)
Remote: origin (lista para agregar)
Estado: Listo para push
```

---

**IMPORTANTE:** Esta guía está diseñada para que Karina pueda ejecutar los pasos cuando regrese. 
Todos los archivos están listos. Solo falta: GitHub → Push → Render Deploy.
