# Quick Start Guide - New Session

**For**: New Claude Code sessions
**Location**: `/home/kc-palantir/math/`
**Last Updated**: 2025-10-12
**Memory System**: MCP Memory-Keeper v4.0

---

## ⚡ 30-Second Setup

### 1. Start Memory-Keeper Session

Ask Claude:
```
"Start memory-keeper session for math-system project"
```

Claude will:
- Execute `mcp_context_session_start()` with project directory
- Create persistent session in SQLite database
- Set up channels and metadata

### 2. Load Previous Context

```
"Load latest context from memory-keeper"
```

Claude will:
- Query `mcp_context_get()` for recent session-state
- Show phase, completed tasks, next tasks
- Resume work automatically

### 3. Start Working

```
"Continue with next task"
```

---

## 📋 Key Files to Read

### First Session
1. **PROJECT_CONTEXT.md** - Complete system overview
2. **.claude/CLAUDE.md** - Claude configuration (v4.0 Memory-Keeper)

### Subsequent Sessions
1. **This file (QUICKSTART.md)** - Quick reference
2. **Memory-Keeper database** - Persistent context (automatic)

---

## 🛠️ Common Commands

### Memory-Keeper Operations

Ask Claude:
```
# Load state
"Load latest context from memory-keeper"

# Save progress
"Save current state to memory-keeper: [milestone-name]"

# View sessions
"List recent memory-keeper sessions"

# Query by category
"Get all architecture decisions from memory-keeper"

# Query by priority
"Get high-priority tasks from memory-keeper"
```

### Local File Operations
```bash
# Check local backups
ls -la .claude/memories/phase-progress/

# View local state
cat .claude/memories/phase-progress/current-state.json
```

---

## 🔄 Memory-Keeper System

### Persistent SQLite Storage
- **Location**: `~/.config/mcp-memory-keeper/context.db`
- **Scope**: User-level (accessible from ALL projects)
- **Features**:
  - Categories (session-state, decisions, tasks, etc.)
  - Priorities (high, medium, low)
  - Channels (topic-based organization)
  - Tags and metadata
  - Time-based queries

### Categories
- `session-state`: Current phase, tasks, progress
- `decisions`: Architecture choices, design decisions
- `tasks`: TODO items, next steps
- `progress`: Completed work, metrics
- `architecture`: System design, agent definitions
- `milestone`: Major achievements
- `debug`: Issues, errors, solutions

### Priority Levels
- `high`: Critical state, blocking issues
- `medium`: Important context, decisions
- `low`: Nice-to-have, reference info

### Channels
- `main-workflow`: Primary development flow
- `agent-development`: Agent implementation
- `documentation`: Docs and guides
- `testing`: Test results, debugging

---

## 📊 Token Management

| Tokens | Status | Action |
|--------|--------|--------|
| 0-139K | ✅ OK | Continue normally |
| 140K | ⚠️ Warning | Save context to memory-keeper |
| 150K+ | 🚨 Critical | Context editing triggered |

After context reset → Ask Claude to load from memory-keeper

---

## 📝 Available MCP Servers

```bash
claude mcp list
```

Active servers:
- ✅ **memory-keeper** - Persistent context management (SQLite)
- ✅ **sequential-thinking** - Complex reasoning
- ✅ **brave-search** - Web search
- ✅ **context7** - Library docs
- ✅ **filesystem** - File operations
- ✅ **playwright** - Browser automation

---

## 🎯 Project Structure

```
/home/kc-palantir/math/
├── PROJECT_CONTEXT.md          # Full project overview
├── QUICKSTART.md               # This file
│
├── .claude/
│   ├── CLAUDE.md               # Claude config (v4.0)
│   └── memories/               # Local backup storage
│       └── phase-progress/     # Project-specific snapshots
│
├── agents/                     # Agent implementations (6 agents)
├── main.py                     # Entry point
└── tests/                      # Test files
```

---

## 🚀 Typical Session Flow

```
1. Open Claude Code in /home/kc-palantir/math

2. Start memory-keeper session
   → "Start memory-keeper session for math-system"

3. Load previous context
   → "Load latest context from memory-keeper"

4. Review current phase and tasks
   → Claude shows phase, completed, next

5. Start working
   → "Continue with next task"

6. At major milestones
   → "Save to memory-keeper: [milestone-name]"

7. If context reset (150K+ tokens)
   → Next message: Load from memory-keeper automatically

8. End session
   → Context persisted in SQLite, ready for next time
```

---

## 💡 Pro Tips

1. **Use memory-keeper for everything** - Persistent across ALL projects
2. **Categorize properly** - Makes retrieval much easier
3. **Set priorities** - High-priority items surface first
4. **Use channels** - Organize by topic/workflow
5. **Add tags & metadata** - Rich context for filtering
6. **Local files as backup** - Git-trackable snapshots
7. **Check token usage** - Ask Claude: "How many tokens?"

---

## 🆘 Troubleshooting

### Memory-Keeper Not Available
```bash
# Check MCP connection
claude mcp list | grep memory-keeper

# Should show: ✓ Connected
# If not, reinstall:
claude mcp add --scope user memory-keeper npx mcp-memory-keeper
```

### No Previous Context
```bash
# This is normal for first session
# Claude will start fresh and create new session
```

### Context Recovery Failed
```bash
# Fallback to local files
cat .claude/memories/phase-progress/current-state.json

# Or check PROJECT_CONTEXT.md
cat PROJECT_CONTEXT.md
```

---

## 📖 Documentation Index

- **PROJECT_CONTEXT.md** - Complete system architecture
- **.claude/CLAUDE.md** - Claude Sonnet 4.5 configuration (v4.0)
- **QUICKSTART.md** - This file (quick reference)
- **.claude/SESSION_RECOVERY.md** - Recovery procedures

---

## ✅ Checklist for New Session

- [ ] Start memory-keeper session (ask Claude)
- [ ] Load latest context (ask Claude)
- [ ] Review current phase and tasks
- [ ] Start working
- [ ] (Optional) Read PROJECT_CONTEXT.md for full context

---

**Memory System**: MCP Memory-Keeper (SQLite) + Local Files
**Primary Storage**: `~/.config/mcp-memory-keeper/context.db` (user-scope)
**Backup Storage**: `.claude/memories/phase-progress/` (project-scope)
**Token Budget**: 200K total

**Ready to work!** 🚀
