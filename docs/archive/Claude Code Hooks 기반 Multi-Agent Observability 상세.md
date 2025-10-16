<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Claude Code Hooks 기반 Multi-Agent Observability 상세 분석

## 시스템 아키텍처 개요

IndyDevDan과 kenneth-liao의 프로젝트를 분석한 결과, Claude Code 2.0의 **Hooks 시스템**을 활용한 실시간 다중 에이전트 모니터링은 다음과 같은 3계층 아키텍처로 구성됩니다.[^1][^2]

### 데이터 흐름 파이프라인

```
Claude Agents → Hook Scripts → HTTP POST → Bun Server → SQLite → WebSocket → Vue Client
```

이 파이프라인은 에이전트의 모든 활동을 **0.1초 이내**에 실시간으로 시각화할 수 있게 합니다.[^2]

## 1. 실시간 모니터링 구현

### Hook 이벤트 타입 (9가지)

Claude Code는 에이전트 라이프사이클의 **9개 주요 지점**에서 Hook을 실행합니다:[^1][^2]


| 이벤트 타입 | 실행 시점 | 활용 사례 |
| :-- | :-- | :-- |
| **PreToolUse** | 도구 실행 전 | 위험한 명령 차단 (rm -rf), 입력 검증 |
| **PostToolUse** | 도구 완료 후 | 실행 결과 로깅, 성능 측정 |
| **UserPromptSubmit** | 프롬프트 제출 시 | 사용자 의도 추적, 대화 흐름 분석 |
| **Notification** | 알림 발생 시 | 사용자 피드백 요청 시점 기록 |
| **Stop** | 응답 완료 시 | 세션 완료 통계, 토큰 사용량 집계 |
| **SubagentStop** | 서브에이전트 완료 | 병렬 작업 완료 추적 |
| **PreCompact** | 컨텍스트 압축 전 | 메모리 관리 모니터링 |
| **SessionStart** | 세션 시작 | 새 작업 시작 감지 |
| **SessionEnd** | 세션 종료 | 최종 성과 보고서 생성 |

### 실시간 대시보드 구성

**IndyDevDan의 구현**은 Vue 3 기반 실시간 대시보드를 제공합니다:[^3][^2]

**LivePulseChart.vue**: 에이전트 활동을 **1분/3분/5분** 단위로 시각화

- 세션별 색상 구분으로 최대 10개 동시 에이전트 추적
- 이벤트 타입별 이모지 표시 (🔧 PreToolUse, ✅ PostToolUse)

**EventTimeline.vue**: 스트리밍 이벤트 목록

- 자동 스크롤 with 수동 오버라이드
- 최대 100개 이벤트 표시 (설정 가능)
- AI 요약 기능 (Haiku 모델 사용)

**FilterPanel.vue**: 다중 선택 필터

- 앱별, 세션별, 이벤트 타입별 필터링
- 실시간 필터 적용 (페이지 리로드 없음)


## 2. 상태 관리 시스템

### Session Management (Claude Agent SDK)

Claude Agent SDK는 **세션 ID 기반 상태 지속성**을 제공합니다:[^4][^5]

```typescript
// 세션 ID 캡처
let sessionId: string | undefined;

const response = query({
  prompt: "웹 애플리케이션 구축 도와줘",
  options: { model: "claude-sonnet-4-5" }
});

for await (const message of response) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;
    console.log(`세션 시작: ${sessionId}`);
  }
}

// 나중에 재개
const resumedResponse = query({
  prompt: "이전 작업 계속하기",
  options: { resume: sessionId }
});
```


### Session Forking (실험적 브랜칭)

**대안 탐색**을 위한 세션 포킹 기능:[^4]

```typescript
// 원본 세션은 그대로 유지하면서 새 브랜치 생성
const forkedResponse = query({
  prompt: "이번엔 GraphQL로 재설계해줘",
  options: {
    resume: sessionId,
    forkSession: true,  // 새 세션 ID 생성
    model: "claude-sonnet-4-5"
  }
});
```

| 옵션 | forkSession: false (기본) | forkSession: true |
| :-- | :-- | :-- |
| 세션 ID | 원본과 동일 | 새 ID 생성 |
| 히스토리 | 원본 세션에 추가 | 재개 시점부터 새 브랜치 |
| 원본 세션 | 수정됨 | 보존됨 |

### SQLite WAL 모드 영구 저장

IndyDevDan 구현은 **SQLite Write-Ahead Logging**을 사용하여:[^2]

- 동시 읽기/쓰기 지원 (여러 에이전트 동시 실행)
- 자동 스키마 마이그레이션
- 30일 자동 정리 (설정 가능)
- 채팅 트랜스크립트 전체 저장

```sql
-- 이벤트 테이블 스키마 예제
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_app TEXT NOT NULL,
  session_id TEXT NOT NULL,
  hook_event_type TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  payload JSON,
  summary TEXT,
  chat_transcript JSON
);

CREATE INDEX idx_session ON events(session_id);
CREATE INDEX idx_timestamp ON events(timestamp);
```


## 3. 체크포인트 시스템 심층 분석

### 자동 추적 메커니즘

Claude Code 2.0의 체크포인트는 **파일 편집 도구**만 추적합니다:[^6][^7]

**추적되는 것**:

- `Edit`, `Write` 도구로 수정한 모든 파일
- 모든 사용자 프롬프트마다 자동 스냅샷
- 세션 재개 시에도 접근 가능 (30일 보관)

**추적되지 않는 것**:

- Bash 명령 (`rm`, `mv`, `cp`, `sed` 등)
- Claude 외부에서 수동으로 변경한 파일
- 다른 동시 세션의 편집


### 복원 옵션 3가지

```bash
# /rewind 명령 또는 Esc+Esc 실행 시 표시되는 메뉴
┌─────────────────────────────────────┐
│ Rewind to Checkpoint                │
├─────────────────────────────────────┤
│ 1. Conversation only (대화만)         │
│    코드 유지, 대화 히스토리만 되감기      │
│                                     │
│ 2. Code only (코드만)                 │
│    대화 유지, 파일 변경만 되돌리기        │
│                                     │
│ 3. Both (대화와 코드 모두)             │
│    세션 전체를 이전 시점으로 복원         │
└─────────────────────────────────────┘
```


### 실전 활용 시나리오

**시나리오 1: 잘못된 리팩토링 복구**[^6]

```
1. Claude에게 "React 컴포넌트를 새 상태관리 라이브러리로 리팩토링해줘" 요청
2. 여러 파일 변경 시작했는데 구식 API 사용 중임을 발견
3. Esc+Esc → "Code only" 선택 → 잘못된 편집 즉시 제거
4. 대화 히스토리는 유지되므로 올바른 문서 링크 제공하여 재시도
5. 전체 복구 시간: 30초 이내
```

**시나리오 2: 대화 방향 전환**

```
1. API 설계에 대한 긴 대화 진행
2. 중간에 더 나은 접근법 떠오름
3. "Conversation only" 선택하여 대화를 3단계 전으로 되감기
4. 코드는 그대로 유지하면서 새로운 방향으로 대화 재개
```


## 4. 통합 구현 가이드

### IndyDevDan 방식 (전체 Observability)

```bash
# 1. 저장소 클론
git clone https://github.com/disler/claude-code-hooks-multi-agent-observability
cd claude-code-hooks-multi-agent-observability

# 2. 의존성 설치
cd apps/server && bun install
cd ../client && npm install

# 3. 환경 변수 설정
echo "ANTHROPIC_API_KEY=your-key" > .env
echo "VITE_MAX_EVENTS_TO_DISPLAY=100" > apps/client/.env

# 4. 시스템 시작
./scripts/start-system.sh

# 5. 브라우저에서 확인
# http://localhost:5173
```


### kenneth-liao 방식 (SDK 학습)

```bash
# 1. 저장소 클론
git clone https://github.com/kenneth-liao/claude-agent-sdk-intro
cd claude-agent-sdk-intro

# 2. Python 환경 설정
uv sync

# 3. .claude/settings.json 경로 수정 (중요!)
# macOS: 기본 경로 사용
# Linux/Windows: 사운드 파일 경로 수정

# 4. 모듈별 실행
python 0_querying.py              # 기본 쿼리
python 1_messages.py              # 메시지 처리
python 2_tools.py                 # 커스텀 도구
python 3_options.py --model claude-opus-4-20250514
python 4_convo_loop.py            # 대화 루프
python 5_mcp.py                   # MCP 통합 (Node.js 필요)
python 6_subagents.py             # 서브에이전트
```


### 사용자 정의 Hook 예제

```python
# .claude/hooks/custom_monitor.py
#!/usr/bin/env python3
import json
import sys
from datetime import datetime

def monitor_tool_usage():
    event = json.load(sys.stdin)
    
    tool_name = event.get('tool_name', 'Unknown')
    session_id = event.get('session_id', 'N/A')
    
    # 로그 파일에 기록
    with open('.claude/tool_usage.log', 'a') as f:
        f.write(f"{datetime.now()} | {session_id} | {tool_name}\n")
    
    # 위험한 도구 차단
    if tool_name == 'Bash':
        command = event.get('tool_input', {}).get('command', '')
        if 'rm -rf' in command or 'sudo' in command:
            # exit 2 = 도구 실행 차단
            sys.exit(2)
    
    # exit 0 = 정상 진행
    sys.exit(0)

if __name__ == "__main__":
    monitor_tool_usage()
```

```json
// .claude/settings.json에 추가
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/hooks/custom_monitor.py"
      }]
    }]
  }
}
```


## 핵심 통찰

### 1. 실시간 모니터링의 가치

다중 에이전트 시스템에서 **가시성 없이는 스케일 불가능**합니다:[^3]

- 5개 이상 에이전트 동시 실행 시 CLI 추적 불가능
- WebSocket 기반 실시간 스트리밍으로 **모든 에이전트 활동 한눈에 파악**
- 문제 발생 시 즉시 감지하여 토큰 낭비 방지


### 2. 상태 관리의 중요성

세션 관리와 체크포인트는 **실험적 개발의 안전망**:[^7][^4]

- 대담한 리팩토링 시도 가능 (언제든 되돌릴 수 있음)
- 여러 접근법 병렬 탐색 (세션 포킹)
- 대화 컨텍스트 보존하면서 코드만 롤백


### 3. 프로덕션 배포 고려사항

IndyDevDan 시스템은 **로컬 개발 환경에 최적화**되어 있습니다:[^2]

**장점**:

- 설정 간단 (5분 이내 실행 가능)
- 보안 샌드박스 (로컬 SQLite)
- 무료 (API 키만 필요)

**확장 시 필요한 것**:

- 컨테이너화 (Docker/Kubernetes)
- 인증/권한 관리
- 분산 데이터베이스 (PostgreSQL/MongoDB)
- 로드 밸런싱 (여러 서버)


## 결론

Claude Code 2.0의 Hooks 시스템은 **다중 에이전트 오케스트레이션의 핵심 인프라**입니다. IndyDevDan의 구현은 실시간 모니터링과 상태 관리를 완벽하게 통합하여, 비디오에서 본 BIG 3 SUPER AGENT의 관찰성(Observability) 부분을 **Claude 생태계 내에서 완전히 구현 가능**함을 증명합니다.[^3][^2]

**다음 단계 권장사항**:

1. IndyDevDan 저장소 클론하여 로컬 실행
2. kenneth-liao 튜토리얼로 Agent SDK 학습
3. 자신의 프로젝트에 `.claude` 디렉토리 복사
4. 커스텀 Hook 작성하여 특정 워크플로우 자동화
5. WebSocket 대시보드로 실시간 모니터링 시작
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://docs.claude.com/en/docs/claude-code/hooks-guide

[^2]: https://github.com/disler/claude-code-hooks-multi-agent-observability

[^3]: https://www.youtube.com/watch?v=9ijnN985O_c

[^4]: https://docs.claude.com/en/api/agent-sdk/sessions

[^5]: https://docs.claude.com/en/api/agent-sdk/streaming-vs-single-mode

[^6]: https://skywork.ai/skypage/en/claude-code-checkpoints-ai-coding/1976917740735229952

[^7]: https://docs.claude.com/en/docs/claude-code/checkpointing

[^8]: https://github.com/kenneth-liao/claude-agent-sdk-intro

[^9]: https://docs.claude.com/en/docs/claude-code/monitoring-usage

[^10]: https://www.builder.io/blog/claude-code

[^11]: https://arize.com/blog/claude-code-observability-and-tracing-introducing-dev-agent-lens/

[^12]: https://suiteinsider.com/complete-guide-creating-claude-code-hooks/

[^13]: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

[^14]: https://www.youtube.com/channel/UC_x36zCEGilGpB1m-V4gmjg/videos

[^15]: https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks

[^16]: https://github.com/wshobson/agents

[^17]: https://dev.to/bredmond1019/multi-agent-orchestration-running-10-claude-instances-in-parallel-part-3-29da

[^18]: https://www.implicator.ai/claude-code-hooks-complete-tutorial/

[^19]: https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/

[^20]: https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/

[^21]: https://www.youtube.com/watch?v=amEUIuBKwvg

[^22]: https://skywork.ai/blog/openai-agent-builder-vs-claude-agent-sdk/

[^23]: https://www.claude-hub.com/resource/github-cli-toomas-tt-claude-code-hooks-multi-agent-observability-claude-code-hooks-multi-agent-observability/

[^24]: https://www.reddit.com/r/ClaudeAI/comments/1loodjn/claude_code_now_supports_hooks/

[^25]: https://docs.langchain.com/langsmith/trace-claude-agent-sdk

[^26]: https://ufukozen.com/blog/claude-code-2-0-autonomous-features

[^27]: https://skywork.ai/blog/claude-code-2-0-checkpoints-subagents-autonomous-coding/

[^28]: https://apidog.com/blog/ccundo/

[^29]: https://www.reddit.com/r/aiagents/comments/1nuh1kq/claude_agent_sdk_build_ai_agents_that_actually/

[^30]: https://anthropic.com/news/enabling-claude-code-to-work-more-autonomously

[^31]: https://github.com/anthropics/claude-code/issues/4472

[^32]: https://anthropic.mintlify.app/en/api/agent-sdk/hosting

[^33]: https://github.com/anthropics/claude-code/issues/8605

[^34]: https://www.reddit.com/r/ClaudeAI/comments/1kz15j7/windusrfcursor_user_claude_code_how_do_you/

[^35]: https://github.com/anthropics/claude-agent-sdk-typescript/issues/3

[^36]: https://www.reddit.com/r/ClaudeAI/comments/1ntnwbq/claude_code_v20_we_got_check_points_o/

[^37]: https://github.com/anthropics/claude-code/issues/353

[^38]: https://softdevai.com/claude-code-2-0-changing-developer-workflows-with-ai/

[^39]: https://www.facebook.com/extremetechdotcom/posts/in-claude-code-checkpoints-allow-users-to-save-and-roll-back-their-work/1239754734858557/

[^40]: https://www.youtube.com/watch?v=gP5iZ6DCrUI

