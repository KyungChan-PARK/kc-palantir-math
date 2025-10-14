# Claude Sonnet 4.5 - Palantir Math System Configuration

**Model**: `claude-sonnet-4-5-20250929`
**Version**: 5.0 (Memory-Keeper Only Edition)
**Last Updated**: 2025-10-14

---

## 🎯 Core Principles

### 1. Memory-First Approach

**ALWAYS check memory at session start:**

```
SESSION START PROTOCOL:
1. Start memory-keeper session:
   mcp_context_session_start(
     name: "math-system-[date]",
     projectDir: "/home/kc-palantir/math"
   )

2. Retrieve previous context:
   mcp_context_get(
     category: "session-state",
     sortBy: "timestamp",
     sortOrder: "desc",
     limit: 1
   )

3. Resume work:
   Continue from last saved context
```

**During work:**
- Save context at critical milestones using `mcp_context_save()`
- Categories: "session-state", "decisions", "tasks", "progress", "architecture"
- Priority levels: "high", "medium", "low"
- Persistent storage in SQLite (context.db)

### 2. Sequential Thinking Integration

Use `mcp__sequential-thinking__sequentialthinking` for complex tasks:

```python
mcp__sequential-thinking__sequentialthinking({
    "thought": "First, analyze the problem...",
    "thought_number": 1,
    "total_thoughts": 5
})
```

### 3. Autonomous Agent Behavior

- Work autonomously for extended periods
- Use parallel tool calls when independent
- Provide fact-based updates only
- Track token usage (200K budget)

### 4. Context Management

**Thresholds:**
- 0-139K tokens: ✅ Normal work
- 140K tokens: ⚠️ Save context with mcp_context_save()
- 150K tokens: 🚨 Context editing triggered

**Recovery:** Load from memory-keeper SQLite database at next session start

**Benefits:**
- Persistent across all projects (user-scope)
- Advanced filtering (category, priority, time-based)
- Git branch tracking
- Metadata and tags support

---

## 🛠️ Tool Usage

### Memory-Keeper Context Management

**Start Session:**
```python
mcp_context_session_start(
    name: "math-system-session",
    description: "Multi-agent math education system",
    projectDir: "/home/kc-palantir/math",
    defaultChannel: "main-workflow"
)
```

**Save Context:**
```python
mcp_context_save(
    key: "current-phase",
    value: {
        "phase": "Phase 3: Specialized Agents",
        "completed": ["task1", "task2"],
        "next": ["task3"]
    },
    category: "session-state",
    priority: "high",
    channel: "main-workflow",
    metadata: {"agent_count": 6}
)
```

**Retrieve Context:**
```python
mcp_context_get(
    category: "session-state",
    priorities: ["high"],
    sortBy: "timestamp",
    sortOrder: "desc",
    limit: 10
)
```

**Search Context:**
```python
mcp_context_search(
    query: "agent performance",
    category: "progress",
    limit: 20
)
```

**List Sessions:**
```python
mcp_context_session_list(limit: 20)
```

### Parallel Tool Calls

```python
# ✅ CORRECT: Independent operations in parallel
[
    Read("file1.py"),
    Read("file2.py"),
    Bash("git status")
]

# ❌ WRONG: Sequential when parallel possible
Read("file1.py") → wait → Read("file2.py")
```

---

## 📁 Memory System Architecture

### MCP Memory-Keeper (SQLite) - Primary & Only Storage
```
~/.config/mcp-memory-keeper/context.db  (user-scope)
├── Sessions table
├── Context entries (categorized, prioritized)
├── Channels (topic-based organization)
└── Metadata & tags
```

**Benefits:**
- Persistent across ALL projects
- Advanced querying (category, priority, time)
- Git integration
- User-scope visibility
- No local file dependencies

---

## 🔄 Session Workflow

### Session Start

```
1. Start memory-keeper session
   mcp_context_session_start(...)

2. Retrieve last context
   mcp_context_get(category: "session-state", ...)

3. Resume from context
   Continue work based on retrieved state
```

### During Work

```
Critical milestone reached
  ↓
Save to memory-keeper (mcp_context_save)
  ↓
Continue work
  ↓
140K tokens → Save context checkpoint
  ↓
150K tokens → Context editing
  ↓
Next session → Load from memory-keeper → Resume
```

### Context Reset Recovery

```
1. Context edited (150K+ tokens)
2. Next session: Start memory-keeper session
3. Retrieve latest context from SQLite
4. Resume from checkpoint automatically
```

---

## 💡 Best Practices

### Always Check Memory First

```python
# At start of ANY session

# 1. Start memory-keeper session
mcp_context_session_start(
    name: f"math-session-{date}",
    projectDir: "/home/kc-palantir/math"
)

# 2. Retrieve last context
last_context = mcp_context_get(
    category: "session-state",
    sortBy: "timestamp",
    sortOrder: "desc",
    limit: 1
)

# 3. Resume from context
# Process retrieved context and continue work
```

### Use Sequential Thinking for Complex Tasks

```python
# Automatically stores reasoning to memory
mcp__sequential-thinking__sequentialthinking({
    "thought": "Need to analyze...",
    "thought_number": 1,
    "total_thoughts": 5
})
```

### Save Context at Milestones

```python
# For critical milestones
mcp_context_save(
    key: "phase1-complete",
    value: {
        "phase": "Phase 1",
        "completed_tasks": [...],
        "state": {...}
    },
    category: "milestone",
    priority: "high",
    channel: "main-workflow",
    tags: ["phase1", "infrastructure"],
    metadata: {"timestamp": "2025-10-14"}
)
```

### ⚠️ CRITICAL: Context Organization

**Categories (use consistently):**
- `session-state`: Current phase, tasks, progress
- `decisions`: Architecture choices, design decisions
- `tasks`: TODO items, next steps
- `progress`: Completed work, metrics
- `architecture`: System design, agent definitions
- `milestone`: Major achievements
- `debug`: Issues, errors, solutions

**Priority Levels:**
- `high`: Critical state, blocking issues
- `medium`: Important context, decisions
- `low`: Nice-to-have, reference info

**Channels (topic-based):**
- `main-workflow`: Primary development flow
- `agent-development`: Agent implementation
- `documentation`: Docs and guides
- `testing`: Test results, debugging

**Best Practices:**
```python
# Save with rich metadata
mcp_context_save(
    key: "descriptive-key",
    value: {...},
    category: "session-state",
    priority: "high",
    channel: "main-workflow",
    tags: ["phase3", "agents"],
    metadata: {"agent": "meta-orchestrator"}
)
```

---

## 🗣️ Communication Style

### ✅ DO:
- Be concise and direct
- Provide fact-based updates
- Skip verbose summaries
- Use parallel operations
- Track token usage

### ❌ DON'T:
- Repeat what user knows
- Add unnecessary explanations
- Use flowery language
- Sequential when parallel possible

---

## 🚨 Troubleshooting

### Memory-Keeper Not Responding

```bash
# Check MCP connection
claude mcp list | grep memory-keeper

# Should show: ✓ Connected
# If not, reinstall:
claude mcp add --scope user memory-keeper npx mcp-memory-keeper
```

### Context Not Found (First Session)

```python
# Normal for first session - start fresh
mcp_context_session_start(
    name: "math-system-initial",
    projectDir: "/home/kc-palantir/math"
)

# Save initial state
mcp_context_save(
    key: "initial-state",
    value: {"phase": "Starting", "tasks": []},
    category: "session-state",
    priority: "high"
)
```

### Context Recovery After Reset

```python
# Automatic recovery
# 1. Start new session (memory-keeper auto-connects)
# 2. Query for last state
last_state = mcp_context_get(
    category: "session-state",
    sortBy: "timestamp",
    sortOrder: "desc",
    limit: 1
)
# 3. Resume from last_state
```

---

## 📊 Performance Metrics

- memory-keeper save: ~150 tokens/call
- memory-keeper get: ~100 tokens/call
- memory-keeper search: ~120 tokens/call
- Context recovery: Immediate (SQLite query)
- Token budget: 200K total
- Storage: Persistent across ALL projects (user-scope)

---

## 🎯 Success Criteria

- ✅ Zero context loss
- ✅ Seamless session continuity
- ✅ Complete thinking process preserved
- ✅ All decisions traceable
- ✅ Token usage optimized (<150K)
- ✅ No file-based dependencies

---

## 🚀 Quick Commands

```bash
# Load state (ask Claude)
"Load latest context from memory-keeper"

# Save context (ask Claude)
"Save current state to memory-keeper: [milestone name]"

# View sessions
"List recent memory-keeper sessions"

# Search context
"Search memory-keeper for [query]"

# View session status
"Show memory-keeper session status"
```

---

**Memory System**: MCP Memory-Keeper (SQLite) ONLY
**Storage**: `~/.config/mcp-memory-keeper/context.db` (user-scope)
**Recovery**: SQLite query (automatic)
**No File Dependencies**: All context in memory-keeper
