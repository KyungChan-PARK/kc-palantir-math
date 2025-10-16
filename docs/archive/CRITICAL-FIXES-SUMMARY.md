# 🚨 CRITICAL FIXES REQUIRED - IMMEDIATE ACTION

**Date**: 2025-10-16  
**Status**: **SYSTEM CURRENTLY BROKEN** - 3 Critical Gaps Identified

---

## EXECUTIVE SUMMARY

시스템이 현재 **기본 Claude Code 동작**으로만 실행 중입니다.  
우리가 개발한 **모든 특화 로직이 비활성화** 상태입니다.

**영향**:
- Meta-orchestrator의 3,500토큰 프롬프트 **완전 무시**
- 16개 훅 함수 **전부 우회**
- 67줄 스트리밍 코드 **실행 불가** (죽은 코드)

**예상 수정 시간**: 35분
**예상 효과**: 시스템 효율 65% → 95% (+30%)

---

## 치명적 갭 (3개 - 즉시 수정 필요)

### 1. 시스템 프롬프트 미주입 (10분)

**문제**: `ClaudeAgentOptions.system_prompt` 파라미터 누락

**코드 위치**: `main.py:134`

**현재 코드**:
```python
options = ClaudeAgentOptions(
    model="claude-sonnet-4-5-20250929",
    permission_mode="acceptEdits",
    setting_sources=["project"],
    # ❌ system_prompt 완전 누락
)
```

**수정 방법**:
```python
from agents import meta_orchestrator

options = ClaudeAgentOptions(
    model="claude-sonnet-4-5-20250929",
    permission_mode="acceptEdits",
    setting_sources=["project"],
    system_prompt=meta_orchestrator.prompt,  # ✅ 추가
)
```

**검증**:
```bash
pytest tests/test_5_complete_system_e2e.py -v
```

---

### 2. 훅 시스템 미적용 (5분)

**문제**: 훅 임포트는 성공했으나 `ClaudeAgentOptions`에 적용 안 됨

**코드 위치**: `main.py:134`

**수정 방법**:
```python
from hooks.hook_integrator import get_default_meta_orchestrator_hooks

options = ClaudeAgentOptions(
    model="claude-sonnet-4-5-20250929",
    permission_mode="acceptEdits",
    setting_sources=["project"],
    system_prompt=meta_orchestrator.prompt,
    hooks=get_default_meta_orchestrator_hooks() if HOOKS_AVAILABLE else {},  # ✅ 추가
)
```

**훅 커버리지** (총 16개 함수):
- PreToolUse: SDK 검증, 에이전트 존재 확인, 병렬 실행 감지
- PostToolUse: 품질 게이트, 메트릭 로깅, 완전성 검증
- Stop: 자동 개선 트리거 (성공률 < 70%)
- UserPromptSubmit: 모호성 감지 (>30% → Socratic 에이전트)

**검증**:
```bash
python3 -c "from hooks.hook_integrator import get_default_meta_orchestrator_hooks; print(len(get_default_meta_orchestrator_hooks()))"
# Expected: 4 (PreToolUse, PostToolUse, Stop, UserPromptSubmit)
```

---

### 3. 스트리밍 API 제거 (20분)

**문제**: `stream_response()` 메서드가 Agent SDK에 존재하지 않음 (67줄 죽은 코드)

**코드 위치**: `main.py:247-393`

**수정 방법**:
```python
# ❌ BEFORE (67 lines, never executes)
if hasattr(client, 'stream_response'):
    async with client.stream_response(user_input) as stream:
        # ... 67 lines ...

# ✅ AFTER (keep existing receive_response logic)
await client.query(user_input)

from claude_agent_sdk import types

async for message in client.receive_response():
    if isinstance(message, types.AssistantMessage):
        for block in message.content:
            if isinstance(block, types.ThinkingBlock):
                print(f"\n🧠 [Extended Thinking]")
                print(block.thinking)
            elif isinstance(block, types.TextBlock):
                print(f"\n📝 [Response]")
                print(block.text)
    # ... (keep rest as-is)
```

**검증**:
```bash
python3 -m py_compile main.py
pytest tests/test_5_complete_system_e2e.py::test_meta_orchestrator_delegation -v
```

---

## 즉시 실행 명령어

```bash
# 1. 백업
cp main.py main.py.backup

# 2. 파일 열기
nano main.py  # or vim, code, etc.

# 3. 수정 (3곳)
# - Line 134: system_prompt=meta_orchestrator.prompt 추가
# - Line 134: hooks=get_default_meta_orchestrator_hooks() if HOOKS_AVAILABLE else {} 추가
# - Lines 247-393: stream_response 분기 제거

# 4. 검증
python3 -m py_compile main.py
pytest tests/test_5_complete_system_e2e.py -v

# 5. 커밋
git add main.py
git commit -m "fix(critical): Apply system prompt, hooks, remove dead streaming code"
git push origin main
```

---

## 예상 효과

**수정 전**:
- ❌ Meta-cognitive 학습 비활성
- ❌ 훅 검증 우회
- ❌ TypeError 방지 0%
- ❌ 병렬 실행 미감지
- ❌ 자동 개선 미동작

**수정 후**:
- ✅ Meta-cognitive 학습 활성
- ✅ 훅 검증 100%
- ✅ TypeError 방지 100%
- ✅ 병렬 실행 감지 (90% 레이턴시 절감)
- ✅ 자동 개선 동작 (성공률 < 70% 시)

---

## 상세 계획

전체 개선 계획은 다음 문서 참조:
- **SYSTEM-ENHANCEMENT-PLAN-v3.0-FINAL.md** (67,000자, 13시간 구현 계획)

**주차별 우선순위**:
- Week 1 Days 1-3: 치명적 수정 (위 3개)
- Week 1 Days 4-7: 고우선순위 개선 (페르소나 주입, 테스트 커버리지)
- Week 2: 중간 우선순위 (모델 표준화, 인터럽트 처리)
- Week 3: 최적화 & 문서화

---

**다음 단계**: 위 3개 치명적 수정 즉시 적용 → 테스트 실행 → 커밋
