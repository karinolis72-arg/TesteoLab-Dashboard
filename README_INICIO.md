# TESTEOLAB DASHBOARD - GUÍA DE INICIO RÁPIDO

Hola Karina,

El deployment de TesteoLab está **99% listo**. Solo necesitas ejecutar 3 pasos simples.

## 📋 QUÉ YA ESTÁ HECHO

✅ Archivos de configuración creados (Procfile, requirements.txt, runtime.txt)
✅ Repositorio Git inicializado localmente  
✅ .gitignore configurado (no sube .env por seguridad)
✅ Backend Flask listo (notion_api.py)
✅ Frontend responsive listo (dashboard_v2.html)
✅ Variables de entorno preparadas

## 🚀 QUÉ FALTA (3 PASOS - 5 MINUTOS)

### PASO 1: Crear Repositorio en GitHub (1 min)
```
1. Ve a: https://github.com/new
2. Nombre: TesteoLab-Dashboard
3. Descripción: TesteoLab - Dashboard responsivo con integración Notion
4. Tipo: PUBLIC (importante)
5. Click "Create repository"
6. COPIA LA URL que genera GitHub
```

### PASO 2: Hacer Push del Código (2 min)
```
1. Abre CMD o PowerShell
2. Navega a: cd C:\apptesteo
3. Ejecuta:
   git remote add origin [PEGA-URL-DE-GITHUB]
   git branch -M main
   git push -u origin main
4. Espera a que termine (te pedirá credenciales)
```

### PASO 3: Deploy en Render (2 min)
```
1. Ve a: https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Conecta el repo: TesteoLab-Dashboard
4. Llena:
   - Name: testeolab-dashboard
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn notion_api:app --bind 0.0.0.0:$PORT
5. Environment variables (agregar):
   NOTION_TOKEN=[TU_NOTION_TOKEN_AQUI]
   FLASK_ENV=production
   FRONT_LANGUAGE=es
   CREATIVES_LANGUAGE=es
6. Click "Create Web Service"
7. Espera a que diga "Live" (2-3 minutos)
```

## 📱 DESPUÉS DE DEPLOY

Cuando Render diga "Live":

- **URL:** https://testeolab-dashboard.onrender.com
- **En PC:** Abre en navegador
- **En Celular:** Misma URL en navegador móvil
- **Verificar:** Dashboard debe mostrar tareas de Notion

## 📚 DOCUMENTACIÓN

En C:\apptesteo encontrarás:

- `QUICK_START_RENDER.md` - Guía rápida (este archivo)
- `DEPLOYMENT_RENDER.md` - Guía completa con troubleshooting
- `GITHUB_PUSH_INSTRUCTIONS.txt` - Instrucciones paso a paso

## ❓ AYUDA RÁPIDA

| Problema | Solución |
|----------|----------|
| "Build failed" en Render | Ver Logs en Render. Generalmente error en requirements.txt (ya verificado ✓) |
| Credenciales Git | Usar Personal Access Token (PAT) en GitHub si pide password |
| Dashboard se ve blanco | Abrir F12 → Console. Ver si hay errores de CORS |
| Notion no carga datos | Verificar NOTION_TOKEN en Render matches con el token correcto |

## 🎯 OBJETIVO FINAL

Dashboard accesible desde celular y PC en:
```
https://testeolab-dashboard.onrender.com
```

---

**Cuando termines, el dashboard estará online 24/7 en Render.**
**Próximo paso después de esto: Agregar dominio personalizado (opcional).**

¡Suerte\!
