# Workflow 1: Math Concept Document Generation

**Purpose:** 사용자 요청 수학 개념 → 심층 조사 → Obsidian 마크다운 문서 생성  
**Agents:** 6 agents (socratic-planner, research-agent, knowledge-builder, quality-agent, example-generator, meta-orchestrator)  
**Avg Duration:** 4.5 seconds (single concept)

---

## Workflow Diagram

```
User: "Fubini's Theorem에 대한 문서 만들어줘"
  │
  ├─> Phase 0 (선택): 요구사항 명확화 [socratic-planner]
  │     If(요청 모호) → Socratic 질문 생성 → 사용자 답변 → 계획 수립
  │
  ├─> Phase 1: 심층 조사 [research-agent]
  │     Brave Search (5 parallel queries) → Context7 (implementation) → JSON report
  │
  ├─> Phase 2: 문서 생성 [knowledge-builder]
  │     JSON parsing → YAML frontmatter → Markdown body → LaTeX formulas → File save
  │
  ├─> Phase 3: 품질 검증 [quality-agent]
  │     Read file → Checklist validation (YAML, wikilinks, LaTeX) → Report
  │
  └─> Phase 4: 예제 추가 [example-generator]
        Graded examples → Python/SymPy code → Practice problems → Edit file
```

---

## Phase 0: 요구사항 명확화 (Optional)

### Agent: socratic-planner

**Trigger Condition:**
```python
if is_ambiguous(user_request):
    # Examples:
    # - "Process concepts" (어떤 개념?)
    # - "Organize files" (어떤 구조로?)
    # - "Improve system" (어느 부분?)
    activate_socratic_planner()
```

### Implementation (socratic_planner.py:326-348)

```python
# Round 1: 5가지 핵심 질문 생성
questions = [
    "처리 범위는? (전체 vs 일부)",
    "파일 단위는? (Major concept vs Sub-unit)",
    "Prerequisites 결정 방법은? (자동 vs 수동 vs 하이브리드)",
    "Obsidian vault 폴더 구조는? (플랫 vs 계층 vs PARA)",
    "다른 수학 분야와 연결할까요? (독립 vs 통합)"
]

# User answers → Extract decisions
user_response = await prompt_user(questions)
decisions = parse_user_response(user_response)

# Round 2: Follow-up questions (if needed)
if has_ambiguities(decisions):
    follow_up_questions = generate_follow_up(decisions)
    # ...

# Final: Detailed implementation plan
plan = generate_detailed_plan(decisions)
user_approval = await request_approval(plan)

if user_approval:
    return plan  # Meta-orchestrator executes
else:
    iterate_planning()
```

### Output Example

```markdown
# 구현 계획 (사용자 답변 반영)

## Scope
- 처리 대상: Fubini's Theorem 단일 개념
- 소요 시간: 약 5초

## File Structure
- 파일 단위: 1 concept = 1 markdown file
- Sub-concepts: Section headings (## 1.1, ### 1.1.1)

## Prerequisites
- 방법: Hybrid (research-agent 자동 추출 + 사용자 검토)
- 필수 전제조건: Measure Theory, Lebesgue Integration, σ-algebras

## Quality Assurance
- YAML 파싱 검증
- [[wikilinks]] 형식 확인
- LaTeX 수식 균형 검증
```

**Tool Calls:**
```
1. Read (previous plans, feedback history)
2. Write (save plan)
3. TodoWrite (track clarification progress)
```

---

## Phase 1: 심층 조사

### Agent: research-agent

**Input:**
```python
Task(
    agent="research-agent",
    prompt="Research Fubini's Theorem in depth. Include: definitions, prerequisites, formulas, applications, related theorems."
)
```

**Execution Steps (research_agent.py:40-225):**

```python
# Step 1: Multi-Source Information Gathering (PARALLEL)
queries = [
    "Fubini's Theorem definition mathematics",
    "Fubini's Theorem prerequisites",
    "Fubini's Theorem mathematical formula",
    "Fubini's Theorem related theorems",
    "Fubini's Theorem applications"
]

# Brave Search (5 parallel calls)
results = await asyncio.gather(*[
    brave_web_search(query) for query in queries
])

# Context7 (if applicable)
implementation_docs = await context7_search("Fubini Theorem SymPy NumPy")

# Step 2: Prerequisite Dependency Analysis
prerequisites = extract_prerequisites(results)
# Output: [
#   {"name": "Measure Theory", "level": "essential", "difficulty": "graduate"},
#   {"name": "Lebesgue Integration", "level": "essential", "difficulty": "graduate"},
#   {"name": "σ-algebras", "level": "essential", "difficulty": "graduate"},
#   ...
# ]

# Step 3: Formula Extraction
formulas = extract_formulas(results)
# LaTeX: \int_{X \times Y} f \, d(\mu \times \nu) = ...

# Step 4: Related Concepts
related = identify_related_concepts(results)
# ["Tonelli's Theorem", "Product Measures", ...]

# Step 5: Generate JSON Research Report
report = {
    "concept": "Fubini's Theorem",
    "concept_id": "fubini-theorem",
    "research_timestamp": "2025-10-14T22:30:00",
    "definitions": [...],
    "formulas": [...],
    "prerequisites": [...],
    "related_concepts": [...],
    "domain_classification": {...},
    "sources": [...]
}

# Step 6: Save JSON
write_file("/tmp/research_report_fubini-theorem.json", json.dumps(report))

# Step 7: Verify
verify_json_valid(report)
```

**Tool Calls:**
```
1. mcp__brave-search__brave_web_search (5 calls, parallel)
2. mcp__context7__resolve-library-id (1 call)
3. mcp__context7__get-library-docs (1 call)
4. Write (/tmp/research_report_fubini-theorem.json)
5. Read (verify JSON file)
6. TodoWrite (track research progress)
```

**Output:**
```json
{
  "concept": "Fubini's Theorem",
  "concept_id": "fubini-theorem",
  "definitions": [
    {"source": "Wikipedia", "text": "...", "url": "https://..."},
    {"source": "Wolfram", "text": "...", "url": "https://..."}
  ],
  "prerequisites": [
    {"name": "Measure Theory", "concept_id": "measure-theory", "level": "essential", "difficulty": "graduate"},
    {"name": "Lebesgue Integration", "concept_id": "lebesgue-integration", "level": "essential"}
  ],
  "formulas": [
    {"latex": "\\int_{X \\times Y} f \\, d(\\mu \\times \\nu) = \\int_X \\left(\\int_Y f(x,y) \\, d\\nu(y)\\right) d\\mu(x)", "description": "Main statement"}
  ]
}
```

**Performance:**
- Duration: ~2,500ms (5 parallel searches)
- API Calls: 7 total (5 Brave + 2 Context7)
- Tokens: ~15K input, ~8K output

---

## Phase 2: 문서 생성

### Agent: knowledge-builder

**Input (Direct Data Passing - scalable.pdf p4):**
```python
# ✅ GOOD: Pass research data directly
research_data = Task(research-agent, "Research Fubini's Theorem")

Task(
    agent="knowledge-builder",
    prompt=f"""Build Obsidian markdown file for Fubini's Theorem.

Research Data:
{research_data}

Requirements:
- YAML frontmatter with type, prerequisites, difficulty
- Use [[wikilinks]] for all concept references
- Include LaTeX formulas
- Save to config.MATH_VAULT_DIR/Theorems/fubini-theorem.md
"""
)
```

**Execution Steps (knowledge_builder.py:42-129):**

```python
# Step 1: Receive Research Data (via prompt parameter)
research_json = extract_json_from_prompt(prompt)

# Step 2: Generate YAML Frontmatter
frontmatter = f"""---
type: theorem
id: fubini-theorem
domain: analysis
level: graduate
difficulty: 8
language: en
prerequisites:
  - "[[measure-theory]]"
  - "[[lebesgue-integration]]"
  - "[[sigma-algebras]]"
used-in:
  - "[[product-measures]]"
  - "[[iterated-integrals]]"
created: {datetime.now().strftime('%Y-%m-%d')}
---"""

# Step 3: Generate Markdown Body
body = f"""# Fubini's Theorem

## Definition

Let $(X, \\mathcal{{A}}, \\mu)$ and $(Y, \\mathcal{{B}}, \\nu)$ be σ-finite measure spaces...

## Prerequisites

To understand this theorem, you need:
- [[measure-theory]]: Fundamental framework for integration
- [[lebesgue-integration]]: Generalized integration theory
- [[sigma-algebras]]: Measurable set structures

## Mathematical Details

$$
\\int_{{X \\times Y}} f \\, d(\\mu \\times \\nu) = \\int_X \\left(\\int_Y f(x,y) \\, d\\nu(y)\\right) d\\mu(x)
$$

## Applications

This theorem is used in:
- [[probability-theory]]: Joint distributions
- [[fourier-analysis]]: Multidimensional transforms
"""

# Step 4: Determine File Path
from config import MATH_VAULT_DIR
file_path = MATH_VAULT_DIR / "Theorems" / "fubini-theorem.md"

# Step 5: Save File
write_file(file_path, frontmatter + "\n\n" + body)

# Step 6: Verify
verify_file_created(file_path)
```

**Tool Calls:**
```
1. Read (optional: check if file exists)
2. Write (MATH_VAULT_DIR/Theorems/fubini-theorem.md)
3. Read (verify file created)
4. TodoWrite (track progress)
```

**Output File (fubini-theorem.md):**
```markdown
---
type: theorem
id: fubini-theorem
domain: analysis
level: graduate
difficulty: 8
prerequisites:
  - "[[measure-theory]]"
  - "[[lebesgue-integration]]"
used-in:
  - "[[product-measures]]"
---

# Fubini's Theorem

## Definition
[Complete mathematical definition]

## Prerequisites
- [[measure-theory]]: Framework for integration
...
```

**Performance:**
- Duration: ~500ms
- File Size: ~3,245 bytes
- Tokens: ~5K input, ~2K output

---

## Phase 3: 품질 검증

### Agent: quality-agent

**Input:**
```python
Task(
    agent="quality-agent",
    prompt="Validate file: /home/kc-palantir/math-vault/Theorems/fubini-theorem.md"
)
```

**Execution Steps (quality_agent.py:34-191):**

```python
# Step 1: Read File
file_content = read_file(file_path)

# Step 2: Validation Checklist
checks = {
    "yaml_frontmatter": validate_yaml(file_content),
    "wikilinks_format": validate_wikilinks(file_content),
    "latex_formulas": validate_latex(file_content),
    "required_sections": validate_sections(file_content),
    "mathematical_accuracy": validate_content(file_content)
}

# Checklist Details:

## A. YAML Frontmatter Validation
try:
    yaml_data = parse_yaml(file_content)
    assert "type" in yaml_data
    assert "id" in yaml_data
    assert "prerequisites" in yaml_data
    # ...
except:
    checks["yaml_frontmatter"] = FAIL

## B. Wikilinks Validation
pattern = r'\[\[([a-z0-9-]+)\]\]'
wikilinks = re.findall(pattern, file_content)

# Check kebab-case format
invalid = [w for w in wikilinks if not re.match(r'^[a-z0-9-]+$', w)]
if invalid:
    checks["wikilinks_format"] = FAIL

## C. LaTeX Formulas Validation
# Check balanced delimiters
latex_blocks = re.findall(r'\$\$(.+?)\$\$', file_content, re.DOTALL)
for block in latex_blocks:
    if not is_balanced(block, '{', '}'):
        checks["latex_formulas"] = FAIL

## D. Required Sections
required = ["## Definition", "## Prerequisites", "## Mathematical Details"]
for section in required:
    if section not in file_content:
        checks["required_sections"] = FAIL

# Step 3: Generate Report
report = generate_validation_report(checks)

# Step 4: Return Result
if all(checks.values()):
    return "PASS"
else:
    return f"FAIL: {report}"
```

**Validation Report Example:**

```markdown
# Quality Validation Report

**File**: /home/kc-palantir/math-vault/Theorems/fubini-theorem.md
**Date**: 2025-10-14

## Summary
✅ PASSED

## Detailed Results

### YAML Frontmatter
✅ Frontmatter exists
✅ All required fields present
✅ Valid YAML syntax

### Wikilinks
✅ All wikilinks use [[kebab-case]] format
✅ 8 wikilinks found: measure-theory, lebesgue-integration, ...

### LaTeX Formulas
✅ 3 formulas found
✅ All delimiters balanced
✅ No syntax errors

### Content Structure
✅ All required sections present
✅ Sections are non-empty

## Conclusion
PASS - File meets all quality standards
```

**Tool Calls:**
```
1. Read (file to validate)
2. Grep (optional: search for patterns)
3. TodoWrite (track validation progress)
```

---

## Phase 4: 예제 추가

### Agent: example-generator

**Input:**
```python
Task(
    agent="example-generator",
    prompt="Add graded examples to /home/kc-palantir/math-vault/Theorems/fubini-theorem.md"
)
```

**Execution Steps (example_generator.py:44-270):**

```python
# Step 1: Read Existing File
file_content = read_file(file_path)
concept_difficulty = parse_yaml(file_content)["difficulty"]  # 8 (graduate)

# Step 2: Plan Example Suite
examples = [
    {"level": 1, "title": "Basic Application", "difficulty": "standard"},
    {"level": 2, "title": "Non-trivial Case", "difficulty": "intermediate"},
    {"level": 3, "title": "Theorem Application", "difficulty": "advanced"}
]

# Step 3: Generate Examples with Solutions

## Example 1: Basic Application
example_1 = """
### Example 1: Basic Application

**Problem**: Compute $\\int_0^1 \\int_0^1 xy \\, dy \\, dx$ using Fubini's Theorem.

**Solution**:

Step 1: Apply Fubini's Theorem
$$
\\int_0^1 \\int_0^1 xy \\, dy \\, dx = \\int_0^1 x \\left(\\int_0^1 y \\, dy\\right) dx
$$

Step 2: Evaluate inner integral
$$
\\int_0^1 y \\, dy = \\left[\\frac{y^2}{2}\\right]_0^1 = \\frac{1}{2}
$$

Step 3: Evaluate outer integral
$$
\\int_0^1 x \\cdot \\frac{1}{2} \\, dx = \\frac{1}{2} \\left[\\frac{x^2}{2}\\right]_0^1 = \\frac{1}{4}
$$

**Answer**: $\\frac{1}{4}$

**Key Insight**: Fubini allows us to compute iterated integrals by changing order of integration.
"""

# Step 4: Add Python/SymPy Implementation
python_code = """
### Python Implementation

```python
from sympy import symbols, integrate

x, y = symbols('x y')

# Define function
f = x * y

# Compute integral using Fubini
result = integrate(integrate(f, (y, 0, 1)), (x, 0, 1))
print(f"Result: {result}")  # Output: 1/4
```

**Output**:
```
Result: 1/4
```
"""

# Step 5: Insert Examples into Document
insertion_point = find_section(file_content, "## Examples")
if not insertion_point:
    insertion_point = find_section(file_content, "## Applications") - 1

new_content = insert_at(file_content, insertion_point, 
                        example_1 + example_2 + example_3 + python_code)

# Step 6: Save Updated File
edit_file(file_path, file_content, new_content)

# Step 7: Verify
verify_examples_added(file_path)
```

**Tool Calls:**
```
1. Read (existing file)
2. Edit (insert examples)
3. Bash (optional: run Python code to verify)
4. Read (verify changes)
5. TodoWrite (track progress)
```

**Final File Size:**
- Before: 3,245 bytes
- After: 6,789 bytes
- Examples added: 3
- Python code blocks: 1
- Practice problems: 2

---

## Complete Workflow Timeline

```
User Request
  │
  ├─> [0ms] Meta-Orchestrator: Parse request
  │
  ├─> [0-60s] Phase 0: Socratic Planner (if ambiguous)
  │     Optional: Multi-turn clarification dialogue
  │
  ├─> [0-2500ms] Phase 1: Research Agent
  │     ├─ Brave Search (5 parallel): 2000ms
  │     ├─ Context7: 300ms
  │     └─ JSON generation: 200ms
  │
  ├─> [2500-3000ms] Phase 2: Knowledge Builder
  │     ├─ YAML generation: 100ms
  │     ├─ Markdown body: 300ms
  │     └─ File save: 100ms
  │
  ├─> [3000-3300ms] Phase 3: Quality Agent
  │     ├─ File read: 50ms
  │     ├─ Validation: 200ms
  │     └─ Report generation: 50ms
  │
  └─> [3300-4500ms] Phase 4: Example Generator
        ├─ File read: 50ms
        ├─ Example generation: 1000ms
        └─ File edit: 150ms

Total: ~4,500ms (4.5 seconds)
```

---

## Error Handling

### Retry Logic (error_handler.py:220-292)

```python
@resilient_task(RetryConfig(max_retries=3, initial_delay=1.0))
async def execute_workflow_phase(agent: str, prompt: str):
    # Automatic retry with exponential backoff
    # 1st retry: 1s delay
    # 2nd retry: 2s delay
    # 3rd retry: 4s delay
    
    try:
        return await Task(agent=agent, prompt=prompt)
    except Exception as e:
        if should_retry(e):  # ConnectionError, TimeoutError, rate limits
            raise  # Retry
        else:
            escalate_to_human(e)  # Non-retryable errors
```

### Escalation (error_handler.py:295-338)

```
⚠️ HUMAN INTERVENTION REQUIRED
Agent: knowledge-builder
Task: fubini-theorem-doc-generation
Failed attempts: 3

Error history:
  1. [2025-10-14 22:30:15] LaTeX parse error: Unbalanced braces
  2. [2025-10-14 22:30:17] LaTeX parse error: Unbalanced braces
  3. [2025-10-14 22:30:21] LaTeX parse error: Unbalanced braces

Action Required: Review errors and manually resolve
```

---

## Optimizations

### 1. Parallel Research Queries (scalable.pdf p4)
```python
# 90% latency reduction
results = await asyncio.gather(
    brave_search("query1"),
    brave_search("query2"),
    brave_search("query3"),
    brave_search("query4"),
    brave_search("query5")
)
# 5 × 2000ms sequential = 10,000ms
# 1 × 2000ms parallel = 2,000ms (80% reduction)
```

### 2. Direct Data Passing
```python
# Eliminates 3 file I/O operations (60ms saved per concept)
```

### 3. Caching
```python
# Check if research already exists
if exists(f"research-reports/{concept_id}.json"):
    research = load_cached_research(concept_id)  # Skip Phase 1
```

---

**Document Status:** ✅ Complete  
**Next:** WORKFLOW-2-DEPENDENCY-MAPPING.md

