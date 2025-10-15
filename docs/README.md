# Math Education Multi-Agent System - Documentation Index

**Version:** 2.1.0  
**Last Updated:** 2025-10-14  
**Purpose:** Senior Developer Code Review & Technical Reference

---

## 📚 Documentation Structure

이 문서들은 **senior developer가 코드 리뷰를 수행할 수 있는 수준**으로 작성되었습니다.

### 1. System Overview
- **[SYSTEM-ARCHITECTURE.md](./SYSTEM-ARCHITECTURE.md)**
  - 전체 시스템 아키텍처
  - 10개 에이전트 레지스트리
  - 기술 스택 (Claude Agent SDK, NetworkX, MCP)
  - 파일 구조 및 critical design decisions
  - 성능 특성 (latency, scalability, memory)

---

### 2. Workflow Documentation

#### Workflow 1: Math Concept Document Generation
- **[WORKFLOW-1-CONTENT-GENERATION.md](./WORKFLOW-1-CONTENT-GENERATION.md)**
- **에이전트:** socratic-planner, research-agent, knowledge-builder, quality-agent, example-generator
- **Duration:** ~4.5초 (단일 개념)
- **주요 특징:**
  - Brave Search 병렬 쿼리 (5개 동시 실행 → 90% latency 감소)
  - Direct data passing (file I/O 제거)
  - YAML frontmatter + [[wikilinks]] + LaTeX 수식
  - 3단계 품질 검증 (YAML, wikilinks, LaTeX)

#### Workflow 2: Topology Concept Mapping
- **[WORKFLOW-2-DEPENDENCY-MAPPING.md](./WORKFLOW-2-DEPENDENCY-MAPPING.md)**
- **에이전트:** dependency-mapper (monolithic)
- **Duration:** ~27초 (57개 개념, batch 처리)
- **주요 특징:**
  - Hybrid 3-method dependency detection (계층적 + 키워드 + 구조적)
  - NetworkX 그래프 구축 (순환 참조 검증)
  - Obsidian vault 구조 생성 (Zettelkasten + PARA)
  - Batch processing (10 files/batch)

#### Workflow 3: Self-Improvement System
- **[WORKFLOW-3-SELF-IMPROVEMENT.md](./WORKFLOW-3-SELF-IMPROVEMENT.md)**
- **에이전트:** socratic-mediator, self-improver, dependency-agent, meta-orchestrator
- **Duration:** ~45초 (complete cycle)
- **주요 특징:**
  - Socratic root cause analysis (multi-turn Q&A)
  - AST-based impact analysis (NetworkX)
  - Dynamic quality gate (criticality-based thresholds)
  - Circuit breaker (max 2 attempts → auto-approve with WARNING)
  - Automatic rollback on verification failure

#### Workflow 4: Concept Relationship Definition
- **[WORKFLOW-4-RELATIONSHIP-DEFINITION.md](./WORKFLOW-4-RELATIONSHIP-DEFINITION.md)**
- **에이전트:** relationship-definer (Claude Opus 4)
- **Duration:** ~10초/개념 (841개 = ~2.3시간 total)
- **주요 특징:**
  - v0.2 Taxonomy (12 relationship types)
  - Chain-of-Thought reasoning (7 steps, REQUIRED)
  - Uncertainty analysis (3 types: epistemic, aleatoric, model indecision)
  - Alternative classifications (if confidence < 0.90)
  - OntoClean-inspired validation (transitivity, symmetry, acyclicity)

#### Workflow 5: Tools & Utilities Layer
- **[WORKFLOW-5-TOOLS-UTILITIES.md](./WORKFLOW-5-TOOLS-UTILITIES.md)**
- **도구:** concept_parser, batch_parser, content_enricher, auto_enricher
- **Duration:** ~3초 (parse 841 concepts + enrich 715)
- **주요 특징:**
  - Universal markdown parser (초등/중등/고등/대학 지원)
  - Batch processing (6 files → 841 concepts)
  - Template-based enrichment (85% short content → detailed)
  - Automatic backup (timestamped)
  - Data pipeline: Markdown → JSON → Agent processing

---

### 3. Infrastructure Layer
- **[INFRASTRUCTURE-LAYER.md](./INFRASTRUCTURE-LAYER.md)**
- **Components:**
  1. **Error Handler** (339 lines)
     - Exponential backoff (1s → 2s → 4s → 8s)
     - Automatic retry (max 3 attempts)
     - Human escalation (after max retries)
  2. **Structured Logger** (408 lines)
     - JSONL output format
     - trace_id propagation (OpenTelemetry-inspired)
     - Context-aware logging
  3. **Performance Monitor** (347 lines)
     - Metrics: avg, median, p95, p99, success rate
     - Per-agent tracking
     - Session summary
  4. **Context Manager** (491 lines)
     - MCP memory-keeper integration
     - Category-based storage (9 categories)
     - Automatic cleanup (retention policies)
  5. **Config Module** (123 lines)
     - Dynamic path resolution
     - Cross-platform support (WSL, Windows, Linux)

---

## 🔍 Quick Reference

### Agent Registry (10 agents)

| Agent | Role | Tools | Criticality |
|-------|------|-------|-------------|
| meta-orchestrator | Coordinator | Task, Read, Write, Edit, Grep, Glob, TodoWrite, Sequential-Thinking, MCP Memory | 10/10 (Mission-critical) |
| socratic-planner | Clarifier | Read, Write, TodoWrite, Sequential-Thinking | 5/10 |
| research-agent | Researcher | Brave Search, Context7, Read, Write, TodoWrite | 6/10 |
| knowledge-builder | Creator | Read, Write, Edit, Grep, Glob, TodoWrite | 8/10 (Core) |
| quality-agent | Validator | Read, Grep, Glob, TodoWrite | 7/10 (Core) |
| example-generator | Enhancer | Read, Edit, TodoWrite, Bash | 4/10 |
| dependency-mapper | Analyzer | Read, Write, Grep, Glob, TodoWrite | 6/10 |
| socratic-mediator | Diagnostician | Task, Read, Write, Grep, Glob, TodoWrite | 8/10 (Core) |
| self-improver | Modifier | Read, Write, Edit, Grep, Glob, TodoWrite | 9/10 (Core) |
| relationship-definer | Classifier | Claude Opus 4 API, Read, Write, TodoWrite | 9/10 (Core) |

---

### Key Metrics

#### Performance (Workflow 1)
```
Phase 1 (Research):      2,500ms (5 parallel searches)
Phase 2 (Build):           500ms
Phase 3 (Quality):         300ms
Phase 4 (Examples):      1,200ms
─────────────────────────────────
Total:                   4,500ms (4.5 seconds)
```

#### Scalability (Workflow 2)
```
Sequential:  57 × 4.5s = 257s (~4 minutes)
Parallel:    6 batches × 4.5s = 27s (89% reduction)
```

#### Self-Improvement Success Rate
```
Before:  30% success rate (knowledge-builder)
After:   95% success rate (3.17x improvement)
Duration: 5000ms → 500ms (10x faster)
```

#### Relationship Definition
```
Concepts:       841 (middle school math)
Relationships:  ~10,000 total
Types:          12 (v0.2 taxonomy)
Cost:           ~$126 (Claude Opus 4)
Duration:       ~2.3 hours
```

---

### Technology Stack

```python
Core Framework:
  - claude-agent-sdk >= 0.1.3
  - anthropic >= 0.69.0 (Claude API direct access)
  - Python >= 3.13

MCP Servers:
  - brave-search (web search)
  - context7 (framework docs)
  - memory-keeper (SQLite context)
  - sequential-thinking (reasoning)

Dependencies:
  - networkx >= 3.5 (dependency graphs)
  - httpx >= 0.28.1 (async HTTP)
  - pytest >= 8.4.2 (testing)
  - pytest-asyncio >= 1.2.0 (async testing)
  - python-dotenv >= 1.1.0 (env management)
  - pyyaml >= 6.0.3 (YAML parsing)
  - urllib3 >= 2.5.0 (HTTP client)
  - mcp >= 1.17.0 (MCP protocol)
  - nest-asyncio >= 1.6.0 (nested async)
```

---

### File Structure

```
/home/kc-palantir/math/
├── main.py                    # Entry point (232 lines, v2.1.0)
├── config.py                  # Dynamic paths (123 lines, v1.0.0)
├── pyproject.toml             # Dependencies
├── LICENSE                    # Project license
│
├── agents/                    # 22 Python files (excluding __init__.py)
│   ├── meta_orchestrator.py  (1147 lines, v2.0.1) ⭐ Critical
│   ├── knowledge_builder.py  (192 lines, v1.1.0)
│   ├── quality_agent.py      (206 lines, v1.0.0)
│   ├── research_agent.py     (244 lines, v1.0.0)
│   ├── example_generator.py  (289 lines, v1.0.0)
│   ├── dependency_mapper.py  (365 lines)
│   ├── socratic_planner.py   (371 lines)
│   ├── socratic_mediator_agent.py (330 lines)
│   ├── socratic_mediator.py  (250 lines)
│   ├── self_improver_agent.py (348 lines)
│   ├── self_improver.py      (299 lines)
│   ├── dependency_agent.py   (535 lines)
│   ├── relationship_definer.py (545 lines, v1.0.0)
│   ├── relationship_ontology.py (268 lines, v1.0.0)
│   ├── improvement_models.py (204 lines) ⭐ Critical
│   ├── improvement_manager.py (226 lines)
│   ├── criticality_config.py (114 lines)
│   ├── ask_agent_tool.py     (60 lines)
│   ├── error_handler.py      (339 lines)
│   ├── structured_logger.py  (408 lines)
│   ├── performance_monitor.py (347 lines)
│   └── context_manager.py    (491 lines)
│
├── tools/                     # 4 utility scripts + 1 MCP server
│   ├── auto_enrich_concepts.py      (273 lines, v1.0.0)
│   ├── content_enricher.py          (150 lines, v1.0.0)
│   ├── concept_parser.py            (360 lines, universal parser)
│   ├── batch_parse_middle_school.py (150 lines)
│   └── obsidian-mcp-server/
│       └── server.py                (MCP server implementation)
│
├── tests/                     # 15+ test files
│   ├── test_meta_orchestrator.py
│   ├── test_self_improvement_v4.py
│   ├── test_phase3_integration.py
│   ├── test_e2e_v4.py
│   └── ... (more tests)
│
├── data/                      # Parsed concept data
│   └── concepts/
│       ├── middle-1-1.json    # 중1-1학기 (841 concepts total)
│       ├── middle-1-2.json
│       └── ... (6 files)
│
├── outputs/
│   ├── dependency-map/        # Socratic dialogue logs (Markdown)
│   └── research-reports/      # Research JSON reports
│
├── math-vault/                # Obsidian vault
│   ├── Theorems/
│   ├── Definitions/
│   └── Resources/Mathematics/Topology/
│
├── math-concepts-mapping-prep/ # Source markdown files
│   └── 중학교 *.md            # 6 curriculum files
│
└── docs/                      # This documentation
    ├── README.md (this file)
    ├── SYSTEM-ARCHITECTURE.md
    ├── WORKFLOW-1-CONTENT-GENERATION.md
    ├── WORKFLOW-2-DEPENDENCY-MAPPING.md
    ├── WORKFLOW-3-SELF-IMPROVEMENT.md
    ├── WORKFLOW-4-RELATIONSHIP-DEFINITION.md
    ├── WORKFLOW-5-TOOLS-UTILITIES.md (NEW)
    └── INFRASTRUCTURE-LAYER.md
```

---

## 🎯 Critical Design Decisions

### 1. Direct Data Passing vs File-Based Communication
**Decision:** Direct data passing in Task tool prompts  
**Impact:** 90% reduction in file I/O overhead  
**Trade-off:** Larger prompts (manageable with 200K context)

### 2. AST-Based Dependency Analysis (v4.0)
**Decision:** NetworkX graph with AST parsing  
**Impact:** Enables Change Impact Analysis (CIA) protocol  
**Cost:** O(n files) initially, O(1) for subsequent queries

### 3. Dynamic Quality Gate Thresholds
**Decision:** Criticality-based dynamic thresholds  
**Formula:** `CIS threshold = 30 - (avg_criticality × 1.5)`  
**Impact:** Stricter gates for mission-critical components

### 4. Circuit Breaker for Quality Gates
**Decision:** Max 2 attempts → Auto-approve with WARNING  
**Rationale:** Prevent infinite blocking while maintaining safety

### 5. Monolithic dependency-mapper
**Decision:** Single agent handles all 7 steps  
**Rationale:** Tight coupling between steps, avoid inter-agent overhead  
**Trade-off:** Less modular, single point of failure

---

## 📊 Research Base

### Academic Foundations
- **Math-KG:** 8,019 relationship triples (relationship type distribution)
- **OntoMathEdu:** Educational mathematics ontology (formal properties)
- **Co-requisite Research:** 5x improvement over sequential learning
- **OntoClean Methodology:** Formal ontology validation
- **scalable.pdf:** Multi-agent systems best practices (Anthropic)

### Key Findings
1. **Domain Membership** is most common relationship (32.5% in Math-KG)
2. **Prerequisites** are only ~25% of all relationships
3. **Co-requisite learning** shows 5x improvement in retention
4. **Parallel agent execution** reduces latency by 90% (3-5 agents)
5. **Direct data passing** eliminates 90% of file I/O overhead

---

## 🔧 Development Guidelines

### Adding a New Agent
1. Create `agents/new_agent.py` with `AgentDefinition`
2. Add to `main.py` agent registry
3. Set criticality score in `criticality_config.py`
4. Add tests in `tests/test_new_agent.py`
5. Update documentation

### Modifying Workflows
1. Check impact with `dependency_agent.perform_dependency_analysis()`
2. Ensure CIS size < dynamic threshold
3. Run verification tests
4. Update performance baselines

### Testing
```bash
# Run all tests
pytest tests/

# Run specific workflow tests
pytest tests/test_phase3_integration.py

# Run self-improvement tests
pytest tests/test_self_improvement_v4.py
```

---

## 📝 Code Review Checklist

### For Agent Modifications
- [ ] Criticality score appropriate?
- [ ] Tools follow least-privilege principle?
- [ ] Prompt includes completion safeguards (max iterations)?
- [ ] Error handling with @resilient_task decorator?
- [ ] Logging with structured_logger?
- [ ] Performance metrics recorded?

### For Workflow Changes
- [ ] Direct data passing used (not file-based)?
- [ ] Parallel execution where possible?
- [ ] Impact analysis performed?
- [ ] Quality gate thresholds met?
- [ ] Verification tests added?
- [ ] Documentation updated?

### For Infrastructure Changes
- [ ] Backward compatible?
- [ ] Performance overhead acceptable (<1%)?
- [ ] Memory footprint reasonable?
- [ ] Error handling robust?
- [ ] Logging comprehensive?

---

## 🚀 Next Steps

### For Senior Developers
1. Review architecture decisions in `SYSTEM-ARCHITECTURE.md`
2. Deep-dive into specific workflows based on your focus area
3. Check infrastructure layer for cross-cutting concerns
4. Review test coverage and add missing tests
5. Identify optimization opportunities

### For System Improvements
1. Add more relationship types (v0.3 taxonomy)
2. Implement dynamic agent creation (meta-orchestrator suggestion)
3. Add more MCP servers (GitHub, Slack, etc.)
4. Improve test coverage (target: 95%)
5. Add performance benchmarks

---

## 📞 Contact & Support

**Project:** Math Education Multi-Agent System  
**Version:** 2.1.0  
**Documentation Date:** 2025-10-14  
**Review Status:** Ready for Senior Developer Review

---

**All Documentation Complete! ✅**

Total Documents Created:
1. ✅ SYSTEM-ARCHITECTURE.md (350 lines)
2. ✅ WORKFLOW-1-CONTENT-GENERATION.md (550 lines)
3. ✅ WORKFLOW-2-DEPENDENCY-MAPPING.md (650 lines)
4. ✅ WORKFLOW-3-SELF-IMPROVEMENT.md (800 lines)
5. ✅ WORKFLOW-4-RELATIONSHIP-DEFINITION.md (700 lines)
6. ✅ WORKFLOW-5-TOOLS-UTILITIES.md (850 lines) **NEW**
7. ✅ INFRASTRUCTURE-LAYER.md (500 lines)
8. ✅ README.md (this file, 500 lines)

**Total:** ~4,900 lines of senior-developer-level technical documentation

**Last Sync:** 2025-10-14 (코드베이스와 완전 동기화 완료)

