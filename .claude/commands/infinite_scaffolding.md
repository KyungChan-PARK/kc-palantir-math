# INFINITE SCAFFOLDING LOOP COMMAND

Think deeply about this infinite scaffolding generation task. You are about to orchestrate parallel AI agents to generate multiple unique, high-quality scaffolding variations for math problems.

**Variables:**

spec_file: $ARGUMENTS
problem_image: $ARGUMENTS  
count: $ARGUMENTS

**ARGUMENTS PARSING:**
Parse the following arguments from "$ARGUMENTS":
1. `spec_file` - Path to scaffolding specification (e.g., specs/scaffolding_spec_v1.md)
2. `problem_image` - Path to math problem image (e.g., sample.png, 3.png)
3. `count` - Number of variations (1-N or "infinite")

**PHASE 1: SPECIFICATION ANALYSIS**

Read and deeply understand the specification file at `spec_file`. This defines:
- Quality criteria for scaffolding (cognitive progression, difficulty curve, hint effectiveness)
- Variation dimensions available (Socratic, Visual, Algebraic, Metacognitive, etc.)
- Output format requirements (JSON structure with validation schema)
- Success metrics (teacher ratings, student performance, pattern reusability)

Think carefully about how each variation dimension creates pedagogically distinct scaffolding.

**PHASE 2: PROBLEM ANALYSIS (Reuse Existing Workflow)**

Use existing tools and workflows for problem analysis:

1. **OCR Extraction**: Call `tools/mathpix_ocr_tool.py::extract_math_from_image(problem_image)`
   - Extracts LaTeX and text with 99.9% confidence
   - Returns: `{text, latex, confidence, success}`

2. **Concept Matching**: Call `workflows/concept_matcher.py::identify_concepts(problem_data, top_k=5)`
   - Matches against 841 middle school math concepts
   - Returns: Top-k concepts with relevance scores

3. **Pattern Query**: Call `workflows/math_scaffolding_workflow.py::query_neo4j_patterns(concepts)`
   - Queries learned patterns from Neo4j
   - Returns: Applicable patterns for reuse

**Shared Context Preparation:**
Create a shared context dict containing:
```python
shared_context = {
    "problem_text": ocr_result["text"],
    "problem_latex": ocr_result["latex"],
    "concepts": matched_concepts,
    "existing_patterns": neo4j_patterns,
    "spec_requirements": spec_parsed
}
```

**PHASE 3: OUTPUT DIRECTORY RECONNAISSANCE**

Analyze output directory `data/scaffolding_variations/{problem_id}/`:
- List all existing variation files: `scaffolding_*_v*.json`
- Identify highest iteration number currently present
- Analyze variation dimensions already used
- Determine which dimensions are underexplored
- Plan which dimensions to assign to new variations

**PHASE 4: VARIATION STRATEGY**

Based on spec and existing variations:
- Determine starting iteration number (highest + 1)
- Select N unique variation dimensions for this wave
- Assign each dimension to a specific sub-agent
- Plan how each variation will differ pedagogically
- If count is "infinite", prepare for wave-based continuous generation

**Variation Dimension Assignment:**
```
Agent 1 → Socratic Depth: Maximize questioning, student discovery
Agent 2 → Visual Emphasis: Geometric/graphical reasoning primacy  
Agent 3 → Algebraic Rigor: Symbolic manipulation focus
Agent 4 → Metacognitive: "Why" questions and reflection
Agent 5 → Minimal Hints: Challenge mode, student independence
Agent 6 → Conceptual Bridges: Cross-concept connections
Agent 7 → Real-World: Application contexts
```

**PHASE 5: PARALLEL SUB-AGENT COORDINATION**

Deploy multiple scaffolding generation agents in parallel for maximum diversity:

**Sub-Agent Distribution Strategy:**
- For count 1-3: Launch all agents simultaneously
- For count 4-10: Launch in batches of 3-4 agents
- For "infinite": Launch waves of 3 agents, monitor context, spawn new waves

**Agent Assignment Protocol:**

Each Sub-Agent receives via Task tool:

```python
Task(
    subagent_type="problem-scaffolding-generator",
    prompt=f"""
TASK: Generate scaffolding variation {iteration_number} for problem

PROBLEM CONTEXT:
- Text: {problem_text}
- LaTeX: {problem_latex}  
- Concepts: {matched_concepts}
- Existing Patterns: {neo4j_patterns}

VARIATION DIRECTIVE:
You are Sub Agent {agent_index} generating variation {iteration_number}.
Your UNIQUE VARIATION DIMENSION: {assigned_dimension}

DIMENSION FOCUS: {dimension_description}
- {specific_instructions_for_this_dimension}
- Ensure your scaffolding embodies this dimension distinctly
- Different from variations: {list_of_existing_variations}

REQUIREMENTS:
1. Generate 6-12 progressive sub-problem steps
2. Each step = measurable problem with expected answer
3. Follow specification quality criteria exactly
4. Embody your assigned variation dimension throughout
5. Ensure uniqueness from existing variations
6. Output as JSON matching specification schema

DELIVERABLE: Single JSON file with complete scaffolding
""",
    description=f"Generate scaffolding variation {iteration_number} ({assigned_dimension})"
)
```

**Parallel Execution Management:**
```python
# Launch all assigned sub-agents simultaneously
tasks = [
    client.delegate_to_agent(agent_spec)
    for agent_spec in agent_assignments
]

# Wait for all to complete (parallel execution)
results = await asyncio.gather(*tasks)

# Validate each result
for result in results:
    validate_spec_compliance(result)
    validate_uniqueness(result, existing_variations)
    save_variation(result, output_dir)
```

**PHASE 6: INFINITE MODE ORCHESTRATION**

For infinite generation mode, orchestrate continuous parallel waves:

**Wave-Based Generation:**
1. **Wave Planning**: Determine next wave size (3 agents) based on context capacity
2. **Context Refresh**: Prepare updated shared context with new patterns from previous wave
3. **Progressive Dimensions**: Each wave explores more advanced dimension combinations
   - Wave 1: Single dimensions (Socratic, Visual, Algebraic)
   - Wave 2: Dual combinations (Socratic+Visual, Algebraic+Metacognitive)
   - Wave 3: Triple combinations (Visual+Metacognitive+Real-world)
4. **Context Monitoring**: Track total context usage across all agents
5. **Graceful Conclusion**: When approaching limits, complete current wave and summarize

**Infinite Execution Cycle:**
```
WHILE context_capacity > threshold AND quality_maintained:
    1. Assess current variations generated
    2. Extract emerging meta-patterns from recent wave
    3. Evolve specification based on patterns
    4. Plan next wave (3 agents, advanced dimensions)
    5. Assign progressively sophisticated variation directives
    6. Launch parallel sub-agent wave
    7. Monitor wave completion and quality
    8. Update shared context with new learnings
    9. Evaluate context capacity remaining
    10. If sufficient + quality good: Continue to next wave
    11. If approaching limits OR quality declining: Complete and summarize
```

**Progressive Sophistication Strategy:**
- **Wave 1**: Single variation dimensions (7 variations)
- **Wave 2**: Dual dimension combinations (choose best 5 from wave 1)
- **Wave 3**: Triple dimensions + multi-modal (synthesize top patterns)
- **Wave 4**: Adaptive + performance-cluster differentiation
- **Wave N**: Revolutionary pedagogies (game-based, error-driven, peer teaching)

**Context Optimization:**
- Each wave uses fresh agent instances (avoid context accumulation)
- Main orchestrator maintains lightweight state (variation index, patterns discovered)
- Progressive summarization of completed variations
- Strategic pruning of less effective dimensions in later waves

**PHASE 7: PARALLEL FEEDBACK COLLECTION**

Coordinate feedback collection across all variations:

**Parallel Feedback Strategy:**
```python
# After wave completes, collect feedback in parallel
feedback_tasks = [
    collect_feedback_for_variation(variation_id)
    for variation_id in completed_variations
]

feedback_results = await asyncio.gather(*feedback_tasks)
```

**Teacher Feedback Format:**
- Quick rating mode: Rate all N variations (1-5 scale) rapidly
- Detailed mode: Full feedback on top-rated variations only
- Comparative mode: Rank variations by preference, comment on differences

**Feedback Synthesis:**
- Identify highest-rated variation dimensions
- Extract common strengths across high-rated variations
- Identify weaknesses to avoid in future waves
- Generate meta-patterns from cross-variation analysis

**PHASE 8: META-PATTERN EXTRACTION**

Extract higher-order patterns from variation analysis:

**Meta-Pattern Types:**
1. **Dimension Effectiveness**: Which variation dimensions consistently rate high
2. **Combination Synergies**: Which dimension pairs work best together
3. **Concept-Specific Preferences**: Optimal dimensions per math concept
4. **Structural Patterns**: Common high-quality step sequences
5. **Progressive Discovery**: How specification evolution improves quality

**Meta-Pattern Storage:**
```python
meta_pattern = {
    "id": "mp_visual_socratic_synergy",
    "type": "dimension_combination",
    "pattern": "Visual + Socratic combination scores 15% higher than either alone",
    "evidence": [variation_2, variation_8, variation_15],
    "avg_rating": 4.8,
    "applicable_concepts": ["geometry", "functions", "graphs"],
    "discovered_wave": 2,
    "confidence": 0.95
}
```

Store to Neo4j as `:MetaPattern` nodes with `:SYNTHESIZED_FROM` relationships to source patterns.

**EXECUTION PRINCIPLES:**

**Quality & Uniqueness:**
- Each variation must be genuinely unique (>0.8 similarity threshold)
- All variations must meet specification quality criteria
- Uniqueness in pedagogy, not just wording
- Build upon shared problem understanding while varying approach

**Parallel Coordination:**
- Deploy sub-agents with distinct, explicit variation directives
- Assign dimensions that maximize creative diversity
- Ensure no two agents receive same dimension in a wave
- Coordinate timing to prevent race conditions in file writes

**Scalability & Efficiency:**
- Wave-based generation for infinite mode (3 agents per wave)
- Reuse shared context (OCR, concepts, patterns) across all agents
- Progressive sophistication: each wave builds on previous learnings
- Balance parallel speed with quality and coordination overhead

**Agent Management:**
- Provide each sub-agent with complete shared context
- Give explicit uniqueness directive with existing variations list
- Handle agent failures gracefully (reassign dimension to backup agent)
- Validate all outputs before accepting into variation pool

**ULTRA-THINKING DIRECTIVE:**

Before beginning generation, engage in extended thinking about:

**Specification & Pedagogy:**
- Deeper implications of each variation dimension
- How to create meaningful pedagogical differences
- What makes scaffolding effective for different learning styles
- Balance between consistency (same problem) and diversity (different approaches)

**Parallel Strategy:**
- Optimal sub-agent distribution for requested count
- How to assign dimensions to maximize pedagogical diversity
- Wave sizing and timing for infinite mode
- Context management across multiple parallel agents

**Coordination Challenges:**
- How to prevent pedagogical overlap despite parallel execution
- Strategies for ensuring genuine uniqueness across variations
- Managing JSON file writes with concurrent agents
- Quality control for parallel outputs

**Infinite Mode Optimization:**
- Wave-based generation patterns for sustained high-quality output
- Progressive sophistication strategies across multiple waves
- Context capacity monitoring and graceful conclusion planning
- Balancing speed of parallel generation with depth of pedagogical innovation

**Meta-Learning:**
- How to extract patterns from patterns (meta-patterns)
- Which variation dimensions to prioritize in later waves
- How to evolve specification based on emerging insights
- Strategies for continuous quality improvement across iterations

**Risk Mitigation:**
- Handling agent failures and variation reassignment
- Ensuring coherent overall progression despite parallel execution
- Managing context window limits across the entire wave system
- Maintaining specification compliance across all parallel outputs
- Preventing quality degradation in later waves

Begin execution with deep analysis of these parallel pedagogical challenges and proceed systematically through each phase, leveraging sub-agents for maximum creative diversity and teaching effectiveness.

