# Blueprint — TesteoLab

> Estado vivo del proyecto. Lo reescribe Claude Code; no hace falta editarlo a mano.
> Última actualización: 2026-10-01

## Qué quiero lograr
Dashboard Flask + Notion con el scheduler NAUTA (briefing 8:30 / cierre 21:30),
desplegado en Render, con los datos persistiendo en Notion.

## En qué punto está
- ✅ Proyecto en `C:\ClaudeProyectos\01-activos\TesteoLab`
- ✅ Corre local: `python notion_api.py` → http://localhost:5000
- ✅ Los 38 endpoints responden; NAUTA arranca con la app (notion_api.py línea ~56)
- 🔴 **102 cambios sin commitear.** Último commit: 11-abr-2026
- 🔴 **Producción (Render) está mutilada**: ver "Deuda crítica" abajo
- ✅ `.env` correctamente excluido por `.gitignore`

## Deuda crítica — producción ≠ local

**1. Tres archivos de código nunca se commitearon** (sin trackear desde el día uno):
`nauta_scheduler.py`, `supabase_client.py`, `m1_supabase.py`.
`notion_api.py` los importa dentro de `try/except ImportError`, así que en Render
`NAUTA_ENABLED = False` y **el briefing de 8:30 y el cierre de 21:30 nunca
corrieron en producción**. Los `NAUTA_CIERRE_*.md` del repo salieron de
ejecuciones locales.

**2. `requirements.txt` en origin no tiene** `APScheduler`, `anthropic` ni
`supabase`. Aunque se suba el scheduler, Render falla al importar hasta
commitear el requirements.

**3. `BASE_URL` hardcodeado** — `dashboard_v2.html` línea 1164:
`BASE_URL = "http://localhost:5000/api"`. En Render eso apunta a la máquina de
Kari, no al servidor. Convive con llamadas a rutas relativas (`/api/...`), así
que en producción parte del dashboard funciona y parte no. **Pendiente**: hacerlo
relativo o derivarlo de `window.location.origin`.

## Archivos en juego
- `notion_api.py` — app Flask principal, 38 endpoints. Render la busca acá, no mover
- `nauta_scheduler.py` — APScheduler, cron 8:30 y 21:30 America/Argentina/Buenos_Aires
- `dashboard_v2.html` — frontend real (126 KB). `dashboard.html` es la v1 de abril, obsoleta
- `iniciar.bat` — lanzador corregido 01-oct
- `run_dashboard.py` — ya no sirve el dashboard; redirige 9000 → 5000
- Nueve `planner_semana_*.xlsx` — salidas, no fuente. No deberían ir al repo

## Intentos fallidos — leer antes de repetirlos

**`notion-client==2.0.1` no existe.** Un cambio sin commitear había bajado la
versión de `2.2.1` a `2.0.1`. `pip install -r requirements.txt` aborta con
*"No matching distribution found"* y no instala nada de lo que viene después en
el archivo. Las versiones reales en PyPI saltan de `2.0.0` a `2.1.0`.
Revertido a `2.2.1` el 01-oct.

**Repuntar `run_dashboard.py` a la v2 no alcanzaba.** La idea inicial era que
sirviera `dashboard_v2.html` en el puerto 9000. No funciona: la v2 hace fetch a
rutas relativas (`/api/...`), que en el 9000 dan 404 porque ahí no hay backend.
Se convirtió en redirector al 5000.

**`iniciar.bat` apuntaba a `C:\apptesteo`.** Quedó de antes de la migración.
Esa carpeta existe pero está casi vacía. Corregido a `%~dp0` (la carpeta del
propio .bat), que sobrevive a futuras mudanzas. De paso se le sacó un
`taskkill /f /im python.exe` que mataba todos los procesos Python de la máquina.

**El briefing mostraba "0 tareas" con tareas cargadas.** No era un filtro mal
hecho: las consultas a Notion de `notion_api.get_today_tasks()` y
`nauta_scheduler._get_today_tasks()` son idénticas. El problema era que
`/api/nauta/briefing-html` leía `nauta_state["briefing_data"]`, que solo se
puebla cuando corre el job de las 8:30. Arrancando el server a la tarde, ese
dict está vacío → `total_tareas_hoy` cae al default 0 y "Generado a las" sale en
blanco. Resuelto con `ensure_briefing_data()` (01-oct), que regenera si el
guardado está vacío o es de otro día.

## Siguientes pasos
1. Commitear en tandas: código → frontend → limpieza de los 38 borrados → docs
2. `git push` y verificar en el log de Render que NO aparezca
   `⚠️ Warning: nauta_scheduler no disponible`
3. Arreglar el `BASE_URL` hardcodeado antes de confiar en producción
4. Agregar `.gitattributes` (con `*.bat text eol=crlf`) y sacar del repo las
   salidas: `NAUTA_CIERRE_*.md`, `planner_semana_*.xlsx`
5. Limpiar las nueve versiones viejas de `planner_semana`
