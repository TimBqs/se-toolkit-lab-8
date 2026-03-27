# Lab 8 — Task 1 Report

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Response:**
```
The agentic loop is the core mechanism that enables AI agents to
operate autonomously and continuously improve. It's a cyclical process 
where an AI agent doesn't just execute commands, but actively learns   
and adapts.                                                            
                                                                       
The Agentic Loop Cycle                                                 
                                                                       
The loop consists of four key stages:                                  
                                                                       
 1 Observation — The agent gathers information from its environment    
 2 Planning — Based on observations, the agent develops a strategy to  
   achieve its goal                                                    
 3 Action — The agent executes its plan and interacts with the         
   environment                                                         
 4 Reflection — The agent evaluates the results, learns from outcomes, 
   and adjusts its strategy                                            
                                                                       
Then the cycle repeats, allowing the agent to become more efficient    
over time.                                                             
                                                                       
Why It Matters                                                         
                                                                       
This enables autonomy — AI agents can accomplish complex tasks without 
constant human intervention. It's a shift from:                        
                                                                       
 • Traditional AI: Stateless request-response execution                
 • Agentic AI: Stateful, iterative, goal-oriented behavior             
                                                                       
In This Lab (Lab 8)                                                    
                                                                       
You're building nanobot, which embodies the agentic loop:              
                                                                       
 • It observes via MCP tools (querying LMS data, logs, traces)         
 • It plans how to answer user questions                               
 • It acts by calling tools and APIs                                   
 • It reflects using memory (MEMORY.md, HISTORY.md) and can schedule   
   proactive tasks                                                      
                                                                       
This is different from a simple chatbot because nanobot has persistent 
memory, reusable tools/skills, and can act proactively via scheduled   
jobs.
```

### Question 2: "What labs are available in our LMS?"

**Response:**
```
Based on the workspace, you're working on Lab 8 — The Agent is the     
Interface.                                                             
                                                                       
Available Labs in This Course                                          
                                                                       
                                                                       
 Lab      Topic                                                        
 ────────────────────────────────────────────────                      
 Lab 1–6  Previous labs (not in this workspace)                        
 Lab 7    Built a client around your own LLM loop                      
 Lab 8    The Agent is the Interface (current)                         
                                                                       
                                                                       
Lab 8 Tasks                                                            
                                                                       
Required                                                               
                                                                       
 1 Task 1 — Set Up the Agent (nanobot, Qwen API, MCP tools)            
 2 Task 2 — Deploy and Connect a Web Client (Docker, WebSocket, Flutter
   UI)                                                                 
 3 Task 3 — Give the Agent New Eyes (observability MCP tools for       
   logs/traces)                                                        
 4 Task 4 — Diagnose a Failure and Make the Agent Proactive (health    
   checks, fix bug)                                                    
                                                                       
Optional                                                               
                                                                       
 1 Task 1 — Add a Telegram Bot Client                                  
                                                                       
The lab builds on an existing LMS system with React dashboard, FastAPI 
backend, PostgreSQL, and an observability stack (OpenTelemetry,        
VictoriaLogs, VictoriaTraces). You're adding nanobot as a              
natural-language interface layer.                                      
                                                                       
Would you like me to open a specific task file for detailed            
instructions?
```

**Observation:** The bare agent answers from its workspace files but has no real LMS tools yet — it cannot query the actual backend API.

---

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Response:**
```
Here are all the labs available in the LMS:                            
                                                                       
                                                                       
 #  Lab Title                                                          
 ──────────────────────────────────────────────────────────            
 1  Lab 01 – Products, Architecture & Roles                            
 2  Lab 02 — Run, Fix, and Deploy a Backend Service                    
 3  Lab 03 — Backend API: Explore, Debug, Implement, Deploy            
 4  Lab 04 — Testing, Front-end, and AI Agents                         
 5  Lab 05 — Data Pipeline and Analytics Dashboard                     
 6  Lab 06 — Build Your Own Agent                                      
 7  Lab 07 — Build a Client with an AI Coding Agent                    
 8  lab-08 (The Agent is the Interface)                                
                                                                       
                                                                       
You're currently working on Lab 8. Would you like me to check stats for
any specific lab (pass rates, completion rate, top learners, etc.)?
```

### Question 2: "Describe the architecture of the LMS system"

**Response:**
```
                        LMS System Architecture                        
                                                                       
Overview                                                               
                                                                       
The LMS (Learning Management System) is a containerized microservices  
architecture built with Docker Compose. It provides a learning platform
with API backend, web dashboard, database, and full observability      
stack.                                                                 
                                                                       
Core Services                                                          
                                                                       
 Service           Technology           Port  Description              
 ───────────────────────────────────────────────────────────────────── 
 backend           FastAPI (Python)     8000  Main LMS API with CRUD   
                                              operations               
 postgres          PostgreSQL 18.3      5432  Persistent data storage  
 client-web-react  React + Vite         5173  Web dashboard UI         
 caddy             Caddy reverse proxy  8080  Gateway routing all      
                                              external traffic         
 pgadmin           pgAdmin 4            80    Database administration  
                                              UI                       
                                                                       
LLM & Agent Services                                                   
                                                                       
 Service              Technology      Port  Description                
 ───────────────────────────────────────────────────────────────────── 
 qwen-code-api        Qwen API proxy  8080  LLM access layer           
 nanobot              Python agent    WS    AI agent with tools/skills 
                                            (Lab 8)                    
 client-web-flutter   Flutter web     8081  Alternative chat UI (Task  
                                            2B)                        
 client-telegram-bot  Python bot      -     Telegram client (Optional) 
                                                                       
                                                                       
Observability Stack                                                    
                                                                       
 Service         Technology      Port       Description                
 ───────────────────────────────────────────────────────────────────── 
 otel-collector  OpenTelemetry   4317/4318  Receives traces & logs via 
                                            OTLP                       
 victorialogs    VictoriaLogs    9428       Log storage & query engine 
 victoriatraces  VictoriaTraces  10428      Distributed trace storage  
                                                                       
Data Flow                                                              

Request Flow                                                           
                                                                       
 1 Client (React/Flutter/Telegram) → Caddy (gateway)                   
 2 Caddy routes to appropriate backend service                         
 3 Backend queries PostgreSQL for data                                 
 4 Response flows back through Caddy to client                         
                                                                       
Observability Flow                                                     
                                                                       
 1 Backend/Nanobot instrumented with OpenTelemetry SDK                 
 2 Traces & logs sent via OTLP to otel-collector                       
 3 Collector batches and exports to:                                   
    • VictoriaLogs for log storage                                     
    • VictoriaTraces for trace storage                                 
 4 UIs accessible at /utils/victorialogs and /utils/victoriatraces     
```

**Observation:** With MCP tools connected, the agent now queries real backend data and provides accurate information about the LMS system.

---

## Task 1C — Skill prompt

### Question: "Show me the scores"

**Response:**
```
                        📊 LMS Scores Overview                          
                                                                       
Completion Rates by Lab                                                
                                                                       
                                                                       
 Lab     Completion Rate  Passed  Total  Status                        
 ───────────────────────────────────────────────────                   
 Lab 01  100.0% ✅        258     258    Complete                       
 Lab 02  89.1%            131     147    In Progress                   
 Lab 03  89.7%            156     174    In Progress                   
 Lab 04  96.7%            238     246    In Progress                   
 Lab 05  98.4%            246     250    In Progress                   
 Lab 06  98.4%            241     245    In Progress                   
 Lab 07  99.6%            236     237    In Progress                   
 Lab 08  0.0%             0       0      Not Started                   
                                                                       
-----------------------------------------------------------------------
                                                                       
Average Scores by Lab & Task                                           
                                                                       
Lab 01 — Products, Architecture & Roles                                
                                                                       
 Task                                        Avg Score  Attempts       
 ───────────────────────────────────────────────────────────────       
 Lab setup                                   84.3%      2990           
 Task 0: Practice the Git workflow           64.5%      306            
 Task 1: Product & architecture description  55.1%      161            
 Task 2: Roles and skills mapping            49.8%      83             
 Optional: Create a release                  60.0%      5              
 Optional: Add a CI check                    42.9%      7              
 Optional: Resolve a merge conflict          34.6%      13             
 Optional: Plan skill development            20.0%      5              
                                                                       
Lab 02 — Run, Fix, and Deploy a Backend Service                        
                                                                       
 Task                                            Avg Score  Attempts   
 ───────────────────────────────────────────────────────────────────   
 Task 1: Run the web server                      67.9%      210        
 Task 2: Identify, report, and fix a bug         66.7%      216        
 Task 4: Deploy the web server to the VM         56.2%      84         
 Optional 3: Implement the post-order traversal  62.5%      6          
 Optional 1: Implement the /outcomes endpoint    36.4%      11         
 Optional 2: Make your VM a proxy                0.0%       3          
                                                                       
[... additional labs omitted for brevity ...]
                                                                       
-----------------------------------------------------------------------
                                                                       
Key Insights                                                           
                                                                       
🔴 Lowest Performing Tasks:                                             
                                                                       
 • Lab 01: "Plan skill development" (20.0%)                            
 • Lab 02: "Make your VM a proxy" (0.0%)                               
 • Lab 04: "CI/CD with GitHub Actions" (33.8%)                         
 • Lab 06: "The System Agent" (42.8%)                                  
                                                                       
🟢 Highest Performing Tasks:                                            
                                                                       
 • Lab 01: "Lab setup" (84.3%)                                         
 • Lab 07: "Plan and Scaffold" (76.9%)                                 
 • Lab 05: "Dashboard Front-end" (74.1%)                               
 • Lab 06: "The Documentation Agent" (73.6%)                           
                                                                       
📈 Most Attempted Tasks:                                                
                                                                       
 • Lab 01: "Lab setup" (2990 attempts)                                 
 • Lab 06: "The System Agent" (2053 attempts)                          
 • Lab 04: "Back-end Testing" (753 attempts)                           
 • Lab 07: "Plan and Scaffold" (755 attempts)
```

**Observation:** The skill prompt guides the agent to format results nicely with percentages, tables, and emoji indicators. The agent provides comprehensive data with key insights.

---

## Acceptance Criteria Checklist

- [x] Nanobot is installed in the repo-local `nanobot/` project from PyPI (`uv add nanobot-ai`)
- [x] Configured via `nanobot onboard` and repo-local `config.json`
- [x] Agent responds to general questions via `config.json`
- [x] MCP tools are configured and the agent returns real backend data
- [x] A skill prompt exists (`workspace/skills/lms/SKILL.md`) that guides the agent's tool usage
- [x] REPORT.md contains responses from all three checkpoints
