# Agentflow - Quick Summary

## What is Agentflow?

Agentflow is a **simple yet powerful agentic framework built for humans** - a Python library for creating AI agents that can interact with language models and execute actions.

## Key Information

- **Version**: 0.1.0
- **License**: MIT
- **Python Support**: 2.7+, 3.4+
- **Author**: Achilles Gasper Rasquinha
- **Repository**: https://github.com/okooai/Agentflow

## Core Concepts

### 1. **Agents**
AI entities with objectives that can use tools to accomplish tasks. They:
- Have a defined objective (system prompt)
- Can execute actions (tools/functions)
- Maintain conversation history
- Support streaming responses

### 2. **Actions**
Reusable, executable functions that agents can invoke:
- Defined in `action.yml` files
- Implemented in `action.py` handlers
- Accept parameters and return results
- Distributed via the Hub

### 3. **Hub**
Central registry for sharing and fetching agents/actions:
- GitHub-based distribution
- Namespace support (e.g., `okooai/agent-name:latest`)
- Local caching
- Version management with tags

### 4. **Providers**
LLM integrations (currently OpenAI, extensible to others):
- API key authentication
- Streaming support
- Tool/function calling
- Configurable timeouts

## Quick Start

### Installation
```bash
pip install agentflow
```

### Basic Usage
```python
from agentflow import hub

# Fetch and use an agent
agent = hub("okooai/my-agent")
result = agent.run("Hello!")

# Or create one programmatically
from agentflow.model.agent import Agent

agent = Agent(
    name="assistant",
    objective="You are a helpful assistant",
    actions=["search"],
    provider="openai"
)

response = agent.run("What's the weather?")
```

### CLI
```bash
agentflow --version
agentflow help
```

## Architecture

```
User Input → Agent → Provider (LLM) → Tool Decision → 
Action Execution → Result → Session → Response
```

## Key Features

✅ **Async-first design** - Built with async/await  
✅ **Tool calling** - Function/tool calling support  
✅ **Streaming** - Real-time response streaming  
✅ **Hub distribution** - Share agents & actions  
✅ **Interactive mode** - Built-in console  
✅ **Extensible** - Plugin-based providers  
✅ **Session management** - Conversation history  

## Environment Variables

- `AF_OPENAI_API_KEY` - OpenAI API key
- `AF_PROVIDER` - Default provider (default: "openai")
- `AF_PROVIDER_TIMEOUT` - Request timeout (default: 30)

## Project Structure

```
src/agentflow/
├── model/
│   ├── agent.py      # Agent implementation
│   ├── action.py     # Action implementation
│   ├── hub.py        # Hub registry
│   ├── provider.py   # LLM provider
│   ├── session.py    # Session management
│   └── message.py    # Message types
├── cli/              # CLI interface
├── commands/         # CLI commands
└── config.py         # Configuration
```

## Use Cases

- **Customer Support**: Answer questions, create tickets
- **Data Analysis**: Query databases, generate reports
- **Research**: Web search, summarize content
- **DevOps**: Deploy services, check logs, scale resources

## Documentation

For comprehensive details, see: [docs/AGENTFLOW_DETAILS.md](docs/AGENTFLOW_DETAILS.md)

---

*Framework: "Agents, for Humans"*
