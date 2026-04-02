"""MCP server for observability tools."""

import os
from mcp.server.fastmcp import FastMCP
from .observability import VictoriaLogsClient, VictoriaTracesClient

# Initialize MCP server
mcp = FastMCP("mcp-obs")

# Initialize clients from environment variables
VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")

logs_client = VictoriaLogsClient(VICTORIALOGS_URL)
traces_client = VictoriaTracesClient(VICTORIATRACES_URL)


@mcp.tool()
def logs_search(query: str, limit: int = 50) -> list[dict]:
    """
    Search VictoriaLogs using LogsQL query.

    Use this to find log entries matching specific criteria.
    Examples:
    - '_time:10m service.name:"Learning Management Service" severity:ERROR'
    - '_time:1h event:request_completed status:500'
    - 'trace_id:abc123'

    Args:
        query: LogsQL query string
        limit: Maximum entries to return (default: 50)

    Returns:
        List of matching log entries
    """
    return logs_client.search(query, limit)


@mcp.tool()
def logs_error_count(time_range: str = "1h") -> list[dict]:
    """
    Count errors per service over a time window.

    Use this first when asked about errors to see which services have issues.

    Args:
        time_range: Time window like "10m", "1h", "24h" (default: "1h")

    Returns:
        List of {service: str, count: int} entries
    """
    return logs_client.count_errors(time_range)


@mcp.tool()
def traces_list(service: str, limit: int = 20) -> list[dict]:
    """
    List recent traces for a service.

    Use this to see recent request traces for a specific service.

    Args:
        service: Service name (e.g., "Learning Management Service")
        limit: Maximum traces to return (default: 20)

    Returns:
        List of trace summaries with trace_id, duration, span count
    """
    return traces_client.list_traces(service, limit)


@mcp.tool()
def traces_get(trace_id: str) -> dict:
    """
    Fetch full details of a specific trace.

    Use this after finding a trace_id in logs to see the complete request flow.
    Shows all spans, their durations, and any errors.

    Args:
        trace_id: The trace ID to fetch

    Returns:
        Full trace with all spans and timing information
    """
    return traces_client.get_trace(trace_id)
