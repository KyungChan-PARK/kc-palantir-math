# Claude Sonnet 4.5 - Palantir Math System Configuration

**Model**: `claude-sonnet-4-5-20250929`
**Version**: 4.0 (MCP Memory-Keeper Edition)
**Last Updated**: 2025-10-12

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

**List Sessions:**
```python
mcp_context_session_list(limit: 20)
```

### Fallback: File-Based Checkpoints

For local project snapshots, use file tools:
```python
Read(".claude/memories/phase-progress/current-state.json")
Write(".claude/memories/phase-progress/checkpoint-name.json", json_data)
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

### Primary: MCP Memory-Keeper (SQLite)
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

### Fallback: Local File Storage
```
.claude/memories/
└── phase-progress/          # Project-specific snapshots
    ├── current-state.json   # Latest local state
    └── checkpoint-*.json    # Named snapshots
```

**Use for:**
- Project-specific backups
- Git version control
- Human-readable archives

---

## 🔄 Session Workflow

### Session Start

```
1. Load State: Read(".claude/memories/phase-progress/current-state.json")
2. Resume: Continue from checkpoint
```

Example checkpoint:
```json
{
    "phase": "Phase 1: Infrastructure",
    "completed_tasks": ["Task 1", "Task 2"],
    "next_tasks": ["Task 3"],
    "timestamp": "2025-10-12T16:30:00"
}
```

### During Work

```
Critical milestone reached
  ↓
Create named checkpoint (Write)
  ↓
Update current-state.json (Write)
  ↓
Continue work
  ↓
140K tokens → Manual checkpoint recommended
  ↓
150K tokens → Context editing
  ↓
Next session → Load current-state.json → Resume
```

### Context Reset Recovery

```
1. Context edited (150K+ tokens)
2. Next session: Read current-state.json
3. Resume from checkpoint
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
# Automatically stores to memory
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
    metadata: {"timestamp": "2025-10-12"}
)

# Optional: Also save to local file for backup
Write(".claude/memories/phase-progress/checkpoint-phase1-complete.json", json.dumps(...))
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

### Memory Not Found

```bash
# Initialize if needed
mkdir -p .claude/memories/phase-progress

# Create initial state
cat > .claude/memories/phase-progress/current-state.json << 'EOF'
{
    "phase": "Starting",
    "completed_tasks": [],
    "next_tasks": ["Initialize"]
}
EOF
```

### Context Lost

```python
# Load from checkpoint
checkpoint = Read(".claude/memories/phase-progress/current-state.json")
state = json.loads(checkpoint)
# Continue from state
```

---

## 📊 Performance Metrics

- memory-keeper save: ~150 tokens/call
- memory-keeper get: ~100 tokens/call
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

---

## 📝 Related Documents

- **PROJECT_CONTEXT.md** - Overall project architecture
- **QUICKSTART.md** - Quick reference for new sessions

---

## 🚀 Quick Commands

```bash
# Load state (ask Claude)
"Load latest context from memory-keeper"

# Save context (ask Claude)
"Save current state to memory-keeper: [milestone name]"

# View sessions
"List recent memory-keeper sessions"

# View local checkpoints
ls -lt .claude/memories/phase-progress/
```

---

**Memory System**: MCP Memory-Keeper (SQLite) + Local Files
**Primary Storage**: `~/.config/mcp-memory-keeper/context.db` (user-scope)
**Backup Storage**: `.claude/memories/phase-progress/` (project-scope)
**Recovery**: SQLite query + file fallback
