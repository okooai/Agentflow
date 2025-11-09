# Agentflow - Detailed Project Overview

## Executive Summary

**Agentflow** is a simple yet powerful agentic framework built for humans. It provides a Python-based infrastructure for creating, managing, and orchestrating AI agents that can interact with language models and execute actions in response to user inputs.

**Version:** 0.1.0  
**Author:** Achilles Gasper Rasquinha  
**License:** MIT License  
**Repository:** https://github.com/okooai/Agentflow  
**Python Support:** Python 2.7+ and Python 3.4+

## What is Agentflow?

Agentflow is an agentic framework that enables developers to:

1. **Create AI Agents**: Define intelligent agents with specific objectives and capabilities
2. **Manage Actions**: Build reusable actions that agents can execute
3. **Integrate LLM Providers**: Connect to various language model providers (e.g., OpenAI)
4. **Orchestrate Workflows**: Chain together agents and actions to accomplish complex tasks
5. **Manage Conversations**: Maintain session history and context across interactions

## Core Architecture

### Key Components

#### 1. **Agent** (`src/agentflow/model/agent.py`)
The central component that represents an AI agent with:
- **Objective**: The agent's primary goal or system prompt
- **Actions**: A collection of executable actions the agent can use
- **Provider**: The LLM provider for generating responses
- **Session**: Conversation history and context management

**Key Features:**
- Async/sync support for running agents
- Interactive console mode for user interactions
- Tool calling capabilities (function calling)
- Streaming response support
- Message history tracking

**Example Agent Structure:**
```python
agent = Agent(
    name="assistant",
    objective="You are a helpful assistant",
    actions=["search", "calculator"],
    provider="openai"
)
```

#### 2. **Action** (`src/agentflow/model/action.py`)
Represents a reusable, executable function that an agent can invoke:
- Defined by an `action.yml` configuration file
- Implemented in an `action.py` handler file
- Can accept parameters
- Returns results to the agent

**Action Structure:**
- `name`: Action identifier
- `description`: What the action does
- `parameters`: Input parameters with descriptions
- `config_path`: Path to the action configuration

**Action Execution Flow:**
1. Agent determines which action to call based on LLM tool calling
2. Action parameters are extracted from the LLM response
3. Action handler is executed in a shell environment
4. Results are returned to the agent and added to conversation history

#### 3. **Hub** (`src/agentflow/model/hub.py`)
A centralized registry for fetching and managing agents and actions:
- Downloads agents/actions from remote repositories
- Caches locally for reuse
- Handles installation and setup
- Supports versioning with tags

**Usage:**
```python
from agentflow import hub

# Fetch an agent from the hub
agent = hub("okooai/my-agent:latest")

# Or use async
agent = await ahub("okooai/my-agent:latest")
```

#### 4. **Provider** (`src/agentflow/model/provider.py`)
Handles communication with LLM providers:
- Supports OpenAI's API format
- API key authentication
- Streaming and non-streaming modes
- Tool/function calling support
- Configurable timeouts

**Supported Providers:**
- OpenAI (GPT-4.1 and compatible APIs)
- Extensible to other providers via configuration

**Provider Configuration:**
```json
{
    "openai/gpt-4.1": {
        "alias": "openai",
        "url": "https://api.openai.com/v1",
        "auth_type": "api_key",
        "endpoints": {
            "chat": "/chat/completions"
        }
    }
}
```

#### 5. **Session** (`src/agentflow/model/session.py`)
Manages conversation state:
- Stores message history
- Maintains user and agent messages
- Tracks action executions
- Enables context-aware conversations

#### 6. **Message Types** (`src/agentflow/model/message.py`)
- **UserMessage**: Messages from the user
- **AgentMessage**: Responses from the agent, including action results

### Architecture Flow

```
User Input
    ↓
Agent (with Objective)
    ↓
Provider (LLM)
    ↓
Tool Calling Decision
    ↓
Action Execution
    ↓
Result to Session
    ↓
Next LLM Call (if needed)
    ↓
Final Response
```

## Configuration System

### Environment Variables

Agentflow uses environment variables with the prefix `AF_`:

- `AF_OPENAI_API_KEY`: OpenAI API key for authentication
- `AF_PROVIDER`: Default provider (default: "openai")
- `AF_PROVIDER_TIMEOUT`: Request timeout in seconds (default: 30)

### File Structure

**Agentfile**: Defines an agent
```yaml
name: my-agent
objective: "Your agent's objective"
actions:
  - action-name-1
  - action-name-2
```

**action.yml**: Defines an action
```yaml
name: search
description: "Search the web for information"
parameters:
  query:
    description: "The search query"
```

**action.py**: Implements the action
```python
async def handle():
    # Get parameters from environment
    params = upy.getenv('AF_ACTION_PARAMETERS')
    # Execute action logic
    result = do_search(params['query'])
    return result
```

### Cache and Storage

- **Cache Directory**: `~/.config/agentflow/`
- **Hub Cache**: `~/.config/agentflow/hub/`
- **Store**: `~/.config/agentflow/store/`
- **Providers Cache**: `~/.config/agentflow/providers.json`

## Installation & Usage

### Installation

```bash
pip install agentflow
```

### Command-Line Interface

```bash
# Show version
agentflow --version

# Get help
agentflow --help

# Available commands
agentflow help
agentflow version
```

### Python API Usage

```python
import agentflow
from agentflow import hub

# Method 1: Fetch agent from hub
agent = hub("okooai/my-agent")
result = agent.run("What is the weather today?")

# Method 2: Create agent programmatically
from agentflow.model.agent import Agent

agent = Agent(
    name="assistant",
    objective="You are a helpful assistant",
    actions=["search"],
    provider="openai"
)

# Run in non-interactive mode
response = agent.run("Hello, how are you?")

# Run in interactive mode (console)
agent.run(interactive=True)

# Async usage
result = await agent.arun("What is 2+2?")
```

## Key Features

### 1. **Async-First Design**
- Built with Python's `async/await` for efficient I/O operations
- All core operations support both sync and async modes
- `upy.run_async()` wrapper for synchronous usage

### 2. **Tool Calling / Function Calling**
- Agents can use tools (actions) to perform tasks
- Automatic parameter extraction from LLM responses
- Structured function schemas generated from action definitions

### 3. **Streaming Support**
- Real-time response streaming from LLMs
- Token-by-token output for better UX
- Supports streaming with tool calls

### 4. **Hub-Based Distribution**
- Central repository for sharing agents and actions
- GitHub-based distribution model
- Namespace support (e.g., `okooai/agent-name:tag`)

### 5. **Interactive Console**
- Built-in interactive mode for testing agents
- Color-coded output for actions and responses
- Real-time action execution feedback

### 6. **Extensible Provider System**
- Plugin-based provider architecture
- Easy to add new LLM providers
- Configuration-based provider setup

### 7. **Session Management**
- Persistent conversation history
- Database-backed message storage
- Context preservation across interactions

## Technical Details

### Dependencies

**Core Dependencies:**
- `upyog`: Utility library for common operations
- `httpx`: Async HTTP client for provider communication
- `click`: CLI framework (implied from command structure)

**Development Dependencies:**
- `pytest`: Testing framework
- `sphinx`: Documentation generation
- `pylint`: Code linting
- `tox`: Test automation
- `coveralls`: Code coverage

### Testing

```bash
# Run tests with pytest
make test

# Run with tox (multiple Python versions)
tox

# Check coverage
make coverage
```

### Project Structure

```
agentflow/
├── src/agentflow/
│   ├── __init__.py          # Package initialization
│   ├── __attr__.py          # Package metadata
│   ├── __main__.py          # Entry point
│   ├── config.py            # Configuration constants
│   ├── environ.py           # Environment utilities
│   ├── exception.py         # Custom exceptions
│   ├── cli/                 # Command-line interface
│   ├── commands/            # CLI commands
│   └── model/               # Core models
│       ├── agent.py         # Agent implementation
│       ├── action.py        # Action implementation
│       ├── hub.py           # Hub registry
│       ├── provider.py      # LLM provider
│       ├── session.py       # Session management
│       ├── message.py       # Message types
│       ├── store.py         # Storage backend
│       ├── base.py          # Base model class
│       └── helper.py        # Helper mixins
├── tests/                   # Test suite
├── docs/                    # Documentation
├── data/                    # Data files (providers.json)
└── requirements/            # Requirements files
```

## Use Cases

### 1. **Customer Support Agent**
- Objective: Answer customer questions
- Actions: search_knowledge_base, create_ticket, escalate

### 2. **Data Analysis Agent**
- Objective: Analyze data and generate reports
- Actions: query_database, generate_chart, export_csv

### 3. **Research Assistant**
- Objective: Help with research tasks
- Actions: web_search, summarize_paper, save_notes

### 4. **DevOps Agent**
- Objective: Manage infrastructure
- Actions: deploy_service, check_logs, scale_resources

## Extensibility

### Creating Custom Actions

1. Create a directory for your action
2. Add `action.yml` with configuration
3. Add `action.py` with handler function
4. Publish to a repository or use locally

### Adding New Providers

1. Add provider configuration to `data/providers.json`
2. Follow OpenAI API format or implement custom provider class
3. Set appropriate authentication method

### Custom Agent Types

- Extend the `Agent` class
- Override methods like `_abuild_model_prompt()` or `_build_schema_tools()`
- Add custom behavior for specialized use cases

## Development Workflow

### Built with boilpy
Agentflow is built using the `boilpy` Python project template, which provides:
- Standardized project structure
- CI/CD pipeline setup
- Documentation framework
- Testing infrastructure

### Continuous Integration
- GitHub Actions workflows
- Automated testing on multiple Python versions
- Code coverage reporting via Coveralls
- Docker image builds

## Docker Support

```bash
# Run Agentflow in Docker
docker run --rm -it ghcr.io/okooai/agentflow --verbose

# With environment variables
docker run --rm -it \
  -e AF_OPENAI_API_KEY=your-key \
  ghcr.io/okooai/agentflow
```

## Roadmap & Future Enhancements

Based on the current implementation, potential enhancements include:

1. **More Providers**: Support for Anthropic, Cohere, local models
2. **Advanced Actions**: File operations, API calls, code execution
3. **Multi-Agent Systems**: Agent-to-agent communication
4. **Observability**: Logging, metrics, tracing
5. **UI/Web Interface**: Web-based agent interaction
6. **Marketplace**: Community-driven agent and action hub

## Conclusion

Agentflow is a well-architected framework for building AI agents with a focus on:
- **Simplicity**: Easy to understand and use
- **Modularity**: Reusable components (agents, actions)
- **Extensibility**: Plugin-based architecture
- **Async Performance**: Built for modern Python
- **Developer Experience**: Good defaults, clear structure

It's designed for developers who want to build production-ready agentic applications without the complexity of larger frameworks, while still maintaining flexibility and power.

## Resources

- **Repository**: https://github.com/okooai/Agentflow
- **Documentation**: [docs/source/](../source/)
- **PyPI Package**: https://pypi.org/project/Agentflow/
- **Issue Tracker**: https://github.com/okooai/Agentflow/issues

---

*Last Updated: November 2025*
*Version: 0.1.0*
