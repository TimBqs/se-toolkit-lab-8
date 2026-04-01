# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

Nanobot gateway startup logs showing successful deployment:

```
nanobot-1  | Resolved config written to /app/nanobot/config.resolved.json
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-04-01 21:56:45.986 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-04-01 21:56:48.940 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-04-01 21:56:50.778 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
nanobot-1  | 2026-04-01 21:56:50.778 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
```

**Verification commands:**
```bash
docker compose --env-file .env.docker.secret ps nanobot
# Shows: se-toolkit-lab-8-nanobot-1  Up

docker compose --env-file .env.docker.secret logs nanobot --tail 20
# Shows: Agent loop started, MCP servers connected
```

## Task 2B — Web client

### WebSocket Endpoint Test

```bash
echo '{"content":"What can you do in this system?"}' | websocat "ws://localhost:42002/ws/chat?access_key=secret"
```

**Response:** Agent returns capabilities description with LMS tools available.

### Flutter Web Client

Access URL: `http://localhost:42002/flutter`

**Login:** Enter `NANOBOT_ACCESS_KEY=secret`

### Screenshots

**Figure 1: Flutter Login Screen**
![Flutter Login Screen](screenshots/task2b-login.png)

**Figure 2: Agent Conversation with LMS Response**
![Agent Conversation](screenshots/task2b-conversation.png)

*Screenshot should show:*
- Login screen with access key input
- Chat conversation with at least one real LMS-backed answer
- Structured lab-choice UI (if multiple labs exist)

### Upload Screenshots

From your local machine, run:

```bash
# Replace <your-username> and <vm-ip> with your actual values
scp screenshots/task2b-login.png root@<vm-ip>:/root/se-toolkit-lab-8/screenshots/
scp screenshots/task2b-conversation.png root@<vm-ip>:/root/se-toolkit-lab-8/screenshots/

# Or using full path:
scp /path/to/local/screenshot.png root@<vm-ip>:/root/se-toolkit-lab-8/screenshots/task2b-conversation.png
```

### Files Modified for Task 2

| File | Change |
|------|--------|
| `nanobot/pyproject.toml` | Added nanobot-webchat, mcp-webchat dependencies |
| `nanobot/entrypoint.py` | Added webchat channel + mcp_webchat MCP config injection |
| `nanobot/Dockerfile` | Added COPY for nanobot-websocket-channel |
| `.dockerignore` | Added `!nanobot-websocket-channel/` exception |
| `pyproject.toml` | Added websocket-channel workspace members |
| `docker-compose.yml` | Uncommented Flutter service, caddy mounts, UI relay env vars |
| `caddy/Caddyfile` | Uncommented `/flutter*` route, added WebSocket timeout settings |
| `.env.docker.secret` | Changed `QWEN_CODE_AUTH_USE=false` → `true` |

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
