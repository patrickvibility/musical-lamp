# Claude Code Frameworks & Development Processes Research

## Executive Summary

This document provides comprehensive research into the best Claude code frameworks, development processes, and strategies for managing context and long-term memory when developing new applications. The findings are based on trending approaches and best practices as of January 2026.

---

## Table of Contents

1. [Core Best Practices](#core-best-practices)
2. [Context Engineering](#context-engineering)
3. [Long-Term Memory Strategies](#long-term-memory-strategies)
4. [Claude Agent SDK](#claude-agent-sdk)
5. [Multi-Agent Orchestration](#multi-agent-orchestration)
6. [RAG (Retrieval Augmented Generation)](#rag-retrieval-augmented-generation)
7. [MCP (Model Context Protocol)](#mcp-model-context-protocol)
8. [Skills, Hooks & Extensibility](#skills-hooks--extensibility)
9. [Frameworks & Tools](#frameworks--tools)
10. [Security Best Practices](#security-best-practices)

---

## Core Best Practices

### CLAUDE.md - The Foundation

The `CLAUDE.md` file is the most critical tool for guiding Claude in your project. It's automatically read by Claude to get context on your project.

**Best Practices:**
- Keep it **100-200 lines maximum** (sweet spot)
- Document repository etiquette (branch naming, merge vs. rebase)
- Include developer environment setup (pyenv, compilers)
- Note any unexpected behaviors or warnings
- For larger projects, use **per-folder CLAUDE.md files** and link them from root

**Structure Example:**
```markdown
# Project Overview
Brief description of what this project does

# Architecture
Key architectural decisions and patterns

# Development Guidelines
- Coding standards
- Testing requirements
- Build commands

# Common Patterns
Project-specific patterns Claude should follow
```

### Planning Before Implementation

Planning is **non-negotiable** for production code:
- Use Planning Mode or written plans before coding
- Conduct architectural reviews for complex features
- Write clear, precise prompts (e.g., "a Linear-style app interface" vs "a UI design")
- "Vibe coding" only works for throwaway MVPs

### Simplicity Over Complexity

**Key Principle:** Simple control loops outperform multi-agent systems in most cases.
- Low-level tools (Bash, Read, Edit) + selective abstractions beat heavy RAG or complex frameworks
- LLMs are fragile; additional complexity makes debugging exponentially harder
- Avoid over-engineering unless explicitly required

---

## Context Engineering

Context engineering has emerged as the evolution of prompt engineering—it's about designing the entire context window, not just the prompt.

### Core Techniques

#### 1. Compaction
The practice of summarizing a conversation nearing the context limit and reinitiating with the summary.

**How Claude Code Implements It:**
- Passes message history to model for summarization
- Preserves: architectural decisions, unresolved bugs, implementation details
- Discards: redundant tool outputs, routine messages
- Includes 5 most recently accessed files

#### 2. Context Editing
Automatically manage conversation context as it grows.

**Results:**
- 84% reduction in token consumption
- 39% performance improvement when combined with memory tools
- Enables completion of workflows that would otherwise fail

#### 3. Just-in-Time Context Loading
Rather than pre-processing all data up front:
- Maintain lightweight identifiers (file paths, queries, links)
- Dynamically load data at runtime using tools
- Reduces initial context overhead

### Optimization Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Initial tokens | 7,584 | 3,434 | 54% reduction |
| Tool discovery | Standard | Improved | Better capability |

### Quality Over Quantity

**Critical Finding:** Performance degrades as models approach context limits.

| Utilization | Output Quality | Recommendation |
|-------------|---------------|----------------|
| 90% | More bugs, inconsistent architecture | Avoid |
| 75% | Higher quality, maintainable code | Optimal |

### Claude 4.5 Context Awareness

Claude 4.5 models feature built-in context awareness:
- Tracks remaining context window ("token budget")
- Automatic compaction at limits
- Don't stop tasks early due to token concerns
- Save progress to memory before context refresh

---

## Long-Term Memory Strategies

### Anthropic's Official Memory Features (2025)

Claude Memory enables persistent context across conversations:
- **Team & Enterprise accounts**: Cross-session memory
- **Storage**: Simple Markdown files (CLAUDE.md hierarchy)
- **Implementation**: `conversation_search` and `recent_chats` tools

### Memory Architecture Best Practices

#### File-Based Memory (Recommended)
```
project/
├── CLAUDE.md              # Essential info for every session
├── docs/
│   ├── architecture.md    # Project architecture
│   ├── decisions.md       # ADRs and decisions
│   └── patterns.md        # Code patterns
└── .claude/
    └── memory/            # Session-specific memories
```

#### External Memory Systems
For custom integrations:
- Offload long-term state outside the prompt
- Store key variables/user facts in external databases
- Selectively reinsert as needed

### Third-Party Memory Tools

| Tool | Description |
|------|-------------|
| **claude-mem** | Captures everything Claude does, compresses with AI, makes knowledge available to future sessions |
| **Continuum** | CLI providing single source of truth across all Claude interfaces |

### Extended Memory Strategies

1. **Persistent Notes**: Maintain concise project briefs (NOTES.md)
2. **Re-insertion**: Insert essentials when needed
3. **Summarization**: Compress completed work phases
4. **External Storage**: Store in databases before proceeding

> **Mental Model:** Claude's context window = working memory; Extended memory = your well-organized notebook

---

## Claude Agent SDK

The Claude Agent SDK (formerly Claude Code SDK) provides the building blocks for production-ready agents.

### Key Features

- **Context Management**: Automatic compaction and management
- **Rich Tool Ecosystem**: File operations, code execution, web search, MCP extensibility
- **Advanced Permissions**: Fine-grained control over capabilities
- **Production Essentials**: Error handling, session management, monitoring

### Basic Agent Loop

```python
from anthropic_ai.claude_agent_sdk import create_agent

# The SDK handles the loop automatically:
# 1. Call model
# 2. Check for tool use
# 3. Execute tool
# 4. Feed result back
# 5. Repeat until done

agent = create_agent(
    permission_mode="default",  # or "acceptEdits", "bypassPermissions"
    tools=[...]
)
```

### Custom Tools via MCP

Custom tools are implemented as in-process MCP servers:
```python
@tool
def my_custom_tool(param: str) -> str:
    """Tool description for Claude"""
    return process(param)
```

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Prompts for approval |
| `acceptEdits` | Auto-approve file edits |
| `bypassPermissions` | No prompts (use cautiously) |

### Use Cases

- **Finance Agents**: Portfolio analysis, investment evaluation
- **Personal Assistants**: Travel booking, calendar management
- **Customer Support**: High-ambiguity request handling with escalation

---

## Multi-Agent Orchestration

### Anthropic's Official Architecture

**Orchestrator-Worker Pattern:**
1. Lead agent analyzes query and develops strategy
2. Spawns subagents for parallel exploration
3. Subagents work on different aspects simultaneously
4. Lead agent coordinates and synthesizes results

### Claude Code Subagents

Built-in subagents are automatically used when appropriate:
- Inherit parent conversation's permissions
- Have additional tool restrictions
- **Cannot spawn other subagents** (use Skills for nested delegation)

### Orchestration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Fan-Out** | Spawn parallel workers for independent tasks | Research, testing |
| **Pipeline** | Sequential task processing | Build processes |
| **Map-Reduce** | Distribute work, aggregate results | Data processing |
| **Hierarchical** | Queen/workers structure | Complex projects |
| **Mesh** | Peer-to-peer communication | Collaborative tasks |

### Frameworks for Multi-Agent Systems

#### Claude Flow
- 54+ specialized agents in coordinated swarms
- Shared memory and consensus mechanisms
- Continuous learning and pattern reuse

#### CC Mirror
- "Conductor" identity for task decomposition
- Dependency graphs with background execution
- Fan-Out, Pipeline, Map-Reduce patterns

#### wshobson/agents
Production-ready system with:
- 108 specialized AI agents
- 15 multi-agent workflow orchestrators
- 129 agent skills
- 72 development tools

### Production Considerations

**Challenges:**
- Conversations can span hundreds of turns
- Standard context windows become insufficient
- Agents are non-deterministic between runs
- Debugging is harder with dynamic decisions

**Solutions:**
- Intelligent compression and memory mechanisms
- Summarize completed work phases
- Store essential info in external memory
- Implement robust logging and monitoring

---

## RAG (Retrieval Augmented Generation)

### Claude's Built-in RAG

When project knowledge approaches context limits:
- Automatically enables RAG mode
- Expands capacity by **up to 10x**
- Uses project knowledge search tool
- Retrieves only relevant information

### When to Use RAG

| Knowledge Base Size | Recommendation |
|--------------------|----------------|
| < 200,000 tokens (~500 pages) | Include directly in prompt |
| > 200,000 tokens | Use RAG |

### Chunking Strategies

**Best Practices:**
- Use **semantic chunking** with contextual headers
- Preserve sections and headings
- Keep chunks at **200-300 words**
- Include heading text in each chunk

**Example:**
```
Chunk: "Installation Steps: First, ensure you have Python 3.9+..."
```

### Contextual Retrieval (Anthropic's Approach)

Combines two techniques:
1. **Contextual Embeddings**
2. **Contextual BM25**

**Results:**
- 49% reduction in failed retrievals
- 67% reduction with reranking added

### Hybrid Search & Reranking

Modern RAG implementations combine:
- Dense retrieval (embeddings)
- Sparse retrieval (BM25)
- Reranking for final selection

**Performance Target:** Sub-100ms retrieval latency

### Vector Database Options

| Database | Best For |
|----------|----------|
| Pinecone | Production-scale, managed |
| Weaviate | Hybrid search, GraphQL |
| Milvus | Self-hosted, high performance |
| pgvector | Postgres integration |

---

## MCP (Model Context Protocol)

### Overview

MCP is an **open standard** introduced by Anthropic (November 2024) for standardizing LLM integrations with external systems.

### 2025-2026 Adoption

- **OpenAI** adopted MCP (March 2025)
- **Microsoft** integrated into Windows 11 (Build 2025)
- **Linux Foundation** received MCP donation (December 2025)
- **1,200+ MCP servers** now available

### Server Capabilities

| Capability | Description |
|------------|-------------|
| **Resources** | File-like data (API responses, file contents) |
| **Tools** | Functions callable by the LLM |
| **Prompts** | Pre-written templates for specific tasks |

### Pre-built Servers

Anthropic provides servers for:
- Google Drive
- Slack
- GitHub / Git
- Postgres
- Puppeteer

### Development SDKs

Available in:
- Python
- TypeScript
- C#
- Java

### Best Practice: Less is More

**Warning:** Too many MCPs consume context—sometimes **40%+ of 200k context** just for MCP tools at startup.

**Recommendation:** Choose MCPs carefully based on actual needs.

---

## Skills, Hooks & Extensibility

### Skills

Skills extend Claude's capabilities via `SKILL.md` files:

```
.claude/skills/review/
├── SKILL.md          # Instructions
├── templates/        # Supporting files
└── scripts/          # Automation scripts
```

**Key Points:**
- Auto-invoked based on context matching
- Can invoke directly with `/skill-name`
- Replace legacy custom slash commands

### Slash Commands

User-invoked commands via `/command`:
- Simple, repeatable terminal entry points
- Single file implementation
- Located at `.claude/commands/`

### Hooks

Hooks execute shell commands automatically:
- Access via `/hooks` command
- Critical for enterprise repos
- Use for formatting, logging, notifications

**Security Warning:** Always review hook code before adding.

### Plugins

Bundled packages of:
- Skills
- Subagents
- Commands

Distributed via marketplace as cohesive units.

### Development Tools

| Tool | Description |
|------|-------------|
| **Claude Code Skill Factory** | Toolkit for building production-ready skills |
| **cc-tools** | High-performance Go implementation |
| **Claude Code Templates** | Comprehensive resource collection |

---

## Frameworks & Tools

### ContextKit

Systematic development framework:
- 4-phase planning methodology
- Specialized quality agents
- Structured workflows
- Production-ready code on first try

### Ralph for Claude Code

Autonomous AI development framework:
- Iterative work until completion
- Intelligent exit detection
- Rate limiting & circuit breakers
- Safety guardrails against infinite loops

### awesome-claude-code

Curated list of:
- Skills
- Hooks
- Slash commands
- Agent orchestrators
- Applications
- Plugins

**GitHub:** [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

---

## Security Best Practices

### Non-Negotiable Security Measures

1. **Least Privilege Tokens**: Restrict repo and environment access
2. **Harden Runners**: Lock down external network calls
3. **Human Review**: Gate merges on human review + green tests
4. **Never Auto-Merge**: Don't auto-merge solely on AI feedback
5. **Treat AI Output as Untrusted**: Until verified
6. **Secrets Management**: Keep secrets out of prompts and contexts

### Code Review Practices

- Run security-focused code review agents
- Scan for OWASP Top 10 vulnerabilities
- Validate input/output at system boundaries
- Use static analysis tools in CI/CD

---

## Summary: Key Takeaways

### For Context Management
1. Use CLAUDE.md religiously (100-200 lines max)
2. Implement compaction for long conversations
3. Prefer 75% context utilization over 90%
4. Use just-in-time context loading

### For Long-Term Memory
1. File-based memory with clear hierarchy
2. Offload state to external databases
3. Summarize and compress completed work
4. Consider claude-mem for persistent sessions

### For Agent Development
1. Start with Claude Agent SDK
2. Use simple control loops over complex multi-agent systems
3. Implement robust error handling and monitoring
4. Use MCP for external integrations (sparingly)

### For Production Systems
1. Plan before implementation (always)
2. Keep it simple (avoid over-engineering)
3. Security hardening is non-negotiable
4. Test thoroughly with evaluation datasets

---

## Sources

- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [Claude Agent SDK Overview](https://docs.claude.com/en/api/agent-sdk/overview)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Slash commands](https://code.claude.com/docs/en/slash-commands)
- [RAG for Projects | Claude Help Center](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)
- [Claude AI Context Window](https://www.datastudios.org/post/claude-ai-context-window-token-limits-and-memory-operational-boundaries-and-long-context-behavior)
- [Claude Agent: Proven 2025 Playbook](https://binaryverseai.com/claude-agent-sdk-context-engineering-long-memory/)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Flow](https://github.com/ruvnet/claude-flow)
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers)

---

*Research compiled: January 2026*
