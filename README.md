# AI-Codebase-Assistant

An Agentic AI application that understands and interacts with software repositories using **RAG, LangGraph, MCP, LLM tool calling, and repository analysis**.

The project started as a RAG-based Codebase Assistant and has evolved into a **LangGraph-based multi-agent architecture** with conversation memory, human-in-the-loop approval, repository tools, GitHub repository indexing, and agent-level observability.

---

# Version 4

## What's New in Version 4

Version 4 evolves the application from a single-agent LangGraph system into the foundation of a **multi-agent AI architecture**.

The major changes are:

* LangGraph-based agent orchestration
* Supervisor agent
* Specialized Repository Agent
* Specialized RAG Agent
* Agent-level logging and observability
* Human-in-the-loop approval using LangGraph interrupts
* Thread-based conversation memory
* LangGraph checkpointing
* Tool-based repository interaction
* Separation of Repository and RAG tools
* Existing Service Layer retained as the single source of truth
* GitHub repository indexing support
* LangSmith-compatible graph/LLM tracing
* Streaming graph execution

---

# Architecture

The current architecture is:

```text
                        REST Client
                            |
                            v
                        FastAPI
                            |
                            v
                       ChatService
                            |
                            v
                    Supervisor Agent
                         LLM
                            |
              +-------------+-------------+
              |                           |
              v                           v
       Repository Agent              RAG Agent
              |                           |
         Repository LLM                RAG LLM
              |                           |
       Repository Tools               RAG Tools
              |                           |
              v                           v
       RepositoryService              RAGService
              |                           |
              v                           v
       Repository Data             ChromaDB / RAG
              |
              v
       IndexingService
```

The important architectural principle is:

```text
                 Service Layer
                      |
          +-----------+-----------+
          |                       |
          v                       v
      LangGraph                  MCP
```

Business logic remains inside the existing services.

Agents and tools are orchestration/integration layers and should not duplicate service logic.

---

# Version History

## Version 1 — Initial RAG Assistant

The project originally provided a basic repository question-answering pipeline.

```text
Repository
    |
    v
Loader
    |
    v
Chunking
    |
    v
Embeddings
    |
    v
ChromaDB
    |
    v
Retriever
    |
    v
LLM
    |
    v
Answer
```

Technologies included:

* Python
* FastAPI
* LangChain
* HuggingFace Embeddings
* ChromaDB
* Ollama

---

# Version 2 — Service Layer + Repository Intelligence

The project was refactored into a service-oriented architecture.

Existing services include:

* `ChatService`
* `RepositoryService`
* `RAGService`
* `IndexingService`

Repository analysis was also introduced using Python AST analysis.

The system can extract information such as:

* Classes
* Functions
* Imports
* Repository statistics

The RAG pipeline also stores repository metadata with the indexed chunks.

---

# Version 3 — LangGraph + MCP + Memory

LangGraph was introduced for agent orchestration.

The application gained:

* `StateGraph`
* Typed graph state
* Nodes
* Edges
* Conditional execution
* Tool calling
* `ToolNode`
* Checkpointing
* Thread-based conversation memory
* Streaming graph execution

MCP integration was also introduced with:

* MCP Tools
* MCP Resources
* MCP Prompts

MCP and LangGraph both use the existing Service Layer.

---

# Version 4 — Agentic Multi-Agent Architecture

Version 4 introduces the foundation of the multi-agent architecture.

Instead of one LLM performing every task:

```text
User
 |
 v
Single LLM
 |
 +-- Tools
```

the system now uses:

```text
User
 |
 v
Supervisor LLM
 |
 +-------------------+
 |                   |
 v                   v
Repository Agent   RAG Agent
```

The Supervisor decides which specialized agent should handle the request.

---

# Supervisor Agent

The Supervisor is responsible for routing requests.

For example:

```text
"List all classes in my repository"
              |
              v
         Supervisor
              |
              v
        Repository Agent
```

While:

```text
"Explain how authentication works"
              |
              v
         Supervisor
              |
              v
           RAG Agent
```

The Supervisor does not directly perform repository operations.

Its responsibility is orchestration.

---

# Repository Agent

The Repository Agent handles repository-level operations.

Current repository tools include:

```text
list_classes
list_functions
list_imports
repository_statistics
index_repository
```

The flow is:

```text
Repository Agent
       |
       v
Repository LLM
       |
       v
Repository Tool
       |
       v
RepositoryService
```

The Repository Agent does not duplicate repository business logic.

---

# RAG Agent

The RAG Agent handles questions that require understanding or reasoning over the repository code.

Example:

```text
"Explain how authentication works"
```

Flow:

```text
RAG Agent
    |
    v
RAG LLM
    |
    v
codebase_chat
    |
    v
RAGService
    |
    v
Retriever
    |
    v
ChromaDB
    |
    v
LLM
    |
    v
Answer
```

---

# Human-in-the-Loop

Human-in-the-loop support was implemented using LangGraph interrupts.

Only repository-changing operations currently require approval.

Current approval-required operation:

```text
index_repository
```

Example:

```text
User
 |
 v
Supervisor
 |
 v
Repository Agent
 |
 v
index_repository
 |
 v
Approval Node
 |
 v
Human Approval
 |
 +---- No ----> Reject
 |
 Yes
 |
 v
Tool Execution
 |
 v
Response
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

# Conversation Memory

Conversation memory uses LangGraph checkpointing.

Each conversation uses a thread ID.

Example:

```text
thread_id = multi-agent-1
```

The graph can therefore maintain state across multiple requests belonging to the same thread.

Current architecture:

```text
Conversation
     |
     v
LangGraph
     |
     v
Checkpoint
     |
     v
Thread State
```

Long-term persistent memory is not implemented yet.

---

# Observability

Version 4 adds structured logging around agent execution.

Example:

```text
request_started
      |
      v
supervisor started
      |
      v
supervisor decision
      |
      v
agent execution
      |
      v
tool execution
      |
      v
final response
      |
      v
request_completed
```

Example logs:

```text
agent=supervisor event=started
```

```text
agent=supervisor event=decision decision=repository
```

```text
graph_node=approval event=not_required
```

```text
tool=list_classes event=started
```

```text
tool=list_classes event=completed
```

```text
chat event=request_completed
```

This makes it possible to understand what the agent actually did instead of treating the LLM as a black box.

---

# LangSmith

LangSmith is part of the project's observability stack.

It can be used to inspect:

* Graph execution
* LLM calls
* Tool calls
* Agent execution
* Latency
* Errors
* Inputs and outputs
* Execution traces

The application also assigns meaningful run names where appropriate.

LangSmith configuration depends on the environment variables described below.

---

# MCP Architecture

MCP is integrated separately from LangGraph but shares the same Service Layer.

```text
                 Service Layer
                      |
              +-------+-------+
              |               |
              v               v
         LangGraph           MCP
              |               |
              v               v
            Tools           Tools
```

MCP components currently include:

* MCP Server
* MCP Tools
* MCP Resources
* MCP Prompts

The MCP server can be started using:

```bash
python run_mcp.py
```

---

# GitHub Repository Indexing

The indexing pipeline supports GitHub repositories.

The flow is:

```text
GitHub URL
    |
    v
Clone Repository
    |
    v
Temporary Local Directory
    |
    v
Repository Loader
    |
    v
Chunking
    |
    v
Embeddings
    |
    v
ChromaDB
```

The existing indexing and repository services are reused.

---

# Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn

## AI / LLM

* Ollama
* Qwen
* LangChain
* LangGraph

Current local model:

```text
qwen2.5:0.5b
```

The project intentionally uses a smaller local model because larger local models cause significant performance problems on the development machine.

## RAG

* HuggingFace Embeddings
* BAAI BGE Small
* ChromaDB
* LangChain Retrieval

Current embedding model:

```text
BAAI/bge-small-en-v1.5
```

## Agent Framework

* LangGraph
* LangChain Tools
* ToolNode
* LangGraph Checkpointing
* LangGraph Interrupts

## Protocol

* Model Context Protocol (MCP)

## Observability

* LangSmith
* Python logging

---

# Project Structure

Current high-level structure:

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
│       └── rag_agent.py
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

# Environment Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd AI-Codebase-Assistant
```

---

# 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Install and Start Ollama

Install Ollama on your machine.

Then make sure the Ollama service is running.

Verify:

```bash
ollama list
```

The current application uses:

```text
qwen2.5:0.5b
```

If it is not available:

```bash
ollama pull qwen2.5:0.5b
```

Do not switch to a significantly larger model unless your hardware can handle it.

---

# 5. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
LLM_MODEL=qwen2.5:0.5b

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

OLLAMA_BASE_URL=http://127.0.0.1:11434

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

For LangSmith, configure the required environment variables if tracing is enabled:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=AI-Codebase-Assistant
```

Do not commit `.env` to Git.

---

# 6. Start the FastAPI Application

From the project root:

```powershell
uvicorn app:app --reload
```

The application should start on the local Uvicorn server.

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Open OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 7. Start MCP Server

If MCP functionality is required:

```powershell
python run_mcp.py
```

The MCP server is separate from the FastAPI application.

---

# Using the Chat API

The main chat endpoint is:

```text
POST /chat
```

Example request:

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

# Example Agent Execution

## Repository Query

Request:

```text
List all the classes in my repository
```

Expected flow:

```text
FastAPI
   ↓
ChatService
   ↓
Supervisor
   ↓
repository
   ↓
Repository Agent
   ↓
Repository LLM
   ↓
list_classes
   ↓
RepositoryService
   ↓
Tool Result
   ↓
Repository LLM
   ↓
Final Answer
```

Example logs:

```text
agent=supervisor event=started
```

```text
agent=supervisor event=decision decision=repository
```

```text
graph_node=approval event=not_required
```

```text
tool=list_classes event=started
```

```text
tool=list_classes event=completed
```

---

# RAG Query

Request:

```text
Explain how authentication works in this project
```

Expected architecture:

```text
FastAPI
   ↓
ChatService
   ↓
Supervisor
   ↓
RAG Agent
   ↓
RAG LLM
   ↓
codebase_chat
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
Answer
```

---

# Human-in-the-Loop Example

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
ApprovalNode
    ↓
LangGraph interrupt
```

The graph pauses until a human decision is supplied.

Possible outcomes:

```text
approved
```

or:

```text
rejected
```

This functionality relies on LangGraph checkpointing.

---

# Repository Indexing

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

GitHub repositories can also be indexed through the GitHub repository workflow.

---

# Important Architecture Rules

## 1. Service Layer is the Source of Truth

Do not put business logic inside:

* LangGraph nodes
* Agents
* MCP tools
* API routes

Instead:

```text
Agent
  ↓
Tool
  ↓
Service
```

---

## 2. Do Not Duplicate Logic

For example:

```text
list_classes
    ↓
RepositoryService
```

The Repository Agent should not implement class extraction itself.

---

## 3. Agents Are Responsible for Orchestration

The Repository Agent decides which repository tool is appropriate.

The RAG Agent decides how to use the RAG tools.

The Supervisor decides which agent should handle the request.

---

# Current Multi-Agent Architecture

The current system intentionally starts with only two specialized agents:

```text
                    Supervisor
                        |
              +---------+---------+
              |                   |
              v                   v
      Repository Agent        RAG Agent
```

Future agents may include:

```text
Code Review Agent
Documentation Agent
Testing Agent
GitHub Agent
```

These should **not** be added until the current architecture is stable.

---

# Current Known Limitation

The Supervisor currently uses the local:

```text
qwen2.5:0.5b
```

model.

Because this is a very small model, routing can occasionally be incorrect.

For example, a conceptual question such as:

```text
Why is this class implemented this way?
```

may sometimes be incorrectly routed to the Repository Agent.

The current Supervisor includes a fallback to the RAG agent when it cannot recognize a valid routing decision.

Improving structured Supervisor routing is the next hardening task.

---

# Performance Considerations

The local LLM is the main performance bottleneck.

A typical request may require multiple LLM calls:

```text
Supervisor LLM
       ↓
Specialized Agent LLM
       ↓
Tool
       ↓
Specialized Agent LLM
```

This is expected in the multi-agent architecture.

Repository tools themselves are comparatively fast.

For example:

```text
list_classes
latency ≈ hundreds of milliseconds
```

while local LLM inference can take several seconds.

The project therefore intentionally avoids unnecessarily large local models.

---

# Development Workflow

When modifying the project:

1. Inspect the existing implementation.
2. Reuse existing services.
3. Modify only the required layer.
4. Test the affected graph path.
5. Check logs.
6. Verify tool execution.
7. Verify the final response.
8. Check LangSmith traces when enabled.

Avoid rewriting working components without a specific reason.

---

# Debugging

If the application fails during startup, inspect the first Python traceback.

Common problems include:

### Import errors

Example:

```text
ImportError: cannot import name ...
```

Check whether an old import is still referencing a class/function removed during the architecture refactor.

### Ollama errors

Verify:

```bash
ollama list
```

and make sure Ollama is running.

### ChromaDB / RAG errors

Verify that the repository has been indexed and that the configured embedding model matches the vectors stored in the database.

### Supervisor routing errors

Check logs for:

```text
agent=supervisor event=decision
```

The expected decision should be:

```text
repository
```

or:

```text
rag
```

---

# Testing Checklist

## Basic API

* [ ] FastAPI starts successfully
* [ ] `/docs` loads
* [ ] `/chat` responds

## Repository Agent

* [ ] List classes
* [ ] List functions
* [ ] List imports
* [ ] Repository statistics

## RAG Agent

* [ ] Codebase questions
* [ ] Authentication explanation
* [ ] Class/function explanation
* [ ] Repository architecture questions

## Supervisor

* [ ] Repository queries route to Repository Agent
* [ ] Conceptual/code-understanding queries route to RAG Agent
* [ ] Invalid Supervisor output has a safe fallback

## Memory

* [ ] Same thread maintains conversation context
* [ ] Different threads remain independent

## HITL

* [ ] Read-only tools execute without approval
* [ ] Repository-changing tools trigger approval
* [ ] Approval resumes execution
* [ ] Rejection prevents execution

## Observability

* [ ] Supervisor logs
* [ ] Agent logs
* [ ] Tool logs
* [ ] Error logs
* [ ] Latency logs
* [ ] LangSmith traces

---

# Roadmap

## Completed

### Phase 1 — Observability & Reliable Agent Execution

Implemented:

* Structured logging
* Node-level visibility
* Tool execution logging
* LLM execution logging
* Latency measurement
* Error logging
* Agent decision logging
* LangSmith integration

---

## Completed

### Phase 2 — Human-in-the-Loop

Implemented:

* LangGraph interrupts
* Approval node
* Checkpoint-based pause/resume
* Approval state
* Approval request information
* Rejection handling
* Protection for repository-changing tools

---

## Current

### Phase 3 — Multi-Agent Architecture

Implemented:

```text
Supervisor
    |
    +-- Repository Agent
    |
    +-- RAG Agent
```

Current focus:

* Supervisor routing reliability
* Agent-level observability
* Shared graph state
* Reliable tool execution
* HITL compatibility with subgraphs

---

## Future Phase 4 — Long-Term Memory

Planned:

```text
Conversation
     ↓
Short-Term Memory
     ↓
LangGraph Checkpoint
     ↓
Long-Term Persistent Memory
```

Possible future capabilities:

* User preferences
* Repository-specific memory
* Conversation summaries
* Persistent project context

This is intentionally not implemented yet.

---

# Design Principles

The project follows these principles:

### Separation of Concerns

Each layer has one primary responsibility.

### Reuse Existing Services

Business logic stays inside the Service Layer.

### Agent Specialization

Each agent should have a clear purpose.

### Controlled Tool Access

Agents receive only the tools relevant to their responsibility.

### Human Oversight

Potentially state-changing operations can require explicit approval.

### Observable AI

Agent decisions should be traceable and debuggable.

### Incremental Architecture

New agents and capabilities should be introduced only when the current system is stable.

---

# Summary

AI-Codebase-Assistant has evolved from a simple RAG application into an agentic AI system.

The current architecture is:

```text
                       User
                        |
                        v
                    FastAPI
                        |
                        v
                   ChatService
                        |
                        v
                  Supervisor LLM
                        |
             +----------+----------+
             |                     |
             v                     v
      Repository Agent          RAG Agent
             |                     |
             v                     v
      Repository Tools          RAG Tools
             |                     |
             v                     v
     RepositoryService         RAGService
             |                     |
             v                     v
      Repository Data          ChromaDB
```

The system now combines:

* RAG
* Agentic AI
* LangGraph
* Multi-agent orchestration
* Tool calling
* Human-in-the-loop
* Conversation memory
* MCP
* GitHub repository indexing
* Vector search
* Repository AST analysis
* LangSmith observability
* FastAPI

The next focus is to make the **Supervisor routing reliable and production-ready** before expanding the number of specialized agents.
