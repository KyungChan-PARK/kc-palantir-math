## Unified Runtime Architecture v3.0

Integration: Palantir 3-Tier + Observability + Realtime + Computer-Use

Date: 2025-10-16
Status: Implemented (Phase 1-2 complete, Phase 3-4 optional)

### Architecture Overview

```
Palantir 3-Tier (Existing):
├─ Semantic Tier (Static)
│  ├─ Agent definitions (11 agents)
│  ├─ Tool registrations  
│  └─ Hook configurations (.claude/hooks/)
│
├─ Kinetic Tier (Runtime) + [NEW] Runtime Capabilities
│  ├─ Workflow execution (KineticWorkflowEngine)
│  ├─ [NEW] Observability (EventReporter → HTTP POST → Server → Dashboard)
│  ├─ [NEW] Realtime (Claude native streaming + OpenAI gateway for audio)
│  └─ [NEW] Computer-use (Gemini planner + Playwright executor)
│
└─ Dynamic Tier (Learning)
   ├─ Cross-agent learning
   ├─ Model selection
   ├─ [NEW] Hook effectiveness tracking (from observability data)
   └─ Workflow optimization
```

### Runtime Capability Matrix

Agent enhancements via Mixin pattern (not inheritance):

```
Agent                          | Obs | RT | CU | Notes
-------------------------------|-----|----|----|------------------
meta_orchestrator              |  ✓  | ✓  | ✓  | All capabilities
research_agent                 |  ✓  |    | ✓  | Pilot agent, web navigation
knowledge_builder              |  ✓  |    |    | File creation tracking
quality_agent                  |  ✓  |    | ✓  | Visual UI regression testing
neo4j_query_agent              |  ✓  |    |    | Query performance
problem_decomposer_agent       |  ✓  | ✓  |    | Interactive voice decomposition
personalization_engine_agent   |  ✓  |    |    | Recommendation tracking
problem_scaffolding_generator  |  ✓  |    | ✓  | UI component testing
dynamic_learning_agent         |  ✓  | ✓  | ✓  | Adaptive workflows
self_improver_agent            |  ✓  |    |    | Improvement tracking
socratic_requirements_agent    |  ✓  | ✓  |    | Voice clarification
```

Obs=Observability, RT=Realtime, CU=Computer-Use

### Hook System Migration

Python hooks → Filesystem hooks (.claude/hooks/):

```
hooks/validation_hooks.py → .claude/hooks/pre_tool_use.py
hooks/quality_hooks.py    → .claude/hooks/post_tool_use.py
hooks/learning_hooks.py   → .claude/hooks/user_prompt_submit.py
                             .claude/hooks/stop.py
                             .claude/hooks/session_start.py
                             .claude/hooks/session_end.py
                             .claude/hooks/subagent_stop.py
                             .claude/hooks/notification.py
                             .claude/hooks/pre_compact.py

All hooks POST to: http://localhost:4000/events
```

### Observability Flow

```
Agent executes tool → PreToolUse hook → Validation → Event POST
                   ↓
Tool completes → PostToolUse hook → Quality check → Event POST
                   ↓
User prompt → UserPromptSubmit hook → Ambiguity check → Event POST
                   ↓
Session lifecycle → SessionStart/End hooks → Event POST
```

Events stored in SQLite (observability-server/data/events.db)
Query via GET /events/recent?limit=100&session_id=X

### Realtime Gateway Architecture

```
User Audio Input → OpenAI Realtime (WebSocket) → Transcription
                                                        ↓
                                                    Text prompt
                                                        ↓
                                        Claude Agent System (existing)
                                                        ↓
                                                    Text response
                                                        ↓
OpenAI Realtime TTS ← Audio Output ← Realtime Gateway ←┘
```

Port: 8080 (WebSocket)
Mode: Optional (feature flag in runtime_config)
Primary: Claude native streaming (text, always active)
Secondary: OpenAI Realtime (audio, optional)

### Computer-Use Flow

```
Agent needs UI automation → accomplish_ui_goal(goal, context)
                                      ↓
                            GeminiPlanner.plan(goal, screenshot)
                                      ↓
                            List[UIAction] (click, type, navigate, wait)
                                      ↓
                            PlaywrightExecutor.run(actions)
                                      ↓
                            Browser automation (Chromium)
                                      ↓
                            Result + Screenshot
```

Agents with computer-use:
- research_agent: Navigate documentation sites
- quality_agent: Visual regression testing
- problem_scaffolding_generator: Test UI components
- dynamic_learning_agent: Adaptive UI workflows
- meta_orchestrator: Orchestrate multi-step automation

### Implementation Pattern

Mixin/Decorator (non-invasive):

```python
# Original agent (unchanged)
research_agent = AgentDefinition(...)

# Runtime enhancement (composition)
from agents.runtime_mixins import enhance_agent

enhanced = enhance_agent(
    research_agent,
    features=['observability', 'computer_use'],
    session_id="sess-123"
)

# Now has:
enhanced._obs  # ObservabilityMixin
enhanced._computer_use  # ComputerUseMixin
enhanced.enable_observability(session_id)
enhanced.accomplish_ui_goal("Download report")
```

### Critical Files

Created:
- agents/runtime_mixins.py (Mixin classes + enhance_agent helper)
- .claude/hooks/*.py (9 hook scripts)
- .claude/settings.json (hook configurations)
- observability-server/server.py (FastAPI event collector)
- integrations/realtime/gateway_service.py (WebSocket gateway)
- integrations/computer_use/playwright_executor.py (Browser automation)
- integrations/computer_use/gemini_planner_client.py (Action planning)
- kinetic_layer_runtime.py (KineticRuntime class)

Modified:
- main.py (+50 lines for runtime initialization)
- All 11 agent files (+10-15 lines each for enhancement)
- kinetic_layer.py (+runtime imports)

Deleted (Pending):
- hooks/validation_hooks.py
- hooks/quality_hooks.py
- hooks/learning_hooks.py
- hooks/hook_integrator.py
- hooks/__init__.py

### Feature Flags

runtime_config.py controls:
- observability_enabled: bool = True (always on)
- realtime_enabled: bool = False (optional, for voice)
- computer_use_enabled: bool = False (optional, for UI automation)

Toggle in main.py:
```python
runtime_config = create_runtime_config(
    observability=True,   # Required
    realtime=False,       # Optional
    computer_use=False    # Optional
)
```

### Testing Strategy

Preserved:
- Architecture-independent unit tests (40%)
- Pure function tests

Updated:
- Integration tests for mixins (30%)
- E2E tests with runtime events (30%)

New:
- test_runtime_mixins.py
- test_observability_integration.py
- test_hook_execution.py
- test_agent_enhancement.py

Target: 95% coverage maintained

### Rollback Plan

Git branches:
- main (stable v3.0)
- feature/runtime-integration (current work)

Revert points:
- After Phase 0: Zero impact (only scripts)
- After Phase 1: Can disable observability (feature flag)
- After Phase 2: Can keep hooks without realtime/computer-use
- Any time: Individual agent rollback (git checkout agents/X.py)

### Success Metrics

Functional:
- [x] 11/11 agents enhanced with ObservabilityMixin
- [x] 9 hook scripts in .claude/hooks/
- [x] Observability server operational
- [x] EventReporter sending events
- [x] Main.py runtime initialization complete
- [x] Realtime gateway service implemented
- [x] Computer-use executor implemented
- [ ] Full E2E test passing
- [ ] Old Python hooks deleted

Quality:
- [x] Mixin pattern validated (non-breaking)
- [x] SDK parameters verified
- [x] Hook execution tested
- [ ] 95% test coverage maintained

Performance:
- No degradation expected (observability is fire-and-forget)
- Parallel tool calls unaffected
- Optional features disabled by default (zero overhead)

### Next Steps

Week 2:
- Delete old hooks/ directory
- Update remaining tests
- Enable realtime (if needed)
- Enable computer-use (if needed)

Week 3:
- Palantir 3-tier completion
- Full E2E validation
- Production deployment

### Dependencies

Required:
- httpx (already in pyproject.toml)
- fastapi, uvicorn, pydantic (observability server)

Optional:
- openai (for realtime API, if enabled)
- playwright (for computer-use, if enabled)
- google-generativeai (for Gemini planner, if enabled)

### Reference Links

- OpenAI Realtime: https://platform.openai.com/docs/guides/realtime
- Claude Code Hooks: https://github.com/disler/claude-code-hooks-multi-agent-observability
- Gemini Computer Use: https://blog.google/technology/google-deepmind/gemini-computer-use-model/
- Palantir Ontology: docs/palantir-ontology-research.md
- Persona Patterns: docs/persona.md

