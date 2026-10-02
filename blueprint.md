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

## Spin-down del plan free — RESUELTO con cron externo

Render avisa: *"Your free instance will spin down with inactivity"*. Un servicio
dormido no ejecuta jobs de APScheduler. Confirmado en la práctica: un TEST RUN
contra el servicio dormido devolvió 503 antes de llegar siquiera a Flask.

Solución montada en **cron-job.org**, zona horaria America/Argentina/Buenos_Aires:

| Job | Hora | Método | URL |
|---|---|---|---|
| 01 Despierta | 8:25 | GET | `/api/health` |
| 02 NAUTA Briefing | 8:30 | POST | `/api/nauta/trigger-briefing` |
| 03 Despertar noche | 21:25 | GET | `/api/health` |
| 04 NAUTA Cierre | 21:30 | POST | `/api/nauta/trigger-cierre` |

Los dos GET van sin credenciales (`/api/health` está exento del guardia a
propósito, para monitores externos). Los dos POST usan Basic auth con
`NAUTA_USER` / `NAUTA_PASS`. Los cuatro probados con TEST RUN: OK.

Los pings de 8:25 y 21:25 son imprescindibles: despiertan el servicio cinco
minutos antes, porque el arranque en frío tarda hasta 50 segundos y el POST daría
timeout. Con esto NAUTA corre todos los días sin plan pago y sin depender de que
el proceso siga vivo entre medio.

## Autenticación

El servicio estaba **completamente abierto**: los 38 endpoints, en una URL pública
escrita en los docs de un repo público. Cualquiera podía leer las tareas,
borrarlas (`DELETE /api/tasks/<id>`), y gastar crédito de Anthropic vía
`POST /api/chat`, sin tope.

Resuelto el 01-oct con un `@app.before_request` de Basic auth (commit `95f3824`).
Diseño: si `NAUTA_USER` y `NAUTA_PASS` no están definidas, la protección queda
apagada y solo loguea un warning. Eso mantiene el desarrollo local sin fricción;
en Render están cargadas, así que ahí sí exige credenciales.

## Zona horaria del contenedor — RESUELTO

Render corre en UTC. El `/api/health` devolvió `2026-10-02T00:36` cuando en
Buenos Aires eran las 21:36 del 1-oct. Hay **31 llamadas a `datetime.now()` sin
zona horaria**, siete de ellas calculando la fecha de hoy.

Impacto: de 21:00 en adelante, en UTC ya es el día siguiente. El cierre de las
21:30 se guardaría en Notion con la fecha de mañana y traería las tareas
programadas para mañana. El briefing de 8:30 no se ve afectado (11:30 UTC, mismo
día).

Arreglo: variable `TZ=America/Argentina/Buenos_Aires` cargada en Render el 01-oct,
en vez de tocar las 31 llamadas. En Linux, Python respeta esa variable, así que
todas pasan a devolver hora de Buenos Aires sin cambiar una línea de código.
Local no se ve afectado: Windows ya está en esa zona.

La prueba es el `timestamp` de `/api/health`: tiene que coincidir con el reloj
de Buenos Aires, no ir tres horas adelante.

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

## Estructura (reorganizada el 01-oct)

La raíz pasó de **68 entradas a 23**. Lo que quedó arriba es solo código y config.

```
TesteoLab/
├── notion_api.py          app Flask, 38 endpoints. Render la busca acá, NO MOVER
├── nauta_scheduler.py     APScheduler, cron 8:30 y 21:30 Buenos Aires
├── dashboard_v2.html      frontend real (126 KB). NO MOVER: ruta relativa
├── m1_supabase.py · supabase_client.py · run_dashboard.py · start_testeolab.py
├── requirements.txt · Procfile · runtime.txt · .env · .gitattributes
├── iniciar.bat            lanzador (corregido 01-oct)
├── CLAUDE.md · blueprint.md
├── salidas/               ignorado por git — se regenera, no es fuente
│   ├── cierres/           13 archivos (NAUTA_CIERRE_*, etc.)
│   ├── planners/          12 (planner_semana_*, .ics, eventos_gcal)
│   └── reportes/          12 (ESTADO_*, RESUMEN_*, CONTROL_EJECUCION_*)
├── _archivo/              ignorado — dashboard.html v1, los .bak, testImage/
├── docs/ · Documentos/ · DOCCOntextoBuild/ · scripts/ · tests/
└── M1/ · fronted-design/
```

**Dos archivos no se pueden mover**: `notion_api.py` (el Procfile dice
`gunicorn notion_api:app`) y `dashboard_v2.html` (lo lee con ruta relativa al
propio archivo).

`testImage/` pasó a `_archivo/`: eran 12 capturas de debug que se habían subido a
un repo público.

## NAUTA — qué cambió el 01-oct

**El cierre de 21:30 era un diccionario hardcodeado.** No consultaba Notion:
escribía `completadas: 2`, `pendientes: 2` y dos tareas de ejemplo de abril
("Investigar ofertas Meta Ads (M1)", "Crear MVP landing page (M2)") todas las
noches, con una nota inventada. Ahora lee las tareas reales del día y separa
completadas de pendientes.

**La "Recomendación del Día" era texto fijo.** Lo único variable era el número de
tareas; decía exactamente lo mismo desde abril. Ahora la arma
`_armar_recomendacion()` con cinco ramas deterministas, por orden de lo que más
traba el día: zombies → sobrecarga de horas → pendientes de anoche → Q1 →
día vacío. Es determinista a propósito: no depende de la API de Anthropic, no
cuesta, y no puede fallar a las 8:30.

**Tareas zombie.** Una tarea arrastrada más de `DIAS_PARA_ZOMBIE` (5) días deja de
listarse como tarea y pasa a un panel propio como decisión pendiente: *"¿hoy,
fecha nueva, o la matás?"*. Ataca el patrón de acumular frentes abiertos.

**Continuidad briefing ↔ cierre.** El briefing ahora lee los pendientes del cierre
de anoche desde `nauta_state["cierre_data"]`. Dejaron de ser dos reportes sueltos.

**Presupuesto de atención.** Suma `Tiempo_estimado` (que estaba en Notion sin
usarse) y lo compara con `HORAS_UTILES_DIA` (6). Si no entra, lo dice.

### Pendiente en NAUTA
- **La rueda de vida como alerta** necesita histórico; hoy solo hay el valor
  actual, así que no se puede calcular tendencia sin persistir snapshots.
- **El número del negocio** (gasto y CPA desde MetaAdsCLI) no se puede traer:
  ese proyecto corre en la máquina de Kari y Render no lo alcanza. Haría falta
  que MetaAdsCLI empuje el dato a Notion o a Supabase primero.

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
1. Arreglar el `BASE_URL` hardcodeado (`dashboard_v2.html:1164`)
2. Pasar el repo a privado
3. `git gc --prune=now` (quedaron temporales en `.git/objects`)
4. Mirar el history de cron-job.org después de la primera semana completa
