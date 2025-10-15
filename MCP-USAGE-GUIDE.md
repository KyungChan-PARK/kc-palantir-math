# MCP Server Usage Guide

**Last Updated**: 2025-10-15  
**Project**: Math Education Multi-Agent System

---

## 🎯 Available MCP Tools

### 1. Memory-Keeper (SQLite-based Memory)

**Purpose**: Persistent memory storage for agent learnings, performance data, and context

**Available Tools**:
```python
# Save context/memory
mcp__memory-keeper__context_save(
    key="agent-performance-meta-orchestrator",
    value={"success_rate": 0.95, "avg_time_ms": 1200}
)

# Retrieve context/memory
mcp__memory-keeper__context_get(
    key="agent-performance-meta-orchestrator"
)

# Search memories
mcp__memory-keeper__context_search(
    query="performance meta-orchestrator"
)
```

**Use Cases**:
- Agent performance tracking
- User feedback storage
- Tool usage statistics
- Error pattern analysis

---

### 2. Obsidian (Math Vault Management)

**Purpose**: Create, read, update Obsidian markdown files in math-vault

**Available Tools**:
```python
# Create new concept file
obsidian__create_note(
    path="Theorems/pythagorean-theorem.md",
    content="""---
type: theorem
domain: geometry
level: middle-school
---

# Pythagorean Theorem
...
"""
)

# Read existing file
obsidian__read_note(
    path="Theorems/pythagorean-theorem.md"
)

# Update file
obsidian__update_note(
    path="Theorems/pythagorean-theorem.md",
    content="Updated content..."
)

# Search vault
obsidian__search_notes(
    query="pythagorean"
)

# List all notes
obsidian__list_notes(
    folder="Theorems"
)
```

**Use Cases**:
- Knowledge-builder agent file creation
- Quality-agent validation
- Dependency-mapper graph construction
- Research-agent content storage

---

### 3. GitHub (Repository Integration)

**Purpose**: Interact with GitHub repository (issues, PRs, commits)

**Available Tools**:
```python
# Create issue
github__create_issue(
    owner="KyungChan-PARK",
    repo="kc-palantir-math",
    title="CI failure in standards-check",
    body="Model alias detected in agent file..."
)

# List issues
github__list_issues(
    owner="KyungChan-PARK",
    repo="kc-palantir-math",
    state="open"
)

# Create PR
github__create_pull_request(
    owner="KyungChan-PARK",
    repo="kc-palantir-math",
    title="fix: update model versions",
    head="feature-branch",
    base="main",
    body="Updates all agents to claude-sonnet-4-5-20250929"
)

# Get file content
github__get_file_content(
    owner="KyungChan-PARK",
    repo="kc-palantir-math",
    path="agents/meta_orchestrator.py"
)

# Search code
github__search_code(
    query='repo:KyungChan-PARK/kc-palantir-math model="sonnet"'
)
```

**Use Cases**:
- Self-improver agent PR creation
- CI failure tracking
- Code review automation
- Documentation updates

---

## 🚀 MCP Tool Usage in Agents

### Example 1: Meta-Orchestrator Performance Tracking

```python
# In meta_orchestrator.py
tools = [
    'Task',
    'Read', 'Write',
    'TodoWrite',
    'mcp__sequential-thinking__sequentialthinking',
    'mcp__memory-keeper__context_save',      # ← MCP tool
    'mcp__memory-keeper__context_get',       # ← MCP tool
    'mcp__memory-keeper__context_search',    # ← MCP tool
]
```

**Usage in prompt**:
```
After completing task orchestration:
1. Save performance metrics using mcp__memory-keeper__context_save
2. Key format: "orchestration-{timestamp}"
3. Value: {agents_used, duration_ms, success, errors}
```

---

### Example 2: Knowledge-Builder with Obsidian

```python
# In knowledge_builder.py
tools = [
    'Read', 'Write', 'Edit',
    'TodoWrite',
    'mcp__obsidian__create_note',    # ← MCP tool
    'mcp__obsidian__read_note',      # ← MCP tool
    'mcp__obsidian__update_note',    # ← MCP tool
]
```

**Usage in prompt**:
```
When creating mathematical concept file:
1. Use mcp__obsidian__create_note instead of Write tool
2. Path: "Theorems/{concept-name}.md"
3. Content: YAML frontmatter + markdown body
4. Verify with mcp__obsidian__read_note
```

---

### Example 3: Self-Improver with GitHub

```python
# In self_improver_agent.py
tools = [
    'Read', 'Write', 'Edit',
    'mcp__github__create_pull_request',  # ← MCP tool
    'mcp__github__create_issue',         # ← MCP tool
]
```

**Usage in prompt**:
```
After generating improvement actions:
1. Create PR using mcp__github__create_pull_request
2. Title: "fix: {improvement_summary}"
3. Body: Include root cause analysis + changes
4. Auto-assign reviewers if available
```

---

## 🔍 MCP Tool Discovery

### Check Available MCP Tools

```bash
# List all MCP resources
curl -X POST http://localhost:3000/mcp/resources

# Test memory-keeper
npx -y mcp-memory-keeper

# Test obsidian server
cd tools/obsidian-mcp-server
uv run python server.py

# Test github server
npx -y @modelcontextprotocol/server-github
```

---

## 📊 MCP Tool Naming Convention

**Format**: `mcp__{server-name}__{tool-name}`

**Examples**:
- `mcp__memory-keeper__context_save`
- `mcp__memory-keeper__context_get`
- `mcp__memory-keeper__context_search`
- `mcp__obsidian__create_note`
- `mcp__obsidian__read_note`
- `mcp__github__create_issue`
- `mcp__sequential-thinking__sequentialthinking`

---

## 🛡️ Security Best Practices

### API Keys in .mcp.json

```json
{
  "mcpServers": {
    "obsidian": {
      "env": {
        "OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}"  // Use env var
      }
    },
    "github": {
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"  // Use env var
      }
    }
  }
}
```

**⚠️ WARNING**: Current `.mcp.json` has hardcoded tokens - should use environment variables!

---

## 🔧 Troubleshooting

### MCP Server Not Starting

```bash
# Check if npx is available
npx --version

# Check if uv is available
uv --version

# Test individual server
npx -y mcp-memory-keeper
```

### Tool Not Found

```bash
# Verify tool name in agent definition
grep -r "mcp__" agents/

# Check .mcp.json configuration
cat .mcp.json
```

### Connection Errors

```bash
# Check if server is running
ps aux | grep mcp

# Check logs
tail -f ~/.mcp/logs/*.log
```

---

## 📚 Related Documentation

- **main.py**: MCP server initialization
- **agents/*.py**: Agent tool configurations
- **.mcp.json**: MCP server definitions
- **CLAUDE-IMPLEMENTATION-STANDARDS.md**: Tool usage standards

---

**Ready for MCP tool usage!** 🚀

Use this guide to integrate MCP tools into agent prompts and workflows.
