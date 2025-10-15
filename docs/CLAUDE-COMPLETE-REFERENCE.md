# Claude Complete Reference - Comprehensive Technical Documentation

**Source:** https://docs.claude.com (All major pages crawled)  
**Extracted:** 2025-10-14  
**Purpose:** Complete technical specification for Claude Sonnet 4.5, Sonnet 4, and Sonnet 3.7

---

## Table of Contents

1. [Model Specifications](#model-specifications)
2. [Extended Thinking](#extended-thinking)
3. [Prompt Caching](#prompt-caching)
4. [Context Windows](#context-windows)
5. [Context Editing](#context-editing)
6. [Tool Use](#tool-use)
7. [Streaming](#streaming)
8. [Vision](#vision)
9. [PDF Support](#pdf-support)
10. [Rate Limits](#rate-limits)
11. [API Reference](#api-reference)
12. [Best Practices](#best-practices)

---

## Model Specifications

### Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

```python
SONNET_4_5 = {
    "model_id": "claude-sonnet-4-5-20250929",
    "alias": "claude-sonnet-4-5",
    "release_date": "2025-09-29",
    
    # Platform IDs
    "aws_bedrock": "anthropic.claude-sonnet-4-5-20250929-v1:0",
    "gcp_vertex": "claude-sonnet-4-5@20250929",
    
    # Description
    "tagline": "Our best model for complex agents and coding",
    "strengths": "Highest intelligence across most tasks with exceptional agent and coding capabilities",
    
    # Capabilities
    "multilingual": True,
    "vision": True,
    "extended_thinking": True,
    "priority_tier": True,
    "prompt_caching": True,
    "context_editing": True,
    "streaming": True,
    "batch_processing": True,
    "citations": True,
    "pdf_support": True,
    
    # Context & Output
    "context_window_default": 200_000,
    "context_window_beta_1m": 1_000_000,  # with beta header
    "max_output": 64_000,
    
    # Knowledge
    "reliable_knowledge_cutoff": "2025-01",
    "training_data_cutoff": "2025-07",
    
    # Performance
    "latency": "Fast",
    
    # Pricing (USD per million tokens)
    "pricing": {
        "base_input": 3.00,
        "cache_write_5m": 3.75,
        "cache_write_1h": 6.00,
        "cache_hit_refresh": 0.30,
        "output": 15.00
    },
    
    # Beta Features
    "beta_headers": {
        "1m_context": "context-1m-2025-08-07",
        "context_management": "context-management-2025-06-27"
    },
    
    # Key Improvements over Sonnet 4
    "improvements": {
        "coding": {
            "swe_bench_verified": "Advanced state-of-the-art on coding benchmarks",
            "planning": "Enhanced planning and system design",
            "security": "Improved security engineering",
            "instruction_following": "Better instruction following"
        },
        "agent_capabilities": {
            "autonomous_operation": "Can work independently for hours",
            "context_awareness": "Tracks token usage throughout conversations",
            "tool_usage": "More effective parallel tool calls",
            "context_management": "Advanced state tracking in external files"
        },
        "communication": {
            "style": "Concise, direct, and natural",
            "updates": "Fact-based progress updates",
            "summaries": "May skip verbose summaries (configurable)"
        },
        "creative": {
            "presentations": "Matches/exceeds Claude Opus 4.1",
            "flair": "Polished, professional output",
            "first_try": "Usable content in initial attempts"
        }
    },
    
    # Important Notes
    "notes": {
        "extended_thinking": "Performs significantly better with extended thinking enabled for coding",
        "context_awareness": "Receives token usage updates after each tool call",
        "production": "Use specific version (not alias) for consistent behavior"
    }
}
```

### Claude Sonnet 4 (claude-sonnet-4-20250514)

```python
SONNET_4 = {
    "model_id": "claude-sonnet-4-20250514",
    "alias": "claude-sonnet-4-0",
    "release_date": "2025-05-14",
    
    "aws_bedrock": "anthropic.claude-sonnet-4-20250514-v1:0",
    "gcp_vertex": "claude-sonnet-4@20250514",
    
    "tagline": "High-performance model",
    "strengths": "High intelligence and balanced performance",
    
    "multilingual": True,
    "vision": True,
    "extended_thinking": True,
    "priority_tier": True,
    "prompt_caching": True,
    
    "context_window_default": 200_000,
    "context_window_beta_1m": 1_000_000,
    "max_output": 64_000,
    
    "reliable_knowledge_cutoff": "2025-01",
    "training_data_cutoff": "2025-03",
    
    "latency": "Fast",
    
    "pricing": {
        "base_input": 3.00,
        "cache_write_5m": 3.75,
        "cache_write_1h": 6.00,
        "cache_hit_refresh": 0.30,
        "output": 15.00
    }
}
```

### Claude Sonnet 3.7 (claude-3-7-sonnet-20250219)

```python
SONNET_3_7 = {
    "model_id": "claude-3-7-sonnet-20250219",
    "alias": "claude-3-7-sonnet-latest",
    "release_date": "2025-02-19",
    
    "aws_bedrock": "anthropic.claude-3-7-sonnet-20250219-v1:0",
    "gcp_vertex": "claude-3-7-sonnet@20250219",
    
    "tagline": "High-performance model with early extended thinking",
    "strengths": "High intelligence with toggleable extended thinking",
    
    "multilingual": True,
    "vision": True,
    "extended_thinking": True,
    "priority_tier": True,
    "prompt_caching": True,
    
    "context_window": 200_000,
    "max_output_default": 64_000,
    "max_output_beta_128k": 128_000,  # with beta header
    
    "reliable_knowledge_cutoff": "2024-10",
    "training_data_cutoff": "2024-11",
    
    "latency": "Fast",
    
    "pricing": {
        "base_input": 3.00,
        "cache_write_5m": 3.75,
        "cache_write_1h": 6.00,
        "cache_hit_refresh": 0.30,
        "output": 15.00
    },
    
    "beta_headers": {
        "128k_output": "output-128k-2025-02-19"
    },
    
    "notes": {
        "full_thinking": "Returns full thinking output (not summarized like Claude 4 models)",
        "128k_output": "Use streaming Messages API to avoid timeouts with 128k output"
    }
}
```

---

## Extended Thinking

### Overview

```python
EXTENDED_THINKING = {
    "description": "Allows Claude to engage in deliberate, in-depth reasoning before responding",
    "supported_models": [
        "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219",
        "claude-opus-4-1-20250805",
        "claude-opus-4-20250514"
    ],
    "not_supported": [
        "claude-3-5-haiku-20241022",
        "claude-3-haiku-20240307"
    ]
}
```

### Configuration

```python
# Basic Configuration
THINKING_CONFIG = {
    "type": "enabled",  # or "disabled"
    "budget_tokens": 10_000  # max tokens for thinking (must be < max_tokens)
}

# Example API Request
REQUEST = {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 16_000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10_000
    },
    "messages": [
        {"role": "user", "content": "Complex problem..."}
    ]
}
```

### Summarized Thinking (Claude 4 Models)

```python
SUMMARIZED_THINKING = {
    "applies_to": [
        "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-20250514",
        "claude-opus-4-1-20250805",
        "claude-opus-4-20250514"
    ],
    "behavior": {
        "output": "Returns summary of full thinking process",
        "billing": "Charged for FULL thinking tokens, not summary tokens",
        "token_mismatch": "Billed output count != visible response tokens",
        "verbosity": "First few lines more verbose (helpful for prompt engineering)",
        "preservation": "Key ideas preserved with minimal latency",
        "processing": "Summarized by different model than target model"
    },
    "exception": {
        "claude_3_7": "Returns full thinking output (no summarization)"
    },
    "full_access": "Contact sales@anthropic.com for full thinking output"
}
```

### Budget Token Guidelines

```python
BUDGET_RECOMMENDATIONS = {
    "small_tasks": 1_000,      # Quick reasoning
    "medium_tasks": 10_000,     # Standard complex problems
    "large_tasks": 32_000,      # Very complex analysis
    "note": "Claude may not use entire budget, especially above 32k",
    "limit": "Must be less than max_tokens",
    "interleaved_exception": "Can exceed when using interleaved thinking with tools (up to 200k)"
}
```

### Streaming Thinking

```python
STREAMING_THINKING = {
    "enabled": True,
    "event_type": "thinking_delta",
    "behavior": "Chunky delivery pattern (batches for optimal performance)",
    "delays": "Possible delays between streaming events (being improved)",
    
    "response_structure": [
        {"event": "message_start", "type": "message_start"},
        {"event": "content_block_start", "type": "thinking"},
        {"event": "content_block_delta", "type": "thinking_delta"},
        # ... more thinking deltas
        {"event": "content_block_delta", "type": "signature_delta"},
        {"event": "content_block_stop"},
        {"event": "content_block_start", "type": "text"},
        {"event": "content_block_delta", "type": "text_delta"},
        # ... more text deltas
        {"event": "content_block_stop"},
        {"event": "message_delta"},
        {"event": "message_stop"}
    ]
}
```

### Tool Use with Extended Thinking

```python
TOOL_USE_LIMITATIONS = {
    "supported_tool_choice": [
        {"type": "auto"},  # default
        {"type": "none"}
    ],
    "unsupported_tool_choice": [
        {"type": "any"},  # ERROR
        {"type": "tool", "name": "..."}  # ERROR
    ],
    "thinking_block_preservation": {
        "requirement": "Must pass thinking blocks back to API",
        "format": "Include complete unmodified block",
        "purpose": "Maintain reasoning continuity"
    }
}
```

### Best Practices

```python
EXTENDED_THINKING_BEST_PRACTICES = {
    "when_to_enable": [
        "Complex coding tasks",
        "Multi-step reasoning problems",
        "Mathematical proofs",
        "Strategic planning",
        "Complex analysis tasks"
    ],
    "sonnet_4_5_coding": "Performs significantly better with extended thinking enabled",
    "budget_sizing": "Start with 10k, increase for complex tasks",
    "production": "Test with and without to verify benefit vs. cost",
    "interleaved_thinking": "Use for long-running agent tasks requiring sustained reasoning"
}
```

---

## Prompt Caching

### Overview

```python
PROMPT_CACHING = {
    "description": "Reduces latency and costs by caching frequently used context",
    "supported_models": [
        "claude-opus-4-1-20250805",
        "claude-opus-4-20250514",
        "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-*",  # deprecated
        "claude-3-5-haiku-20241022",
        "claude-3-haiku-20240307",
        "claude-opus-3-*"  # deprecated
    ],
    "cache_types": {
        "5m": {"lifetime": "5 minutes", "price_multiplier": 1.25},
        "1h": {"lifetime": "1 hour", "price_multiplier": 2.0}
    },
    "cache_hit": {"price_multiplier": 0.1}
}
```

### Minimum Cacheable Length

```python
MIN_CACHE_LENGTH = {
    "opus_sonnet_models": 1024,  # tokens
    "haiku_models": 2048  # tokens
}

# Models with 1024 token minimum
MODELS_1024 = [
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-*",
    "claude-opus-3-*"
]

# Models with 2048 token minimum
MODELS_2048 = [
    "claude-3-5-haiku-20241022",
    "claude-3-haiku-20240307"
]
```

### Pricing Example

```python
# Claude Sonnet 4.5 Prompt Caching Pricing
SONNET_4_5_CACHE_PRICING = {
    "base_input": 3.00,            # $3.00 / MTok
    "5m_cache_write": 3.75,        # $3.75 / MTok (1.25x base)
    "1h_cache_write": 6.00,        # $6.00 / MTok (2.0x base)
    "cache_hit_refresh": 0.30,     # $0.30 / MTok (0.1x base)
    "output": 15.00                # $15.00 / MTok
}

# Cost Calculation Example
EXAMPLE_COST = {
    "scenario": "1M token context cached, 1000 queries",
    "initial_request": {
        "cache_write": 1_000_000 * 0.00000375,  # $3.75
        "output": 1_000 * 0.000015               # $0.015
    },
    "subsequent_999_requests": {
        "cache_hits": 999 * 1_000_000 * 0.0000003,  # $299.70
        "output": 999 * 1_000 * 0.000015             # $14.99
    },
    "total": 318.46,  # $318.46
    "savings_vs_no_cache": "90%+"
}
```

### Cache Control Structure

```python
CACHE_CONTROL = {
    "parameter": "cache_control",
    "type": {"type": "ephemeral"},  # only type supported
    "max_breakpoints": 4,
    "order": ["tools", "system", "messages"],  # hierarchy
    "automatic_prefix_check": {
        "enabled": True,
        "lookback": "~20 content blocks from explicit breakpoint",
        "behavior": "Uses longest matching prefix automatically"
    }
}

# Example Usage
REQUEST_WITH_CACHE = {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 4096,
    "system": [
        {
            "type": "text",
            "text": "Long system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {"role": "user", "content": "Question"}
    ]
}
```

### Multiple Breakpoints Strategy

```python
MULTIPLE_BREAKPOINTS_USE_CASES = {
    "different_update_frequency": {
        "example": "Tools rarely change, but context updates daily",
        "structure": [
            {"section": "tools", "cache_control": "ephemeral"},
            {"section": "system", "cache_control": "ephemeral"},
            {"section": "context", "cache_control": "ephemeral"},
            {"section": "messages", "cache_control": "ephemeral"}
        ]
    },
    "granular_control": "Exact control over what gets cached",
    "long_prompts": "Ensure caching for content >20 blocks before final breakpoint"
}
```

### Caching with Thinking Blocks

```python
CACHE_WITH_THINKING = {
    "challenge": "Thinking content varies between requests",
    "impact": "Can reduce cache hit rates",
    "mitigation": {
        "approach_1": "Place thinking blocks after cached content",
        "approach_2": "Use shorter thinking budgets",
        "approach_3": "Cache only static portions"
    },
    "recommendation": "Test cache effectiveness with thinking enabled"
}
```

---

## Context Windows

### Standard Context Windows

```python
CONTEXT_WINDOWS = {
    "claude-sonnet-4-5-20250929": 200_000,
    "claude-sonnet-4-20250514": 200_000,
    "claude-3-7-sonnet-20250219": 200_000,
    "claude-opus-4-1-20250805": 200_000,
    "claude-opus-4-20250514": 200_000,
    "claude-3-5-haiku-20241022": 200_000,
    "claude-3-haiku-20240307": 200_000
}
```

### 1M Token Beta Context

```python
BETA_1M_CONTEXT = {
    "supported_models": [
        "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-20250514"
    ],
    "header": "context-1m-2025-08-07",
    "context_window": 1_000_000,
    "pricing": "Long context pricing applies to requests >200k tokens",
    "status": "Beta",
    
    "usage": {
        "header": {"anthropic-beta": "context-1m-2025-08-07"},
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 64_000
    }
}
```

### Context Awareness (Sonnet 4.5 Only)

```python
CONTEXT_AWARENESS = {
    "model": "claude-sonnet-4-5-20250929",
    "feature": "Tracks token usage throughout conversations",
    "updates": "Receives updates after each tool call",
    "benefits": [
        "Prevents premature task abandonment",
        "Enables effective execution on long-running tasks",
        "Better multi-window workflow management"
    ],
    "technical_details_url": "/en/docs/build-with-claude/context-windows#context-awareness-in-claude-sonnet-4-5",
    "prompting_guidance_url": "/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#context-awareness-and-multi-window-workflows"
}
```

---

## Context Editing

### Overview

```python
CONTEXT_EDITING = {
    "description": "Intelligent context management through automatic tool call clearing",
    "supported_models": [
        "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219"
    ],
    "beta_header": "context-management-2025-06-27",
    "status": "Beta"
}
```

### Configuration

```python
# Example: Remove specific tool calls
CONTEXT_EDITING_REQUEST = {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 4096,
    "betas": ["context-management-2025-06-27"],
    "messages": [
        {"role": "user", "content": "..."}
    ],
    "context_management": {
        "edits": [
            {
                "type": "clear",
                "location": "tool_use",
                "tool_use_id": "toolu_abc123"
            }
        ]
    }
}
```

### Edit Types

```python
EDIT_TYPES = {
    "clear": {
        "description": "Remove tool call and its result from context",
        "location": "tool_use",
        "required": ["tool_use_id"]
    }
}
```

### Use Cases

```python
CONTEXT_EDITING_USE_CASES = {
    "reduce_context": "Remove old tool calls to stay within token limits",
    "refine_conversation": "Clean up exploratory searches",
    "optimize_cost": "Remove redundant information",
    "improve_focus": "Keep conversation on track"
}
```

---

## Tool Use

### Overview

```python
TOOL_USE = {
    "description": "Enable Claude to interact with external tools and APIs",
    "supported_models": "All Claude models",
    "max_tools": 1024,  # per request
    "parallel_calls": True
}
```

### Tool Definition Structure

```python
TOOL_DEFINITION = {
    "name": "string",  # ^[a-zA-Z0-9_-]{1,64}$
    "description": "string",  # detailed description for Claude
    "input_schema": {
        "type": "object",
        "properties": {
            "param_name": {
                "type": "string|number|boolean|array|object",
                "description": "parameter description"
            }
        },
        "required": ["param_name"]
    }
}

# Example: Weather Tool
WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    }
}
```

### Tool Choice Options

```python
TOOL_CHOICE = {
    "auto": {
        "type": "auto",
        "description": "Claude decides whether to call tools (default)"
    },
    "any": {
        "type": "any",
        "description": "Claude must use at least one tool"
    },
    "tool": {
        "type": "tool",
        "name": "specific_tool_name",
        "description": "Force specific tool use"
    },
    "none": {
        "type": "none",  # Not officially in schema but mentioned in extended thinking
        "description": "Prevent tool use"
    }
}
```

### Parallel Tool Calls

```python
PARALLEL_TOOL_CALLS = {
    "enabled": True,
    "description": "Claude can make multiple tool calls simultaneously",
    "example_scenario": "Research task with multiple speculative searches",
    "benefits": [
        "Faster information gathering",
        "More efficient multi-step workflows",
        "Better context building"
    ],
    "sonnet_4_5_improvement": "More effective at firing off multiple speculative searches"
}
```

### Memory Tool (Beta)

```python
MEMORY_TOOL = {
    "type": "memory_20250818",
    "name": "memory",
    "beta_header": "context-management-2025-06-27",
    "description": "Store and retrieve information outside context window",
    "capabilities": [
        "Build knowledge bases over time",
        "Maintain project state across sessions",
        "Preserve effectively unlimited context through file-based storage"
    ],
    
    "usage": {
        "tools": [
            {
                "type": "memory_20250818",
                "name": "memory"
            }
        ],
        "betas": ["context-management-2025-06-27"]
    }
}
```

---

## Streaming

### Overview

```python
STREAMING = {
    "description": "Receive responses incrementally via Server-Sent Events (SSE)",
    "supported": "All models",
    "protocol": "Server-Sent Events (SSE)",
    "parameter": "stream: true"
}
```

### Event Types

```python
STREAM_EVENTS = {
    "message_start": "Start of message",
    "content_block_start": "Start of content block (text/thinking)",
    "content_block_delta": "Incremental content update",
    "content_block_stop": "End of content block",
    "message_delta": "Message metadata update",
    "message_stop": "End of message",
    "ping": "Keep-alive ping",
    "error": "Error event"
}
```

### Streaming with Thinking

```python
STREAMING_WITH_THINKING = {
    "thinking_event": "thinking_delta",
    "behavior": "Chunky delivery pattern (batches for performance)",
    "note": "May have delays between streaming events",
    "improvement": "Being continuously improved for smoother delivery",
    
    "example_sequence": [
        "message_start",
        "content_block_start (thinking)",
        "content_block_delta (thinking_delta) x N",
        "content_block_delta (signature_delta)",
        "content_block_stop",
        "content_block_start (text)",
        "content_block_delta (text_delta) x N",
        "content_block_stop",
        "message_delta",
        "message_stop"
    ]
}
```

### Streaming Request Example

```python
import anthropic

client = anthropic.Anthropic(api_key="...")

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16_000,
    thinking={"type": "enabled", "budget_tokens": 10_000},
    messages=[
        {"role": "user", "content": "What is 27 * 453?"}
    ]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            print(event.delta.text or event.delta.thinking, end="", flush=True)
```

---

## Vision

### Overview

```python
VISION = {
    "supported_models": "All Claude models",
    "formats": ["image/jpeg", "image/png", "image/gif", "image/webp"],
    "max_size": 5_242_880,  # 5 MB per image
    "input_methods": ["base64", "url"]
}
```

### Image Input Format

```python
IMAGE_MESSAGE = {
    "role": "user",
    "content": [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": "base64_encoded_image_data..."
            }
        },
        {
            "type": "text",
            "text": "What's in this image?"
        }
    ]
}
```

### Best Practices

```python
VISION_BEST_PRACTICES = {
    "image_quality": "Higher resolution = better accuracy",
    "orientation": "Ensure images are correctly oriented",
    "text_in_images": "Works well for OCR tasks",
    "multiple_images": "Can process multiple images in single request",
    "cost": "Images count toward input token limit (calculated by size)"
}
```

---

## PDF Support

### Overview

```python
PDF_SUPPORT = {
    "supported_models": [
        "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219",
        "claude-opus-4-1-20250805",
        "claude-opus-4-20250514",
        "claude-3-5-haiku-20241022"
    ],
    "max_size": 32_000_000,  # 32 MB
    "max_pages": 100,  # per PDF
    "processing": "Converts to images internally"
}
```

### PDF Input Format

```python
PDF_MESSAGE = {
    "role": "user",
    "content": [
        {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": "base64_encoded_pdf_data..."
            }
        },
        {
            "type": "text",
            "text": "Summarize this document"
        }
    ]
}
```

### Token Calculation

```python
PDF_TOKEN_CALCULATION = {
    "method": "Each page converted to ~1500 tokens (approximate)",
    "example": {
        "pages": 100,
        "estimated_tokens": 150_000
    },
    "note": "Actual token count may vary based on content density"
}
```

---

## Rate Limits

### Default Rate Limits by Model

```python
RATE_LIMITS = {
    "claude-sonnet-4-5-20250929": {
        "requests_per_minute": 50,
        "tokens_per_minute": 40_000,
        "tokens_per_day": 1_000_000
    },
    "claude-sonnet-4-20250514": {
        "requests_per_minute": 50,
        "tokens_per_minute": 40_000,
        "tokens_per_day": 1_000_000
    },
    "claude-3-7-sonnet-20250219": {
        "requests_per_minute": 50,
        "tokens_per_minute": 40_000,
        "tokens_per_day": 1_000_000
    },
    "claude-3-5-haiku-20241022": {
        "requests_per_minute": 50,
        "tokens_per_minute": 50_000,
        "tokens_per_day": 5_000_000
    }
}
```

### Tier System

```python
TIERS = {
    "tier_1": {
        "criteria": "New API users",
        "limits": "Lower limits"
    },
    "tier_2": {
        "criteria": "$50+ spend",
        "limits": "Medium limits"
    },
    "tier_3": {
        "criteria": "$500+ spend",
        "limits": "Higher limits"
    },
    "tier_4": {
        "criteria": "$5,000+ spend",
        "limits": "Highest standard limits"
    },
    "enterprise": {
        "criteria": "Contact sales",
        "limits": "Custom limits"
    }
}
```

### Rate Limit Headers

```python
RATE_LIMIT_HEADERS = {
    "anthropic-ratelimit-requests-limit": "Max requests per minute",
    "anthropic-ratelimit-requests-remaining": "Remaining requests",
    "anthropic-ratelimit-requests-reset": "Reset time (RFC 3339)",
    "anthropic-ratelimit-tokens-limit": "Max tokens per minute",
    "anthropic-ratelimit-tokens-remaining": "Remaining tokens",
    "anthropic-ratelimit-tokens-reset": "Reset time (RFC 3339)",
    "retry-after": "Seconds to wait before retry (on 429 error)"
}
```

---

## API Reference

### Messages API Endpoint

```python
API_ENDPOINT = {
    "base_url": "https://api.anthropic.com",
    "messages_endpoint": "/v1/messages",
    "method": "POST",
    "headers": {
        "x-api-key": "YOUR_API_KEY",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
}
```

### Request Schema

```python
REQUEST_SCHEMA = {
    "model": "string (required)",
    "messages": "array (required)",
    "max_tokens": "integer (required)",
    "system": "string|array (optional)",
    "temperature": "number 0-1 (optional, default: 1.0)",
    "top_p": "number 0-1 (optional, default: 0.999)",
    "top_k": "integer (optional, default: -1)",
    "stop_sequences": "array (optional)",
    "stream": "boolean (optional, default: false)",
    "thinking": "object (optional)",
    "tools": "array (optional)",
    "tool_choice": "object (optional)",
    "metadata": "object (optional)"
}
```

### Response Schema

```python
RESPONSE_SCHEMA = {
    "id": "string",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "thinking|text|tool_use",
            "thinking|text": "string",
            # or for tool_use
            "id": "string",
            "name": "string",
            "input": "object"
        }
    ],
    "model": "string",
    "stop_reason": "end_turn|max_tokens|stop_sequence|tool_use",
    "stop_sequence": "string|null",
    "usage": {
        "input_tokens": "integer",
        "output_tokens": "integer",
        "cache_creation_input_tokens": "integer (optional)",
        "cache_read_input_tokens": "integer (optional)"
    }
}
```

---

## Best Practices

### Model Selection

```python
MODEL_SELECTION = {
    "complex_agents_coding": "claude-sonnet-4-5-20250929",
    "general_high_performance": "claude-sonnet-4-20250514",
    "extended_thinking_focus": "claude-3-7-sonnet-20250219",
    "cost_sensitive": "claude-3-5-haiku-20241022",
    "specialized_complex": "claude-opus-4-1-20250805",
    
    "production_guideline": "Use specific versions, not aliases",
    "development_guideline": "Aliases OK for testing"
}
```

### Extended Thinking Usage

```python
EXTENDED_THINKING_GUIDELINES = {
    "enable_for": [
        "Complex coding (especially Sonnet 4.5)",
        "Multi-step reasoning",
        "Mathematical problems",
        "Strategic analysis"
    ],
    "budget_tokens": {
        "simple": 1_000,
        "medium": 10_000,
        "complex": 32_000
    },
    "cost_consideration": "Charged for full thinking tokens, even if summarized",
    "testing": "Compare with/without to verify ROI"
}
```

### Prompt Caching Strategy

```python
CACHING_STRATEGY = {
    "ideal_for": [
        "Long system prompts",
        "Tool definitions",
        "Static context/examples",
        "Repeated queries with same context"
    ],
    "structure": "Place static content first, mark with cache_control",
    "min_length": "1024 tokens (Opus/Sonnet) or 2048 tokens (Haiku)",
    "breakpoints": "1 at end usually sufficient (up to 4 for granular control)",
    "roi": "Significant savings after ~3-5 requests with same context"
}
```

### Streaming Best Practices

```python
STREAMING_BEST_PRACTICES = {
    "when_to_use": [
        "Long responses",
        "User-facing applications",
        "Extended thinking enabled",
        "Large output tokens (>8k)"
    ],
    "implementation": "Handle chunky delivery (especially with thinking)",
    "error_handling": "Process ping events, handle reconnection",
    "timeout": "Use for 128k output to avoid timeouts"
}
```

### Context Management

```python
CONTEXT_MANAGEMENT_BEST_PRACTICES = {
    "token_awareness": "Monitor token usage (Sonnet 4.5 does this automatically)",
    "context_editing": "Use to remove old tool calls and optimize context",
    "1m_context": "Test thoroughly before production use (beta feature)",
    "memory_tool": "For cross-session persistence and unlimited context",
    "structure": "Place important information early and late in context"
}
```

### Tool Use Best Practices

```python
TOOL_USE_BEST_PRACTICES = {
    "descriptions": "Clear, detailed descriptions for each tool",
    "naming": "Use descriptive snake_case names",
    "parameters": "Specify required vs optional clearly",
    "parallel_calls": "Design for parallel execution when possible",
    "error_handling": "Return clear error messages in tool results",
    "thinking_integration": "Use tool_choice: auto with extended thinking for best results"
}
```

---

## Complete Code Examples

### Basic Request

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)

print(response.content[0].text)
```

### With Extended Thinking

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16_000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10_000
    },
    messages=[
        {"role": "user", "content": "Prove there are infinitely many primes"}
    ]
)

# Response will have thinking block first, then text
for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking[:200]}...")
    elif block.type == "text":
        print(f"Response: {block.text}")
```

### With Prompt Caching

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": "Very long system prompt with examples...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "Question"}
    ]
)

# Check cache usage
print(f"Cache creation: {response.usage.cache_creation_input_tokens}")
print(f"Cache read: {response.usage.cache_read_input_tokens}")
```

### With 1M Context Beta

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64_000,
    extra_headers={
        "anthropic-beta": "context-1m-2025-08-07"
    },
    messages=[
        {"role": "user", "content": "Very long document (up to 1M tokens)..."}
    ]
)
```

### With Tools

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    tools=[
        {
            "name": "get_weather",
            "description": "Get current weather",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    ],
    messages=[
        {"role": "user", "content": "What's the weather in SF?"}
    ]
)

# Check for tool use
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}")
        print(f"Input: {block.input}")
```

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16_000,
    thinking={"type": "enabled", "budget_tokens": 10_000},
    messages=[
        {"role": "user", "content": "Write a poem"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

**Reference Complete**

All major documentation pages crawled and integrated:
- https://docs.claude.com/en/docs/about-claude/models/overview
- https://docs.claude.com/en/docs/about-claude/models/whats-new-sonnet-4-5
- https://docs.claude.com/en/docs/about-claude/models/choosing-a-model
- https://docs.claude.com/en/docs/build-with-claude/extended-thinking
- https://docs.claude.com/en/docs/build-with-claude/prompt-caching
- https://docs.claude.com/en/docs/build-with-claude/context-windows
- https://docs.claude.com/en/docs/build-with-claude/context-editing
- https://docs.claude.com/en/docs/agents-and-tools/tool-use
- https://docs.claude.com/en/docs/build-with-claude/streaming
- https://docs.claude.com/en/docs/build-with-claude/vision
- https://docs.claude.com/en/docs/build-with-claude/pdf-support
- https://docs.claude.com/en/api/rate-limits
- https://docs.claude.com/en/api/messages

