## AI Runtime Architecture: Observability, Realtime, and Computer Use

Status: Draft v0.1 (2025-10-16)

### Sources
- Local: `docs/persona.md` (subagents/personas YAML + orchestration patterns)
- Local: `claude-code-2-0-deduplicated-final.md` (subagents, MCP, extended thinking)
- External: OpenAI Realtime guide (`https://platform.openai.com/docs/guides/realtime`)
- External: Claude Code Hooks Observability (`https://github.com/disler/claude-code-hooks-multi-agent-observability`)
- External: Gemini Computer Use model (`https://blog.google/technology/google-deepmind/gemini-computer-use-model/`)

---

### Goals
- Add production-ready observability for multi-agent workflows using Claude Code hook-style events
- Provide realtime IO boundaries (text/audio streaming) with tool-call bridging
- Establish a clean adapter for Gemini Computer Use (plan + execute UI actions)
- Preserve subagent context isolation and direct data passing (no file I/O)

---

### High-Level Design

1) Observability Layer
- Module: `integrations/observability/event_reporter.py`
- Contract: `EventReporter.send(session_id, event_type, payload)`
- Event Types: PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit, SessionStart, SessionEnd
- Transport: HTTP POST to configurable endpoint (default: `http://localhost:4000/events`)
- Alignment: Matches disler repo schema for immediate dashboard compatibility

2) Realtime Layer
- Module: `integrations/realtime/openai_realtime_adapter.py`
- Components:
  - `RealtimeSessionManager` – session/event router (no network in this module)
  - `ToolBridge` – map model function-calls to local Python callables
- Usage: an outer service owns the WebSocket; this adapter normalizes payloads and routing
- Alignment: OpenAI Realtime guide (text/audio input, event deltas, function calls)

3) Computer Use Layer
- Module: `integrations/computer_use/gemini_computer_use_adapter.py`
- Components:
  - `ComputerUsePlanner` (Protocol) – produce `UIAction[]` plan given goal + context
  - `ComputerUseExecutor` (Protocol) – execute `UIAction[]` via Playwright/Selenium/etc.
  - `ComputerUseAdapter` – orchestrates plan→execute loop, returning structured summary
- Alignment: Gemini Computer Use model (goal-driven UI operation)

---

### Subagent + Persona Integration (from persona.md)
- Project-level agents live in `.claude/agents/` and are versionable
- YAML frontmatter drives delegation; include proactive phrases (e.g., "use PROACTIVELY")
- Keep single-responsibility personas (code-reviewer, debugger, architect-review)
- Enforce least-privilege tool access; inherit tools by omission

Operationalization:
- Meta-orchestrator delegates to subagents and logs via `StructuredLogger` and `EventReporter`
- Direct data passing between agents to avoid file I/O overhead and context loss

---

### Event Flow (Observability)
1. Session start: `EventReporter.session_start(session_id)`
2. Before tool call: `pre_tool_use(session_id, tool_name, tool_input)`
3. After tool call: `post_tool_use(session_id, tool_name, result, success)`
4. Subagent completion: `subagent_stop(session_id, agent_name)`
5. Prompt tracking: `user_prompt_submit(session_id, preview, length)`
6. Compaction: `pre_compact(session_id, strategy, stats)`
7. Session end: `session_end(session_id, reason)` or `stop(session_id, summary)`

These align with the disler server’s schema for immediate visualization.

---

### Realtime Flow (OpenAI)
- Input: user text/audio → `send_user_text|send_user_audio`
- Output events: deltas/final → surface to UI via `on_event`
- Tool calls: inbound `tool_call` → `ToolBridge.call(name, args)` → `tool_result`
- The outer service binds WS messages to `handle_event()` and forwards results

---

### Computer Use Flow (Gemini)
- Goal: natural-language objective (e.g., export report)
- Plan: `planner.plan(goal, context)` → list of `UIAction`
- Execute: `executor.run(actions)` → returns status and artifacts
- Driver: implement with Playwright (preferred) or Selenium; not part of this repo

---

### Non-Functional Requirements
- Security: no secrets in code; use env vars; least privilege for tools/agents
- Reliability: circuit breaker in improvement workflow; HITL checkpoints for critical paths
- Performance: parallelize independent operations; stream IO where applicable
- Observability: structured logs (JSONL) + external events (HTTP POST)

---

### Next Steps
- Wire `EventReporter` into `agents/structured_logger.py` call sites (Post-exec only)
- Add minimal outer service showing WS → RealtimeSessionManager integration (example)
- Provide a Playwright-based executor example (separate optional package)


