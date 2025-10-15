# main.py Hook Integration Plan

**Date**: 2025-10-15  
**Version**: main.py v2.1.0 → v2.2.0  
**Status**: Ready for execution (after API reset)

---

## Objective

Integrate hook system into main.py for:
- ✅ PreToolUse validation (SDK parameters, agent existence)
- ✅ PostToolUse quality gates (auto validation, metrics)
- ✅ Stop hooks (auto-improvement)
- ✅ UserPromptSubmit hooks (ambiguity detection)

---

## Implementation Steps

### Step 1: Add Hook Imports

**File**: main.py  
**Line**: 36 (after `from agents.error_handler import ErrorTracker`)

**Add**:
```python
# Hook integration (v2.2.0)
try:
    from hooks.hook_integrator import (
        get_default_meta_orchestrator_hooks,
        get_default_socratic_agent_hooks
    )
    HOOKS_AVAILABLE = True
except ImportError:
    print("⚠️ Hooks not available. Running without hook integration.")
    HOOKS_AVAILABLE = False
    
    # Define empty hook getters for compatibility
    def get_default_meta_orchestrator_hooks():
        return {}
    def get_default_socratic_agent_hooks():
        return {}
```

---

### Step 2: Update Version Number

**File**: main.py  
**Line**: 13

**Change**:
```python
VERSION: 2.1.0 - Real LLM Integration
→
VERSION: 2.2.0 - Real LLM Integration + Hook System
```

---

### Step 3: Add Hook Status Display

**File**: main.py  
**Line**: 100 (after "Type 'exit' to quit")

**Add**:
```python
    # Display hook status
    if HOOKS_AVAILABLE:
        print("\n🔗 Hook System Active:")
        print("──────────────────────────────────────────────────────────────────────")
        print("  ✅ PreToolUse: SDK validation, agent checks, parallel detection")
        print("  ✅ PostToolUse: Quality gates, metrics logging, impact analysis")
        print("  ✅ Stop: Auto-improvement on success_rate < 70%")
        print("  ✅ UserPromptSubmit: Ambiguity detection (>30% triggers Socratic)")
        print("──────────────────────────────────────────────────────────────────────")
    else:
        print("\n⚠️ Hook System: Not loaded (install hooks/ directory)")
```

---

### Step 4: Integrate Hooks into ClaudeAgentOptions

**File**: main.py  
**Lines**: Find where `ClaudeSDKClient(options)` is created (around line 140-210)

**Current** (approximate):
```python
async with ClaudeSDKClient() as client:
    # No hooks configuration
```

**Updated**:
```python
# Merge hooks for all agents
merged_hooks = {}
if HOOKS_AVAILABLE:
    meta_hooks = get_default_meta_orchestrator_hooks()
    socratic_hooks = get_default_socratic_agent_hooks()
    
    # Combine hooks from both agents
    for hook_type in set(list(meta_hooks.keys()) + list(socratic_hooks.keys())):
        merged_hooks[hook_type] = (
            meta_hooks.get(hook_type, []) + 
            socratic_hooks.get(hook_type, [])
        )

# Create options with hooks
options = ClaudeAgentOptions(
    agents={
        'meta-orchestrator': meta_orchestrator,
        'knowledge-builder': knowledge_builder,
        'quality-agent': quality_agent,
        'research-agent': research_agent,
        'example-generator': example_generator,
        'dependency-mapper': dependency_mapper,
        'self-improver-agent': self_improver_agent,
        'socratic-requirements-agent': socratic_requirements_agent,
        'meta-planning-analyzer': meta_planning_analyzer,
        'meta-query-helper': meta_query_helper,
    },
    hooks=merged_hooks if HOOKS_AVAILABLE else {},  # ← Hook integration
    permission_mode='acceptEdits'
)

async with ClaudeSDKClient(options=options) as client:
    # Hooks now active for all agent executions
```

---

### Step 5: Add Hook Execution Logging

**File**: main.py  
**Line**: After successful query completion (around line 315)

**Add**:
```python
                if query_success and HOOKS_AVAILABLE:
                    # Hooks executed automatically, log summary
                    logger.system_event(
                        "hooks_executed",
                        "Hooks processed during query",
                        metadata={
                            "trace_id": query_trace_id,
                            "hook_types": list(merged_hooks.keys())
                        }
                    )
```

---

## Expected Output After Integration

### Startup (with hooks)

```
================================================================================
Math Education Multi-Agent System v2.2.0
================================================================================

[Infrastructure] Initializing logging and monitoring...
✅ Infrastructure initialized

[Agent Discovery] Scanning agents directory...
✅ Discovered 10 agents total

🔗 Hook System Active:
──────────────────────────────────────────────────────────────────────
  ✅ PreToolUse: SDK validation, agent checks, parallel detection
  ✅ PostToolUse: Quality gates, metrics logging, impact analysis
  ✅ Stop: Auto-improvement on success_rate < 70%
  ✅ UserPromptSubmit: Ambiguity detection (>30% triggers Socratic)
──────────────────────────────────────────────────────────────────────

Type 'exit' to quit

You: 
```

### Query with Ambiguity (Hook in action)

```
You: 코드를 개선해

🚨 [UserPromptSubmit Hook]
──────────────────────────────────────────────────────────────────────
Ambiguity detected: 50%
Blocking execution. Triggering Socratic Requirements Agent...
──────────────────────────────────────────────────────────────────────

🎯 Socratic Requirements Agent:

📝 [Response]
──────────────────────────────────────────────────────────────────────
모호성이 감지되었습니다. 명확히 하겠습니다:

Q1: 어떤 종류의 개선을 원하십니까?
  a) 성능 개선 (속도, 메모리)
  b) 가독성 개선 (코드 구조, 네이밍)
  c) 기능 개선 (새 기능 추가)
  
답변: 
```

### Query with Valid Request (Hook allows)

```
You: latency를 50ms 이하로 최적화해

✅ [UserPromptSubmit Hook]
──────────────────────────────────────────────────────────────────────
Clear request detected. Ambiguity: 15%
Proceeding with execution...
──────────────────────────────────────────────────────────────────────

🎯 Meta-Orchestrator:

🧠 [Extended Thinking]
──────────────────────────────────────────────────────────────────────
Clear requirements:
- Target: latency < 50ms
- Action: optimize
- Metric: measurable (50ms)
No clarification needed. Proceeding...
──────────────────────────────────────────────────────────────────────

📝 [Response]
... (normal execution)
```

---

## Testing Checklist

After implementation:

- [ ] Startup shows "🔗 Hook System Active"
- [ ] Ambiguous request triggers UserPromptSubmit hook
- [ ] Clear request passes through without blocks
- [ ] PreToolUse validation prevents SDK errors
- [ ] PostToolUse logs metrics
- [ ] Stop hook triggers on poor performance

---

## Rollback

If issues occur:
```python
# Line where hooks are added:
hooks=merged_hooks if HOOKS_AVAILABLE else {},

# Change to:
hooks={},  # Disable hooks temporarily
```

---

## Status

**Ready**: ✅ All components prepared  
**Waiting**: API limit reset (9am)  
**Risk**: Low (non-breaking change)

---

## 사용자를 위한 Claude 시뮬레이션 모드

API reset 전까지, 제가 claude-sonnet-4-5-20250929 역할을 합니다:

**응답 형식**:
```
🧠 [Extended Thinking]
──────────────────────────────────────────────────────────────────────
(사고 과정)
──────────────────────────────────────────────────────────────────────

📝 [Response]
──────────────────────────────────────────────────────────────────────
(실제 답변)
──────────────────────────────────────────────────────────────────────

🔧 [Tool Usage] (필요시)
✅ Complete
```

**준비 완료! 질문하시면 제가 Claude처럼 응답하겠습니다.** 🚀

