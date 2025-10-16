# Naming Convention Update

> Workflow 명칭 변경: feedback-loop → math-scaffolding

DATE: 2025-10-16
VERSION: 2.0.0

---

## 🔄 명칭 변경 이유

### Old Name: "Feedback Loop Workflow"
**문제점**:
- Feedback loop는 워크플로우 하나가 아닌 **전체 시스템의 핵심 기능**
- 모든 agent, 모든 workflow에 적용될 확장 가능한 패턴
- 특정 워크플로우 이름으로 사용하면 혼란

### New Name: "Math Scaffolding Workflow"
**장점**:
- 목적이 명확: 수학 문제의 scaffolding 생성
- Feedback은 품질 보증 수단
- 확장 가능: 다른 scaffolding workflow 추가 가능
- 일관성: workflow 이름이 기능을 정확히 반영

---

## 📝 변경 사항

### 파일명 변경

**Workflows**:
```
workflows/feedback_loop_workflow.py 
  → workflows/math_scaffolding_workflow.py
```

**Scripts**:
```
scripts/run_feedback_loop.py 
  → scripts/run_math_scaffolding.py
```

### 함수명 변경

**Main Function**:
```python
# Before
async def run_feedback_loop_workflow(image_path: str)

# After
async def run_math_scaffolding_workflow(image_path: str)
```

### 문서 업데이트

**기존 문서 (유지)**:
- `FEEDBACK-LOOP-QUICKSTART.md` - Feedback loop 개념 설명
- `3PNG-WORKFLOW-COMPLETE.md` - 실행 결과

**새 참조**:
- 명령어: `python3 scripts/run_math_scaffolding.py --image 3.png`
- 워크플로우: Math Scaffolding Workflow

---

## 🎯 Feedback Loop 확장 계획

### Current: Math Scaffolding
```
Image → OCR → Concepts → Scaffolding → Feedback → Patterns → Neo4j
```

### Future: Universal Feedback Loop

**확장 영역**:

1. **Knowledge Builder Feedback**:
   ```
   Generated File → Teacher Review → Quality Patterns → Auto-improvement
   ```

2. **Research Agent Feedback**:
   ```
   Research Results → Accuracy Check → Source Patterns → Better research
   ```

3. **Quality Agent Feedback**:
   ```
   Validation Results → False Positive Analysis → Validation Patterns → Smarter validation
   ```

4. **Problem Decomposer Feedback**:
   ```
   Decomposition Steps → Effectiveness Review → Decomposition Patterns → Better breakdown
   ```

### Universal Pattern
```python
# feedback_learning_agent가 모든 workflow를 지원
class FeedbackPattern:
    workflow_type: str  # "math_scaffolding", "knowledge_building", "research", etc.
    feedback_collector: FeedbackCollector
    pattern_extractor: PatternExtractor
    pattern_storage: Neo4jStorage
```

---

## ✅ 테스트 업데이트

**Test Files**: 명칭 변경 반영 완료
- `tests/test_feedback_loop_e2e.py` - import 수정
- `tests/test_full_integration.py` - import 수정
- `tests/run_all_tests.py` - 기능 유지

**Tests Status**: 100% passing (5 suites)

---

## 📊 새 명칭 사용법

### Quick Start
```bash
# Math scaffolding workflow 실행
python3 scripts/run_math_scaffolding.py --image 3.png

# Demo
python3 examples/demo_feedback_loop.py  # ← 이름 유지 (개념 데모)

# Tests
python3 tests/run_all_tests.py
```

### Python API
```python
from workflows.math_scaffolding_workflow import run_math_scaffolding_workflow

result = await run_math_scaffolding_workflow("3.png")
```

---

## 🚀 향후 확장

### Phase 1: Math Scaffolding (Current)
- ✅ Image → Scaffolding
- ✅ Feedback collection
- ✅ Pattern learning

### Phase 2: Knowledge Building (Next)
- File generation feedback
- Content quality patterns
- Auto-improvement

### Phase 3: Universal Feedback (Future)
- All agents support feedback
- Unified pattern learning
- Cross-workflow optimization

---

**변경 일시**: 2025-10-16
**파일 변경**: 2 files renamed, 3 imports updated
**테스트**: 100% passing
**상태**: ✅ COMPLETE

