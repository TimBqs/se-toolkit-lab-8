"""
VictoriaLogs and VictoriaTraces HTTP API clients.

These clients provide low-level access to the observability backends.
The MCP server wraps these as tools for the agent.
"""

import httpx
from typing import Any


class VictoriaLogsClient:
    """Client for VictoriaLogs HTTP API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=30.0)

    def search(self, query: str, limit: int = 50, time_range: str = "1h") -> list[dict[str, Any]]:
        """
        Search logs using LogsQL query.

        Args:
            query: LogsQL query string (e.g., '_time:1h service.name:"backend" severity:ERROR')
            limit: Maximum number of log entries to return
            time_range: Time range override (query may contain its own _time filter)

        Returns:
            List of log entries as dictionaries
        """
        url = f"{self.base_url}/select/logsql/query"
        params = {"query": query, "limit": str(limit)}

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            # VictoriaLogs returns JSON array of log entries
            return response.json() if response.text else []
        except httpx.HTTPError as e:
            return [{"error": f"VictoriaLogs query failed: {str(e)}"}]

    def count_errors(self, time_range: str = "1h") -> list[dict[str, Any]]:
        """
        Count errors per service over a time window.

        Args:
            time_range: Time window (e.g., "1h", "10m", "24h")

        Returns:
            List of {service: str, count: int} dictionaries
        """
        query = f'_time:{time_range} severity:ERROR | stats by (service.name) count()'
        return self.search(query, limit=100)


class VictoriaTracesClient:
    """Client for VictoriaTraces HTTP API (Jaeger-compatible)."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=30.0)

    def list_traces(self, service: str, limit: int = 20) -> list[dict[str, Any]]:
        """
        List recent traces for a service.

        Args:
            service: Service name to filter traces
            limit: Maximum number of traces to return

        Returns:
            List of trace summaries
        """
        url = f"{self.base_url}/select/jaeger/api/traces"
        params = {"service": service, "limit": str(limit)}

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            # Jaeger API returns {"data": [...]}
            return data.get("data", []) if isinstance(data, dict) else []
        except httpx.HTTPError as e:
            return [{"error": f"VictoriaTraces list failed: {str(e)}"}]

    def get_trace(self, trace_id: str) -> dict[str, Any]:
        """
        Fetch a specific trace by ID.

        Args:
            trace_id: The trace ID to fetch

        Returns:
            Full trace data with spans
        """
        url = f"{self.base_url}/select/jaeger/api/traces/{trace_id}"

        try:
            response = self.client.get(url)
            response.raise_for_status()
            data = response.json()
            # Jaeger API returns {"data": [trace]}
            traces = data.get("data", []) if isinstance(data, dict) else []
            return traces[0] if traces else {"error": "Trace not found"}
        except httpx.HTTPError as e:
            return {"error": f"VictoriaTraces fetch failed: {str(e)}"}
