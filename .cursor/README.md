# Cursor IDE Configuration

This directory contains Cursor IDE-specific configuration files.

## MCP Server Configuration

**File**: `mcp_settings.json`

This file configures MCP (Model Context Protocol) servers for Cursor IDE.

### How to Enable MCP Servers in Cursor

#### Method 1: Via Cursor Settings UI

1. Open Cursor Settings:
   - `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac)
   - Or: `File → Preferences → Settings`

2. Search for "MCP" in settings

3. Click "Edit in settings.json"

4. Add MCP server configuration from `.cursor/mcp_settings.json`

#### Method 2: Manual Configuration

**Global MCP Settings Location**:

- **Windows**: `%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

**Copy the contents of `.cursor/mcp_settings.json` to the global settings file.**

#### Method 3: Project-Level Settings (Recommended)

Cursor automatically detects `.cursor/mcp_settings.json` in the project root.

**Steps**:
1. Ensure `.cursor/mcp_settings.json` exists (already created)
2. Restart Cursor IDE
3. MCP servers should appear in Cursor's MCP panel

### Configured MCP Servers

1. **memory-keeper**
   - Purpose: SQLite-based persistent memory
   - Command: `npx -y mcp-memory-keeper`
   - Status: Enabled

2. **sequential-thinking**
   - Purpose: Step-by-step reasoning for complex tasks
   - Command: `npx -y @modelcontextprotocol/server-sequential-thinking`
   - Status: Enabled

3. **github**
   - Purpose: GitHub API integration
   - Command: `npx -y @modelcontextprotocol/server-github`
   - Status: Enabled
   - Requires: `GITHUB_PERSONAL_ACCESS_TOKEN`

4. **brave-search** (Optional)
   - Purpose: Web search capabilities
   - Command: `npx -y @modelcontextprotocol/server-brave-search`
   - Status: Disabled (no API key)
   - Requires: `BRAVE_API_KEY`

### Verification

After configuring MCP servers:

1. **Check MCP Panel in Cursor**:
   - Look for MCP icon in Cursor sidebar
   - Should show list of available MCP servers

2. **Test MCP Tools**:
   ```
   Ask Claude: "What MCP tools are available?"
   ```

3. **Check Logs**:
   - Cursor logs: `Help → Toggle Developer Tools → Console`
   - Look for MCP server initialization messages

### Troubleshooting

#### "No MCP tools" in Cursor Settings

**Possible causes**:
1. MCP servers not installed
2. Configuration file not in correct location
3. Cursor needs restart
4. Node.js/npx not available in PATH

**Solutions**:

1. **Install Node.js** (if not installed):
   ```bash
   # Check if node/npx is available
   node --version
   npx --version
   ```

2. **Manually test MCP servers**:
   ```bash
   # Test memory-keeper
   npx -y mcp-memory-keeper

   # Test sequential-thinking
   npx -y @modelcontextprotocol/server-sequential-thinking

   # Test github (requires token)
   GITHUB_PERSONAL_ACCESS_TOKEN=your_token npx -y @modelcontextprotocol/server-github
   ```

3. **Restart Cursor IDE**:
   - Close all Cursor windows
   - Reopen project
   - Check MCP panel again

4. **Check Cursor version**:
   - MCP support requires Cursor >= 0.40.0
   - Update Cursor if needed

#### MCP Servers Not Starting

**Check logs**:
```bash
# Cursor logs location
# Windows: %APPDATA%\Cursor\logs
# macOS: ~/Library/Logs/Cursor
# Linux: ~/.config/Cursor/logs

# Look for MCP-related errors
tail -f ~/.config/Cursor/logs/main.log | grep -i mcp
```

**Common issues**:
- Missing `npx` in PATH
- Network issues (downloading MCP packages)
- Permission errors
- Port conflicts

### Security Notes

⚠️ **API Keys**: 
- Never commit API keys to git
- Use environment variables when possible
- Rotate keys regularly

**Current configuration**:
- GitHub token is hardcoded (should use env var)
- Brave API key is empty (disabled)

**Recommended**:
```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Then set environment variable:
```bash
export GITHUB_TOKEN=your_token_here
```

### Related Documentation

- **MCP-USAGE-GUIDE.md**: Comprehensive MCP tool usage guide
- **.mcp.json**: Agent SDK MCP configuration (different from Cursor)
- **main.py**: Agent SDK MCP initialization

---

**Last Updated**: 2025-10-15

