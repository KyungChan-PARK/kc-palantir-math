# MCP Setup Guide

## ✅ MCP Configuration

This project uses **Model Context Protocol (MCP)** to enhance agent capabilities.

### Configuration File

**`.mcp.json`** (in project root, gitignored)

Defines 3 MCP servers:
1. **memory-keeper**: Persistent SQLite-based memory
2. **obsidian**: Custom Obsidian vault integration
3. **github**: GitHub API operations

### Environment Variables

**`.env`** (in project root, gitignored)

Required variables:
```bash
GITHUB_TOKEN=your_github_token
OBSIDIAN_API_KEY=your_obsidian_api_key
OBSIDIAN_API_URL=https://127.0.0.1:27124
```

## 🚀 Usage

### Start Agent System with MCP

```bash
cd /home/kc-palantir/math
uv run python main.py
```

**That's it!** The agent system will:
- Load MCP servers from `.mcp.json`
- Connect to memory-keeper, obsidian, github
- Make MCP tools available to all agents

### Available MCP Tools

When agents run, they have access to:

**Memory Keeper**:
- `mcp__memory-keeper__context_save`
- `mcp__memory-keeper__context_get`
- `mcp__memory-keeper__context_search`

**Obsidian**:
- Custom vault operations (see `tools/obsidian-mcp-server/`)

**GitHub**:
- Repository operations
- File management
- PR creation (used by self-improver agent)

## 📁 Project Structure

```
/home/kc-palantir/math/
├── .mcp.json                    # MCP server configuration (gitignored)
├── .env                         # API keys (gitignored)
├── main.py                      # Entry point - loads MCP
├── tools/
│   └── obsidian-mcp-server/     # Custom Obsidian MCP server
│       └── server.py
└── agents/                      # 9 specialized agents
    ├── meta_orchestrator.py
    ├── knowledge_builder.py
    └── ...
```

## 🔧 How It Works

1. **`main.py`** initializes `ClaudeSDKClient`
2. Loads `ClaudeAgentOptions` with `mcp_servers` from `.mcp.json`
3. Agent SDK spawns MCP server processes (`npx`, `uv run python`)
4. Agents can call MCP tools via `mcp__<server>__<tool>` format
5. MCP servers handle requests and return results

## 📝 Notes

- **No Cursor IDE configuration needed** - MCP works through Agent SDK
- **No manual MCP server management** - Agent SDK handles lifecycle
- **Environment variables required** - Set in `.env` file
- **Node.js required** - For `npx` MCP servers (memory-keeper, github)

## 🔒 Security

- `.mcp.json` and `.env` are in `.gitignore`
- Never commit API keys
- Use environment variables for all secrets

---

**Quick Start**: Just run `uv run python main.py` and MCP tools are ready! 🚀

