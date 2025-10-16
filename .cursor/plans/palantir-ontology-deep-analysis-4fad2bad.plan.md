<!-- 4fad2bad-da89-46ba-aa16-8416dbb28c0f 48566507-86ad-4ca5-af39-811a26b2438b -->
# Palantir 3-Tier Ontology Code-Level Enhancement Plan

## Analysis Summary

**Current State**: 85% complete, practically usable, 78% Palantir alignment

**Target State**: 95% complete, production-ready, Claude Code 2.0 best practices integrated

## Critical Fixes (Immediate - 30min)

### Fix 1: orchestrate_semantic 'tier' key

**File**: `agents/meta_orchestrator.py:1592-1681`

**Issue**: Missing 'tier' key causing test failures

**Action**: Add `"tier": "semantic"` to all return statements in orchestrate_semantic()

### Fix 2: Run remaining E2E tests

**Files**:

- `tests/test_2_kinetic_tier_e2e.py`
- `tests/test_3_dynamic_tier_e2e.py`
- `tests/test_4_cross_tier_integration_e2e.py`

**Action**: Execute with python3, fix any failures

### Fix 3: Migrate remaining 3 agents

**Files**:

- `agents/knowledge_builder.py`
- `agents/research_agent.py`
- `agents/quality_agent.py`

**Action**: Change `AgentDefinition` → `SemanticAgentDefinition`, add semantic metadata

## Claude Code 2.0 Integration (High Priority - 2h)

### Enhancement 1: Implement Hooks System (from docs)

**Based on**: claude-code-2-0.md lines 13743-15200, Multi-Agent Observability docs

**Files to create**:

- `.claude/hooks/pre_tool_validation.py`
- `.claude/hooks/post_tool_learning.py`
- `.claude/hooks/session_metrics.py`
- `.claude/settings.json` with hooks configuration

**Implementation**:

```python
# pre_tool_validation.py
#!/usr/bin/env python3
import json, sys
event = json.load(sys.stdin)
tool_name = event.get('tool_name')
tool_input = event.get('tool_input', {})

# Validate semantic tier immutability
if tool_name == 'Edit' and 'semantic_layer.py' in tool_input.get('file_path', ''):
    if 'SemanticRole' in tool_input.get('old_string', ''):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": "Modifying semantic tier enum - requires approval"
            }
        }))
        sys.exit(0)

# Detect tier violations
if tool_name == 'Task':
    subagent = tool_input.get('subagent_type', '')
    if 'semantic' in subagent and 'runtime' in tool_input.get('prompt', '').lower():
        print("Semantic tier should not handle runtime operations", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```



```python
# post_tool_learning.py
#!/usr/bin/env python3
import json, sys
from pathlib import Path
event = json.load(sys.stdin)

# Learn from tool usage for dynamic tier
if event.get('tool_name') == 'Task':
    result = event.get('tool_response', {})
    duration = result.get('duration_ms', 0)
    
    # Save to dynamic tier learning log
    log_file = Path.home() / '.claude/dynamic_learning.jsonl'
    with open(log_file, 'a') as f:
        learning = {
            "timestamp": event.get('timestamp'),
            "subagent": event.get('tool_input', {}).get('subagent_type'),
            "duration_ms": duration,
            "success": 'error' not in str(result).lower()
        }
        f.write(json.dumps(learning) + '\n')

sys.exit(0)
```

### Enhancement 2: Parallel Tool Calling Optimization

**Based on**: claude-code-2-0.md lines 25677-25680

**Files to modify**:

- `agents/meta_orchestrator.py` - Add parallel execution pattern to prompt
- `kinetic_layer.py:138-155` - Already implemented, enhance documentation

**Prompt addition**:

```
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

### Enhancement 3: Prompt Templates with {{variables}}

**Based on**: claude-code-2-0.md lines 25796-25840

**Files to create**:

- `tools/prompt_template_manager.py` (already planned in research doc)

**Enhancement**: Add {{variable}} support for agent prompts

```python
class PromptTemplateManager:
    def instantiate_template(self, template: str, variables: Dict[str, str]) -> str:
        """Fill {{variables}} in template."""
        result = template
        for var_name, var_value in variables.items():
            result = result.replace(f"{{{{{var_name}}}}}", var_value)
        return result
```

### Enhancement 4: Subagent Pattern Alignment

**Based on**: persona.md, claude-code-2-0.md lines 2091-2800

**Current**: Using `SemanticAgentDefinition` (custom)

**Claude Code**: Uses markdown files with YAML frontmatter

**Action**: Create converter to export agents as .claude/agents/*.md format for compatibility

**Files to create**:

- `tools/export_agents_to_claude_format.py`
```python
def export_agent_to_claude_format(agent: SemanticAgentDefinition, output_dir: Path):
    """Export SemanticAgentDefinition to .claude/agents/*.md format."""
    name = agent.name.replace('_', '-')
    tools_str = ', '.join(agent.tools) if hasattr(agent, 'tools') else ''
    
    content = f"""---
name: {name}
description: {agent.description}
tools: {tools_str}
model: sonnet
---

{agent.prompt}
"""
    
    output_path = output_dir / f"{name}.md"
    output_path.write_text(content)
```


### Enhancement 5: Extended Thinking Integration

**Based on**: claude-code-2-0.md lines 1200-1300, 25644-25654

**Files to modify**:

- `agents/meta_orchestrator.py` - Add thinking_budget configuration
- `agents/dynamic_learning_agent.py` - Use thinking for model selection

**Prompt enhancement**:

```
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

## Medium Priority Enhancements (4h)

### Enhancement 6: Observability Dashboard (from IndyDevDan)

**Based on**: Claude Code Hooks 기반 Multi-Agent Observability 상세.md

**Architecture**:

```
Claude Agents → Hook Scripts → HTTP POST → Server → SQLite → WebSocket → Dashboard
```

**Files to create**:

- `.claude/hooks/send_observability_event.py`
- `observability-server/enhanced/hooks_integration.ts`
- Dashboard already exists, enhance integration

### Enhancement 7: Memory Tool Integration

**Based on**: claude-code-2-0.md lines 24927-25375

**Purpose**: Replace partial memory-keeper with full memory tool

**Files to create**:

- `tools/memory_tool_adapter.py`
- `/memories/` directory structure

**Implementation**:

```python
class MemoryToolAdapter:
    """Adapter for Claude Code memory tool (memory_20250818)."""
    
    def view(self, path: str, view_range: Optional[tuple] = None):
        """View directory or file contents."""
        ...
    
    def create(self, path: str, file_text: str):
        """Create or overwrite file."""
        ...
    
    def str_replace(self, path: str, old_str: str, new_str: str):
        """Replace text in file."""
        ...
```

### Enhancement 8: Context Editing for Long Sessions

**Based on**: claude-code-2-0.md lines 16286-16960

**Purpose**: Handle context window limits automatically

**Files to modify**:

- `agents/meta_orchestrator.py` - Add context awareness prompt

**Prompt addition**:

```
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes.
```

### Enhancement 9: Semantic Pattern Validator

**Purpose**: Runtime validation of semantic patterns

**Files to create**:

- `semantic_pattern_validator.py`
```python
class SemanticPatternValidator:
    def validate_parallel_execution(self, workflow: WorkflowSpec) -> bool:
        """Ensure no shared mutable state in parallel tasks."""
        for step in workflow.steps:
            if step.parallel_group > 0:
                if self._has_shared_state(step):
                    raise PatternViolation(
                        "Parallel execution requires no shared mutable state"
                    )
        return True
    
    def validate_tier_boundaries(self, operation: str, source_tier: str):
        """Ensure tier operations follow ontology rules."""
        if source_tier == 'semantic' and 'runtime' in operation.lower():
            raise TierViolation("Semantic tier cannot perform runtime operations")
```


### Enhancement 10: Data Flow Detailed Tracking

**Purpose**: Enhanced kinetic tier data flow visibility

**Files to modify**:

- `kinetic_layer.py:250-351` - Enhance KineticDataFlowOrchestrator
```python
class DataFlowTracker:
    def track_lineage(self, data: Any, source: str, transformations: List[str]):
        """Track data origin and transformation history."""
        return {
            "data_id": hash(str(data)),
            "source_agent": source,
            "transformations": transformations,
            "timestamp": time.time()
        }
    
    def visualize_flow(self, session_id: str) -> str:
        """Generate mermaid diagram of data flows."""
        flows = self.get_flows_for_session(session_id)
        return self._generate_mermaid_graph(flows)
```


## Low Priority Polish (2h)

### Enhancement 11: Evolution Tracker Integration

**Files to modify**:

- `dynamic_layer_orchestrator.py:279-297`
- `agents/dynamic_learning_agent.py`

**Action**: Wire EvolutionTracker into DynamicTier.process_execution_results()

### Enhancement 12: Tier Contract Enforcement

**Files to create**:

- `tier_contract_validator.py`
```python
class TierContractValidator:
    ALLOWED_SEMANTIC_MODIFIERS = ['self-improver-agent', 'admin']
    
    def validate_semantic_modification(self, change: Dict) -> bool:
        """Only self-improver can modify semantic tier."""
        if change['tier'] == 'semantic':
            if change['source'] not in self.ALLOWED_SEMANTIC_MODIFIERS:
                raise TierViolation(
                    f"Semantic tier immutable except via {self.ALLOWED_SEMANTIC_MODIFIERS}"
                )
        return True
```


### Enhancement 13: Documentation Generation

**Files to create**:

- `CLAUDE-CODE-2-0-INTEGRATION.md` - Integration guide
- Architecture diagrams with mermaid

## Implementation Sequence

**Phase 1 (30min)**: Critical fixes

1. Fix orchestrate_semantic 'tier' key
2. Run all E2E tests
3. Migrate 3 remaining agents

**Phase 2 (2h)**: Claude Code 2.0 core integration

1. Implement hooks system (.claude/hooks/)
2. Add parallel tool calling prompts
3. Create prompt template manager
4. Export agents to .claude/agents/ format
5. Add extended thinking prompts

**Phase 3 (4h)**: Advanced features

1. Integrate observability hooks with existing dashboard
2. Implement memory tool adapter
3. Add context editing awareness
4. Create semantic pattern validator
5. Enhance data flow tracking

**Phase 4 (2h)**: Polish and documentation

1. Wire evolution tracker
2. Add tier contract validator
3. Generate documentation
4. Create architecture diagrams

## Success Metrics

- [ ] All E2E tests passing (60/60)
- [ ] Hooks system active (9 hook events)
- [ ] Parallel tool calling: 90%+ adoption
- [ ] Memory persistence across sessions
- [ ] Observability dashboard showing all tiers
- [ ] 15/15 agents with semantic metadata (100%)
- [ ] Tier contract violations: 0
- [ ] Context awareness prompts active

## Code-Level Actions (AI Executable)

**Immediate**:

```bash
# Fix 1
search_replace agents/meta_orchestrator.py old='return {"matches": matches, "count": len(matches)}' new='return {"tier": "semantic", "operation": "discover", "matches": matches, "count": len(matches)}'

# Fix 2  
python3 tests/test_2_kinetic_tier_e2e.py
python3 tests/test_3_dynamic_tier_e2e.py

# Fix 3
grep -l "AgentDefinition" agents/knowledge_builder.py agents/research_agent.py agents/quality_agent.py
```

**Hook System**:

```bash
mkdir -p .claude/hooks
write .claude/hooks/pre_tool_validation.py <FULL_IMPLEMENTATION>
write .claude/hooks/post_tool_learning.py <FULL_IMPLEMENTATION>
write .claude/settings.json <HOOK_CONFIG>
chmod +x .claude/hooks/*.py
```

**Parallel Execution**:

```bash
search_replace agents/meta_orchestrator.py old='# Meta-Orchestrator Logic Class' new='<use_parallel_tool_calls>\nIf you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel...\n</use_parallel_tool_calls>\n\n# Meta-Orchestrator Logic Class'
```

**Memory Tool**:

```bash
mkdir -p memories
write tools/memory_tool_adapter.py <FULL_IMPLEMENTATION>
```

**Pattern Validator**:

```bash
write semantic_pattern_validator.py <FULL_IMPLEMENTATION>
write tier_contract_validator.py <FULL_IMPLEMENTATION>
```

**Agent Export**:

```bash
mkdir -p .claude/agents
python3 -c "from tools.export_agents_to_claude_format import export_all_agents; export_all_agents()"
```

**Tests**:

```bash
python3 tests/test_week3_full_tier_integration.py
pytest tests/ -v --cov=agents --cov=hooks --cov-report=term-missing
```

## Evidence-Based Implementation

All enhancements based on:

1. PALANTIR-ONTOLOGY-ANALYSIS-REPORT.md findings
2. claude-code-2-0.md official documentation
3. persona.md subagent patterns
4. Multi-Agent Observability implementation guides
5. Current codebase analysis (80 Python files, 1,297 tier implementation lines)

## Post-Implementation Validation

```bash
# Verify hooks
python3 -c "import json; print(json.load(open('.claude/settings.json'))['hooks'])"

# Verify agents
ls -1 .claude/agents/*.md | wc -l  # Should be 15

# Verify tests
pytest tests/ -v | grep "PASSED" | wc -l  # Should be 60+

# Verify tier coordination
python3 -c "from agents.meta_orchestrator import MetaOrchestratorLogic; m=MetaOrchestratorLogic(); print(m.orchestrate_semantic('list_all'))"
```

### To-dos

- [ ] Fix orchestrate_semantic 'tier' key in meta_orchestrator.py
- [ ] Run test_2, test_3, test_4 kinetic/dynamic E2E tests
- [ ] Migrate knowledge_builder, research_agent, quality_agent to SemanticAgentDefinition
- [ ] Implement .claude/hooks system with pre/post tool validation and learning
- [ ] Add parallel tool calling optimization prompts to meta-orchestrator
- [ ] Implement prompt template manager with {{variable}} support
- [ ] Create tool to export agents to .claude/agents/*.md format
- [ ] Add extended thinking prompts for complex reasoning tasks
- [ ] Integrate hooks with existing observability dashboard
- [ ] Implement memory tool adapter for cross-session persistence
- [ ] Add context editing awareness prompts to meta-orchestrator
- [ ] Create semantic pattern validator for runtime validation
- [ ] Enhance kinetic data flow tracking with lineage and visualization
- [ ] Wire evolution tracker into dynamic tier processing
- [ ] Implement tier contract validator for boundary enforcement
- [ ] Run full test suite and verify all metrics