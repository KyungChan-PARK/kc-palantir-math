# Feedback Loop System - Quick Start Guide

> 피드백 기반 학습 시스템 사용 가이드

VERSION: 3.1.0
DATE: 2025-10-16

---

## 시스템 개요

**목적**: 수학 문제 이미지 → 단계별 scaffolding 생성 → 인간 피드백 수집 → 패턴 학습 → 자동 개선

**핵심 기능**:
- 📸 Mathpix OCR: 99.9% 정확도로 수식 추출
- 🎯 Concept Matching: 841개 중학교 수학 개념 자동 매칭
- 📝 Scaffolding: 문제 유형별 맞춤 단계 생성
- 💬 Interactive Feedback: CLI로 단계별 평가
- 🧠 Pattern Learning: 피드백에서 재사용 가능한 패턴 추출
- 💾 Neo4j Storage: LearnedPattern 저장 및 자동 적용
- 📊 Real-time Observability: 전 과정 대시보드 모니터링

---

## Quick Start

### 1. 사전 준비

필수 서비스 실행 확인:
```bash
# Neo4j (포트 7687)
docker-compose ps | grep neo4j

# Observability Server (포트 4000)
curl http://localhost:4000/health

# Observability Dashboard (포트 3000) - 선택사항
cd observability-dashboard && bun run dev
```

### 2. 테스트 실행

**전체 테스트 스위트 (권장)**:
```bash
cd /home/kc-palantir/math
python3 tests/run_all_tests.py
```

예상 결과:
```
✅ PASSED: E2E Test Suite (10 tests)
✅ PASSED: Actual Problem Scaffolding
✅ PASSED: Full Integration Test
Success Rate: 100.0%
```

**개별 테스트**:
```bash
# E2E 테스트 (10개)
python3 tests/test_feedback_loop_e2e.py

# 실제 문제 scaffolding
python3 tests/test_actual_problem_scaffolding.py

# 통합 테스트
python3 tests/test_full_integration.py
```

### 3. 실제 워크플로우 실행

**자동화 스크립트 (권장)**:
```bash
python3 scripts/run_feedback_loop.py --image sample.png
```

**수동 실행** (개발/디버깅용):
```python
import asyncio
from workflows.feedback_loop_workflow import run_feedback_loop_workflow

# 실행
result = asyncio.run(run_feedback_loop_workflow("sample.png"))

# 결과 확인
print(f"Success: {result['success']}")
print(f"Patterns learned: {len(result['learned_patterns'])}")
```

---

## 워크플로우 단계

### Step 1: OCR Extraction
```
sample.png → Mathpix API → 수식 추출
```

**출력**:
- Text: "Q3 그림과 같이 좌표평면에서..."
- LaTeX: (수식)
- Confidence: 99.90%

### Step 2: Concept Matching
```
OCR 텍스트 → 841개 개념 분석 → Top-K 매칭
```

**출력**:
- Top 1: 좌표평면의 구성 (score: 1.000)
- Top 2: 점의 좌표 나타내기 (score: 1.000)
- Top 3: 교점의 좌표와 연립방정식 (score: 1.000)

### Step 3: Pattern Query
```
매칭된 개념 → Neo4j 조회 → 학습된 패턴 검색
```

**출력**:
- 적용 가능한 패턴 목록 (현재: 0개, 학습 후 증가)

### Step 4: Scaffolding Generation
```
문제 + 개념 + 패턴 → 단계별 문제 생성
```

**출력** (좌표평면 삼각형 넓이 문제):
```
Step 1: 주어진 정보를 정리해보세요
Step 2: y=0을 대입해야 하나요?
Step 3: 방정식을 풀면?
Step 4: 점 C의 좌표는?
Step 5: 직선 AB의 기울기는?
Step 6: 기울기 계산
Step 7: y절편 구하기
Step 8: 삼각형 넓이 공식
Step 9: 밑변 길이
Step 10: 높이 구하기
```

### Step 5: Feedback Collection (Interactive)
```
각 단계에 대해 CLI로 피드백 수집
```

**프롬프트**:
```
Step 2: y=0을 대입해야 하나요?
Rate this step (1-5): 3
Comment: Could be clearer about which value to substitute
Suggested improvement: y=0을 대입해야 하나요? (x축 위의 점)
```

### Step 6: Pattern Extraction
```
피드백 분석 → 재사용 가능한 패턴 추출
```

**추출 예시**:
```json
{
  "pattern_id": "lp_clarify_substitution",
  "type": "question_improvement",
  "rule": "Add clarification in parentheses for substitution steps",
  "confidence": 1.0,
  "examples": [
    {
      "before": "y=0을 대입해야 하나요?",
      "after": "y=0을 대입해야 하나요? (x축 위의 점)"
    }
  ]
}
```

### Step 7: Neo4j Storage
```
패턴 → LearnedPattern 노드 생성 → 자동 적용 준비
```

**Cypher 예시**:
```cypher
CREATE (:LearnedPattern {
  id: 'lp_clarify_substitution',
  type: 'question_improvement',
  confidence: 1.0,
  applicable_concepts: ['linear_function', 'coordinate_geometry'],
  auto_apply: true
})
```

---

## 데이터 위치

모든 데이터는 `/home/kc-palantir/math/data/`에 저장됩니다:

```
data/
├── ocr_results/          # Mathpix OCR 추출 결과
│   └── ocr_YYYYMMDD_HHMMSS.json
├── feedback_sessions/    # 피드백 세션
│   └── fs_YYYYMMDD_HHMMSS.json
└── learned_patterns/     # 학습된 패턴 (백업)
    └── patterns_YYYYMMDD_HHMMSS.json
```

---

## Observability 모니터링

### Dashboard 접속
```
http://localhost:3000
```

### 추적되는 이벤트
- `ocr_started` / `ocr_completed`
- `concept_match_started` / `concept_match_completed`
- `pattern_query_started` / `pattern_query_completed`
- `scaffolding_started` / `scaffolding_completed`
- `feedback_started` / `feedback_step_collected` / `feedback_completed`
- `learning_started` / `pattern_extracted` / `learning_completed`
- `neo4j_write_started` / `neo4j_write_completed`
- `validation_completed`

### 이벤트 조회 (API)
```bash
# 최근 100개 이벤트
curl "http://localhost:4000/events/recent?limit=100"

# 특정 세션 이벤트
curl "http://localhost:4000/events/recent?session_id=YOUR_SESSION_ID"

# 특정 이벤트 타입
curl "http://localhost:4000/events/recent?event_type=pattern_extracted"
```

---

## 테스트 검증

### 전체 테스트
```bash
python3 tests/run_all_tests.py
```

**기대 결과**:
```
Total: 3
Passed: 3
Failed: 0
Success Rate: 100.0%
🎉 ALL TESTS PASSED!
```

### 개별 컴포넌트 테스트
```bash
# OCR 테스트
python3 -m tools.mathpix_ocr_tool

# Concept matching 테스트
python3 -m workflows.concept_matcher

# Feedback collector 테스트
python3 -m tools.feedback_collector
```

---

## 트러블슈팅

### OCR 실패
**증상**: `OCR failed: API returned status 401`

**해결**:
1. Mathpix API key 확인
2. `tools/mathpix_ocr_tool.py`에서 `MATHPIX_APP_KEY` 검증

### Concept Matching 낮은 스코어
**증상**: `Top concept score < 0.5`

**해결**:
1. OCR 결과 확인 (텍스트가 올바르게 추출되었는지)
2. `workflows/concept_matcher.py`의 `keyword_map` 확장

### Observability 연결 실패
**증상**: `Observability server not available`

**해결**:
1. Observability server 실행 확인:
   ```bash
   curl http://localhost:4000/health
   ```
2. 없으면 시작:
   ```bash
   cd observability-server
   uv run python server.py
   ```

**참고**: Observability 서버가 없어도 워크플로우는 정상 작동 (이벤트 전송만 실패)

### Neo4j 연결 실패
**증상**: `Neo4j connection error`

**해결**:
```bash
docker-compose up -d neo4j
```

---

## 다음 단계

### 1. 더 많은 문제 유형 추가
`workflows/feedback_loop_workflow.py`의 `generate_scaffolding()` 함수에 추가:
- 이차방정식
- 확률 문제
- 도형 넓이/둘레

### 2. Agent 통합
Meta-orchestrator에서 feedback-learning-agent 사용:
```python
# .claude/CLAUDE.md에 추가
사용자가 문제 이미지를 제공하면:
1. Task: feedback-learning-agent에게 위임
2. 자동으로 OCR → Scaffolding → Feedback 수집
```

### 3. 패턴 자동 적용
`subagents/problem_generator_agent.py`에서:
- Neo4j에서 LearnedPattern 조회
- 프롬프트에 자동 주입
- 생성 품질 향상

### 4. A/B Testing
학습된 패턴의 효과성 검증:
- Control group: 패턴 미적용
- Treatment group: 패턴 적용
- 성공률/이해도 비교

---

## API Reference

### Mathpix OCR
```python
from tools.mathpix_ocr_tool import extract_math_from_image

result = extract_math_from_image("problem.png")
# Returns: {"text": "...", "latex": "...", "confidence": 0.99, "success": True}
```

### Concept Matching
```python
from workflows.concept_matcher import identify_concepts

concepts = identify_concepts(ocr_result, top_k=5)
# Returns: [{"concept_id": "...", "name": "...", "relevance_score": 0.95}, ...]
```

### Feedback Collection
```python
from tools.feedback_collector import collect_interactive_feedback

feedback = collect_interactive_feedback(scaffolding)
# Interactive CLI prompts, returns feedback session JSON
```

### Pattern Extraction
```python
from workflows.feedback_loop_workflow import extract_patterns_from_feedback

patterns = await extract_patterns_from_feedback(feedback_session)
# Returns: [{"pattern_id": "...", "rule": "...", "confidence": 1.0}, ...]
```

---

## 성능 메트릭

### 실제 측정 값 (sample.png)

| Metric | Value |
|--------|-------|
| OCR Confidence | 99.90% |
| OCR Time | ~2 seconds |
| Concept Matching | 1.000 (perfect match) |
| Concepts Loaded | 841 concepts |
| Scaffolding Steps | 10 steps (coordinate geometry) |
| Pattern Extraction | 2 patterns per session |
| Total Workflow Time | < 30 seconds |
| Test Success Rate | 100% (10/10 tests) |

---

## 문서 링크

- [전체 아키텍처](./ARCHITECTURE-DIAGRAMS.md)
- [초보자용 가이드](./PROJECT-ARCHITECTURE-VISUALIZATION.md)
- [Neo4j 스키마](./neo4j/feedback_schema.cypher)
- [테스트 코드](./tests/)

---

**작성일**: 2025-10-16
**버전**: 3.1.0
**테스트**: 100% 통과 (10/10 E2E + 3/3 Integration)

