[![CI](https://github.com/KyungChan-PARK/kc-palantir-math/actions/workflows/ci.yml/badge.svg)](https://github.com/KyungChan-PARK/kc-palantir-math/actions/workflows/ci.yml)

# Math Education Multi-Agent System

> **Claude Sonnet 4.5 powered mathematics education platform with multi-agent architecture**

## 🚀 Quick Start

This project implements a comprehensive mathematics education system using Claude Agent SDK with 9 specialized agents.

## 📚 Documentation

- **[CLAUDE-IMPLEMENTATION-STANDARDS.md](./CLAUDE-IMPLEMENTATION-STANDARDS.md)** - MANDATORY standards for all code
- **[CLAUDE-FEATURES-ANALYSIS-REPORT.md](./CLAUDE-FEATURES-ANALYSIS-REPORT.md)** - Comprehensive feature analysis
- **[.claude.md](./.claude.md)** - Claude Max x20 configuration guide

## 🤖 Agents

1. **meta-orchestrator** - Coordinates all agents
2. **knowledge-builder** - Creates Obsidian markdown files
3. **quality-agent** - Validates content quality
4. **research-agent** - Deep concept research
5. **example-generator** - Generates mathematical examples
6. **dependency-mapper** - Maps prerequisite dependencies
7. **socratic-planner** - Requirements clarification
8. **socratic-mediator** - Root cause analysis
9. **self-improver** - Automated code improvement

## ⚡ Features

- ✅ Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) - All 9 agents
- ✅ Extended Thinking for complex reasoning
- ✅ Prompt Caching for cost optimization
- ✅ 1M Context window for meta-orchestrator
- ✅ Streaming responses for better UX
- ✅ MCP integration (memory-keeper, sequential-thinking)
- ✅ Self-improvement system v4.0
- ✅ Automated CI/CD with standards enforcement

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **AI**: Claude Agent SDK 0.1.3+
- **MCP Servers**: memory-keeper, obsidian, github
- **Testing**: pytest, pytest-asyncio
- **CI/CD**: GitHub Actions (validate, lint, standards-check)

## 📖 Getting Started

See [.claude.md](./.claude.md) for detailed setup instructions.
