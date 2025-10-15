# Quick Start Guide

## 🚀 Running the Agent System

### Single Command

```bash
cd /home/kc-palantir/math
uv run python main.py
```

**That's all you need!** The system will:
- ✅ Load environment variables from `.env`
- ✅ Initialize 9 specialized agents
- ✅ Connect to 3 MCP servers (memory-keeper, obsidian, github)
- ✅ Start interactive conversation loop

### What Happens

1. **Infrastructure initialized**:
   - Structured logging
   - Performance monitoring
   - Context management
   - Error tracking

2. **MCP servers started**:
   - `memory-keeper`: Persistent memory across sessions
   - `obsidian`: Obsidian vault integration
   - `github`: GitHub API operations

3. **Agents ready**:
   - Meta-Orchestrator (main coordinator)
   - Knowledge-Builder (creates Obsidian notes)
   - Quality-Agent (validates content)
   - Research-Agent (deep concept research)
   - Example-Generator (mathematical examples)
   - Dependency-Mapper (prerequisite graphs)
   - Socratic-Planner (requirement clarification)
   - Socratic-Mediator (user interaction)
   - Self-Improver (continuous improvement)

### Example Session

```bash
$ uv run python main.py

================================================================================
Math Education Multi-Agent System v2.1
================================================================================

[Infrastructure] Initializing logging and monitoring...
[Auth] Using Claude Code authentication (API key not required) ✓

✅ Infrastructure initialized

Main Agent: Meta-Orchestrator
Subagents: 6 specialized agents
  - knowledge-builder: Create Obsidian markdown files
  - quality-agent: Validate file quality
  - research-agent: Deep concept research
  - example-generator: Generate mathematical examples
  - dependency-mapper: Map prerequisite dependencies
  - socratic-planner: Clarify user requirements

Type 'exit' to quit

You: Create a note about the Pythagorean theorem

[Agent starts working with MCP tools...]
```

### MCP Tools in Action

When you ask the system to create a note, it will:

1. **Research** the concept (research-agent)
2. **Save context** to memory-keeper MCP
3. **Create markdown file** in Obsidian vault via obsidian MCP
4. **Validate quality** (quality-agent)
5. **Map dependencies** (dependency-mapper)
6. **Commit to GitHub** via github MCP (if self-improver enabled)

All of this happens automatically using MCP tools!

## 📋 Prerequisites

### Required

- ✅ Python 3.13+
- ✅ `uv` package manager
- ✅ Node.js (for `npx` MCP servers)
- ✅ `.env` file with API keys

### Check Prerequisites

```bash
# Check Python
python3 --version  # Should be 3.13+

# Check uv
uv --version  # Should be 0.9.2+

# Check Node.js
node --version  # Should be v22+
npx --version

# Check .env
cat .env  # Should have GITHUB_TOKEN, OBSIDIAN_API_KEY
```

## 🔧 Configuration

### `.env` File

Create `.env` in project root:

```bash
GITHUB_TOKEN=your_github_personal_access_token
OBSIDIAN_API_KEY=your_obsidian_local_rest_api_key
OBSIDIAN_API_URL=https://127.0.0.1:27124
```

### `.mcp.json` File

Already configured! Defines MCP servers:

```json
{
  "mcpServers": {
    "memory-keeper": {...},
    "obsidian": {...},
    "github": {...}
  }
}
```

## 🎯 Common Tasks

### Create a Math Concept Note

```
You: Create a comprehensive note about Euler's formula
```

### Research a Topic

```
You: Research the historical development of calculus
```

### Map Dependencies

```
You: Map the prerequisite dependencies for linear algebra
```

### Generate Examples

```
You: Generate 5 examples of integration by parts
```

## 🐛 Troubleshooting

### "No module named 'anthropic'"

```bash
cd /home/kc-palantir/math
uv pip install -e .
```

### "GITHUB_TOKEN not found"

Check `.env` file exists and has correct format:
```bash
cat .env
```

### "npx command not found"

Install Node.js:
```bash
# Check if nvm is installed
nvm --version

# Install Node.js
nvm install 22
nvm use 22
```

### MCP Server Connection Issues

Check if MCP servers work independently:
```bash
# Test memory-keeper
npx -y mcp-memory-keeper

# Test github
GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN npx -y @modelcontextprotocol/server-github
```

## 📚 More Information

- **MCP Setup**: See `docs/MCP-SETUP.md`
- **Implementation Standards**: See `CLAUDE-IMPLEMENTATION-STANDARDS.md`
- **Project Overview**: See `README.md`

---

**Ready to start?** Just run `uv run python main.py`! 🚀

