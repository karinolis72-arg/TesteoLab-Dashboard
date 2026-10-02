# Blueprint — TesteoLab

> Estado vivo del proyecto. Lo reescribe Claude Code; no hace falta editarlo a mano.
> Última actualización: 2026-10-01 (deploy verificado)

## Qué quiero lograr
Dashboard Flask + Notion con el scheduler NAUTA (briefing 8:30 / cierre 21:30),
desplegado en Render, con los datos persistiendo en Notion.

## En qué punto está
- ✅ Proyecto en `C:\ClaudeProyectos\01-activos\TesteoLab`
- ✅ Corre local: `python notion_api.py` → http://localhost:5000
- ✅ Los 38 endpoints responden; NAUTA arranca con la app (notion_api.py línea ~56)
- ✅ **Todo commiteado y pusheado** (6 commits, ~2.700 líneas) el 01-oct
- ✅ **Producción al día**: deploy `7e783c7` Live, NAUTA arranca en Render
- 🟡 **Pero el plan free duerme el servicio**: ver "Spin-down" abajo
- ✅ `.env` correctamente excluido por `.gitignore`

## Deuda crítica — estado al 01-oct

**1. Los tres archivos sin commitear** (`nauta_scheduler.py`, `supabase_client.py`,
`m1_supabase.py`) — ✅ **RESUELTO**. Commit `cebc57b`. Verificado en el log de
Render: `✓ NAUTA Scheduler iniciado`, `8:30 AM Briefing`, `21:30 Log de cierre`,
timezone Buenos Aires. Primera vez que NAUTA corre en producción.

**2. `requirements.txt` incompleto en origin** — ✅ **RESUELTO**. Los nueve
paquetes instalan. El build pasaba de largo `notion-client` por primera vez.

**3. `BASE_URL` hardcodeado** — 🔴 **PENDIENTE**. `dashboard_v2.html` línea 1164:
`BASE_URL = "http://localhost:5000/api"`. En Render apunta a la máquina de Kari.
Convive con llamadas relativas (`/api/...`), así que en producción parte del
dashboard funciona y parte no. Arreglo: derivarlo de `window.location.origin`.

## Spin-down del plan free — el límite real

Render avisa: *"Your free instance will spin down with inactivity"*. Un servicio
dormido **no ejecuta jobs de APScheduler**: a las 8:30 no hay proceso vivo que
dispare el briefing. NAUTA está correctamente configurado en producción y aun así
no va a correr solo mientras el servicio esté en free.

Opciones evaluadas (sin decidir todavía):
- Plan pago de Render — el servicio no duerme
- Ping externo cada 10 min (UptimeRobot / cron-job.org) — gratis, lo mantiene vivo
- Cron externo que llame a `/api/nauta/trigger-briefing` a las 8:30 — despierta
  el servicio Y dispara el job. Hace innecesario APScheduler en producción.
  Falta un endpoint equivalente para el cierre de 21:30.

## Seguridad — incidente del 01-oct

GitHub Push Protection frenó un push con el token de Notion hardcodeado en
`scripts/load_tasks.py:4`. Al revisar apareció que el repo es **público** y que un
token más viejo estaba expuesto desde el 11-abr en el commit `c071d6c`, dentro de
`ARCHIVOS_CREADOS_HOY.txt` y `CAMBIOS_REALIZADOS_HOY.md`. Forks: 0.

Resuelto: token rotado, los dos `.env` actualizados (TesteoLab y
`MetaAdsCLI/Configuracion/.env` compartían el mismo), variable actualizada en
Render, `load_tasks.py` ahora lee de `os.environ`, docs redactados.

**La lección**: el commit `71dcf1c "Limpieza: Remover token de documentación"`
sacó el token del archivo pero NO del historial. En git, borrar una línea no
borra el commit que la trajo. Un secreto commiteado está comprometido para
siempre; lo único que lo neutraliza es rotarlo.

Pendiente menor: pasar el repo a privado (no arregla el pasado, pero expone IDs
de bases de Notion sin ninguna ganancia).

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
1. Decidir cómo resolver el spin-down, o NAUTA en producción no corre nunca solo
2. Arreglar el `BASE_URL` hardcodeado
3. Reorganizar: los 39 archivos de salida a `salidas/`, al `.gitignore`.
   Incluye los `testImage/*.png` que se subieron a un repo público
4. Pasar el repo a privado
5. `git gc --prune=now` (quedaron temporales en `.git/objects`)
