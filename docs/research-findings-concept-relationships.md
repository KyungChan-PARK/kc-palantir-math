# Research Findings: Mathematical Concept Relationship Types

**DATE**: 2025-10-14
**RESEARCH METHOD**: Brave Search + Literature Review
**PURPOSE**: Validate and refine our v0.1 taxonomy with existing academic research

---

## Executive Summary

Research reveals that mathematical concept relationships have been extensively studied in:
1. **Educational Ontologies** (OntoMathEdu, Math-KG)
2. **Curriculum Design** (Learning Progressions, Vertical/Horizontal Alignment)
3. **Knowledge Graphs** (Math-KG with 8,019 triples)
4. **Educational Platforms** (Khan Academy Knowledge Map)

Key finding: **Math-KG defines 6 core relation types** with 8,019 triples across 1,905 entities.

---

## 1. Math-KG: A Reference Implementation

### Source
- Paper: "Math-KG: Construction and Applications of Mathematical Knowledge Graph" (arXiv:2205.03772)
- Dataset: 1,905 entities, 8,019 triples
- Entities: 1,337 concepts + 568 theorems

### Six Relation Types

| Relation Type | Triple Count | Percentage | Description |
|---------------|--------------|------------|-------------|
| **Dependencies** | 2,016 | 25.1% | Prerequisite relationships |
| **Affiliation** | 2,609 | 32.5% | Domain/category membership |
| **Has Properties** | 2,524 | 31.5% | Concept characteristics |
| **Synonyms** | 493 | 6.1% | Alternative names/notations |
| **Antisense** | 301 | 3.8% | Opposite/complementary concepts |
| **Equivalence** | 76 | 0.9% | Equivalent formulations |

**Key Insight**: Dependencies (prerequisites) are only 25% of relationships. Domain affiliation and properties are equally important.

### Bidirectional Nature
All 6 relations have two directions, creating 12 types of edges total:
- A depends on B ↔ B is depended by A
- A is affiliated with B ↔ B contains A
- Etc.

---

## 2. OntoMathEdu: Educational Math Ontology

### Source
- Paper: "Prerequisite Relationships of the OntoMathEdu Educational Mathematical Ontology" (Springer 2021)
- Focus: Educational mathematics knowledge organization

### Prerequisite Definition

**Definition**: Concept A is a prerequisite for Concept B if a learner **must study** Concept A before approaching Concept B.

### Two Approaches to Prerequisites

#### 2.1 Direct Relationships
Explicitly establish `prerequisite_of` relationship between concepts.

#### 2.2 Educational Level Arrangement
Indirectly define prerequisites by arranging concepts across educational levels:
- Elementary → Middle → High → University
- Grade 1 → Grade 2 → Grade 3 → ...

**Implication**: Prerequisites can be **explicit** (A → B) or **implicit** (A is taught before B in curriculum).

### Validation Methodology: OntoClean

OntoMathEdu uses **OntoClean methodology** to validate taxonomic relationships:
1. **Identity Conditions**: What makes a concept unique?
2. **Subsumption vs Instantiation**: "is-a" vs "instance-of"
3. **Subtopic vs Prerequisite**: Related but distinct

**Finding**: Validation revealed errors in initial taxonomy, including:
- Incompatible identity conditions
- Confusion between subsumption and instantiation
- Conflation of "subtopic" with "prerequisite"

---

## 3. Curriculum Design: Vertical & Horizontal Relationships

### Source
- Multiple curriculum design frameworks
- Freudenthal/Treffers Mathematisation Theory

### Vertical vs Horizontal: Two Interpretations

#### 3.1 Curriculum Alignment (Structural)

**Vertical Alignment**:
- Concept progression across **grade levels**
- Example: Grade 1 addition → Grade 2 multiplication → Grade 3 division
- Ensures foundational skills build to complex concepts

**Horizontal Alignment**:
- Connections **within same grade level**
- Example: Grade 8 algebra concepts connect to Grade 8 geometry
- Ensures consistent standards across subjects

#### 3.2 Mathematisation Process (Cognitive)

**Horizontal Mathematisation**:
- Organizing real-world contexts
- Making them amenable to mathematical treatment
- Using existing mathematical tools
- Example: Word problems → equations

**Vertical Mathematisation**:
- Level-raising through organizing, symbolizing
- Building formal models from paradigmatic situations
- Increasing abstraction
- Example: Concrete counting → abstract number → set cardinality

**Key Distinction**:
- Structural: Curriculum organization (what is taught when)
- Cognitive: Thinking processes (how students learn)

---

## 4. Learning Progressions

### Source
- "Learning Progressions Frameworks Designed for Use with..." (NCIEA)
- Various state education departments (Ohio, California)

### Definition
**Learning Progression**: A fine-grain map of possible learning pathways a child may take within a particular domain.

### Key Characteristics
1. **Research-Based**: How understanding develops over time with quality instruction
2. **Linked Framework**: Curriculum + instruction + assessment + learning levels
3. **Not Standards-Driven**: Based on cognitive development, not policy

### Application to Concept Relationships
Learning progressions reveal:
- **Sequential Dependencies**: Must learn A before B
- **Developmental Readiness**: Cognitive prerequisites (not just logical)
- **Alternative Pathways**: Multiple routes to same concept
- **Sophistication Levels**: From intuitive → procedural → conceptual → formal

**Implication**: Prerequisites should consider **cognitive development**, not just logical necessity.

---

## 5. Co-Requisites in Higher Education

### Source
- Multiple higher education institutions' course catalogs
- Complete College America research

### Definitions

**Prerequisite**: Course/skill required **before** enrolling (sequential)

**Co-Requisite**: Course taken **concurrently** with another course (parallel support)

**Prereq or Coreq**: Flexible - can be taken before or concurrently

### Co-Requisite Models

#### Traditional Model (Sequential)
```
Prerequisite Course (Quarter 1)
    ↓
College-Level Course (Quarter 2)
```

#### Co-Requisite Model (Concurrent)
```
Support Course ←→ College-Level Course (Same Quarter)
```

### Effectiveness Data
Co-requisite models show dramatic improvements:
- Traditional: 12% college math completion
- Co-requisite: 61% college math completion
- 5x improvement in gateway course completion

**Implication**: Some "prerequisites" are better taught **concurrently** rather than sequentially.

---

## 6. Khan Academy Knowledge Map (Historical)

### Source
- Khan Academy community forums
- Educational technology discussions

### What It Was
- Spider-web visualization of mathematical concepts
- Showed incremental progress
- Displayed connections and dependencies between topics
- "Building blocks build on other building blocks"

### Why It Matters
- Demonstrated **user demand** for dependency visualization
- Showed **pedagogical value** of seeing relationships
- Community actively recreated it after removal

### Current Status
- Removed (Google Maps API deprecated)
- Sal Khan announced: "Coming back in ~1 year using generative AI"

**Implication**: Dependency mapping has proven educational value and user demand.

---

## 7. Bloom's Taxonomy in Mathematics

### Source
- Bloom's Taxonomy interpreted for mathematics (University of Toronto)
- Webb's Depth of Knowledge

### Hierarchical Learning
Bloom's Taxonomy shows **prerequisite structure in cognitive processes**:

```
Lower Levels (Prerequisites for Higher)
↓
Remember → Understand → Apply → Analyze → Evaluate → Create
```

**In Mathematics**:
- Remember: Definitions, formulas
- Understand: Explain concepts
- Apply: Use in problems
- Analyze: Break down proofs
- Evaluate: Judge solution validity
- Create: Develop new proofs

**Implication**: Cognitive level is a dimension of prerequisites (can't analyze before understanding).

---

## 8. Research Gaps Identified

### What Existing Research Lacks

1. **Comprehensive Taxonomy**
   - Most focus on prerequisites only
   - Math-KG has 6 types but lacks granularity
   - No standard for "extension", "formalization", "application"

2. **Pedagogical vs Logical**
   - Confusion between "must learn first" (pedagogical) and "logically requires" (logical)
   - OntoMathEdu mixes both

3. **Cross-Level Relationships**
   - Little research on elementary → middle → high → university
   - Most focus on single education level

4. **Quantitative Measures**
   - No standard for "strength" of prerequisite
   - Essential vs helpful not formalized

5. **Implicit Prerequisites**
   - How to handle unstated assumptions?
   - Example: "Triangle angles sum to 180°" assumes Euclidean geometry

---

## Comparison with Our v0.1 Taxonomy

### Mapping Existing Types to Our Taxonomy

| Math-KG Type | Our v0.1 Type | Match Quality | Notes |
|--------------|---------------|---------------|-------|
| Dependencies | Prerequisite | ✅ Exact | Core concept |
| Equivalence | Mutual Definition | ✅ Good | Slightly different emphasis |
| Synonyms | — | ❌ Missing | Need to add |
| Antisense | — | ⚠️ Partial | Similar to Parallel (opposite) |
| Affiliation | Application? | ⚠️ Unclear | Domain membership ≠ application |
| Has Properties | — | ❓ Different | Properties vs relationships |

### Our Unique Contributions

Types **not found** in existing research:
1. **Extension** (domain extension, generalization)
2. **Formalization** (intuition → rigor progression)
3. **Abstraction Level** (vertical cognitive progression)
4. **Essential vs Optional** (prerequisite strength)
5. **Inverse Operation** (mathematical duality)

### Gaps in Our v0.1

Types **missing** from our taxonomy:
1. **Synonyms** (alternative names/notations)
2. **Affiliation** (domain/category membership)
3. **Has Properties** (if we want concept characteristics)

---

## Key Insights for Refinement

### 1. Distinguish Relationship Dimensions

Our taxonomy conflates multiple dimensions:

**Dimension 1: Temporal**
- Sequential (prerequisite)
- Concurrent (co-requisite)
- Independent

**Dimension 2: Logical**
- Necessary (hard prerequisite)
- Helpful (soft prerequisite)
- Optional (background)

**Dimension 3: Cognitive**
- Same abstraction level (horizontal)
- Different abstraction levels (vertical)

**Dimension 4: Domain**
- Within-domain (algebra → algebra)
- Cross-domain (algebra → physics)

### 2. Add Missing Types

From research, should add:
- **Synonyms/Notation**: Alternative representations
- **Domain Membership**: Concept belongs to field/category

### 3. Clarify Existing Types

**Prerequisite** needs sub-classification:
- Logical prerequisite (definition requires)
- Cognitive prerequisite (developmental readiness)
- Pedagogical prerequisite (curriculum sequencing)
- Tool prerequisite (needed for method)

**Application** vs **Affiliation**:
- Application: Using A to solve problems in B
- Affiliation: A belongs to category B

### 4. Bidirectional Relationships

Math-KG shows all relations are bidirectional:
- A prerequisite_of B ↔ B depends_on A
- Should we model both directions explicitly?

---

## Recommendations for v0.2 Taxonomy

### 1. Core Relationship Types (10 → 12)

**Keep from v0.1:**
1. Prerequisite (refine subtypes)
2. Co-requisite
3. Inverse Operation
4. Extension
5. Formalization
6. Application
7. Mutual Definition
8. Abstraction Level
9. Essential vs Optional (as property, not type)

**Add from research:**
10. **Synonyms/Notation** - Alternative representations
11. **Domain Membership** - Belongs to field/category
12. **Complementary** - Opposite concepts (antisense)

**Merge:**
- Parallel Concepts → absorbed into other types

### 2. Add Relationship Properties

Every relationship should have:
- `direction`: unidirectional vs bidirectional
- `strength`: essential | recommended | helpful
- `temporal`: sequential | concurrent | independent
- `cognitive_level`: same_level | level_raising
- `domain_scope`: within | cross

### 3. Validation Protocol

Adopt OntoClean-style validation:
- Identity conditions for concepts
- Distinguish subsumption vs instantiation
- Verify prerequisite transitivity
- Check for circular dependencies

### 4. Multi-Level Framework

Explicitly model:
- Elementary (Grades 1-6)
- Middle (Grades 7-9)
- High (Grades 10-12)
- University (Undergrad)
- University (Graduate)

Cross-level relationships need special handling.

---

## Next Steps

1. **Refine v0.1 → v0.2** based on research findings
2. **Add missing types**: Synonyms, Domain Membership, Complementary
3. **Add relationship properties**: direction, strength, temporal, cognitive_level
4. **Create examples** for each type using 841 middle school concepts
5. **Validate taxonomy** using OntoClean-style methodology
6. **Build relationship definition agent** using refined taxonomy
7. **Test on sample** (20 concepts) before full deployment

---

## References

1. Math-KG: Construction and Applications (arXiv:2205.03772)
2. OntoMathEdu: Educational Mathematical Ontology (Springer 2021)
3. Learning Progressions Frameworks (NCIEA)
4. OntoClean Methodology (Guarino & Welty)
5. Khan Academy Knowledge Map (Community Archives)
6. Bloom's Taxonomy for Mathematics (U. Toronto)
7. Co-Requisite Models (Complete College America)
8. Vertical/Horizontal Mathematisation (Freudenthal/Treffers)

---

**This document provides the research foundation for refining our concept relationship taxonomy.**
