# QUICK START - DEPLOY TESTEOLAB EN RENDER

## CHECKLIST RÁPIDO (5 MINUTOS)

### 1️⃣ GitHub (2 min)
```bash
# Abre CMD/PowerShell en C:\apptesteo
cd C:\apptesteo

# Crear repo en https://github.com/new
# Nombre: TesteoLab-Dashboard
# Tipo: PUBLIC

# Luego ejecutar:
git remote add origin https://github.com/[TU-USUARIO]/TesteoLab-Dashboard.git
git branch -M main
git push -u origin main
```

**Esperar:** Git te pedirá credenciales. Usar PAT (Personal Access Token) si sale error de autenticación.

### 2️⃣ Render (2 min)
1. Ve a https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Conecta repo: `TesteoLab-Dashboard`
4. Llena:
   - Name: `testeolab-dashboard`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn notion_api:app --bind 0.0.0.0:$PORT`
5. Agrega variables de entorno:
   ```
   NOTION_TOKEN=[TU_NOTION_TOKEN_AQUI]
   FLASK_ENV=production
   FRONT_LANGUAGE=es
   CREATIVES_LANGUAGE=es
   ```
6. Click "Create Web Service"

### 3️⃣ Esperar (1 min)
- Render mostrará "Building..." → "Deploying..." → "Live"
- Cuando aparezca URL verde, ¡LISTO\!
- Ejemplo: `https://testeolab-dashboard.onrender.com`

---

## TESTING INMEDIATO

Después que Render diga "Live":

1. **Desde PC:** Abre la URL en navegador
   ```
   https://testeolab-dashboard.onrender.com
   ```

2. **Desde Celular:** 
   - Misma URL en navegador del celular
   - Debe verse responsive (menú colapsado, botones grandes)

3. **Verificar Datos:**
   - Dashboard debe mostrar tareas y hábitos de Notion
   - Si no carga: revisar logs de Render (Dashboard → Logs)

---

## TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| "Build failed" | Ver Render → Logs. Generalmente falta `gunicorn` en requirements.txt (ya está ✓) |
| "Module not found" | Render automáticamente instala `requirements.txt`. Esperar 2-3 min. |
| "Port already in use" | No cambiar nada. Render usa $PORT dinámicamente. |
| Notion 404 | Verificar NOTION_TOKEN en Render env vars. Debe ser exacto. |
| Dashboard se ve blanco | Revisar F12 → Console. Ver si hay errores de CORS. |

---

## URLS IMPORTANTES

- **GitHub:** https://github.com/new
- **Render Dashboard:** https://render.com/dashboard
- **Tu Dashboard:** https://testeolab-dashboard.onrender.com (después de deploy)
- **Notion Token:** Ya configurado en Render env vars

---

## ARCHIVOS LISTOS

```
C:\apptesteo\
├── Procfile              ✓ Configurado
├── requirements.txt      ✓ Con gunicorn
├── runtime.txt          ✓ Python 3.11.7
├── .gitignore           ✓ Listo
├── notion_api.py        ✓ Backend
├── dashboard_v2.html    ✓ Frontend
└── .git/                ✓ Repositorio
```

**TODO ESTÁ LISTO. Solo ejecutar GitHub → Render.**

