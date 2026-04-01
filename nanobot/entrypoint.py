#!/usr/bin/env python3
"""
Entrypoint for nanobot gateway in Docker.

Reads config.json, injects environment variables for:
- LLM provider API key and base URL
- Gateway host/port
- Webchat host/port
- MCP server env vars (backend URL + API key)
- Webchat channel config (Task 2B)
- MCP webchat server config (Task 2B)

Writes config.resolved.json and execs nanobot gateway.
"""

import json
import os
import sys

CONFIG_PATH = "/app/nanobot/config.json"
RESOLVED_CONFIG_PATH = "/app/nanobot/config.resolved.json"
WORKSPACE_PATH = "/app/nanobot/workspace"


def main():
    # Load the base config
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    # Inject LLM provider config from env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    # Inject MCP server env vars
    if "tools" in config and "mcpServers" in config["tools"]:
        lms_server = config["tools"]["mcpServers"].get("lms", {})
        if "env" not in lms_server:
            lms_server["env"] = {}

        backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
        backend_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

        if backend_url:
            lms_server["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url
        if backend_api_key:
            lms_server["env"]["NANOBOT_LMS_API_KEY"] = backend_api_key

    # Task 2B — Inject webchat channel config from env vars
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY")

    if "channels" not in config:
        config["channels"] = {}

    if webchat_host or webchat_port:
        config["channels"]["webchat"] = {
            "enabled": True,
            "host": webchat_host or "0.0.0.0",
            "port": int(webchat_port) if webchat_port else 8765,
            "allow_from": ["*"],
            "relay_host": "0.0.0.0",
            "relay_port": 8766,
        }

    # Task 2B — Inject mcp_webchat MCP server config
    ui_relay_url = os.environ.get("NANOBOT_UI_RELAY_URL")
    ui_relay_token = os.environ.get("NANOBOT_UI_RELAY_TOKEN")

    if ui_relay_url or ui_relay_token:
        if "mcpServers" not in config["tools"]:
            config["tools"]["mcpServers"] = {}

        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {},
        }
        if ui_relay_url:
            config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_UI_RELAY_URL"] = ui_relay_url
        if ui_relay_token:
            config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_UI_RELAY_TOKEN"] = ui_relay_token

    # Write the resolved config
    with open(RESOLVED_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Resolved config written to {RESOLVED_CONFIG_PATH}", file=sys.stderr)

    # Exec nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", RESOLVED_CONFIG_PATH, "--workspace", WORKSPACE_PATH])


if __name__ == "__main__":
    main()
