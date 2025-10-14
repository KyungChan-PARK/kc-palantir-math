# Mathematical Concept Relationship Types

**VERSION**: 0.2.0
**DATE**: 2025-10-14
**PURPOSE**: Define relationship types for math education dependency mapping (Elementary through University)
**BASED ON**: Research findings from Math-KG, OntoMathEdu, Learning Progressions, Co-requisite Models

---

## Changes from v0.1

### Added Relationship Types:
- **Synonyms/Notation**: Alternative representations (Math-KG: 6.1% of relationships)
- **Domain Membership**: Category/field belonging (Math-KG: 32.5%, most common)
- **Complementary**: Opposite/complementary concepts (Math-KG Antisense: 3.8%)
- **Equivalence**: Equivalent formulations (Math-KG: 0.9%, separated from Mutual Definition)

### Removed as Relationship Types:
- **Essential vs Optional**: Moved to relationship property `strength`
- **Parallel Concepts**: Integrated into Complementary

### Added Relationship Properties:
All relationships now have 5 properties:
1. **Direction**: unidirectional | bidirectional
2. **Strength**: essential | recommended | helpful
3. **Temporal**: sequential | concurrent | independent
4. **Cognitive_level**: same_level | level_raising
5. **Domain_scope**: within_domain | cross_domain

---

## Relationship Type Definitions

### 1. PREREQUISITE (선수 개념)

**Definition**: Concept A is a prerequisite for Concept B if understanding A is **logically, cognitively, or pedagogically necessary** to understand B.

**Research Validation**:
- Math-KG: 2,016 "Dependencies" triples (25.1%)
- OntoMathEdu: "A is prerequisite for B if learner must study A before B"
- Finding: Prerequisites are only ~25% of all relationships

**Subtypes**:

#### 1.1 Logical Prerequisite
A's definition is required in B's definition.
- Example: "소수 정의" → "소인수분해 정의"
- Properties: {direction: unidirectional, strength: essential, temporal: sequential, cognitive_level: same_level, domain_scope: within_domain}

#### 1.2 Cognitive Prerequisite
Developmental readiness - student must reach certain cognitive maturity.
- Example: "구체물 세기" (elem-1) → "추상적 자연수" (middle-1)
- Properties: {direction: unidirectional, strength: essential, temporal: sequential, cognitive_level: level_raising, domain_scope: within_domain}

#### 1.3 Pedagogical Prerequisite
Curriculum sequencing - taught before for optimal learning, but not logically required.
- Example: "일차함수" → "이차함수" (pedagogically sequenced, but could be taught independently)
- Properties: {direction: unidirectional, strength: recommended, temporal: sequential, cognitive_level: same_level, domain_scope: within_domain}

#### 1.4 Tool Prerequisite
Method/algorithm requires prior knowledge as a tool.
- Example: "소인수분해" → "소인수분해를 이용한 최대공약수 구하기"
- Properties: {direction: unidirectional, strength: essential, temporal: sequential, cognitive_level: same_level, domain_scope: within_domain}

**Examples from 841 Concepts**:

1. **middle-1-1-ch1-1.1.1** (소수 정의) → **middle-1-1-ch1-1.3.1** (소인수분해 정의)
   - Type: Logical prerequisite
   - Reason: Cannot define prime factorization without knowing "prime"
   - Confidence: 0.98

2. **middle-1-1-ch1-1.2.1** (거듭제곱 정의) → **middle-1-1-ch1-1.3.4** (지수를 이용한 간단한 표기)
   - Type: Logical prerequisite (notation)
   - Reason: Need exponent notation to express 2² × 3
   - Confidence: 0.95

3. **middle-1-1-ch1-1.3.1** (소인수분해) → **middle-1-1-ch1-1.4.3** (소인수분해를 이용한 GCD)
   - Type: Tool prerequisite
   - Reason: This method requires factorization as a tool
   - Confidence: 0.90

4. **elem-6** (분수의 나눗셈) → **middle-1** (유리수)
   - Type: Cognitive prerequisite
   - Reason: Concrete fraction operations → abstract rational number concept
   - Confidence: 0.85

5. **middle-2** (일차방정식) → **high-1** (이차방정식)
   - Type: Pedagogical prerequisite
   - Reason: Curriculum progression, but not logically required
   - Confidence: 0.70

---

### 2. CO-REQUISITE (공동 필수)

**Definition**: Concepts that should be learned **simultaneously** or in **close temporal proximity** for optimal understanding.

**Research Validation**:
- Complete College America: Co-requisite models show **5x improvement** (12% → 61% completion)
- Finding: Some "prerequisites" are better taught **concurrently**

**Properties Template**: {direction: bidirectional, strength: recommended, temporal: concurrent, cognitive_level: same_level, domain_scope: within_domain}

**Examples from 841 Concepts**:

1. **high-1** (삼각함수 정의) ↔ **high-1** (단위원)
   - Reason: Unit circle provides geometric meaning; trig functions give it practical use
   - Learning together enhances both concepts

2. **high-2** (미분 - 순간변화율) ↔ **high-2** (미분 - 접선의 기울기)
   - Reason: Two interpretations of same concept
   - Should be presented together for complete understanding

3. **middle-1-1-ch1-1.4.1** (공약수) ↔ **middle-1-1-ch1-1.5.1** (공배수)
   - Reason: Structurally symmetric concepts
   - Comparing them enhances understanding

4. **middle-1-1-ch3** (평균 Mean) ↔ **middle-1-1-ch3** (중앙값 Median) ↔ **middle-1-1-ch3** (최빈값 Mode)
   - Reason: Alternative methods for central tendency
   - Learning together allows comparison

---

### 3. INVERSE OPERATION (역연산)

**Definition**: Operations that "undo" each other.

**Properties Template**: {direction: bidirectional, strength: essential, temporal: concurrent, cognitive_level: same_level, domain_scope: within_domain}

**Examples**:

1. **high-2** (미분) ↔ **high-2** (적분)
   - Fundamental Theorem of Calculus
   - While inverse, differentiation usually taught first

2. **elem-1** (덧셈) ↔ **elem-1** (뺄셈)
   - Subtraction undoes addition

3. **elem-2** (곱셈) ↔ **elem-3** (나눗셈)
   - Division undoes multiplication

4. **middle-2** (거듭제곱) ↔ **middle-2** (제곱근)
   - Root undoes power

5. **high-2** (로그) ↔ **high-2** (지수)
   - Logarithm undoes exponential

---

### 4. EXTENSION (확장)

**Definition**: Concept B **extends** Concept A to a broader domain or adds new properties. B contains A as a special case.

**Research Note**: This is our **unique contribution** - not found in Math-KG or OntoMathEdu.

**Properties Template**: {direction: unidirectional, strength: recommended, temporal: sequential, cognitive_level: level_raising, domain_scope: within_domain}

**Examples**:

1. **Number System Extension Chain**:
   - 자연수 (elem-1) → 정수 (middle-1) → 유리수 (middle-1) → 실수 (high-1) → 복소수 (high-2)
   - Each extends previous, containing it as special case

2. **Equation Generalization**:
   - 일차방정식 (middle-1) → 이차방정식 (middle-3) → 다항방정식 (high-1)
   - From degree 1 → 2 → n

3. **Geometry Extension**:
   - 평면기하 (middle-2) → 입체기하 (middle-3) → 해석기하 (high-1)
   - 2D → 3D → coordinate system

4. **Function Extension**:
   - 일차함수 (middle-2) → 이차함수 (middle-3) → 다항함수 (high-1) → 초월함수 (high-2)
   - Linear → quadratic → polynomial → transcendental

---

### 5. FORMALIZATION (형식화)

**Definition**: Concept B provides **rigorous formal definition** of an intuitive idea in Concept A. Progressive formalization across education levels.

**Research Connection**: Related to Freudenthal's **Vertical Mathematisation** (level-raising through symbolizing and formalizing).

**Properties Template**: {direction: unidirectional, strength: recommended, temporal: sequential, cognitive_level: level_raising, domain_scope: within_domain}

**Examples**:

1. **Area Concept Formalization**:
   - 넓이 (elem-3: 직사각형 세기) → 넓이 (middle-1: 공식 적용) → 넓이 (high-2: 적분으로 정의) → 넓이 (univ: Lebesgue 측도)
   - Concrete → procedural → analytical → measure-theoretic

2. **Fraction to Rational Number**:
   - 분수 계산 (elem-4-6: 규칙 적용) → 유리수 (middle-1-2: 체의 성질) → 유리수체 (univ: 대수적 구조)
   - Procedural → axiomatic → abstract algebra

3. **Limit Formalization**:
   - 극한 (high-2: 직관적 "접근") → 극한 (univ: ε-δ 정의)
   - Intuitive → rigorous

4. **Function Formalization**:
   - 패턴 찾기 (elem-5) → 일차함수 (middle-2) → 함수 일반 (high-1) → 사상 (univ) → 함자 (univ-advanced)
   - Pattern → specific function → general function → mapping → functor

---

### 6. APPLICATION (응용)

**Definition**: Concept B applies the principles of Concept A to solve specific problems or domains.

**Distinction from Domain Membership**:
- Application: Using A to solve problems in B
- Domain Membership: A belongs to category B

**Research Note**: Math-KG has "Affiliation" (32.5%), but it means category membership, not application.

**Properties Template**: {direction: unidirectional, strength: helpful, temporal: sequential, cognitive_level: same_level, domain_scope: varies}

**Examples**:

1. **middle-2** (피타고라스 정리) → **middle-3** (좌표평면에서 두 점 사이 거리)
   - Within-domain application
   - Properties: {domain_scope: within_domain}

2. **middle-3** (이차함수) → **high-physics** (포물선 운동)
   - Cross-domain application
   - Properties: {domain_scope: cross_domain}

3. **middle-1** (소인수분해) → **middle-1** (최대공약수/최소공배수 구하기)
   - Tool application within same chapter

4. **high-1** (삼각함수) → **high-physics** (진동, 파동)
   - Cross-domain to physics

5. **high-2** (미적분) → **engineering** (최적화 문제)
   - Cross-domain to engineering

---

### 7. MUTUAL DEFINITION (상호 정의)

**Definition**: Concepts defined **in terms of each other** as logical complements within a classification.

**Distinction from Equivalence**:
- Mutual Definition: Complementary definitions (A = not B)
- Equivalence: Same concept, different formulations

**Properties Template**: {direction: bidirectional, strength: essential, temporal: concurrent, cognitive_level: same_level, domain_scope: within_domain}

**Examples**:

1. **middle-1-1-ch1-1.1.1** (소수) ↔ **middle-1-1-ch1-1.1.2** (합성수)
   - "Composite = natural number that is not prime (excluding 1)"
   - Defining one defines the other

2. **middle-1** (유리수) ↔ **high-1** (무리수)
   - "Irrational = real number that is not rational"

3. **high-1** (정의역 Domain) ↔ **high-1** (치역 Range)
   - Function concept requires both

4. **middle-2** (예각) ↔ **middle-2** (둔각) ↔ **middle-2** (직각)
   - Angle classification: 0°<acute<90°=right<obtuse<180°

---

### 8. ABSTRACTION LEVEL (추상화 수준)

**Definition**: The same underlying concept at different levels of abstraction. Vertical progression from concrete to abstract.

**Research Connection**:
- Freudenthal's **Vertical Mathematisation** (level-raising)
- Bloom's Taxonomy (prerequisite structure in cognitive processes)

**Properties Template**: {direction: unidirectional, strength: recommended, temporal: sequential, cognitive_level: level_raising, domain_scope: within_domain}

**Examples**:

1. **Counting Abstraction Hierarchy**:
   - 구체물 세기 (elem-1) → 자연수 (middle-1) → 집합의 원소 개수 (high-1) → 기수 Cardinal (univ)
   - Concrete objects → abstract numbers → cardinality → transfinite cardinals

2. **Function Abstraction Hierarchy**:
   - 패턴 찾기 (elem-5) → 일차함수 (middle-2) → 함수 일반 (high-1) → 사상 Mapping (univ) → 함자 Functor (univ-advanced)
   - Pattern recognition → linear function → general function → mapping → category theory

3. **Addition Abstraction**:
   - 손가락으로 세기 (elem-1) → 덧셈 기호 + (elem-1) → 이항연산 (middle-1) → 군 연산 (univ)
   - Physical counting → symbolic operation → binary operation → group operation

4. **Shape Abstraction**:
   - 구체적 삼각형 그림 (elem-2) → 삼각형 정의 (middle-1) → 다각형 일반화 (middle-2) → 위상공간 (univ)
   - Concrete triangle → definition → polygon → topological space

---

### 9. COMPLEMENTARY (보완 개념)

**Definition**: Concepts that represent **opposite** or **complementary** aspects of a classification, alternative methods, or dual perspectives.

**Research Validation**: Math-KG "Antisense" relation (301 triples, 3.8%)

**Note**: Absorbed "Parallel Concepts" from v0.1

**Properties Template**: {direction: bidirectional, strength: helpful, temporal: concurrent, cognitive_level: same_level, domain_scope: within_domain}

**Subtypes**:

#### 9.1 Opposite Concepts
- **유리수** ↔ **무리수**
- **소수** ↔ **합성수**
- **양수** ↔ **음수**

#### 9.2 Alternative Methods
- **평균 Mean** ↔ **중앙값 Median** ↔ **최빈값 Mode**
- **기하학적 증명** ↔ **대수적 증명**
- **종이접기로 각 이등분** ↔ **컴퍼스로 각 이등분**

#### 9.3 Dual Perspectives
- **미분 (순간변화율)** ↔ **미분 (접선의 기울기)**
- **벡터 (크기+방향)** ↔ **벡터 (화살표 표현)**

#### 9.4 Symmetric Structures
- **공약수** ↔ **공배수** (divisor vs multiple)
- **최대공약수 GCD** ↔ **최소공배수 LCM**

---

### 10. SYNONYMS/NOTATION (동의어/표기법)

**Definition**: Alternative names, notations, or representations for the **same concept**.

**Research Validation**: Math-KG "Synonyms" relation (493 triples, 6.1%)

**NEW in v0.2** based on Math-KG analysis.

**Properties Template**: {direction: bidirectional, strength: helpful, temporal: concurrent, cognitive_level: same_level, domain_scope: within_domain}

**Examples**:

1. **자연수 = Natural Number = ℕ**
   - Korean term, English term, notation

2. **소수 = 素數 = Prime Number**
   - Multiple language representations

3. **거듭제곱 = 지수 = Power = Exponent**
   - Different terminology for same concept

4. **최대공약수 = GCD = Greatest Common Divisor = 최대공통인수**
   - Multiple terms, abbreviation

5. **π = 원주율 = Pi = 3.14159...**
   - Symbol, Korean, English, approximation

6. **f(x) = y (함수 표기법)**
   - Different notations for function

7. **∠ABC = ∠B (각의 표기법)**
   - Three-point notation vs single-vertex notation

---

### 11. DOMAIN MEMBERSHIP (분야 소속)

**Definition**: Concept belongs to a mathematical **field, category, or branch**.

**Research Validation**: Math-KG "Affiliation" relation (**2,609 triples, 32.5%** - MOST COMMON)

**NEW in v0.2** based on Math-KG finding that domain membership is the most common relationship.

**Properties Template**: {direction: unidirectional (concept → domain), strength: helpful, temporal: independent, cognitive_level: same_level, domain_scope: within_domain}

**Examples**:

1. **피타고라스 정리 ∈ 기하학 (Geometry)**

2. **소인수분해 ∈ 정수론 (Number Theory)**

3. **미적분 ∈ 해석학 (Analysis)**

4. **이차방정식 ∈ 대수학 (Algebra)**

5. **확률 ∈ 통계학 (Statistics)**

6. **삼각함수 ∈ 해석학 & 기하학** (can belong to multiple domains)

7. **벡터 ∈ 선형대수 (Linear Algebra)**

8. **집합 ∈ 집합론 (Set Theory)**

**Hierarchical Domain Structure**:
```
수학 (Mathematics)
├── 대수학 (Algebra)
│   ├── 방정식론
│   ├── 군론
│   └── 체론
├── 기하학 (Geometry)
│   ├── 평면기하
│   ├── 입체기하
│   └── 해석기하
├── 해석학 (Analysis)
│   ├── 미적분
│   ├── 실해석
│   └── 복소해석
├── 정수론 (Number Theory)
├── 통계학 (Statistics)
└── 조합론 (Combinatorics)
```

---

### 12. EQUIVALENCE (동치)

**Definition**: Different **formulations or representations** of the **same mathematical truth**. Not just notation, but equivalent mathematical statements.

**Research Validation**: Math-KG "Equivalence" relation (76 triples, 0.9% - rare but important)

**Distinction from Synonyms**:
- Synonyms: Different names for same concept
- Equivalence: Different mathematical formulations proving same result

**Properties Template**: {direction: bidirectional, strength: recommended, temporal: concurrent, cognitive_level: same_level, domain_scope: within_domain}

**Examples**:

1. **피타고라스 정리 ⇔ 코사인 법칙 (c=90°일 때)**
   - a² + b² = c² ⇔ c² = a² + b² - 2ab·cos(90°) = a² + b²

2. **삼각함수 정의 (직각삼각형) ⇔ 삼각함수 정의 (단위원)**
   - sin θ = opposite/hypotenuse ⇔ sin θ = y-coordinate on unit circle

3. **로그 법칙 ⇔ 지수 법칙**
   - log(ab) = log(a) + log(b) ⇔ e^(x+y) = e^x · e^y

4. **적분의 정의 (Riemann) ⇔ 적분의 정의 (Fundamental Theorem)**
   - ∫f(x)dx = lim(Σf(x_i)Δx) ⇔ ∫f(x)dx = F(b) - F(a) where F'=f

5. **벡터 내적 (대수적) ⇔ 벡터 내적 (기하학적)**
   - a·b = a₁b₁ + a₂b₂ ⇔ a·b = |a||b|cos θ

---

## Relationship Properties

Every relationship instance has these 5 properties:

### 1. Direction
- **unidirectional**: A → B only (e.g., Prerequisite)
- **bidirectional**: A ↔ B (e.g., Co-requisite, Inverse Operation)

### 2. Strength
- **essential**: Cannot proceed without this (hard blocker)
- **recommended**: Can proceed but with significant difficulty
- **helpful**: Enhances understanding but not strictly necessary

### 3. Temporal
- **sequential**: Must learn A before B (time gap allowed)
- **concurrent**: Learn A and B together (co-requisite models)
- **independent**: Order doesn't matter

### 4. Cognitive_level
- **same_level**: Horizontal relationship (same abstraction level)
- **level_raising**: Vertical relationship (abstraction increase)

### 5. Domain_scope
- **within_domain**: Same mathematical field
- **cross_domain**: Different fields (math → physics, etc.)

---

## Validation Methodology (OntoClean-inspired)

### 1. Identity Conditions
What makes each concept unique? Check if relationships respect identity.

**Example**:
- ✅ "소수 정의" prerequisite for "소인수분해"
- ❌ "소수 정의" synonym of "소인수분해" (different identity)

### 2. Subsumption vs Instantiation
Distinguish "is-a" (subsumption) vs "instance-of" (instantiation).

**Example**:
- ✅ "이차방정식" is-a-type-of "방정식" (subsumption)
- ❌ "x² + 2x + 1 = 0" is-a "이차방정식" (should be "instance-of")

### 3. Subtopic vs Prerequisite
Related but distinct - don't conflate.

**Example**:
- ✅ "소인수분해" prerequisite for "GCD using 소인수분해"
- ❌ "소수" subtopic of "정수론" (should be Domain Membership, not Prerequisite)

### 4. Prerequisite Transitivity
If A → B → C, then A → C (but with different strength).

**Example**:
- "자연수" → "정수" → "유리수"
- Therefore: "자연수" → "유리수" (transitive, but longer path)

### 5. Circular Dependency Check
No concept should be its own prerequisite through any path.

**Example**:
- ❌ A → B → C → A (circular, invalid)

---

## Implementation Format

### JSON Output for Relationship Definition Agent

```json
{
  "source_concept_id": "middle-1-1-ch1-1.3.1",
  "source_name": "소인수분해 정의",
  "target_concept_id": "middle-1-1-ch1-1.1.1",
  "target_name": "소수 정의",
  "relationship": {
    "type": "prerequisite",
    "subtype": "logical",
    "properties": {
      "direction": "unidirectional",
      "strength": "essential",
      "temporal": "sequential",
      "cognitive_level": "same_level",
      "domain_scope": "within_domain"
    },
    "reason": "소인수분해는 '소수'의 개념을 정의에서 직접 사용하므로 논리적으로 필수적인 선수 개념이다.",
    "examples": [
      "12 = 2² × 3에서 2와 3이 소수임을 알아야 소인수분해가 성립한다.",
      "소인수분해는 '소수들의 곱'으로 나타내는 것이므로 소수 정의가 선행되어야 한다."
    ],
    "confidence": 0.98,
    "validation": {
      "identity_check": "pass",
      "subsumption_check": "pass",
      "transitivity": "A(소수) → B(소인수분해) → C(GCD) implies A → C",
      "circular_check": "pass"
    }
  }
}
```

---

## Quantitative Analysis from Math-KG

**Total**: 8,019 relationship triples across 1,905 entities (1,337 concepts + 568 theorems)

| Relation Type | Math-KG Count | Percentage | Our v0.2 Equivalent |
|---------------|---------------|------------|---------------------|
| Affiliation | 2,609 | 32.5% | Domain Membership |
| Has Properties | 2,524 | 31.5% | (not modeled) |
| Dependencies | 2,016 | 25.1% | Prerequisite |
| Synonyms | 493 | 6.1% | Synonyms/Notation |
| Antisense | 301 | 3.8% | Complementary |
| Equivalence | 76 | 0.9% | Equivalence |

**Key Insight**: Prerequisites (Dependencies) are only **25%** of relationships. Domain membership and concept properties are equally important.

---

## Usage Examples

### Example 1: Complete Relationship Graph for "소인수분해"

```json
{
  "concept": "middle-1-1-ch1-1.3.1 소인수분해 정의",
  "relationships": [
    {
      "target": "middle-1-1-ch1-1.1.1 소수 정의",
      "type": "prerequisite",
      "subtype": "logical",
      "properties": {
        "direction": "unidirectional",
        "strength": "essential",
        "temporal": "sequential",
        "cognitive_level": "same_level",
        "domain_scope": "within_domain"
      }
    },
    {
      "target": "middle-1-1-ch1-1.2.1 거듭제곱 정의",
      "type": "prerequisite",
      "subtype": "tool",
      "properties": {
        "direction": "unidirectional",
        "strength": "essential",
        "temporal": "sequential",
        "cognitive_level": "same_level",
        "domain_scope": "within_domain"
      }
    },
    {
      "target": "middle-1-1-ch1-1.4.3 GCD using 소인수분해",
      "type": "application",
      "subtype": null,
      "properties": {
        "direction": "unidirectional",
        "strength": "helpful",
        "temporal": "sequential",
        "cognitive_level": "same_level",
        "domain_scope": "within_domain"
      }
    },
    {
      "target": "정수론 Number Theory",
      "type": "domain_membership",
      "subtype": null,
      "properties": {
        "direction": "unidirectional",
        "strength": "helpful",
        "temporal": "independent",
        "cognitive_level": "same_level",
        "domain_scope": "within_domain"
      }
    },
    {
      "target": "Prime Factorization (English)",
      "type": "synonyms",
      "subtype": null,
      "properties": {
        "direction": "bidirectional",
        "strength": "helpful",
        "temporal": "concurrent",
        "cognitive_level": "same_level",
        "domain_scope": "within_domain"
      }
    }
  ]
}
```

---

## Summary of v0.2 Taxonomy

**12 Relationship Types**:
1. Prerequisite [logical, cognitive, pedagogical, tool]
2. Co-requisite
3. Inverse Operation
4. Extension
5. Formalization
6. Application
7. Mutual Definition
8. Abstraction Level
9. Complementary [opposite, alternative, dual, symmetric]
10. Synonyms/Notation (NEW)
11. Domain Membership (NEW)
12. Equivalence (NEW)

**5 Relationship Properties**:
- Direction: unidirectional | bidirectional
- Strength: essential | recommended | helpful
- Temporal: sequential | concurrent | independent
- Cognitive_level: same_level | level_raising
- Domain_scope: within_domain | cross_domain

**Validation**: OntoClean-inspired methodology with 5 checks

**Research Foundation**: Math-KG (8,019 triples), OntoMathEdu, Co-requisite models (5x effectiveness), Learning Progressions

---

## Next Steps

1. ✅ **v0.2 Taxonomy Complete**: 12 types + 5 properties defined
2. **Create More Examples**: Extract 10-20 examples for each type from 841 concepts
3. **Build Relationship Definition Agent**: Claude Max with detailed prompts
4. **Test on Sample**: 20 concepts, validate with OntoClean methodology
5. **Refine Based on Testing**: Adjust definitions, subtypes, properties
6. **Apply to Full 841 Concepts**: Generate complete dependency graph
7. **Extend to Elementary/High/University**: Scale across education levels

---

**This taxonomy provides a comprehensive framework for mathematical concept relationship modeling across all education levels.**
