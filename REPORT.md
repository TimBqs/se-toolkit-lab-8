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

**Test Command:**
```bash
echo '{"content":"What can you do in this system?"}' | websocat "ws://localhost:42002/ws/chat?access_key=secret"
```

**Actual Response (What can you do?):**
```json
{
  "type": "text",
  "content": "I'm **nanobot** 🐈, your personal AI assistant. Here's what I can do in this system:\n\n## Core Capabilities\n\n**File & Workspace Management**\n- Read, write, and edit files in your workspace\n- List directory contents and explore project structure\n\n**Web Access**\n- Search the web for information\n- Fetch and extract content from URLs\n\n**Task Management**\n- Schedule reminders and recurring tasks (via cron)\n- Spawn subagents for background/long-running tasks\n\n## Learning Management System (LMS)\n\nI have integrated LMS tools:\n- List available labs and learners\n- Track pass rates, completion rates, and submission timelines\n- View group performance and top learners\n\n## Skills System\n\n**Available Skills:**\n- **memory** — Long-term facts + searchable event log\n- **lms** — LMS integration\n- **clawhub** — Search and install public agent skills\n- **skill-creator** — Create or update custom skills\n- **cron** — Schedule reminders and recurring tasks",
  "format": "markdown"
}
```

**Actual Response (Backend health with LMS tool call):**
```
nanobot logs show: Tool call: mcp_lms_lms_health({})

Agent Response:
The LMS backend is **healthy** ✅

- **Status**: Healthy
- **Item Count**: 56 items in the system
- **Errors**: None

Everything looks good!
```

**Actual Response (Labs list with LMS tool call):**
```
nanobot logs show: Tool call: mcp_lms_lms_labs({})

Agent Response:
Here are the available labs:

1. **Lab 01** – Products, Architecture & Roles
2. **Lab 02** — Run, Fix, and Deploy a Backend Service
3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy
4. **Lab 04** — Testing, Front-end, and AI Agents
5. **Lab 05** — Data Pipeline and Analytics Dashboard
6. **Lab 06** — Build Your Own Agent
7. **Lab 07** — Build a Client with an AI Coding Agent
8. **Lab 08** — lab-08

Would you like more details about any specific lab?
```

### Flutter Web Client

**Access URL:** `http://localhost:42002/flutter`

**Login:** Enter `NANOBOT_ACCESS_KEY=secret`

**Evidence Files:**
- `screenshots/flutter-page.html` — Saved Flutter app HTML (proves client is served)
- `screenshots/task2b-login.png` — Flutter login screen (397 KB)
- `screenshots/task2b-conversation.png` — Agent conversation screenshot (487 KB)

### Screenshots

**Figure 1: Flutter Login Screen**

![Flutter Login Screen](screenshots/task2b-login.png)

*Login page at `/flutter` — enter `NANOBOT_ACCESS_KEY=secret` to access the chat*

**Figure 2: Agent Conversation with LMS Response**

![Agent Conversation](screenshots/task2b-conversation.png)

*Agent responds with real LMS data — shows 8 available labs retrieved via `mcp_lms_lms_labs` tool*

### Evidence Files

- `screenshots/task2b-login.png` — Flutter login screen (397 KB)
- `screenshots/task2b-conversation.png` — Agent conversation with LMS response (487 KB)
- `screenshots/flutter-page.html` — Saved Flutter app HTML source

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
| `nanobot/workspace/skills/lms/SKILL.md` | Updated to use structured UI for lab selection |

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
