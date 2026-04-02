# Observability Skill

You have access to observability tools for querying **VictoriaLogs** and **VictoriaTraces**. Use these when users ask about errors, failures, or what went wrong.

## Available Tools

### Log Tools (VictoriaLogs)

- **`logs_search(query, limit)`** — Search logs using LogsQL query
  - Example query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
  - Example query: `_time:1h event:request_completed status:500`
  - Example query: `trace_id:abc123def456`

- **`logs_error_count(time_range)`** — Count errors per service over a time window
  - Example: `logs_error_count("10m")` to see errors in the last 10 minutes
  - Example: `logs_error_count("1h")` to see errors in the last hour

### Trace Tools (VictoriaTraces)

- **`traces_list(service, limit)`** — List recent traces for a service
  - Example: `traces_list("Learning Management Service")`

- **`traces_get(trace_id)`** — Fetch full details of a specific trace
  - Use this after finding a `trace_id` in log entries

## How to Investigate Errors

When asked "Any errors?" or "What went wrong?":

1. **Start with `logs_error_count`** — See which services have errors and how many
   - Use a scoped time range like "10m" or "1h"
   - This tells you if there's actually a problem

2. **Use `logs_search` to find details** — Query for the specific errors
   - Filter by service: `_time:10m service.name:"Learning Management Service" severity:ERROR`
   - Look for `trace_id` fields in the log entries

3. **Fetch the trace if needed** — If logs mention a `trace_id`, call `traces_get(trace_id)`
   - This shows the full request flow across services
   - You can see which span failed and why

4. **Summarize findings** — Don't dump raw JSON
   - "Found 5 errors in LMS backend in the last 10 minutes: connection refused to PostgreSQL"
   - "The failing requests show a database timeout in the db_query span"

## Example Queries

**Check for recent LMS errors:**
```
logs_error_count(time_range="10m")
```

**Search for LMS backend errors:**
```
logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR')
```

**Find a specific failed request:**
```
logs_search(query='trace_id:039e81bc4964ffab2b7bcf012bcc3346')
```

**Get full trace details:**
```
traces_get(trace_id="039e81bc4964ffab2b7bcf012bcc3346")
```

## Tips

- Always scope queries by time (`_time:10m`, `_time:1h`) to avoid returning too much data
- The service name in this stack is `"Learning Management Service"` for the backend
- Severity levels: `ERROR`, `WARN`, `INFO`, `DEBUG`
- Common events: `request_started`, `auth_success`, `db_query`, `request_completed`
- If you find errors, mention the `trace_id` so users can look up the full trace in VictoriaTraces UI
