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

### Quick Health Check

When asked **"Any errors?"** or **"Is the system healthy?"**:

1. **Start with `logs_error_count`** — See which services have errors and how many
   - Use a scoped time range like "10m" or "1h"
   - This tells you if there's actually a problem

2. **Use `logs_search` to find details** — Query for the specific errors
   - Filter by service: `_time:10m service.name:"Learning Management Service" severity:ERROR`
   - Look for `trace_id` fields in the log entries

3. **Summarize findings** — Don't dump raw JSON
   - "Found 5 errors in LMS backend in the last 10 minutes: connection refused to PostgreSQL"
   - "The failing requests show a database timeout in the db_query span"

### Full Investigation Flow

When asked **"What went wrong?"** or **"Check system health"** or **"Investigate the failure"**:

Follow this complete investigation flow in a single pass:

1. **Call `logs_error_count("10m")`** — Get error counts per service for the last 10 minutes
   - This identifies which service is failing

2. **Call `logs_search()`** — Find specific error details
   - Query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
   - Extract the `trace_id` from the most recent error log entry

3. **Call `traces_get(trace_id)`** — Fetch the full trace using the trace_id from step 2
   - This shows the complete request flow and which span failed

4. **Synthesize a single coherent response** that includes:
   - **Log evidence**: What the error logs show (error message, timestamp, service)
   - **Trace evidence**: What the trace shows (which span failed, duration, error location)
   - **Root cause**: Name the affected service and the failing operation
   - **HTTP status discrepancy** (if applicable): Note if the HTTP response code doesn't match the actual error

**Example investigation response:**
```
## Investigation Results

**Log Evidence:**
Found 3 errors in Learning Management Service in the last 10 minutes.
Most recent error at 19:21:00:
- Event: db_query
- Error: "connection is closed"
- Trace ID: dce031501ad0813848698c1e9f20d224

**Trace Evidence:**
Trace dce031501ad0813848698c1e9f20d224 shows:
- Root span: GET /items/ (HTTP request)
- Failed span: db_query (duration: 2ms)
- Error location: app.db.items - SQLAlchemy connection failure

**Root Cause:**
The LMS backend (Learning Management Service) is failing because PostgreSQL is unavailable.
The db_query operation cannot establish a database connection.

**Note:** The HTTP response shows 404 "Items not found" but the actual error is a database connection failure (should be 500).
```

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
- For "What went wrong?" always chain: error_count → logs_search → traces_get → summary
