# Agentflow Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Agentflow System                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐
│    User     │  Interacts via CLI or Python API
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Agent Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                         Agent                             │  │
│  │  - Name, Objective (System Prompt)                        │  │
│  │  - Actions (Tool List)                                    │  │
│  │  - Provider (LLM Connection)                              │  │
│  │  - Session (Conversation State)                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│              │                                  │                │
│              ▼                                  ▼                │
│    ┌──────────────────┐            ┌──────────────────┐        │
│    │  Interactive     │            │  Non-Interactive │        │
│    │  Console Mode    │            │  API Mode        │        │
│    └──────────────────┘            └──────────────────┘        │
└──────────────┬──────────────────────────────┬──────────────────┘
               │                               │
               ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Provider Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                       Provider                            │  │
│  │  - OpenAI / Custom LLM Integration                        │  │
│  │  - API Authentication (API Key)                           │  │
│  │  - Request/Response Handling                              │  │
│  │  - Streaming Support                                      │  │
│  │  - Tool/Function Calling                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────┬──────────────────────────────┬──────────────────┘
               │                               │
        Prompt │                               │ Response
               ▼                               │
┌─────────────────────────────────────────────┼──────────────────┐
│                      LLM Service             │                  │
│              (OpenAI GPT-4, etc.)            │                  │
└──────────────────────────────────────────────┼──────────────────┘
                                               │
                      Tool Call Decision       │
                               │               │
                               ▼               │
┌─────────────────────────────────────────────┼──────────────────┐
│                       Action Layer           │                  │
├──────────────────────────────────────────────┼─────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌─┴───────────────┐  │
│  │   Action 1     │  │   Action 2     │  │   Action N      │  │
│  │  - search      │  │  - calculator  │  │  - custom_tool  │  │
│  │  - params      │  │  - params      │  │  - params       │  │
│  │  - handler     │  │  - handler     │  │  - handler      │  │
│  └────────┬───────┘  └────────┬───────┘  └────────┬────────┘  │
│           │                   │                    │            │
│           └───────────────────┼────────────────────┘            │
│                               │ Execute                         │
│                               ▼                                 │
│                    ┌──────────────────┐                         │
│                    │  Action Handler  │                         │
│                    │  (Python Code)   │                         │
│                    └──────────┬───────┘                         │
│                               │ Result                          │
└───────────────────────────────┼─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Session Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                       Session                             │  │
│  │  - Message History (User + Agent + Actions)               │  │
│  │  - Context Management                                     │  │
│  │  - Database Storage                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│           │                                                      │
│           ├─► UserMessage                                       │
│           ├─► AgentMessage (with content)                       │
│           └─► AgentMessage (with action results)                │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Execution Flow

```
1. User Input
   │
   ▼
2. Agent receives input and creates UserMessage
   │
   ▼
3. Session stores message and builds prompt from history
   │
   ▼
4. Prompt sent to Provider (LLM)
   │
   ├─► If tool calling needed:
   │   ├─► Extract tool name and parameters
   │   ├─► Execute corresponding Action
   │   ├─► Store action result in session as AgentMessage
   │   └─► Loop back to step 4 with updated context
   │
   └─► If response ready:
       ├─► Stream or return content
       ├─► Store as AgentMessage in session
       └─► Return to user
```

## Hub Distribution System

```
┌─────────────────────────────────────────────────────────────────┐
│                           Hub System                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   GitHub Repository: okooai/Agentflow                           │
│        │                                                         │
│        ├─► agents/                                              │
│        │   ├─► namespace/agent-name/                            │
│        │   │   ├─► Agentfile (YAML config)                      │
│        │   │   └─► README.md                                    │
│        │   └─► ...                                              │
│        │                                                         │
│        └─► actions/                                             │
│            ├─► namespace/action-name/                           │
│            │   ├─► action.yml (config)                          │
│            │   ├─► action.py (handler)                          │
│            │   └─► requirements.txt                             │
│            └─► ...                                              │
│                                                                  │
│   ┌──────────────────────────────────────────────────────┐     │
│   │              Local Cache                              │     │
│   │  ~/.config/agentflow/hub/                            │     │
│   │    ├─► agents/                                       │     │
│   │    │   └─► namespace/agent-name/tag/                │     │
│   │    └─► actions/                                      │     │
│   │        └─► namespace/action-name/tag/               │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                  │
│   Usage:                                                        │
│   agent = hub("okooai/my-agent:latest")                        │
│   agent = hub("namespace/custom-agent:v1.0")                   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interaction Matrix

```
┌──────────┬────────┬────────┬──────────┬─────────┬─────────┐
│          │ Agent  │ Action │ Provider │ Session │   Hub   │
├──────────┼────────┼────────┼──────────┼─────────┼─────────┤
│ Agent    │   -    │  Uses  │   Uses   │  Uses   │ Loaded  │
│ Action   │ Used by│   -    │    -     │    -    │ Loaded  │
│ Provider │ Used by│   -    │    -     │    -    │ Config  │
│ Session  │ Used by│   -    │    -     │    -    │    -    │
│ Hub      │ Loads  │ Loads  │    -     │    -    │    -    │
└──────────┴────────┴────────┴──────────┴─────────┴─────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       Data Flow                                  │
└─────────────────────────────────────────────────────────────────┘

Input
  │
  ▼
┌─────────────────┐
│ User Message    │───┐
└─────────────────┘   │
                      │
                      ▼
              ┌─────────────┐
              │  Session    │
              │  (append)   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Build Prompt│
              │ from History│
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  Provider   │──► LLM API
              │  (request)  │◄── Response
              └──────┬──────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    Tool Call?              Content?
         │                       │
         ▼                       ▼
  ┌─────────────┐        ┌─────────────┐
  │ Execute     │        │ Agent       │
  │ Action      │        │ Message     │
  └──────┬──────┘        └──────┬──────┘
         │                      │
         ▼                      │
  ┌─────────────┐               │
  │ Action      │               │
  │ Result      │               │
  └──────┬──────┘               │
         │                      │
         ▼                      │
  ┌─────────────┐               │
  │ Agent       │               │
  │ Message     │               │
  │ (actions)   │               │
  └──────┬──────┘               │
         │                      │
         └──────────┬───────────┘
                    │
                    ▼
              ┌─────────────┐
              │  Session    │
              │  (store)    │
              └──────┬──────┘
                     │
          Loop back  │  Or done
                     │
                     ▼
                  Output
```

## File Structure Relationships

```
agentflow/
│
├── src/agentflow/
│   ├── __init__.py ──────────┐
│   │                          │ Exports
│   ├── model/                 │
│   │   ├── agent.py ◄─────────┤
│   │   ├── action.py ◄────────┤
│   │   ├── hub.py ◄───────────┤
│   │   ├── provider.py ◄──────┤
│   │   ├── session.py ◄───────┤
│   │   └── message.py ◄───────┘
│   │
│   ├── config.py ◄──── Used by all models
│   │   - CONST (constants)
│   │   - DEFAULT (defaults)
│   │   - PATH (paths)
│   │
│   ├── cli/ ──────────► Commands
│   └── commands/ ─────► CLI entry points
│
├── data/
│   └── providers.json ─► Provider configs
│
└── ~/.config/agentflow/ (Runtime)
    ├── hub/
    │   ├── agents/
    │   └── actions/
    ├── store/
    │   └── [database files]
    └── providers.json (cached)
```

## Key Design Patterns

### 1. Hub Pattern
- Centralized registry for reusable components
- Lazy loading and caching
- Namespace-based organization

### 2. Provider Pattern
- Abstract LLM integration
- Pluggable backends
- Unified interface

### 3. Action Pattern
- Reusable tools/functions
- Declarative configuration
- Isolated execution

### 4. Session Pattern
- Stateful conversations
- Message history
- Context preservation

### 5. Async Pattern
- Non-blocking I/O
- Concurrent operations
- Sync/async dual support

---

*This diagram represents the architecture as of version 0.1.0*
