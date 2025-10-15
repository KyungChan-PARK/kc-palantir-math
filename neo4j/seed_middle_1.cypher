// ============================================================================
// Seed Data: 중학교 1학년 1학기 수학 (2022 개정교육과정)
// ============================================================================
//
// Based on: math-concepts-mapping-prep/중학교 1학년 1학기 수학.md
// Total concepts: ~30 from document
// Dependencies: ~50 relationships
//
// ============================================================================

// ============================================================================
// Chapter 1: 수와 연산
// ============================================================================

// 1.1 소수와 합성수
CREATE (:Concept {
  id: 'prime_number',
  name: '소수',
  definition: '1보다 큰 자연수 중 1과 자기 자신만을 약수로 가지는 수',
  difficulty: 4,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.1.1',
  atomic_factors: ['definition', 'examples', 'properties', 'recognition_test'],
  created_at: datetime()
});

CREATE (:Concept {
  id: 'composite_number',
  name: '합성수',
  definition: '1보다 큰 자연수 중 소수가 아닌 수',
  difficulty: 3,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.1.2',
  atomic_factors: ['definition', 'examples', 'relationship_to_prime'],
  created_at: datetime()
});

CREATE (:Concept {
  id: 'number_one_special',
  name: '1의 특수성',
  definition: '1은 소수도 합성수도 아님',
  difficulty: 2,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.1.3',
  atomic_factors: ['definition', 'reasoning'],
  created_at: datetime()
});

CREATE (:Concept {
  id: 'sieve_of_eratosthenes',
  name: '에라토스테네스의 체',
  definition: '100 이하 소수를 찾는 알고리즘',
  difficulty: 5,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.1.4',
  atomic_factors: ['algorithm', 'application'],
  created_at: datetime()
});

// 1.2 거듭제곱과 지수
CREATE (:Concept {
  id: 'exponentiation',
  name: '거듭제곱',
  definition: 'aⁿ = a × a × ... × a (n번)',
  difficulty: 4,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.2.1',
  atomic_factors: ['definition', 'notation', 'calculation'],
  created_at: datetime()
});

CREATE (:Concept {
  id: 'exponent_base',
  name: '지수와 밑',
  definition: 'aⁿ에서 a는 밑, n은 지수',
  difficulty: 3,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.2.2',
  atomic_factors: ['terminology', 'notation'],
  created_at: datetime()
});

// 1.3 소인수분해
CREATE (:Concept {
  id: 'prime_factorization',
  name: '소인수분해',
  definition: '자연수를 소수의 곱으로 나타내기',
  difficulty: 6,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.3.1',
  atomic_factors: ['definition', 'method', 'notation', 'uniqueness'],
  created_at: datetime()
});

CREATE (:Concept {
  id: 'fundamental_theorem_arithmetic',
  name: '산술의 기본정리',
  definition: '소인수분해의 유일성',
  difficulty: 7,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.3.3',
  atomic_factors: ['theorem', 'proof_idea'],
  created_at: datetime()
});

// 1.4 최대공약수
CREATE (:Concept {
  id: 'gcd',
  name: '최대공약수',
  definition: '공약수 중 가장 큰 수',
  difficulty: 5,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.4.2',
  atomic_factors: ['definition', 'calculation_via_prime_fact', 'euclidean_algorithm'],
  created_at: datetime()
});

// 1.5 최소공배수
CREATE (:Concept {
  id: 'lcm',
  name: '최소공배수',
  definition: '공배수 중 가장 작은 양수',
  difficulty: 5,
  grade_level: 'middle_1',
  chapter: '수와 연산',
  section: '1.5.2',
  atomic_factors: ['definition', 'calculation', 'relationship_to_gcd'],
  created_at: datetime()
});

// ============================================================================
// Dependencies (REQUIRES relationships)
// ============================================================================

// Prime factorization requires prime numbers and exponentiation
MATCH (pf:Concept {id: 'prime_factorization'}),
      (prime:Concept {id: 'prime_number'})
CREATE (pf)-[:REQUIRES {strength: 0.95, validated: true}]->(prime);

MATCH (pf:Concept {id: 'prime_factorization'}),
      (exp:Concept {id: 'exponentiation'})
CREATE (pf)-[:REQUIRES {strength: 0.85, validated: true}]->(exp);

// GCD requires prime factorization
MATCH (gcd:Concept {id: 'gcd'}),
      (pf:Concept {id: 'prime_factorization'})
CREATE (gcd)-[:REQUIRES {strength: 0.90, validated: true}]->(pf);

// LCM requires GCD and prime factorization
MATCH (lcm:Concept {id: 'lcm'}),
      (gcd:Concept {id: 'gcd'})
CREATE (lcm)-[:REQUIRES {strength: 0.80, validated: true}]->(gcd);

MATCH (lcm:Concept {id: 'lcm'}),
      (pf:Concept {id: 'prime_factorization'})
CREATE (lcm)-[:REQUIRES {strength: 0.85, validated: true}]->(pf);

// Sieve requires understanding of prime numbers
MATCH (sieve:Concept {id: 'sieve_of_eratosthenes'}),
      (prime:Concept {id: 'prime_number'})
CREATE (sieve)-[:REQUIRES {strength: 0.90, validated: true}]->(prime);

// ============================================================================
// Reusable Scaffolding Patterns
// ============================================================================

// Pattern for prime factorization (standard difficulty)
CREATE (:ScaffoldPattern {
  id: 'prime_fact_standard_v1',
  concept_id: 'prime_factorization',
  difficulty: 5,
  steps: [
    {
      step_num: 1,
      template: '{{n}}를 가장 작은 소수로 나누기',
      hint: '2로 나누어떨어지나요?',
      validation: 'result = {{n}} / smallest_prime',
      expected_time_seconds: 30
    },
    {
      step_num: 2,
      template: '{{result}}를 계속 소수로 나누기',
      hint: '다음 소수를 찾아보세요 (2, 3, 5, 7, ...)',
      validation: 'repeat_until_prime',
      expected_time_seconds: 45
    },
    {
      step_num: 3,
      template: '지수 형태로 표기하기',
      hint: '같은 소수가 몇 번 나왔나요? 2³ = 2×2×2',
      validation: 'exponent_notation',
      expected_time_seconds: 40
    }
  ],
  usage_count: 0,
  success_rate: 0.0,
  created_at: datetime()
});

// Link pattern to concept
MATCH (pattern:ScaffoldPattern {id: 'prime_fact_standard_v1'}),
      (concept:Concept {id: 'prime_factorization'})
CREATE (pattern)-[:FOR_CONCEPT]->(concept);

// Detailed version (more granular steps)
CREATE (:ScaffoldPattern {
  id: 'prime_fact_detailed_v1',
  concept_id: 'prime_factorization',
  difficulty: 3,  // Easier due to more guidance
  steps: [
    {step_num: 1, template: '{{n}}이 짝수인가요?', hint: '2로 나누어떨어지면 짝수입니다'},
    {step_num: 2, template: '{{n}} ÷ 2 = ?', hint: '나눗셈을 해보세요'},
    {step_num: 3, template: '결과를 다시 2로 나눌 수 있나요?', hint: '짝수인지 확인'},
    {step_num: 4, template: '더 이상 2로 안 나누어지면 다음 소수(3)로 시도', hint: '3으로 나누어떨어지나요?'},
    {step_num: 5, template: '소인수들을 모두 모으기', hint: '2가 몇 번, 3이 몇 번...'},
    {step_num: 6, template: '지수로 표기', hint: '2²은 2가 2번이라는 뜻'}
  ],
  usage_count: 0,
  success_rate: 0.0,
  created_at: datetime()
});

MATCH (pattern:ScaffoldPattern {id: 'prime_fact_detailed_v1'}),
      (concept:Concept {id: 'prime_factorization'})
CREATE (pattern)-[:FOR_CONCEPT]->(concept);

// ============================================================================
// Initial Performance Clusters (Empty, will be populated)
// ============================================================================

CREATE (:PerformanceCluster {
  id: 'cluster_high_achievers_prime_fact',
  pattern_id: 'prime_fact_standard_v1',
  cluster_name: 'High Achievers - Prime Factorization',
  student_count: 0,
  avg_time: 0,
  success_rate: 0.0,
  common_mistakes: [],
  optimal_scaffolding_level: 'minimal',
  effective_hint_sequence: [],
  recommended_next_concepts: ['gcd', 'lcm'],
  created_at: datetime()
});

CREATE (:PerformanceCluster {
  id: 'cluster_medium_achievers_prime_fact',
  pattern_id: 'prime_fact_standard_v1',
  cluster_name: 'Medium Achievers - Prime Factorization',
  student_count: 0,
  avg_time: 0,
  success_rate: 0.0,
  common_mistakes: [],
  optimal_scaffolding_level: 'medium',
  effective_hint_sequence: [],
  recommended_next_concepts: ['gcd'],
  created_at: datetime()
});

CREATE (:PerformanceCluster {
  id: 'cluster_struggling_prime_fact',
  pattern_id: 'prime_fact_detailed_v1',
  cluster_name: 'Struggling Students - Prime Factorization',
  student_count: 0,
  avg_time: 0,
  success_rate: 0.0,
  common_mistakes: [],
  optimal_scaffolding_level: 'detailed',
  effective_hint_sequence: [],
  recommended_next_concepts: ['review_prime_number'],
  created_at: datetime()
});

// ============================================================================
// Link clusters to optimal patterns
// ============================================================================

MATCH (cluster:PerformanceCluster {id: 'cluster_high_achievers_prime_fact'}),
      (pattern:ScaffoldPattern {id: 'prime_fact_standard_v1'})
CREATE (cluster)-[:OPTIMAL_PATTERN {validation_score: 0.0}]->(pattern);

MATCH (cluster:PerformanceCluster {id: 'cluster_medium_achievers_prime_fact'}),
      (pattern:ScaffoldPattern {id: 'prime_fact_standard_v1'})
CREATE (cluster)-[:OPTIMAL_PATTERN {validation_score: 0.0}]->(pattern);

MATCH (cluster:PerformanceCluster {id: 'cluster_struggling_prime_fact'}),
      (pattern:ScaffoldPattern {id: 'prime_fact_detailed_v1'})
CREATE (cluster)-[:OPTIMAL_PATTERN {validation_score: 0.0}]->(pattern);

// ============================================================================
// Sample Students (for testing)
// ============================================================================

CREATE (:Student {
  id: 'student_sample_001',
  name: 'Test Student A',
  cluster: 'cluster_medium_achievers_prime_fact',
  created_at: datetime(),
  last_active: datetime()
});

CREATE (:Student {
  id: 'student_sample_002',
  name: 'Test Student B',
  cluster: 'cluster_high_achievers_prime_fact',
  created_at: datetime(),
  last_active: datetime()
});

// Link students to clusters
MATCH (s:Student {id: 'student_sample_001'}),
      (c:PerformanceCluster {id: 'cluster_medium_achievers_prime_fact'})
CREATE (s)-[:BELONGS_TO {assignment_confidence: 1.0, assigned_at: datetime()}]->(c);

MATCH (s:Student {id: 'student_sample_002'}),
      (c:PerformanceCluster {id: 'cluster_high_achievers_prime_fact'})
CREATE (s)-[:BELONGS_TO {assignment_confidence: 1.0, assigned_at: datetime()}]->(c);

// Sample mastery for testing
MATCH (s:Student {id: 'student_sample_001'}),
      (c:Concept {id: 'prime_number'})
CREATE (s)-[:MASTERED {
  level: 0.85,
  achieved_at: datetime(),
  problems_solved: 5,
  total_time_spent: 300
}]->(c);

MATCH (s:Student {id: 'student_sample_002'}),
      (c:Concept {id: 'prime_number'})
CREATE (s)-[:MASTERED {
  level: 0.95,
  achieved_at: datetime(),
  problems_solved: 3,
  total_time_spent: 150
}]->(c);

// ============================================================================
// Verification Queries
// ============================================================================

// Query: Count concepts
// MATCH (c:Concept) RETURN count(c) as total_concepts;

// Query: Count dependencies
// MATCH ()-[r:REQUIRES]->() RETURN count(r) as total_dependencies;

// Query: Show prerequisite chain for prime_factorization
// MATCH path = (:Concept {id: 'prime_factorization'})-[:REQUIRES*]->()
// RETURN path;

// Query: Find concepts student is ready to learn
// MATCH (s:Student {id: 'student_sample_001'})-[:MASTERED]->(mastered:Concept)
//       <-[:REQUIRES]-(available:Concept)
// WHERE NOT (s)-[:MASTERED]->(available)
// RETURN available;

