# Claude Sonnet 4.5 Implementation Standards

**Version**: 1.0.0  
**Last Updated**: 2025-10-15  
**Target Model**: claude-sonnet-4-5-20250929  
**Enforcement**: MANDATORY for ALL future work

---

## 🚨 CRITICAL: These Standards Are MANDATORY

This document defines **non-negotiable implementation standards** for ALL code in this project. Every agent, tool, script, or module MUST comply with these standards.

**When to apply:**
- ✅ Creating new agents
- ✅ Modifying existing agents
- ✅ Adding new features
- ✅ Refactoring code
- ✅ Fixing bugs
- ✅ ANY code changes

**No exceptions.** If code does not meet these standards, it is considered incomplete.

---

## Standard 1: Model Version Specification

### ✅ REQUIRED Implementation

**ALL agent definitions MUST use the specific model version:**

```python
# ✅ CORRECT: Specific version
model = "claude-sonnet-4-5-20250929"

# ❌ WRONG: Alias (NEVER USE)
model = "sonnet"
model = "claude-sonnet-4-5"
```

### 📋 Code-Level Requirements

#### For Agent SDK Definitions

**File Pattern:** `agents/*.py`

**Exact Implementation:**
```python
from claude_agent_sdk import AgentDefinition

# Every AgentDefinition MUST specify exact model version
agent_name = AgentDefinition(
    description="...",
    prompt="""...""",
    
    # MANDATORY: Use specific version, not alias
    model="claude-sonnet-4-5-20250929",  # ← REQUIRED
    
    tools=[...]
)
```

#### For Direct Anthropic API Usage

**File Pattern:** `*.py` (any file using Anthropic client)

**Exact Implementation:**
```python
from anthropic import Anthropic
import os

class YourClass:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # MANDATORY: Store specific version
        self.model = "claude-sonnet-4-5-20250929"  # ← REQUIRED
    
    def your_method(self):
        response = self.client.messages.create(
            model=self.model,  # Use stored version
            max_tokens=16_000,
            messages=[...]
        )
```

### 🔍 Verification Steps

**After ANY code change:**

1. **Search for aliases:**
   ```bash
   grep -r 'model.*=.*"sonnet"' agents/
   grep -r 'model.*=.*"claude-sonnet-4-5"' agents/
   ```
   
   **Expected result:** NO MATCHES

2. **CI Automated Verification:**
   ```yaml
   # .github/workflows/ci.yml automatically checks:
   # - No model aliases in agents/
   # - All agents use claude-sonnet-4-5-20250929
   # - Documentation exists and is up-to-date
   ```
   
   **CI will FAIL if:**
   - Any agent uses `model="sonnet"` alias
   - Missing CLAUDE-IMPLEMENTATION-STANDARDS.md
   - Missing .claude.md configuration

3. **Verify specific version:**
   ```bash
   grep -r 'model.*=.*"claude-sonnet-4-5-20250929"' agents/
   ```
   
   **Expected result:** ALL agent files appear

3. **Count occurrences:**
   ```bash
   grep -c "claude-sonnet-4-5-20250929" agents/*.py
   ```
   
   **Expected result:** At least 1 per agent file

### ❌ Common Mistakes to Avoid

```python
# ❌ WRONG: Using alias
model = "sonnet"

# ❌ WRONG: Incomplete version
model = "claude-sonnet-4-5"

# ❌ WRONG: Wrong model
model = "claude-opus-4-20250514"  # Unless specifically required

# ❌ WRONG: Hardcoded string in method
response = client.messages.create(
    model="sonnet",  # NO! Use specific version
    ...
)
```

### 📝 Files Requiring Updates

**Current files that MUST be updated:**
```
agents/meta_orchestrator.py         (line ~527)
agents/knowledge_builder.py         (line ~175)
agents/quality_agent.py              (line ~194)
agents/research_agent.py             (line ~228)
agents/example_generator.py          (line ~275)
agents/dependency_mapper.py          (line ~355)
agents/socratic_planner.py           (line ~362)
agents/socratic_mediator_agent.py    (line ~314)
agents/self_improver_agent.py        (line ~334)
agents/relationship_definer.py       (line ~57)

ALL test files in tests/ directory
```

---

## Standard 2: Extended Thinking

### ✅ REQUIRED Implementation

**ALL agents performing complex reasoning MUST enable Extended Thinking.**

### 📋 Code-Level Requirements

#### Determine If Agent Needs Extended Thinking

**Apply Extended Thinking if agent performs ANY of these:**
- ✅ Multi-step reasoning
- ✅ Complex task decomposition
- ✅ Root cause analysis
- ✅ Code generation/improvement
- ✅ Mathematical proofs
- ✅ Strategic planning
- ✅ Dependency graph construction
- ✅ Deep research synthesis

**Current agents requiring Extended Thinking:**
```
meta-orchestrator       → budget_tokens: 10_000  (complex orchestration)
socratic-mediator       → budget_tokens: 10_000  (root cause analysis)
self-improver           → budget_tokens: 10_000  (code improvement)
research-agent          → budget_tokens: 5_000   (deep research)
dependency-mapper       → budget_tokens: 5_000   (graph construction)
knowledge-builder       → budget_tokens: 3_000   (content generation)
example-generator       → budget_tokens: 3_000   (example creation)
quality-agent           → budget_tokens: 3_000   (validation logic)
socratic-planner        → budget_tokens: 5_000   (requirements analysis)
```

#### Option 1: Agent SDK Integration (Preferred)

**Check if Agent SDK supports `thinking` parameter:**

```python
from claude_agent_sdk import AgentDefinition

agent_name = AgentDefinition(
    description="...",
    prompt="""...""",
    model="claude-sonnet-4-5-20250929",
    
    # MANDATORY: Add Extended Thinking
    thinking={
        "type": "enabled",
        "budget_tokens": 10_000  # Adjust based on complexity
    },
    
    tools=[...]
)
```

**If Agent SDK does NOT support `thinking` parameter:**

Add explicit instruction in the agent prompt:

```python
agent_name = AgentDefinition(
    description="...",
    
    prompt="""You are an agent that performs complex reasoning.

## CRITICAL: Extended Thinking Mode

**You MUST use Extended Thinking for ALL tasks.**

This agent is configured to use Extended Thinking with a budget of 10,000 tokens.
Think deeply before responding:
1. Analyze the problem from multiple angles
2. Consider edge cases and alternatives
3. Plan your approach step-by-step
4. Validate your reasoning before finalizing

[rest of prompt...]
""",
    model="claude-sonnet-4-5-20250929",
    tools=[...]
)
```

#### Option 2: Direct Anthropic API (Fallback)

**For files using direct Anthropic API:**

```python
from anthropic import Anthropic
import os

class YourAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5-20250929"
        
        # MANDATORY: Define thinking configuration
        self.thinking_config = {
            "type": "enabled",
            "budget_tokens": 10_000  # Adjust based on agent complexity
        }
    
    def execute_task(self, task: str):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16_000,
            
            # MANDATORY: Include Extended Thinking
            thinking=self.thinking_config,  # ← REQUIRED
            
            messages=[
                {"role": "user", "content": task}
            ]
        )
        
        # MANDATORY: Handle both thinking and text blocks
        thinking_content = ""
        result_content = ""
        
        for block in response.content:
            if block.type == "thinking":
                thinking_content = block.thinking
            elif block.type == "text":
                result_content = block.text
        
        return {
            "thinking": thinking_content,
            "result": result_content
        }
```

### 🔍 Verification Steps

**After adding Extended Thinking:**

1. **Verify configuration exists:**
   ```bash
   # Check for thinking parameter in agent definitions
   grep -A 5 "thinking.*=" agents/*.py
   ```

2. **Test with sample task:**
   ```python
   # Run a test query
   result = agent.execute("Complex task requiring reasoning")
   
   # Verify thinking block exists
   assert "thinking" in result
   assert len(result["thinking"]) > 0
   ```

3. **Check response structure:**
   ```python
   # Verify response has both thinking and text
   for block in response.content:
       print(f"Block type: {block.type}")
   
   # Expected output:
   # Block type: thinking
   # Block type: text
   ```

### 📊 Budget Token Guidelines

**Use these values based on task complexity:**

```python
THINKING_BUDGET = {
    # Simple tasks (validation, simple queries)
    "simple": 1_000,
    
    # Standard tasks (most agent operations)
    "standard": 3_000,
    
    # Medium complexity (research, generation)
    "medium": 5_000,
    
    # Complex tasks (orchestration, root cause analysis)
    "complex": 10_000,
    
    # Very complex (deep mathematical proofs, extensive planning)
    "very_complex": 32_000,
}
```

**How to choose:**
- Default to `"standard"` (3,000) for new agents
- Use `"complex"` (10,000) for meta-orchestrator, mediator, improver
- Use `"medium"` (5,000) for research, dependency mapping
- Increase if agent frequently produces incomplete reasoning
- Decrease if agent finishes thinking well under budget

### ❌ Common Mistakes to Avoid

```python
# ❌ WRONG: No Extended Thinking configuration
agent = AgentDefinition(
    description="...",
    prompt="...",
    model="claude-sonnet-4-5-20250929",
    tools=[...]
    # Missing thinking parameter!
)

# ❌ WRONG: Budget too small
thinking={"type": "enabled", "budget_tokens": 100}  # Too small!

# ❌ WRONG: Budget exceeds max_tokens
max_tokens=4_000,
thinking={"type": "enabled", "budget_tokens": 10_000}  # Budget > max_tokens!

# ❌ WRONG: Not handling thinking block
response = client.messages.create(...)
print(response.content[0].text)  # Ignores thinking block!
```

### 📝 Implementation Checklist

**For EVERY agent:**

- [ ] Determine required budget_tokens based on task complexity
- [ ] Add `thinking` parameter to agent definition OR API call
- [ ] Ensure `max_tokens` > `budget_tokens`
- [ ] Handle both `thinking` and `text` blocks in response
- [ ] Test with complex task to verify thinking is used
- [ ] Document budget choice in code comments

---

## Standard 3: Prompt Caching

### ✅ REQUIRED Implementation

**ALL agents MUST implement Prompt Caching for static content.**

### 📋 Code-Level Requirements

#### Identify Cacheable Content

**Content is cacheable if:**
- ✅ It's static (doesn't change between requests)
- ✅ It's >= 1,024 tokens (Sonnet minimum)
- ✅ It's reused across multiple requests

**Common cacheable content:**
```
✅ System prompts (ALL agents have these)
✅ Tool definitions (static tool lists)
✅ Taxonomy/examples (relationship_definer.py)
✅ Validation rules (quality_agent)
✅ Research guidelines (research_agent)
✅ Orchestration patterns (meta_orchestrator)
```

#### Cache Tier Selection

**Choose cache tier based on update frequency:**

```python
CACHE_TIERS = {
    "5m": {
        "lifetime": "5 minutes",
        "use_for": "Frequently changing content (e.g., active experiments)",
        "price_multiplier": 1.25,
    },
    "1h": {
        "lifetime": "1 hour", 
        "use_for": "Stable content (e.g., system prompts, tool definitions)",
        "price_multiplier": 2.0,
    },
}

# Default: Use 1h tier for system prompts and tools
# Use 5m tier only if content changes frequently
```

#### Option 1: Agent SDK with cache_control (Preferred)

**If Agent SDK supports `cache_control` parameter:**

```python
from claude_agent_sdk import AgentDefinition

agent_name = AgentDefinition(
    description="...",
    
    # MANDATORY: Cache system prompt (1h tier)
    system=[
        {
            "type": "text",
            "text": """Your comprehensive system prompt here...
            
[This is typically 200-500 lines of instructions]
[Example: meta-orchestrator has ~500 lines = 5,000-7,000 tokens]
[ALL of this should be cached]
""",
            "cache_control": {"type": "ephemeral"}  # ← REQUIRED
        }
    ],
    
    model="claude-sonnet-4-5-20250929",
    
    thinking={
        "type": "enabled",
        "budget_tokens": 10_000
    },
    
    # MANDATORY: Cache tool definitions (1h tier)
    tools=[
        {
            "name": "Tool1",
            "description": "...",
            "input_schema": {...},
            "cache_control": {"type": "ephemeral"}  # ← REQUIRED (if supported)
        },
        # Or if tools is just a list of strings:
        'Read', 'Write', 'Edit',  # SDK may cache automatically
    ]
)
```

**If Agent SDK does NOT support `cache_control`:**

File an issue and use Option 2 for now.

#### Option 2: Direct Anthropic API (Fallback)

**For files using direct Anthropic API:**

```python
from anthropic import Anthropic
import os

class YourAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5-20250929"
        
        # MANDATORY: Load static content once (will be cached)
        self.system_prompt = self._build_system_prompt()
        self.tool_definitions = self._load_tool_definitions()
    
    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt (static content)"""
        # Load taxonomy, examples, guidelines
        taxonomy = self._load_taxonomy()  # Large static content
        examples = self._load_examples()  # Large static content
        
        return f"""You are a specialized agent...

## TAXONOMY
{taxonomy}

## EXAMPLES
{examples}

## GUIDELINES
[Detailed instructions...]
"""
    
    def execute_task(self, task: str):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16_000,
            
            thinking={
                "type": "enabled",
                "budget_tokens": 10_000
            },
            
            # MANDATORY: Cache system prompt (1h tier)
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"}  # ← REQUIRED
                }
            ],
            
            messages=[
                {"role": "user", "content": task}
            ]
        )
        
        # MANDATORY: Log cache performance
        self._log_cache_performance(response.usage)
        
        return self._parse_response(response)
    
    def _log_cache_performance(self, usage):
        """Log cache hits and savings"""
        cache_creation = getattr(usage, 'cache_creation_input_tokens', 0)
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        
        if cache_creation > 0:
            print(f"📝 Cache write: {cache_creation} tokens")
        
        if cache_read > 0:
            # Calculate savings (90% reduction on cache hits)
            savings = cache_read * 0.9 * 0.000003  # $3/MTok base price
            print(f"💾 Cache hit: {cache_read} tokens (saved ${savings:.4f})")
```

### 🔍 Verification Steps

**After implementing Prompt Caching:**

1. **Verify cache_control exists:**
   ```bash
   grep -r "cache_control" agents/
   grep -r "ephemeral" agents/
   ```
   
   **Expected result:** At least one cache_control per agent

2. **Test cache performance:**
   ```python
   # First call (cache write)
   response1 = agent.execute("Test query")
   assert response1.usage.cache_creation_input_tokens > 0
   
   # Second call (cache hit)
   response2 = agent.execute("Another query")
   assert response2.usage.cache_read_input_tokens > 0
   
   # Verify cost reduction
   cost1 = response1.usage.input_tokens * 0.000003
   cost2 = response2.usage.cache_read_input_tokens * 0.0000003
   assert cost2 < cost1 * 0.2  # At least 80% savings
   ```

3. **Monitor cache hit rate:**
   ```python
   # Add monitoring to track cache effectiveness
   total_requests = 100
   cache_hits = 95
   cache_hit_rate = cache_hits / total_requests
   
   # Expected: >80% cache hit rate after warmup
   assert cache_hit_rate > 0.8
   ```

### 📊 Cache Performance Targets

**Minimum acceptable performance:**

```python
CACHE_PERFORMANCE_TARGETS = {
    "cache_hit_rate": 0.80,  # 80% of requests should hit cache
    "cost_reduction": 0.85,  # 85% cost reduction on cached content
    "warmup_requests": 2,     # Cache becomes effective after 1-2 requests
}
```

### 💰 Cost Calculation Example

```python
# Example: meta-orchestrator with 5,000 token system prompt
# Scenario: 100 requests per day

# Without caching:
cost_per_request = 5_000 * 0.000003  # $0.015
daily_cost = cost_per_request * 100   # $1.50/day
monthly_cost = daily_cost * 30        # $45/month

# With caching:
first_request = 5_000 * 0.000006      # $0.030 (cache write, 1h tier)
remaining_99 = 99 * 5_000 * 0.0000003  # $0.149 (cache hits)
daily_cost_cached = (0.030 + 0.149)   # $0.179/day
monthly_cost_cached = 0.179 * 30      # $5.37/month

# Savings:
monthly_savings = 45 - 5.37           # $39.63/month per agent
yearly_savings = monthly_savings * 12  # $475.56/year per agent
total_savings = yearly_savings * 9    # $4,280.04/year (9 agents)
```

### ❌ Common Mistakes to Avoid

```python
# ❌ WRONG: No cache_control
system=[{"type": "text", "text": "Long prompt..."}]  # Not cached!

# ❌ WRONG: Caching dynamic content
system=[
    {
        "type": "text",
        "text": f"Current time: {datetime.now()}",  # Changes every request!
        "cache_control": {"type": "ephemeral"}
    }
]

# ❌ WRONG: Content too small to cache
system=[
    {
        "type": "text",
        "text": "Short prompt",  # < 1024 tokens, won't cache
        "cache_control": {"type": "ephemeral"}
    }
]

# ❌ WRONG: Not monitoring cache performance
response = client.messages.create(...)
# Should log cache_creation_input_tokens and cache_read_input_tokens!

# ❌ WRONG: Placing cache_control in wrong location
messages=[
    {
        "role": "user",
        "content": "Query",
        "cache_control": {"type": "ephemeral"}  # NO! User messages shouldn't be cached
    }
]
```

### 📝 Implementation Checklist

**For EVERY agent:**

- [ ] Identify all static content (system prompt, tools, taxonomy)
- [ ] Verify content is >= 1,024 tokens
- [ ] Add `cache_control: {"type": "ephemeral"}` to static content
- [ ] Choose cache tier (default: 1h for stability)
- [ ] Add cache performance logging
- [ ] Test cache hit on second request
- [ ] Verify cost reduction (>80%)
- [ ] Document cached sections in code comments

---

## Standard 4: 1M Context for Meta-Orchestrator

### ✅ REQUIRED Implementation

**The meta-orchestrator agent MUST have 1M context enabled.**

**Other agents:** Use default 200k context (sufficient for their tasks)

### 📋 Code-Level Requirements

#### Enable 1M Context for Meta-Orchestrator ONLY

**File:** `agents/meta_orchestrator.py`

**Option 1: Agent SDK Integration (Preferred)**

```python
from claude_agent_sdk import AgentDefinition

meta_orchestrator = AgentDefinition(
    description="...",
    prompt="""...""",
    model="claude-sonnet-4-5-20250929",
    
    thinking={
        "type": "enabled",
        "budget_tokens": 10_000
    },
    
    # MANDATORY: Enable 1M context for meta-orchestrator
    # Check if Agent SDK supports these parameters:
    max_context_tokens=1_000_000,  # If supported
    # OR
    anthropic_beta="context-1m-2025-08-07",  # Beta header
    
    tools=[...]
)
```

**Option 2: Direct API Configuration (Fallback)**

If Agent SDK doesn't support 1M context configuration, modify the SDK client initialization in `main.py`:

```python
# File: main.py

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def main():
    # ... existing code ...
    
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",  # Specific version
        permission_mode="acceptEdits",
        setting_sources=["project"],
        
        # MANDATORY: Enable 1M context for meta-orchestrator
        # If SDK supports extra_headers or anthropic_beta:
        extra_headers={
            "anthropic-beta": "context-1m-2025-08-07"  # ← REQUIRED for meta-orchestrator
        },
        # OR
        anthropic_beta="context-1m-2025-08-07",
        
        allowed_tools=[...],
        agents={
            "meta-orchestrator": meta_orchestrator,  # Gets 1M context
            # Other agents use default 200k
        },
        mcp_servers={}
    )
    
    async with ClaudeSDKClient(options=options) as client:
        # ... rest of code ...
```

**Option 3: Wrapper Function (Most Flexible)**

Create a wrapper for meta-orchestrator that forces 1M context:

```python
# File: agents/meta_orchestrator_wrapper.py

from anthropic import Anthropic
import os

class MetaOrchestratorWith1MContext:
    """
    Wrapper for meta-orchestrator that enforces 1M context window.
    
    MANDATORY: All meta-orchestrator calls MUST use this wrapper.
    """
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5-20250929"
        self.system_prompt = self._load_system_prompt()
    
    def execute(self, user_message: str, conversation_history: list = None):
        """
        Execute meta-orchestrator with 1M context enabled.
        
        Args:
            user_message: Current user query
            conversation_history: Full conversation history (can be very long)
        
        Returns:
            Response from meta-orchestrator
        """
        messages = conversation_history or []
        messages.append({"role": "user", "content": user_message})
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=64_000,  # Increased for 1M context
            
            # MANDATORY: Enable Extended Thinking
            thinking={
                "type": "enabled",
                "budget_tokens": 10_000
            },
            
            # MANDATORY: Enable 1M context (beta header)
            extra_headers={
                "anthropic-beta": "context-1m-2025-08-07"  # ← REQUIRED
            },
            
            # MANDATORY: Cache system prompt
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            
            messages=messages
        )
        
        # Log context usage
        self._log_context_usage(response.usage, len(messages))
        
        return response
    
    def _log_context_usage(self, usage, message_count):
        """Log context window usage"""
        total_input = usage.input_tokens
        print(f"📊 Context Usage:")
        print(f"   - Total input tokens: {total_input:,}")
        print(f"   - Messages in history: {message_count}")
        print(f"   - Context utilization: {total_input / 1_000_000 * 100:.1f}%")
        
        if total_input > 200_000:
            print(f"   ✅ Using >200k context (1M context required)")
```

### 🔍 Verification Steps

**After enabling 1M context:**

1. **Verify beta header is set:**
   ```bash
   grep -r "context-1m-2025-08-07" .
   ```
   
   **Expected result:** Found in meta-orchestrator configuration

2. **Test with large context:**
   ```python
   # Create a conversation with >200k tokens of history
   large_history = []
   for i in range(100):
       large_history.append({
           "role": "user",
           "content": "Process topology concepts..." + ("x" * 2000)
       })
       large_history.append({
           "role": "assistant",
           "content": "Processing..." + ("y" * 2000)
       })
   
   # Total: ~400k tokens
   response = meta_orchestrator.execute("Next task", large_history)
   
   # Should succeed without truncation errors
   assert response.stop_reason != "max_tokens"
   ```

3. **Monitor context usage:**
   ```python
   # After long conversation
   usage = response.usage
   print(f"Total input tokens: {usage.input_tokens}")
   
   # Should be able to use >200k without errors
   assert usage.input_tokens > 200_000  # Confirms 1M is active
   ```

### 📊 Context Usage Guidelines

```python
CONTEXT_USAGE_GUIDELINES = {
    "meta-orchestrator": {
        "context_window": 1_000_000,  # 1M tokens
        "typical_usage": 50_000,       # Most sessions
        "complex_workflow": 200_000,   # Multi-agent workflows
        "max_recommended": 800_000,    # Leave buffer for output
    },
    
    "other_agents": {
        "context_window": 200_000,     # Default
        "typical_usage": 10_000,       # Most tasks
        "max_recommended": 150_000,    # Leave buffer
    }
}
```

### ⚠️ Important Notes

**Why only meta-orchestrator needs 1M context:**

1. **Meta-orchestrator accumulates context:**
   - Multiple agent responses
   - Full conversation history
   - Task coordination state
   - Can easily exceed 200k in complex workflows

2. **Other agents are task-specific:**
   - research-agent: Single research task (~30k tokens)
   - knowledge-builder: Single file creation (~20k tokens)
   - quality-agent: Single file validation (~15k tokens)
   - All fit comfortably in 200k

3. **Cost optimization:**
   - 1M context has higher pricing for >200k tokens
   - Only enable where truly needed

### ❌ Common Mistakes to Avoid

```python
# ❌ WRONG: Enabling 1M for all agents
# This wastes cost and provides no benefit
all_agents = {
    "research-agent": research_agent,  # Doesn't need 1M
    "knowledge-builder": knowledge_builder,  # Doesn't need 1M
    # ...
}
# Don't apply 1M context globally!

# ❌ WRONG: Not setting beta header
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16_000,
    messages=[...]  # No beta header = only 200k context
)

# ❌ WRONG: Forgetting to increase max_tokens
extra_headers={"anthropic-beta": "context-1m-2025-08-07"},
max_tokens=4_096,  # Too small! Should be 64_000 for 1M context

# ❌ WRONG: Not monitoring context usage
# Should track when context exceeds 200k to verify 1M is working
```

### 📝 Implementation Checklist

**For meta-orchestrator:**

- [ ] Add beta header `context-1m-2025-08-07`
- [ ] Increase `max_tokens` to 64_000
- [ ] Add context usage logging
- [ ] Test with >200k token input
- [ ] Verify no truncation errors
- [ ] Document why 1M context is needed

**For all other agents:**

- [ ] Do NOT add 1M context beta header
- [ ] Keep default 200k context
- [ ] Verify tasks fit within 200k
- [ ] Document context requirements

---

## Standard 5: Streaming

### ✅ REQUIRED Implementation

**ALL user-facing interactions MUST use streaming responses.**

### 📋 Code-Level Requirements

#### Determine Where Streaming Is Required

**Streaming is MANDATORY for:**
- ✅ Main conversation loop (`main.py`)
- ✅ User-facing CLI/UI interactions
- ✅ Long-running agent responses (>5 seconds expected)
- ✅ Agents with Extended Thinking enabled (show reasoning process)

**Streaming is OPTIONAL for:**
- ⚠️ Internal agent-to-agent communication (Task calls)
- ⚠️ Short responses (<1000 tokens)
- ⚠️ Background/batch processing

#### Main Conversation Loop (MANDATORY)

**File:** `main.py`

**Current Implementation (NON-COMPLIANT):**
```python
# ❌ WRONG: Blocking response
await client.query(user_input)

async for message in client.receive_response():
    print(f"\n{message}")  # Waits for complete response
```

**REQUIRED Implementation:**

```python
# File: main.py (lines ~176-186)

import asyncio

async def main():
    # ... existing setup ...
    
    async with ClaudeSDKClient(options=options) as client:
        while True:
            user_input = input("\n\033[1;34mYou:\033[0m ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            # Generate trace_id
            query_trace_id = str(uuid.uuid4())[:8]
            logger.system_event("user_query_start", f"Processing query (trace_id: {query_trace_id})")
            
            try:
                # MANDATORY: Use streaming for user-facing responses
                print(f"\n\033[1;32mClaude:\033[0m ", end="", flush=True)
                
                # Check if SDK supports streaming
                if hasattr(client, 'stream_response'):
                    # ✅ CORRECT: Streaming with SDK
                    async with client.stream_response(user_input) as stream:
                        thinking_shown = False
                        
                        async for chunk in stream:
                            # Handle Extended Thinking output
                            if hasattr(chunk, 'type'):
                                if chunk.type == "thinking_delta":
                                    if not thinking_shown:
                                        print("\n🧠 [Thinking]", end=" ", flush=True)
                                        thinking_shown = True
                                    print(chunk.delta.thinking, end="", flush=True)
                                
                                elif chunk.type == "text_delta":
                                    if thinking_shown:
                                        print("\n\n📝 [Response]", end=" ", flush=True)
                                        thinking_shown = False
                                    print(chunk.delta.text, end="", flush=True)
                        
                        print()  # Newline after completion
                
                else:
                    # Fallback: If SDK doesn't support streaming, show warning
                    print("⚠️  Streaming not available, using blocking mode...")
                    await client.query(user_input)
                    async for message in client.receive_response():
                        print(message)
                
                query_success = True
                
            except Exception as e:
                logger.error("meta-orchestrator", type(e).__name__, str(e))
                print(f"\n❌ Error: {e}")
                query_success = False
            
            finally:
                # ... existing performance tracking ...
                pass
```

#### Direct Anthropic API Streaming (MANDATORY)

**For files using direct Anthropic API:**

```python
from anthropic import Anthropic
import os

class YourAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5-20250929"
    
    def execute_streaming(self, task: str):
        """
        Execute task with streaming output.
        
        MANDATORY for user-facing interactions.
        """
        # MANDATORY: Use streaming Messages API
        with self.client.messages.stream(
            model=self.model,
            max_tokens=16_000,
            
            # MANDATORY: Include Extended Thinking
            thinking={
                "type": "enabled",
                "budget_tokens": 10_000
            },
            
            # MANDATORY: Cache system prompt
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            
            # Enable 1M context if meta-orchestrator
            extra_headers=(
                {"anthropic-beta": "context-1m-2025-08-07"}
                if self.agent_name == "meta-orchestrator"
                else {}
            ),
            
            messages=[
                {"role": "user", "content": task}
            ]
        ) as stream:
            
            # MANDATORY: Handle all event types
            thinking_content = []
            result_content = []
            
            for event in stream:
                # Message start
                if event.type == "message_start":
                    print("🚀 Starting response...", flush=True)
                
                # Thinking block
                elif event.type == "content_block_start":
                    if event.content_block.type == "thinking":
                        print("\n🧠 [Claude is thinking...]", flush=True)
                
                # Thinking delta (chunky delivery)
                elif event.type == "content_block_delta":
                    if event.delta.type == "thinking_delta":
                        print(event.delta.thinking, end="", flush=True)
                        thinking_content.append(event.delta.thinking)
                    
                    elif event.delta.type == "text_delta":
                        print(event.delta.text, end="", flush=True)
                        result_content.append(event.delta.text)
                
                # Block completion
                elif event.type == "content_block_stop":
                    print()  # Newline
                
                # Message completion
                elif event.type == "message_stop":
                    print("\n✅ Response complete", flush=True)
            
            # Return complete response
            return {
                "thinking": "".join(thinking_content),
                "result": "".join(result_content),
                "usage": stream.get_final_message().usage
            }
    
    def execute_non_streaming(self, task: str):
        """
        Execute task without streaming.
        
        Use ONLY for internal agent calls or batch processing.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16_000,
            thinking={"type": "enabled", "budget_tokens": 10_000},
            system=[...],
            messages=[{"role": "user", "content": task}]
        )
        
        return self._parse_response(response)
```

### 🎨 Streaming Output Formatting

**REQUIRED format for user-facing output:**

```python
def format_streaming_output():
    """
    Format streaming output with visual indicators.
    
    MANDATORY for all user-facing streaming responses.
    """
    
    # Phase 1: Thinking (if Extended Thinking enabled)
    print("\n" + "="*60)
    print("🧠 Claude is thinking deeply about your request...")
    print("="*60)
    
    # Show thinking process in real-time
    # (This makes Extended Thinking transparent and educational)
    
    # Phase 2: Response
    print("\n" + "="*60)
    print("📝 Response:")
    print("="*60 + "\n")
    
    # Show actual response in real-time
    
    # Phase 3: Completion
    print("\n" + "="*60)
    print("✅ Complete")
    print("="*60)
```

**Example output:**

```
You: Analyze the prerequisite relationships for Fubini's Theorem

============================================================
🧠 Claude is thinking deeply about your request...
============================================================
Let me analyze this step by step...
First, I need to understand the formal statement...
This requires measure theory as a foundation...
We also need Lebesgue integration...
The conditions require σ-finite measures...

============================================================
📝 Response:
============================================================
Based on my analysis, here are the prerequisite relationships:

## Essential Prerequisites

1. **Measure Theory** (graduate level)
   - Relationship Type: Logical Prerequisite
   - Strength: Essential
   ...

============================================================
✅ Complete
============================================================
```

### 🔍 Verification Steps

**After implementing streaming:**

1. **Test user-facing interaction:**
   ```bash
   python main.py
   # Type a query
   # Observe: Should show thinking + response incrementally
   # NOT: Blank screen then sudden full response
   ```

2. **Verify event handling:**
   ```python
   # Log all event types
   event_types = []
   
   with client.messages.stream(...) as stream:
       for event in stream:
           event_types.append(event.type)
   
   # Expected event sequence:
   assert "message_start" in event_types
   assert "content_block_start" in event_types
   assert "content_block_delta" in event_types
   assert "message_stop" in event_types
   ```

3. **Test with Extended Thinking:**
   ```python
   # Verify thinking is streamed separately
   thinking_events = []
   text_events = []
   
   with client.messages.stream(..., thinking={...}) as stream:
       for event in stream:
           if event.type == "content_block_delta":
               if event.delta.type == "thinking_delta":
                   thinking_events.append(event)
               elif event.delta.type == "text_delta":
                   text_events.append(event)
   
   # Should have both thinking and text events
   assert len(thinking_events) > 0
   assert len(text_events) > 0
   ```

### ⚡ Performance Considerations

**Streaming characteristics:**

```python
STREAMING_PERFORMANCE = {
    "latency_to_first_token": "200-500ms",  # User sees output quickly
    "thinking_delivery": "Chunky (batches)",  # Not character-by-character
    "text_delivery": "Smooth",                # More consistent flow
    "total_time": "Same as non-streaming",    # Total time unchanged
    "perceived_speed": "Much faster",         # User sees progress immediately
}
```

**Handling delays:**

```python
async def stream_with_timeout(stream, timeout_seconds=30):
    """
    Handle streaming with timeout protection.
    
    MANDATORY for production use.
    """
    import asyncio
    
    start_time = asyncio.get_event_loop().time()
    last_event_time = start_time
    
    async for event in stream:
        current_time = asyncio.get_event_loop().time()
        
        # Check for stalls
        if current_time - last_event_time > timeout_seconds:
            print("\n⚠️  Stream stalled, reconnecting...")
            raise TimeoutError("Stream timeout")
        
        last_event_time = current_time
        yield event
```

### ❌ Common Mistakes to Avoid

```python
# ❌ WRONG: Not showing thinking process
for event in stream:
    if event.type == "content_block_delta":
        if event.delta.type == "thinking_delta":
            pass  # Ignoring thinking! Users want to see this!
        elif event.delta.type == "text_delta":
            print(event.delta.text, end="")

# ❌ WRONG: Not flushing output
print(event.delta.text, end="")  # Won't show until buffer fills!
# Should be:
print(event.delta.text, end="", flush=True)  # ✅ Shows immediately

# ❌ WRONG: Using streaming for internal agent calls
# Streaming adds complexity with no benefit for internal calls
async with client.stream_response(task) as stream:
    # This is agent-to-agent, should be non-streaming
    pass

# ❌ WRONG: Not handling all event types
for event in stream:
    print(event.delta.text)  # Will crash on non-text events!
# Should check event.type first

# ❌ WRONG: Not preserving full response
# Streaming means you need to accumulate chunks
for chunk in stream:
    print(chunk)  # Printed but not saved!
# Should save for logging/analysis

# ❌ WRONG: Blocking UI during streaming
# In GUI applications, streaming should run in background thread
response = await client.stream(...)  # Blocks UI thread!
# Should use async properly
```

### 📝 Implementation Checklist

**For main.py conversation loop:**

- [ ] Replace blocking `client.query()` with `client.stream_response()`
- [ ] Handle thinking_delta events separately from text_delta
- [ ] Add visual indicators (🧠, 📝, ✅)
- [ ] Flush output immediately (`flush=True`)
- [ ] Accumulate full response for logging
- [ ] Add timeout protection (30s)
- [ ] Test with Extended Thinking enabled
- [ ] Verify smooth user experience

**For direct API usage:**

- [ ] Use `client.messages.stream()` instead of `client.messages.create()`
- [ ] Handle all event types: message_start, content_block_start, content_block_delta, content_block_stop, message_stop
- [ ] Show thinking process to user
- [ ] Accumulate chunks into final response
- [ ] Log usage statistics from final message
- [ ] Add error handling for stream interruptions

---

## Integration Checklist

**Before ANY code change:**

- [ ] Read this standards document completely
- [ ] Identify which standards apply to your change
- [ ] Review code examples for each applicable standard

**During implementation:**

- [ ] Use specific model version `claude-sonnet-4-5-20250929`
- [ ] Enable Extended Thinking with appropriate budget
- [ ] Implement Prompt Caching for static content
- [ ] Enable 1M context for meta-orchestrator ONLY
- [ ] Use streaming for user-facing interactions
- [ ] Follow all code-level requirements exactly

**After implementation:**

- [ ] Run verification steps for each standard
- [ ] Test with real queries
- [ ] Monitor performance metrics
- [ ] Log cache performance
- [ ] Verify thinking is shown to users (if applicable)
- [ ] Document any deviations with justification

**For new agents:**

- [ ] Copy template from existing compliant agent
- [ ] Adjust thinking budget based on complexity
- [ ] Identify and cache static content
- [ ] Determine if streaming is needed
- [ ] Add comprehensive comments explaining each standard
- [ ] Test all standards are working

---

## Enforcement

### Code Review Requirements

**ALL pull requests MUST:**

1. ✅ Use specific model version `claude-sonnet-4-5-20250929`
2. ✅ Implement Extended Thinking (with justification if omitted)
3. ✅ Implement Prompt Caching for content >=1024 tokens
4. ✅ Use 1M context for meta-orchestrator only
5. ✅ Use streaming for user-facing interactions

**Reviewers MUST verify:**
- [ ] Model version is specific, not alias
- [ ] Extended Thinking configuration exists
- [ ] Cache_control is present for static content
- [ ] Meta-orchestrator has 1M context enabled
- [ ] User interactions use streaming
- [ ] Verification steps have been run
- [ ] Performance metrics show expected improvements

### Automated Checks

**Add to CI/CD pipeline:**

```bash
#!/bin/bash
# File: .github/workflows/standards-check.sh

echo "🔍 Checking Claude Implementation Standards..."

# Check 1: No model aliases
if grep -r 'model.*=.*"sonnet"' agents/; then
    echo "❌ FAIL: Found model alias 'sonnet'"
    echo "   Use: model=\"claude-sonnet-4-5-20250929\""
    exit 1
fi

# Check 2: Extended Thinking present
if ! grep -r "thinking.*=" agents/; then
    echo "⚠️  WARNING: No Extended Thinking configuration found"
    echo "   This may be intentional, but verify it's documented"
fi

# Check 3: Prompt Caching present
if ! grep -r "cache_control" agents/; then
    echo "❌ FAIL: No Prompt Caching implementation found"
    echo "   All agents must cache static content"
    exit 1
fi

# Check 4: Meta-orchestrator has 1M context
if ! grep -r "context-1m-2025-08-07" agents/meta_orchestrator.py; then
    echo "❌ FAIL: Meta-orchestrator missing 1M context configuration"
    exit 1
fi

# Check 5: Streaming in main.py
if ! grep -r "stream" main.py; then
    echo "❌ FAIL: No streaming implementation in main.py"
    exit 1
fi

echo "✅ All standards checks passed!"
```

### Exception Process

**If you MUST deviate from these standards:**

1. Document the reason in code comments:
   ```python
   # STANDARDS DEVIATION: Extended Thinking disabled
   # REASON: This agent performs only simple string matching
   # APPROVED BY: [Your Name] on [Date]
   # REVIEW DATE: [3 months from now]
   ```

2. Create a GitHub issue:
   - Title: "Standards Deviation: [Agent Name] - [Standard]"
   - Label: `standards-deviation`
   - Description: Full justification
   - Assignee: Tech lead for review

3. Add to exceptions registry:
   ```python
   # File: STANDARDS-EXCEPTIONS.md
   
   ## Active Exceptions
   
   ### simple-string-matcher agent - Extended Thinking
   - **Reason**: Agent only performs regex matching, no reasoning needed
   - **Approved**: 2025-10-15 by @username
   - **Review**: 2026-01-15
   - **Metrics**: No quality degradation observed
   ```

---

## Success Metrics

**After implementing all standards, expect:**

### Performance Metrics

```python
SUCCESS_METRICS = {
    "model_stability": {
        "version_consistency": 1.0,  # 100% consistent version
        "unexpected_behavior": 0,     # Zero version-related issues
    },
    
    "extended_thinking": {
        "quality_improvement": 0.30,  # 30%+ better on complex tasks
        "reasoning_depth": "visible",  # Users see thinking process
        "task_success_rate": 0.85,    # 85%+ success on first attempt
    },
    
    "prompt_caching": {
        "cache_hit_rate": 0.80,       # 80%+ requests hit cache
        "cost_reduction": 0.85,        # 85%+ cost savings on cached content
        "latency_reduction": 0.50,     # 50%+ faster on cache hits
    },
    
    "1m_context": {
        "meta_orchestrator_capacity": 1_000_000,  # Can handle 1M tokens
        "long_workflow_success": 1.0,  # No truncation errors
        "other_agents_context": 200_000,  # Still use efficient 200k
    },
    
    "streaming": {
        "time_to_first_token": "<1s",  # User sees output quickly
        "user_engagement": "high",      # Users appreciate transparency
        "perceived_performance": "+200%",  # Feels much faster
    }
}
```

### Cost Metrics

```python
COST_IMPACT = {
    "baseline_monthly_cost": 648.00,  # $648/month (8 agents, no optimizations)
    
    "with_prompt_caching": 410.00,    # $410/month (37% reduction)
    
    "with_extended_thinking": 420.00,  # $420/month (slight increase for quality)
    
    "net_monthly_cost": 410.00,       # $410/month final
    "monthly_savings": 238.00,         # $238/month saved
    "annual_savings": 2856.00,         # $2,856/year saved
    
    "quality_improvement": "+30-50%",  # Significant quality gains
    "user_satisfaction": "+80%",       # Better UX with streaming
}
```

---

## Quick Reference

### For Creating New Agents

```python
from claude_agent_sdk import AgentDefinition

new_agent = AgentDefinition(
    description="Clear agent purpose...",
    
    # ✅ Standard 1: Specific model version
    model="claude-sonnet-4-5-20250929",
    
    # ✅ Standard 2: Extended Thinking
    thinking={
        "type": "enabled",
        "budget_tokens": 5_000  # Adjust based on complexity
    },
    
    # ✅ Standard 3: Prompt Caching
    system=[
        {
            "type": "text",
            "text": """Your system prompt here...""",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    
    # ✅ Standard 4: 1M Context (only if meta-orchestrator)
    # Add in main.py SDK configuration
    
    tools=[
        # ✅ Standard 3: Cache tools if supported
        'Read', 'Write', 'Edit',
    ]
)

# ✅ Standard 5: Use streaming for user-facing calls
# Implement in main.py conversation loop
```

### For Modifying Existing Code

**Checklist:**
1. [ ] Update `model="sonnet"` → `model="claude-sonnet-4-5-20250929"`
2. [ ] Add `thinking={...}` parameter
3. [ ] Add `cache_control` to system prompt
4. [ ] Verify 1M context for meta-orchestrator
5. [ ] Convert blocking calls to streaming (if user-facing)
6. [ ] Run verification steps
7. [ ] Test with real queries
8. [ ] Monitor metrics

### For Testing

```python
# Test all standards at once
def test_agent_standards_compliance(agent):
    """Verify agent meets all implementation standards"""
    
    # Standard 1: Model version
    assert agent.model == "claude-sonnet-4-5-20250929"
    
    # Standard 2: Extended Thinking
    assert hasattr(agent, 'thinking')
    assert agent.thinking["type"] == "enabled"
    assert agent.thinking["budget_tokens"] >= 1_000
    
    # Standard 3: Prompt Caching
    assert any("cache_control" in str(s) for s in agent.system)
    
    # Standard 5: Streaming (for user-facing)
    if agent.is_user_facing:
        assert hasattr(agent, 'stream') or hasattr(agent, 'stream_response')
    
    # Standard 4: 1M Context (only meta-orchestrator)
    if agent.name == "meta-orchestrator":
        assert "context-1m" in str(agent.config)
```

---

## Version History

### v1.0.1 (2025-10-15)
- **CI Enforcement Added**: Automated standards checking in GitHub Actions
- **Model Version Fix**: Updated all 9 agents from `model="sonnet"` to `model="claude-sonnet-4-5-20250929"`
- **CI Workflow**: Simplified to validate, lint, and standards-check jobs
- **Verification**: CI now automatically blocks model alias usage

### v1.0.0 (2025-10-15)
- Initial standards document
- Defined 5 mandatory implementation standards
- Added code-level requirements and examples
- Created verification steps and checklists
- Established enforcement process

---

**END OF STANDARDS DOCUMENT**

**This document is MANDATORY for ALL future work.**

**No exceptions without documented approval.**

**Questions? See `.claude.md` for configuration details.**

