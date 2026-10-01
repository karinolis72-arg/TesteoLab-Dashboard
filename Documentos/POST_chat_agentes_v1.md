# POST — Chat de Agentes v1
**Fecha: 2026-04-12**

## Qué se hizo

### Backend (notion_api.py)
- Agregado `import anthropic` (condicional en el endpoint)
- Agregado dict `AGENT_SYSTEM_PROMPTS` con system prompts para: NAUTA, Espía, Crea, Creativo, Analista Meta, SISTEMA
- Agregado endpoint `POST /api/chat` que:
  - Recibe: `{agent, message, history[], context}`
  - Usa `claude-sonnet-4-6`
  - Mantiene historial de hasta 20 mensajes
  - Inyecta contexto dinámico (estado NAUTA si el agente es NAUTA)
  - Retorna: `{success, reply, agent, input_tokens, output_tokens}`
  - Error claro si falta `ANTHROPIC_API_KEY`

### Frontend (dashboard_v2.html)
- Agregado CSS del panel de chat flotante (desliza desde la derecha)
- Agregado botón "💬 HABLAR CON NAUTA" en módulo NAUTA
- Agregado contenido completo para módulos M1, M2, M3, M4, SISTEMA:
  - Descripción del módulo
  - KPIs con IDs para actualización dinámica futura
  - Flujo visual paso a paso
  - Botón "💬 Hablar con [Agente]"
- Actualizado sidebar: íconos M3→🎨, M4→📈, etiquetas con nombres de agentes
- Agregado HTML del panel de chat (flotante, lado derecho)
- Agregado JS completo del chat:
  - `openChat(agent, avatar, role)` — abre el panel con el agente correcto
  - `closeChat()` — cierra el panel
  - `sendChatMessage()` — envía a `/api/chat`, maneja respuesta, typing indicator
  - Historial persistido en `localStorage` por agente
  - Adjuntar archivos (`.txt`, `.md`, `.html`, `.csv`, `.json` — máx 100KB)
  - Micrófono (Web Speech API, idioma `es-AR`) → transcribe a texto
  - `clearChatHistory()` — limpia conversación actual

### requirements.txt
- Agregado `anthropic==0.40.0`

## Qué falta para que funcione al 100%
1. **`ANTHROPIC_API_KEY`** en `.env` (sin esto el chat devuelve error descriptivo)
2. Si la key no está, el chat muestra instrucciones para obtenerla

## Cómo probarlo
1. Agregar `ANTHROPIC_API_KEY=sk-ant-...` al `.env`
2. Reiniciar el servidor: `python notion_api.py`
3. Abrir el dashboard → click en cualquier módulo → click "💬 Hablar con [Agente]"
4. El panel se desliza desde la derecha con el agente correcto

## Archivos modificados
- `notion_api.py` — endpoint `/api/chat` + system prompts
- `dashboard_v2.html` — UI de chat + contenido M1-M4 + SISTEMA
- `requirements.txt` — agregado anthropic
