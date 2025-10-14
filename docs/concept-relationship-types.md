# Mathematical Concept Relationship Types

**VERSION**: 0.1.0 (Draft)
**DATE**: 2025-10-14
**PURPOSE**: Define relationship types for math education dependency mapping (Elementary through University)

---

## Introduction

This document explores and defines the types of relationships between mathematical concepts across education levels. Each relationship type is illustrated with concrete examples from our 841 middle school concepts and extended to elementary/high school/university levels.

---

## 1. PREREQUISITE (선수 개념)

**Definition**: Concept A is a prerequisite for Concept B if understanding A is **logically necessary** to understand B.

### Examples:

#### Example 1.1: Foundational Definition
- **A**: "소수(Prime Number) 정의" (middle-1-1-ch1-1.1.1)
- **B**: "소인수분해 정의" (middle-1-1-ch1-1.3.1)
- **Relationship**: Cannot define "prime factorization" without knowing what "prime" means
- **Type**: **Hard Prerequisite** - Absolute logical necessity

#### Example 1.2: Notation Dependency
- **A**: "거듭제곱 정의" (middle-1-1-ch1-1.2.1)
- **B**: "지수를 이용한 간단한 표기" (middle-1-1-ch1-1.3.4)
- **Relationship**: Need exponent notation to express 2² × 3
- **Type**: **Hard Prerequisite** - Notational requirement

#### Example 1.3: Tool Prerequisite
- **A**: "소인수분해 정의" (middle-1-1-ch1-1.3.1)
- **B**: "소인수분해를 이용한 최대공약수 구하기" (middle-1-1-ch1-1.4.3)
- **Relationship**: Need to know how to factorize before using it as a tool
- **Type**: **Soft Prerequisite** - Can learn GCD concept independently, but this method requires factorization

### Cross-Level Prerequisites:

- **Elementary → Middle**: 분수의 나눗셈 (elem-6) → 유리수 (middle-1)
- **Middle → High**: 일차방정식 (middle-2) → 이차방정식 (high-1)
- **High → University**: 함수 (high-1) → 극한 (univ-calculus-1)

### Questions to Answer:
1. **Q**: If a student can mechanically perform prime factorization without knowing the definition of "prime", do they understand the concept?
2. **Q**: Should we distinguish between "logical prerequisite" and "pedagogical prerequisite"?
3. **Q**: How to handle cases where prerequisite is needed for *formal understanding* but not *intuitive grasp*?

---

## 2. CO-REQUISITE (공동 필수)

**Definition**: Concepts that should be learned **simultaneously** or in **close temporal proximity** for optimal understanding.

### Examples:

#### Example 2.1: Mutually Reinforcing
- **A**: "삼각함수 정의" (high-1)
- **B**: "단위원" (high-1)
- **Relationship**: Unit circle provides geometric meaning to trig functions; trig functions give unit circle practical application
- **Nature**: Neither is strictly prerequisite, but learning together enhances both

#### Example 2.2: Dual Perspectives
- **A**: "미분 - 순간변화율" (high-2)
- **B**: "미분 - 접선의 기울기" (high-2)
- **Relationship**: Two interpretations of the same concept
- **Nature**: Should be presented together for complete understanding

### Questions to Answer:
1. **Q**: Is co-requisite different from "should be taught together" vs "must be learned together"?
2. **Q**: Can co-requisites be learned separately if student has strong foundation?

---

## 3. INVERSE OPERATION (역연산)

**Definition**: Operations that "undo" each other.

### Examples:

#### Example 3.1: Classic Inverse
- **A**: "미분" (high-2)
- **B**: "적분" (high-2)
- **Relationship**: Integration reverses differentiation (Fundamental Theorem of Calculus)
- **Note**: While inverse, differentiation is usually taught first (historical and pedagogical reasons)

#### Example 3.2: Elementary Inverse
- **A**: "덧셈" (elem-1)
- **B**: "뺄셈" (elem-1)
- **Relationship**: Subtraction undoes addition

### Questions to Answer:
1. **Q**: Should inverse operations always be taught together?
2. **Q**: Is "inverse" a relationship type or a property of the operations themselves?

---

## 4. EXTENSION (확장)

**Definition**: Concept B **extends** Concept A to a broader domain or adds new properties.

### Examples:

#### Example 4.1: Domain Extension
- **A**: "자연수" (elem-1)
- **B**: "정수" (elem-6 or middle-1)
- **C**: "유리수" (middle-1)
- **D**: "실수" (high-1)
- **E**: "복소수" (high-2)
- **Relationship Chain**: Each extends the previous number system
- **Nature**: B contains A as a special case

#### Example 4.2: Concept Generalization
- **A**: "일차방정식" (middle-1)
- **B**: "이차방정식" (middle-3)
- **C**: "다항방정식" (high-1)
- **Relationship**: From degree 1 → 2 → n

### Questions to Answer:
1. **Q**: Is extension always a prerequisite relationship? (Must know A before B?)
2. **Q**: How to distinguish "extension" from "generalization" vs "specialization"?

---

## 5. FORMALIZATION (형식화)

**Definition**: Concept B provides **rigorous formal definition** of an intuitive idea in Concept A.

### Examples:

#### Example 5.1: Intuition to Rigor
- **A**: "넓이 (초등 - 직사각형 세기)" (elem-3)
- **B**: "넓이 (중등 - 공식 적용)" (middle-1)
- **C**: "넓이 (고등 - 적분으로 정의)" (high-2)
- **D**: "넓이 (대학 - Lebesgue 측도)" (univ-real-analysis)
- **Relationship**: Progressive formalization of the same concept

#### Example 5.2: Procedural to Axiomatic
- **A**: "분수 계산 (초등 - 규칙 적용)" (elem-4-6)
- **B**: "유리수 (중등 - 체의 성질)" (middle-1-2)
- **C**: "유리수체 (대학 - 대수적 구조)" (univ-abstract-algebra)

### Questions to Answer:
1. **Q**: Is formalization a type of extension or a distinct relationship?
2. **Q**: Can students "skip" informal stages and start with formal definitions?

---

## 6. PARALLEL CONCEPTS (병렬 개념)

**Definition**: Concepts that address **similar problems** using **different approaches** or represent **symmetric structures**.

### Examples:

#### Example 6.1: Symmetric Structures
- **A**: "공약수" (middle-1-1-ch1-1.4.1)
- **B**: "공배수" (middle-1-1-ch1-1.5.1)
- **Relationship**: Structurally symmetric (divisor vs multiple)
- **Nature**: Can be learned independently but comparing them enhances understanding

#### Example 6.2: Alternative Methods
- **A**: "평균(Mean)" (middle-1-1-ch3)
- **B**: "중앙값(Median)" (middle-1-1-ch3)
- **C**: "최빈값(Mode)" (middle-1-1-ch3)
- **Relationship**: Different methods for measuring "central tendency"
- **Nature**: Not prerequisites for each other, but should be compared

#### Example 6.3: Dual Formulations
- **A**: "기하학적 증명" (middle-2)
- **B**: "대수적 증명" (middle-2)
- **Relationship**: Different proof methods for the same theorem

### Questions to Answer:
1. **Q**: Should parallel concepts be tagged as "compare-with" relationships?
2. **Q**: Is there pedagogical value in learning one before the other?

---

## 7. APPLICATION (응용)

**Definition**: Concept B applies the principles of Concept A to solve specific problems or domains.

### Examples:

#### Example 7.1: Tool Application
- **A**: "피타고라스 정리" (middle-2)
- **B**: "평면 좌표에서 두 점 사이 거리" (middle-3)
- **Relationship**: Pythagorean theorem applied to coordinate geometry

#### Example 7.2: Domain-Specific Application
- **A**: "이차함수" (middle-3)
- **B**: "포물선 운동" (high-physics)
- **Relationship**: Math concept applied to physics

### Questions to Answer:
1. **Q**: Should we track applications in other domains (physics, engineering)?
2. **Q**: Is "application" always unidirectional?

---

## 8. MUTUAL DEFINITION (상호 정의)

**Definition**: Concepts that are defined **in terms of each other** or as **complements**.

### Examples:

#### Example 8.1: Complementary Definition
- **A**: "소수(Prime)" (middle-1-1-ch1-1.1.1)
- **B**: "합성수(Composite)" (middle-1-1-ch1-1.1.2)
- **Relationship**: "Composite = not prime (excluding 1)"
- **Nature**: Defining one automatically defines the other

#### Example 8.2: Dual Concepts
- **A**: "정의역(Domain)" (high-1)
- **B**: "치역(Range)" (high-1)
- **Relationship**: Function concept requires both

### Questions to Answer:
1. **Q**: Should mutually defined concepts always be taught together?
2. **Q**: Is this a special case of co-requisite?

---

## 9. ABSTRACTION LEVEL (추상화 수준)

**Definition**: The same concept at different levels of abstraction.

### Examples:

#### Example 9.1: Counting Abstraction
- **Elementary**: "구체물 세기" - Counting physical objects
- **Middle**: "자연수" - Abstract number concept
- **High**: "집합의 원소 개수" - Cardinality
- **University**: "기수(Cardinal Number)" - Transfinite numbers

#### Example 9.2: Function Abstraction
- **Elementary**: "패턴 찾기" (elem-5)
- **Middle**: "일차함수" (middle-2)
- **High**: "함수 일반" (high-1)
- **University**: "사상(Mapping)" (univ-abstract-algebra)
- **University Advanced**: "함자(Functor)" (univ-category-theory)

### Questions to Answer:
1. **Q**: Is abstraction level a relationship or a property of concepts?
2. **Q**: Can students jump abstraction levels or must they be sequential?
3. **Q**: How to represent vertical (abstraction) vs horizontal (extension) relationships?

---

## 10. ESSENTIAL vs OPTIONAL

**Definition**: Degree of necessity for a prerequisite.

### Types:

#### 10.1 Essential (필수)
- **Cannot** proceed without this
- Example: Cannot learn calculus without functions

#### 10.2 Strongly Recommended (강력 권장)
- **Can** proceed but with significant difficulty
- Example: Can learn calculus without trigonometry, but integration becomes very limited

#### 10.3 Helpful (도움이 됨)
- Enhances understanding but not strictly necessary
- Example: Knowing Greek alphabet helps in learning advanced math notation

### Questions to Answer:
1. **Q**: Should this be a relationship type or a property (weight/strength) of prerequisite relationships?
2. **Q**: How to objectively measure "essential" vs "helpful"?

---

## OPEN QUESTIONS FOR REFINEMENT

### Fundamental Questions:
1. **Logical vs Pedagogical Prerequisites**: Should we distinguish?
   - Logical: A is necessary to define/understand B
   - Pedagogical: A should be taught before B for optimal learning

2. **Capability vs Knowledge**: Are these different?
   - Knowledge: Knowing the definition of "prime number"
   - Capability: Being able to identify prime numbers
   - Skill: Efficient prime factorization algorithm

3. **Implicit Prerequisites**: How to handle?
   - Example: "삼각형 내각의 합" requires "parallel lines" (implicit)
   - Should all implicit prerequisites be made explicit?

4. **Cross-Domain Dependencies**: Math → Physics → Engineering
   - Should we track these or stay within mathematics?

5. **Temporal Proximity**:
   - Co-requisites: Learn together
   - Sequential Prerequisites: Learn in order, but with time gap allowed
   - How to represent this in a dependency graph?

### Implementation Questions:
1. **How to query Claude Max?**
   - For each concept, provide: name, content, grade, chapter, all 841 concepts?
   - Or provide smaller context (same grade + adjacent grades)?

2. **Output format?**
```json
{
  "concept_id": "middle-1-1-ch1-1.3.1",
  "relationships": [
    {
      "target_concept_id": "middle-1-1-ch1-1.1.1",
      "relationship_type": "prerequisite",
      "subtype": "hard",
      "reason": "Prime factorization requires knowing what prime means",
      "confidence": 0.98,
      "bidirectional": false
    },
    {
      "target_concept_id": "middle-1-1-ch1-1.4.3",
      "relationship_type": "enables",
      "subtype": "application",
      "reason": "Prime factorization enables GCD calculation method",
      "confidence": 0.95,
      "bidirectional": false
    }
  ]
}
```

3. **Relationship Type Hierarchy?**
```
- Prerequisite
  - Hard (logical necessity)
  - Soft (strongly recommended)
  - Background (helpful)
- Co-requisite
  - Mutually reinforcing
  - Dual perspective
- Extension
  - Domain extension
  - Generalization
- Application
  - Tool application
  - Domain-specific
...
```

---

## NEXT STEPS

1. **Gather User Feedback**: Discuss these definitions and questions
2. **Refine Taxonomy**: Based on feedback, finalize relationship types
3. **Create Examples Database**: 50-100 well-documented relationship examples
4. **Design Claude Max Prompts**: Create detailed prompts for each relationship type detection
5. **Build Relationship Definition Agent**: Agent that uses this taxonomy to classify relationships
6. **Validate on Sample**: Test on 20 concepts, refine definitions
7. **Apply to 841 Concepts**: Full dependency mapping

---

## FEEDBACK NEEDED

Please provide feedback on:
1. Are these relationship types comprehensive?
2. Which types should be merged or split?
3. Which open questions are most critical to resolve?
4. What examples would clarify the definitions?
5. How should we prioritize: completeness vs simplicity?

**This is a living document and will be refined through iterative discussion.**
