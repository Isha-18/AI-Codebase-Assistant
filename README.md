# 🤖 AI-Codebase-Assistant

An **Agentic AI Codebase Assistant** that understands, analyzes, and interacts with software repositories using **RAG, LangGraph, Multi-Agent Systems, MCP, LLM Tool Calling, Repository Analysis, Memory, and Human-in-the-Loop workflows**.

The project started as a simple RAG-based codebase question-answering system and has evolved incrementally into a **multi-agent architecture** where specialized agents collaborate under the control of a Supervisor.

> **Core principle:** Agents orchestrate. Services own the business logic.

---

# 🚀 Project Evolution

The project has evolved through several architectural stages:

```text
RAG
  ↓
Service Layer
  ↓
LangGraph
  ↓
Tool Calling
  ↓
MCP
  ↓
Conversation Memory
  ↓
Human-in-the-Loop
  ↓
Multi-Agent AI
  ↓
Agent-to-Agent Handoffs
```

The goal has not been to rebuild the application at every stage, but to **continuously improve the architecture while keeping the existing codebase and service layer intact**.

---

# 🧠 Current Architecture

The current system uses a Supervisor-driven multi-agent workflow.

Instead of:

```text
User
  ↓
LLM
  ↓
Tools
  ↓
Response
```

the system now follows:

```text
                         User
                           │
                           ▼
                        FastAPI
                           │
                           ▼
                     ChatService
                           │
                           ▼
                      Supervisor
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        Repository       RAG Agent   Code Review
           Agent                       Agent
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                       Supervisor
                           │
                           ▼
                     Final Response
```

The Supervisor decides **which specialized agent should act next** instead of making one LLM responsible for every task.

---

# 🏗️ Multi-Agent Architecture

## Supervisor Agent

The Supervisor is responsible for:

- Understanding the user's request
- Selecting the appropriate specialized agent
- Managing agent-to-agent handoffs
- Deciding when the task is complete
- Controlling the number of agent iterations
- Preventing unnecessary agent execution

The Supervisor is an **orchestration layer**, not a repository business-logic layer.

Example:

```text
User:
"Find the authentication classes and review their architecture"

              │
              ▼
        ┌─────────────┐
        │ Supervisor  │
        └──────┬──────┘
               │
               ▼
      ┌─────────────────┐
      │ Repository Agent│
      └────────┬────────┘
               │
        Finds authentication
        classes and code
               │
               ▼
        ┌─────────────┐
        │ Supervisor  │
        └──────┬──────┘
               │
               ▼
      ┌──────────────────┐
      │ Code Review Agent│
      └────────┬─────────┘
               │
               ▼
          Final Result
```

This allows the system to break complex tasks into specialized steps.

---

# 🔎 Specialized Agents

The current architecture contains three specialized agents.

## 1. Repository Agent

The Repository Agent handles structural and repository-level operations.

Typical responsibilities include:

- Finding classes
- Finding functions
- Finding imports
- Repository statistics
- Repository indexing
- Inspecting repository structure
- Collecting codebase information required by another agent

Typical tools:

```text
list_classes
list_functions
list_imports
repository_statistics
index_repository
```

Flow:

```text
Repository Agent
      │
      ▼
Repository Tools
      │
      ▼
RepositoryService
      │
      ▼
Repository Data
```

The Repository Agent does **not** implement repository analysis logic itself.

---

## 2. RAG Agent

The RAG Agent handles questions that require contextual understanding of the indexed codebase.

Examples:

```text
"Explain how authentication works."

"Where is database connection handled?"

"How does the request flow through this application?"

"Explain this class and its dependencies."
```

Flow:

```text
RAG Agent
    │
    ▼
RAG Tools
    │
    ▼
RAGService
    │
    ▼
Retriever
    │
    ▼
ChromaDB
    │
    ▼
Relevant Context
    │
    ▼
LLM
    │
    ▼
Answer
```

The RAG Agent focuses on **reasoning over repository context**, rather than directly implementing retrieval logic.

---

## 3. Code Review Agent

The Code Review Agent is responsible for architecture and code-quality analysis.

It can be used after another agent has gathered the required repository information.

Typical responsibilities include:

- Reviewing architecture
- Identifying design issues
- Evaluating separation of concerns
- Identifying potential coupling
- Reviewing implementation patterns
- Highlighting maintainability concerns
- Providing architectural recommendations

Example workflow:

```text
User
  │
  ▼
Supervisor
  │
  ▼
Repository Agent
  │
  ├── Find authentication classes
  ├── Find related functions
  └── Inspect dependencies
  │
  ▼
Supervisor
  │
  ▼
Code Review Agent
  │
  ├── Analyze architecture
  ├── Identify issues
  └── Provide recommendations
  │
  ▼
Supervisor
  │
  ▼
Final Response
```

This is an important distinction:

> The Repository Agent gathers facts.  
> The Code Review Agent reasons about those facts.

---

# 🔄 Agent-to-Agent Handoffs

The architecture now supports controlled handoffs between specialized agents.

A task does not necessarily end after one agent completes its work.

For example:

```text
Supervisor
    │
    ▼
Repository Agent
    │
    ▼
Repository Result
    │
    ▼
Supervisor
    │
    ▼
Code Review Agent
    │
    ▼
Review Result
    │
    ▼
Supervisor
    │
    ▼
Final Response
```

The Supervisor acts as the coordinator between agents.

This makes it possible to support workflows where:

```text
One agent gathers information
        ↓
Another agent analyzes it
        ↓
Another step validates the result
        ↓
Supervisor produces the final response
```

---

# 🧩 Shared Graph State

Agents communicate through shared LangGraph state rather than relying on isolated execution.

The state can carry information such as:

```text
User Request
    ↓
Current Agent
    ↓
Agent Decision
    ↓
Intermediate Results
    ↓
Tool Results
    ↓
Review Results
    ↓
Approval State
    ↓
Iteration Count
    ↓
Final Response
```

Conceptually:

```text
                  Shared Graph State
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
 Repository Agent     RAG Agent      Code Review Agent
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                     Supervisor
```

This allows the output of one agent to become useful context for another agent.

---

# 🔁 Controlled Agent Iterations

Multi-agent systems can easily become inefficient if agents continuously hand work back and forth.

The current architecture therefore introduces **controlled agent iterations**.

Conceptually:

```text
iteration = 0

       ↓

Supervisor
       ↓
Agent
       ↓
Supervisor
       ↓
Agent
       ↓
Complete
```

The graph tracks agent execution so that unnecessary loops can be avoided.

The objective is:

- Prevent infinite agent loops
- Reduce unnecessary LLM calls
- Keep execution predictable
- Make multi-agent workflows easier to debug
- Control local-model latency

---

# 🧑‍💻 Human-in-the-Loop

Human-in-the-loop workflows are implemented using **LangGraph interrupts and checkpointing**.

Operations that can change repository state require explicit approval.

Example:

```text
User
  │
  ▼
Supervisor
  │
  ▼
Repository Agent
  │
  ▼
index_repository
  │
  ▼
Approval Node
  │
  ▼
LangGraph Interrupt
  │
  ├───────────────┐
  │               │
 Approve        Reject
  │               │
  ▼               ▼
Execute          Stop
```

The graph pauses until a human decision is supplied.

Possible outcomes:

```text
approved
rejected
```

Read-only operations such as:

```text
list_classes
list_functions
list_imports
repository_statistics
```

do not require approval.

---

# 🧠 Conversation Memory

Conversation state is maintained using LangGraph checkpointing.

Each conversation can use a thread ID:

```json
{
  "thread_id": "multi-agent-1"
}
```

Conceptually:

```text
Conversation
     │
     ▼
LangGraph
     │
     ▼
Checkpoint
     │
     ▼
Thread State
```

This provides short-term conversation continuity across requests in the same thread.

### Current limitation

Long-term persistent memory is **not implemented yet**.

Future memory capabilities may include:

- Repository-specific memory
- User preferences
- Conversation summaries
- Persistent project context

---

# 📊 Observability

The system includes structured observability across the execution pipeline.

The goal is to make agentic execution understandable instead of treating the LLM as a black box.

The execution flow can be traced as:

```text
Request Started
      │
      ▼
Supervisor Started
      │
      ▼
Supervisor Decision
      │
      ▼
Agent Started
      │
      ▼
Tool Started
      │
      ▼
Tool Completed
      │
      ▼
Agent Completed
      │
      ▼
Supervisor Decision
      │
      ▼
Final Response
      │
      ▼
Request Completed
```

Logging covers:

- Supervisor decisions
- Agent execution
- Agent handoffs
- Tool execution
- Node execution
- LLM calls
- Errors
- Latency
- Request completion
- Intermediate execution state

Example:

```text
agent=supervisor event=started
```

```text
agent=supervisor event=decision decision=repository
```

```text
agent=repository event=completed
```

```text
agent=supervisor event=handoff target=code_review
```

```text
tool=list_classes event=completed
```

This provides visibility into **what the system actually did**.

---

# 🔬 LangSmith

LangSmith is part of the observability stack.

It can be used to inspect:

- Graph execution
- LLM calls
- Tool calls
- Agent execution
- Latency
- Errors
- Inputs and outputs
- Execution traces

Typical environment configuration:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=AI-Codebase-Assistant
```

---

# 🔌 MCP Architecture

Model Context Protocol is integrated separately from LangGraph while sharing the same Service Layer.

```text
                  Service Layer
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
         LangGraph             MCP
              │                 │
              ▼                 ▼
            Tools             Tools
```

MCP components include:

- MCP Server
- MCP Tools
- MCP Resources
- MCP Prompts

Start the MCP server with:

```bash
python run_mcp.py
```

The MCP server is separate from the FastAPI application.

---

# 🗂️ Repository Intelligence

The project uses repository analysis to understand source-code structure.

Python AST analysis can extract information such as:

- Classes
- Functions
- Imports
- Repository statistics

The RAG pipeline also stores repository metadata with indexed chunks.

Conceptually:

```text
Repository
    │
    ├───────────────┐
    ▼               ▼
AST Analyzer       RAG Pipeline
    │               │
    ▼               ▼
Code Structure   Chunking
                    │
                    ▼
                Embeddings
                    │
                    ▼
                 ChromaDB
```

---

# 🐙 GitHub Repository Indexing

GitHub repositories can be indexed through the repository indexing workflow.

```text
GitHub URL
    │
    ▼
Clone Repository
    │
    ▼
Temporary Local Directory
    │
    ▼
Repository Loader
    │
    ▼
Analyzer
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
ChromaDB
```

The existing indexing and repository services are reused rather than duplicating the implementation inside agents.

---

# 🏛️ Service Layer: Single Source of Truth

One of the most important architectural rules is that the **Service Layer owns business logic**.

```text
                 Service Layer
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      LangGraph                  MCP
          │                       │
          ▼                       ▼
        Agents                  Tools
```

Business logic should **not** be duplicated inside:

- LangGraph nodes
- Agents
- MCP tools
- API routes

Instead:

```text
Agent
  ↓
Tool
  ↓
Service
```

For example:

```text
list_classes
      ↓
RepositoryService
```

The Repository Agent chooses the appropriate tool, but the actual class extraction logic remains inside the existing service/analyzer layer.

---

# 🧱 Service Architecture

The current services include:

```text
ChatService
RepositoryService
RAGService
IndexingService
```

Their responsibilities remain separated:

### ChatService

Coordinates the application-level chat workflow.

### RepositoryService

Handles repository-related business operations.

### RAGService

Handles retrieval and contextual codebase questions.

### IndexingService

Handles repository indexing and ingestion.

This separation allows LangGraph, MCP, API routes, and tools to reuse the same underlying functionality.

---

# 📁 Project Structure

High-level structure:

```text
AI-Codebase-Assistant/
│
├── api/
│   └── routes.py
│
├── analyzers/
│   └── ...
│
├── config/
│   └── settings.py
│
├── graph/
│   ├── __init__.py
│   ├── builder.py
│   ├── state.py
│   ├── memory.py
│   ├── llm.py
│   ├── nodes.py
│   ├── tool_registry.py
│   │
│   └── agents/
│       ├── supervisor.py
│       ├── repository_agent.py
│       ├── rag_agent.py
│       └── code_review_agent.py
│
├── indexing/
│   └── ...
│
├── llm/
│   └── ...
│
├── mcp/
│   └── ...
│
├── models/
│   ├── requests.py
│   └── responses.py
│
├── prompts/
│   └── ...
│
├── retrieval/
│   └── ...
│
├── services/
│   ├── chat_service.py
│   ├── repository_service.py
│   ├── rag_service.py
│   └── indexing_service.py
│
├── storage/
│   └── ...
│
├── tools/
│   ├── rag_tools.py
│   ├── repository_tools.py
│   └── indexing_tools.py
│
├── app.py
├── run_mcp.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn

## AI / LLM

- Ollama
- Qwen
- LangChain
- LangGraph

Current local model:

```text
qwen2.5:0.5b
```

A smaller local model is intentionally used because larger models can cause significant performance issues on the development machine.

## RAG

- HuggingFace Embeddings
- BAAI BGE Small
- ChromaDB
- LangChain Retrieval

Current embedding model:

```text
BAAI/bge-small-en-v1.5
```

## Agent Framework

- LangGraph
- LangChain Tools
- ToolNode
- LangGraph Checkpointing
- LangGraph Interrupts
- Multi-Agent Orchestration

## Protocol

- Model Context Protocol (MCP)

## Observability

- LangSmith
- Python logging

---

# ⚙️ Environment Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd AI-Codebase-Assistant
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start Ollama

Verify that Ollama is running:

```bash
ollama list
```

The current application uses:

```text
qwen2.5:0.5b
```

If required:

```bash
ollama pull qwen2.5:0.5b
```

## 5. Configure `.env`

Example:

```env
LLM_MODEL=qwen2.5:0.5b

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

OLLAMA_BASE_URL=http://127.0.0.1:11434

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

Optional LangSmith configuration:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=AI-Codebase-Assistant
```

Do not commit `.env` to Git.

## 6. Start FastAPI

```powershell
uvicorn app:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

## 7. Start MCP

```powershell
python run_mcp.py
```

---

# 💬 Chat API

The main chat endpoint is:

```text
POST /chat
```

Example:

```json
{
  "question": "List all the classes in my repository",
  "thread_id": "multi-agent-1"
}
```

Another example:

```json
{
  "question": "Explain how authentication works in this project",
  "thread_id": "multi-agent-2"
}
```

The `thread_id` allows LangGraph checkpointing to maintain conversation state.

---

# 🔄 Example Multi-Agent Workflows

## Workflow 1 — Repository Query

Request:

```text
List all the classes in my repository.
```

Flow:

```text
FastAPI
   ↓
ChatService
   ↓
Supervisor
   ↓
Repository Agent
   ↓
Repository Tool
   ↓
RepositoryService
   ↓
Tool Result
   ↓
Repository Agent
   ↓
Supervisor
   ↓
Final Answer
```

---

## Workflow 2 — RAG Query

Request:

```text
Explain how authentication works in this project.
```

Flow:

```text
FastAPI
   ↓
ChatService
   ↓
Supervisor
   ↓
RAG Agent
   ↓
RAG Tool
   ↓
RAGService
   ↓
Retriever
   ↓
ChromaDB
   ↓
Context
   ↓
LLM
   ↓
RAG Agent
   ↓
Supervisor
   ↓
Final Answer
```

---

## Workflow 3 — Repository Analysis + Code Review

Request:

```text
Find the authentication classes and review their architecture.
```

Flow:

```text
                   Supervisor
                       │
                       ▼
              Repository Agent
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Find Classes        Find Functions
             │                   │
             └─────────┬─────────┘
                       ▼
                 Shared State
                       │
                       ▼
                   Supervisor
                       │
                       ▼
               Code Review Agent
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Architecture         Code Quality
          Review                Review
             │                   │
             └─────────┬─────────┘
                       ▼
                   Supervisor
                       │
                       ▼
                 Final Response
```

This workflow demonstrates the main benefit of the multi-agent architecture:

> **Different agents can specialize in different stages of the same task.**

---

# 🧑‍⚖️ Example HITL Workflow

A repository-changing operation such as:

```text
Index this repository
```

can trigger:

```text
Supervisor
    ↓
Repository Agent
    ↓
index_repository
    ↓
Approval Node
    ↓
LangGraph Interrupt
    ↓
Human Decision
    │
    ├── Approve → Tool Execution → Continue
    │
    └── Reject  → Stop Execution
```

Checkpointing allows the graph to pause and later resume from the interrupted state.

---

# 📚 Repository Indexing

Before asking repository questions, the repository needs to be indexed.

The indexing pipeline performs:

```text
Repository
    ↓
Loader
    ↓
Analyzer
    ↓
Chunker
    ↓
Embeddings
    ↓
ChromaDB
```

GitHub repositories can also be processed through the GitHub indexing workflow.

---

# 🔐 Architecture Rules

## Rule 1 — Service Layer Owns Business Logic

```text
Agent
  ↓
Tool
  ↓
Service
```

Do not move service logic into the agent.

## Rule 2 — Agents Own Responsibilities

Each agent should have a clear purpose.

```text
Supervisor       → Routing & orchestration
Repository Agent → Repository operations
RAG Agent        → Contextual code reasoning
Code Review      → Architecture & code review
```

## Rule 3 — Tools Are Controlled Interfaces

Agents should access application functionality through tools rather than directly manipulating infrastructure.

## Rule 4 — No Duplicate Business Logic

Do not implement the same operation in:

- API routes
- Agents
- LangGraph nodes
- MCP tools
- Services

The Service Layer remains the source of truth.

## Rule 5 — Keep Agent Loops Controlled

Agent handoffs must have clear completion conditions and iteration limits.

## Rule 6 — State Changes Need Oversight

Operations that modify repository state should be protected by Human-in-the-Loop workflows where appropriate.

---

# ⚠️ Current Limitations

## Local LLM Performance

The current Supervisor and specialized agents use:

```text
qwen2.5:0.5b
```

Because this is a small local model:

- Routing can occasionally be incorrect
- Complex multi-step reasoning can be limited
- Multiple agent calls increase latency
- Tool selection can require additional safeguards

A multi-agent request may involve:

```text
Supervisor LLM
      ↓
Specialized Agent LLM
      ↓
Tool
      ↓
Specialized Agent LLM
      ↓
Supervisor LLM
```

This is expected, but it makes performance optimization important.

---

# 🧪 Testing Checklist

## Basic API

- [ ] FastAPI starts successfully
- [ ] `/docs` loads
- [ ] `/chat` responds

## Supervisor

- [ ] Repository queries route to Repository Agent
- [ ] Contextual questions route to RAG Agent
- [ ] Review requests can reach Code Review Agent
- [ ] Invalid routing has a safe fallback
- [ ] Agent iterations terminate correctly

## Repository Agent

- [ ] List classes
- [ ] List functions
- [ ] List imports
- [ ] Repository statistics
- [ ] Repository indexing

## RAG Agent

- [ ] Codebase questions
- [ ] Authentication explanation
- [ ] Class/function explanation
- [ ] Architecture questions

## Code Review Agent

- [ ] Architecture review
- [ ] Separation-of-concerns review
- [ ] Code-quality analysis
- [ ] Review receives previous agent results

## Agent Handoffs

- [ ] Repository → Supervisor handoff works
- [ ] Supervisor → Code Review handoff works
- [ ] Shared state survives handoffs
- [ ] Agent loops terminate

## Memory

- [ ] Same thread maintains context
- [ ] Different threads remain independent

## HITL

- [ ] Read-only tools execute without approval
- [ ] State-changing tools trigger approval
- [ ] Approval resumes execution
- [ ] Rejection prevents execution

## Observability

- [ ] Supervisor logs
- [ ] Agent logs
- [ ] Handoff logs
- [ ] Tool logs
- [ ] Error logs
- [ ] Latency logs
- [ ] LangSmith traces

---

# 🗺️ Development Roadmap

## ✅ Completed — Phase 1: RAG Foundation

- Repository loading
- Chunking
- Embeddings
- ChromaDB
- Retrieval
- Basic codebase Q&A
- Ollama integration

## ✅ Completed — Phase 2: Service Layer & Repository Intelligence

- Service-oriented architecture
- `ChatService`
- `RepositoryService`
- `RAGService`
- `IndexingService`
- Python AST analysis
- Repository metadata
- Repository statistics
- Structured repository tools

## ✅ Completed — Phase 3: LangGraph & Tool Calling

- StateGraph
- Typed graph state
- Nodes
- Edges
- Conditional execution
- Tool calling
- ToolNode
- Graph execution
- Streaming

## ✅ Completed — Phase 4: MCP & Memory

- MCP Server
- MCP Tools
- MCP Resources
- MCP Prompts
- LangGraph checkpointing
- Thread-based conversation memory

## ✅ Completed — Phase 5: Observability & HITL

- Structured logging
- Node-level visibility
- Agent decision logging
- Tool execution logging
- LLM execution logging
- Latency measurement
- Error logging
- LangSmith integration
- LangGraph interrupts
- Approval workflows
- Checkpoint-based pause/resume

## 🚀 Current — Phase 6: Multi-Agent AI

Current architecture:

```text
                 Supervisor
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
 Repository         RAG        Code Review
   Agent           Agent          Agent
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
                 Shared State
```

Current focus:

- Reliable Supervisor routing
- Agent-to-agent handoffs
- Shared state
- Controlled agent iterations
- Agent-level observability
- HITL compatibility
- Better intermediate-result handling
- Reliable multi-step workflows

## 🔭 Future — Phase 7: Long-Term Memory

Potential capabilities:

```text
Conversation
     ↓
Short-Term Memory
     ↓
LangGraph Checkpoint
     ↓
Long-Term Persistent Memory
```

Possible features:

- Repository-specific memory
- Conversation summaries
- Persistent project context
- User preferences

## 🔭 Future — Phase 8: Repository Intelligence

Potential improvements:

- Better dependency analysis
- Cross-file relationship analysis
- Improved code graph representation
- Deeper architectural understanding
- Smarter retrieval
- Repository-wide reasoning

## 🔭 Future — Phase 9: Safer Automated Coding

Potential capabilities:

- Code modification proposals
- Patch generation
- Test generation
- Automated validation
- Git diff generation
- Human approval before applying changes
- Safer repository modification workflows

---

# 🎯 What This Project Is Teaching Me

The biggest lesson from the multi-agent phase is:

> **Multi-Agent AI is not simply about adding more LLMs.**

The difficult part is designing:

- Clear agent responsibilities
- Reliable routing
- Shared state
- Agent handoffs
- Controlled iterations
- Tool boundaries
- Human approval
- Observability
- Failure handling

A good multi-agent system is therefore closer to **distributed software architecture** than simply calling multiple LLMs.

---

# 🧠 Design Principles

### Separation of Concerns

Each layer has one primary responsibility.

### Service Reuse

Existing business logic should be reused instead of duplicated.

### Agent Specialization

Each agent should solve a clearly defined class of problems.

### Controlled Tool Access

Agents receive only the tools relevant to their responsibility.

### Agent Coordination

The Supervisor coordinates specialized agents instead of performing every task itself.

### Human Oversight

Potentially state-changing operations can require explicit approval.

### Observable AI

Agent decisions, tool calls, handoffs, and failures should be traceable.

### Controlled Autonomy

Agents should have bounded execution rather than unrestricted loops.

### Incremental Architecture

New capabilities should be introduced only when the current architecture is stable.

---

# 📌 Current System Summary

The AI-Codebase-Assistant has evolved from:

```text
Simple RAG
```

into:

```text
                    User
                     │
                     ▼
                  FastAPI
                     │
                     ▼
                ChatService
                     │
                     ▼
                Supervisor
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
    Repository      RAG      Code Review
       Agent       Agent        Agent
          │          │          │
          ▼          ▼          ▼
       Tools       Tools       Tools
          │          │          │
          └──────────┼──────────┘
                     ▼
               Service Layer
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
 RepositoryService RAGService IndexingService
        │            │            │
        ▼            ▼            ▼
 Repository Data  ChromaDB   Repository Index
```

With supporting infrastructure:

```text
                 ┌───────────────────────┐
                 │      LangGraph        │
                 │                       │
                 │ State + Memory + HITL │
                 │ Handoffs + Routing    │
                 └───────────┬───────────┘
                             │
                             ▼
                    Multi-Agent System

                 ┌───────────────────────┐
                 │         MCP           │
                 │ Tools + Resources     │
                 │ + Prompts             │
                 └───────────────────────┘

                 ┌───────────────────────┐
                 │      LangSmith        │
                 │ Tracing + Observability│
                 └───────────────────────┘
```

---

# 🚀 Final Architecture Journey

```text
RAG
 ↓
Repository Intelligence
 ↓
Service Layer
 ↓
LangGraph
 ↓
Tool Calling
 ↓
MCP
 ↓
Conversation Memory
 ↓
Human-in-the-Loop
 ↓
Supervisor Agent
 ↓
Specialized Agents
 ↓
Agent-to-Agent Handoffs
 ↓
Shared State
 ↓
Controlled Multi-Agent Execution
```

The project is now focused on building a **reliable, observable, and controlled AI system for understanding software repositories** rather than simply generating answers from retrieved documents.

---

# 🔭 Next Focus

The immediate priorities are:

1. **Improve Supervisor routing reliability**
2. **Improve multi-agent evaluation**
3. **Strengthen agent handoff logic**
4. **Improve repository intelligence**
5. **Add long-term memory**
6. **Optimize streaming and performance**
7. **Build safer automated coding workflows**

The architecture will continue to evolve incrementally while keeping the **Service Layer as the single source of truth**.

---

## ⭐ If you find this project interesting

The project is being built incrementally to explore how modern AI engineering concepts can be combined into a practical developer tool:

**RAG → Agents → Multi-Agent Systems → MCP → Memory → HITL → Repository Intelligence**

More improvements coming. 🚀
