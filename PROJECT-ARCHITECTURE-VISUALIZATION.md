# 수학 교육 시스템 완전 가이드 (초보자용)

> **프로그래밍 처음 접하시는 분들을 위한 완전 분석**
> 이 문서는 main.py부터 시작해서 모든 파일이 어떻게 동작하는지 설명합니다.

---

## 📚 목차

1. [프로그램 시작부터 끝까지](#1-프로그램-시작부터-끝까지)
2. [파일 구조 한눈에 보기](#2-파일-구조-한눈에-보기)
3. [각 파일의 역할](#3-각-파일의-역할)
4. [컴포넌트 상호작용](#4-컴포넌트-상호작용)
5. [코드 레벨 상세 분석](#5-코드-레벨-상세-분석)

---

## 1. 프로그램 시작부터 끝까지

### 🎬 실행 흐름 다이어그램

```
┌──────────────────────────────────────────────────────────────────┐
│  사용자가 터미널에서 실행: python main.py                         │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  1단계: 프로그램 시작 (main.py 최하단)                            │
│  ────────────────────────────────────────────────────────────    │
│  if __name__ == "__main__":                                      │
│      nest_asyncio.apply()        # 비동기 처리 준비              │
│      asyncio.run(main())         # main() 함수 실행              │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  2단계: 초기화 (main() 함수 시작)                                 │
│  ────────────────────────────────────────────────────────────    │
│  ① load_dotenv()                 # .env 파일에서 설정 읽기       │
│  ② print("환영 메시지")          # 시스템 정보 출력              │
│  ③ Infrastructure 초기화 (선택)                                  │
│     - StructuredLogger           # 로그 기록                     │
│     - PerformanceMonitor         # 성능 측정                     │
│     - ErrorTracker               # 에러 추적                     │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  3단계: AI 에이전트 시스템 설정                                    │
│  ────────────────────────────────────────────────────────────    │
│  ClaudeAgentOptions 생성:                                        │
│  - model: "claude-sonnet-4-5"    # 어떤 AI 모델 사용할지         │
│  - system_prompt: .claude/CLAUDE.md를 읽어서 설정                │
│  - allowed_tools: [Task, Read, Write, Edit, ...]                │
│  - agents: { 11개 subagent 등록 }                               │
│  - mcp_servers: { memory-keeper, sequential-thinking }          │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  4단계: 대화 시스템 시작                                           │
│  ────────────────────────────────────────────────────────────    │
│  async with ClaudeSDKClient(options) as client:                  │
│      while True:  ← 무한 반복 (사용자가 종료할 때까지)            │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  5단계: 사용자 입력 대기                                           │
│  ────────────────────────────────────────────────────────────    │
│  user_input = input("You: ")    # 사용자 질문 기다림              │
│                                                                  │
│  만약 "exit"을 입력하면 → 프로그램 종료                           │
│  만약 빈 줄이면 → 다시 입력 대기                                  │
│  그 외 → 다음 단계로                                              │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  6단계: AI에게 질문 전송                                           │
│  ────────────────────────────────────────────────────────────    │
│  await client.query(user_input)  # 사용자 질문을 AI에게 보냄      │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  7단계: AI 응답 받기 및 출력                                       │
│  ────────────────────────────────────────────────────────────    │
│  async for message in client.receive_response():                │
│      if TextBlock:         → 텍스트 출력                         │
│      if ThinkingBlock:     → "🧠 생각 중..." 출력                │
│      if ToolUseBlock:      → "🔧 도구 사용 중..." 출력           │
│      if ResultMessage:     → "✅ 완료" 출력                      │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
                  5단계로 돌아감 (다음 질문 대기)
```

### 🔍 **초보자를 위한 설명**

**1. python main.py를 실행하면?**
- 컴퓨터가 main.py 파일을 읽기 시작합니다
- 파일 맨 아래 `if __name__ == "__main__":` 부분이 실행됩니다
- 이것은 "이 파일이 직접 실행될 때만 아래 코드를 실행해라"라는 뜻입니다

**2. asyncio.run(main())이란?**
- `async`는 "비동기"라는 뜻입니다
- 여러 작업을 동시에 처리할 수 있게 해줍니다
- 예: AI가 생각하는 동안 다른 작업도 할 수 있음

**3. while True는 무한 루프**
- "True는 항상 참"이므로 무한히 반복됩니다
- 사용자가 "exit"을 입력하거나 Ctrl+C를 누르면 종료됩니다

**4. await client.query()는 기다림**
- AI에게 질문을 보내고 답변을 기다립니다
- `await`은 "이 작업이 끝날 때까지 기다려"라는 의미입니다

---

## 2. 파일 구조 한눈에 보기

```
/home/kc-palantir/math/              ← 프로젝트 루트 (최상위 폴더)
│
├── main.py                          ★ 진입점 (프로그램 시작점)
├── config.py                        ★ 설정 파일 (경로, 디렉토리)
│
├── subagents/                       ★ 11개 전문 AI 에이전트
│   ├── __init__.py                  → 11개 agent를 하나로 모음
│   ├── file_builder_agent.py        → 파일 생성 전문가
│   ├── validator_agent.py           → 품질 검증 전문가
│   ├── web_research_agent.py        → 웹 검색 전문가
│   ├── requirements_agent.py        → 요구사항 명확화 전문가
│   ├── graph_query_agent.py         → 그래프DB 전문가
│   ├── decomposer_agent.py          → 문제 분해 전문가
│   ├── problem_generator_agent.py   → 문제 생성 전문가
│   ├── personalization_agent.py     → 개인화 전문가
│   ├── code_improver_agent.py       → 코드 개선 전문가
│   ├── planning_analyzer_agent.py   → 계획 분석 전문가
│   └── query_helper_agent.py        → 쿼리 도우미
│
├── infrastructure/                  ★ 시스템 지원 서비스
│   ├── __init__.py                  → 모든 서비스를 하나로 모음
│   ├── logging_service.py           → 로그 기록 (누가 언제 뭘 했는지)
│   ├── monitoring_service.py        → 성능 측정 (얼마나 빠른지)
│   ├── error_service.py             → 에러 처리 (문제 생기면 재시도)
│   ├── context_service.py           → 대화 맥락 관리
│   └── registry_service.py          → 에이전트 등록부
│
├── tools/                           ★ 유틸리티 도구들
│   ├── weight_calculator_tool.py    → 가중치 계산
│   ├── feedback_collector_tool.py   → 피드백 수집
│   ├── log_optimizer_tool.py        → 로그 최적화
│   ├── decision_tracer_tool.py      → 의사결정 추적
│   ├── graph_client_tool.py         → 그래프 DB 클라이언트
│   └── memory_adapter_tool.py       → 메모리 어댑터
│
├── .claude/                         ★ AI 설정 디렉토리
│   ├── CLAUDE.md                    → Meta-orchestrator 시스템 프롬프트
│   ├── hooks/                       → 훅 시스템
│   ├── session_summaries/           → 세션 요약
│   └── templates/                   → 프롬프트 템플릿
│
├── tests/                           ★ 테스트 코드
│   ├── test_1_semantic_tier_e2e.py  → 의미 계층 테스트
│   ├── test_2_kinetic_tier_e2e.py   → 실행 계층 테스트
│   └── ...
│
├── pyproject.toml                   → 프로젝트 설정 & 의존성
├── uv.lock                          → 의존성 버전 잠금
└── README.md                        → 프로젝트 설명서
```

### 🔍 **각 폴더의 역할**

| 폴더/파일 | 역할 | 비유 |
|---------|------|------|
| `main.py` | 프로그램의 시작점 | 회사의 대표이사 |
| `subagents/` | 11개 전문 AI | 각 부서의 전문가들 |
| `infrastructure/` | 시스템 지원 | 인사팀, 총무팀 (뒷받침) |
| `tools/` | 유틸리티 | 사무용품, 도구함 |
| `.claude/` | AI 설정 | 회사 규정집 |
| `config.py` | 환경 설정 | 회사 주소록 |
| `tests/` | 품질 검증 | 품질관리팀 |

---

## 3. 각 파일의 역할

### 3.1 main.py (진입점) - 197줄

**역할**: 프로그램의 시작점이자 전체 흐름을 제어하는 중앙 컨트롤러

**주요 코드 분석**:

```python
# 줄 13-30: 필요한 모듈 가져오기
import asyncio                      # 비동기 처리 (여러 작업 동시에)
from dotenv import load_dotenv       # .env 파일 읽기
from claude_agent_sdk import ClaudeSDKClient  # AI SDK

from subagents import (              # 11개 전문 에이전트 가져오기
    knowledge_builder,
    quality_agent,
    research_agent,
    # ... 나머지 8개
)

# 줄 33-37: 인프라 가져오기 (선택)
try:
    from infrastructure import StructuredLogger, ...
    INFRASTRUCTURE_AVAILABLE = True  # 있으면 True
except ImportError:
    INFRASTRUCTURE_AVAILABLE = False  # 없으면 False

# 줄 40-71: 초기화
async def main():
    load_dotenv()  # .env 파일에서 API 키 등 읽기
    print("환영 메시지")

    # 인프라가 있으면 초기화
    if INFRASTRUCTURE_AVAILABLE:
        logger = StructuredLogger(...)  # 로그 기록 시작
        perf_monitor = PerformanceMonitor()  # 성능 측정 시작

# 줄 73-126: AI 옵션 설정
options = ClaudeAgentOptions(
    model="claude-sonnet-4-5",       # 어떤 AI 모델?
    permission_mode="acceptEdits",   # 편집 권한
    system_prompt={...},             # .claude/CLAUDE.md 읽기
    allowed_tools=[...],             # 사용 가능한 도구들
    agents={...},                    # 11개 subagent 등록
    mcp_servers={...}                # 외부 서버 설정
)

# 줄 129-189: 대화 루프
async with ClaudeSDKClient(options) as client:
    while True:
        user_input = input("You: ")  # 사용자 질문 입력

        if user_input == "exit":
            break  # 종료

        await client.query(user_input)  # AI에게 질문

        # AI 답변 받아서 출력
        async for message in client.receive_response():
            print(message)

# 줄 191-197: 프로그램 시작
if __name__ == "__main__":
    nest_asyncio.apply()  # 비동기 준비
    asyncio.run(main())   # main() 실행
```

**초보자를 위한 설명**:
- `async`와 `await`: "동시에 여러 일을 할 수 있게 해주는 마법"
- `import`: "다른 파일의 코드를 가져와서 쓰겠다"
- `while True`: "사용자가 exit을 입력할 때까지 계속 반복"
- `try-except`: "에러가 나면 무시하고 계속 진행"

---

### 3.2 subagents/__init__.py (에이전트 모음) - 45줄

**역할**: 11개 전문 에이전트를 하나로 묶어서 main.py에 제공

```python
# 줄 13-18: 핵심 수학 교육 에이전트 (6개)
from .file_builder_agent import knowledge_builder
from .validator_agent import quality_agent
from .web_research_agent import research_agent
# ...

# 줄 20-27: 확장 기능 & 시스템 개선 (5개)
from .graph_query_agent import neo4j_query_agent
from .personalization_agent import personalization_engine_agent
# ...

# 줄 29-44: 외부에 공개할 이름들
__all__ = [
    "knowledge_builder",
    "quality_agent",
    # ... 총 11개
]
```

**비유**:
- 회사의 조직도 같은 역할
- "연구팀은 3층, 개발팀은 4층"처럼 각 전문가가 어디 있는지 알려줌

---

### 3.3 subagents/file_builder_agent.py (파일 생성 전문가) - 164줄

**역할**: Obsidian 마크다운 파일을 생성하는 전문 AI

```python
# 줄 11: AgentDefinition으로 에이전트 정의
from claude_agent_sdk import AgentDefinition

# 줄 13-163: 에이전트 설정
knowledge_builder = AgentDefinition(
    # 줄 14: 간단한 설명
    description="수학 개념 파일을 만드는 전문가",

    # 줄 16-151: 상세한 작업 지침서 (프롬프트)
    prompt="""
    # 당신의 역할
    - 파일 생성 전문가
    - LaTeX 수식 전문가
    - 위키링크 연결 전문가

    # 작업 흐름
    1. 연구 데이터 받기
    2. 분석 & 분해
    3. Obsidian 파일 생성
    4. 파일 저장
    5. 검증
    """,

    # 줄 153: 어떤 AI 모델 사용?
    model="sonnet",

    # 줄 155-162: 사용 가능한 도구들
    tools=[
        'Read',    # 파일 읽기
        'Write',   # 파일 쓰기
        'Edit',    # 파일 수정
        'Grep',    # 파일 검색
        'Glob',    # 파일 찾기
        'TodoWrite'  # 할 일 목록
    ]
)
```

**초보자를 위한 설명**:
- `AgentDefinition`: "에이전트를 정의하는 설계도"
- `description`: "이 에이전트가 뭘 하는지 한 줄 요약"
- `prompt`: "에이전트에게 주는 상세한 작업 지침서"
- `tools`: "에이전트가 사용할 수 있는 도구들"

**예시**:
```
사용자: "피타고라스 정리 파일 만들어줘"
  ↓
Meta-orchestrator: knowledge_builder에게 Task 위임
  ↓
knowledge_builder:
  1. Write 도구로 파일 생성
  2. LaTeX로 수식 작성: $a^2 + b^2 = c^2$
  3. 위키링크로 연결: [[직각삼각형]]
  4. Read 도구로 검증
  ↓
완료!
```

---

### 3.4 infrastructure/logging_service.py (로그 기록) - 413줄

**역할**: 누가, 언제, 무엇을, 어떻게 했는지 기록

```python
# 줄 26: trace_id로 작업 추적
trace_id_var = ContextVar('trace_id', default=None)

# 줄 29-46: 로그 엔트리 구조
@dataclass
class LogEntry:
    timestamp: str      # 언제?
    trace_id: str       # 어느 작업?
    event_type: str     # 무슨 이벤트?
    agent_name: str     # 누가?
    level: str          # 중요도? (INFO, ERROR, ...)
    message: str        # 메시지
    duration_ms: float  # 얼마나 걸렸나?

# 줄 203-365: StructuredLogger 클래스
class StructuredLogger:
    def __init__(self, log_dir="/tmp/math-agent-logs"):
        self.log_dir = Path(log_dir)
        self.log_file = ...  # JSONL 파일

    def agent_start(self, agent_name, task):
        # 에이전트 시작 기록
        entry = LogEntry(...)
        self._write_log(entry)

    def agent_complete(self, agent_name, duration, success):
        # 에이전트 완료 기록
        entry = LogEntry(...)
        self._write_log(entry)
```

**초보자를 위한 설명**:
- **로그(Log)**: 프로그램이 무슨 일을 했는지 기록하는 일기장
- **trace_id**: 여러 작업을 추적할 수 있는 "작업 번호"
- **JSONL**: JSON 형식으로 한 줄씩 저장하는 파일 형식

**예시**:
```
[2025-10-16 10:30:15] START knowledge_builder: 피타고라스 정리 파일 생성
[2025-10-16 10:30:17] Tool call: Write (12ms)
[2025-10-16 10:30:18] ✅ knowledge_builder: 2500ms
```

---

### 3.5 infrastructure/monitoring_service.py (성능 측정)

**역할**: 각 작업이 얼마나 빠른지, 얼마나 자주 실패하는지 측정

```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}  # 측정 데이터 저장

    def record_execution(self, agent_name, duration_ms, success):
        # 실행 시간과 성공 여부 기록
        if agent_name not in self.metrics:
            self.metrics[agent_name] = AgentMetrics()

        self.metrics[agent_name].total_calls += 1
        self.metrics[agent_name].total_duration_ms += duration_ms
        if success:
            self.metrics[agent_name].success_count += 1

    def print_summary(self):
        # 통계 출력
        for agent, metrics in self.metrics.items():
            avg_duration = metrics.total_duration_ms / metrics.total_calls
            success_rate = metrics.success_count / metrics.total_calls
            print(f"{agent}: 평균 {avg_duration:.0f}ms, 성공률 {success_rate:.1%}")
```

**비유**:
- 회사의 업무 성과 평가 시스템
- "A팀은 평균 2분 걸림, 성공률 95%"

---

### 3.6 infrastructure/error_service.py (에러 처리)

**역할**: 문제가 생기면 자동으로 재시도하거나 사람에게 알림

```python
class ErrorTracker:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries  # 최대 3번 재시도
        self.error_history = []

    def record_error(self, agent_name, task_id, error, context):
        # 에러 발생 기록
        self.error_history.append({
            'agent': agent_name,
            'task': task_id,
            'error': str(error),
            'context': context,
            'timestamp': datetime.now()
        })

    async def resilient_task(self, task_func, *args, **kwargs):
        # 자동 재시도
        for attempt in range(self.max_retries):
            try:
                return await task_func(*args, **kwargs)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # 1초, 2초, 4초 대기
                    continue
                else:
                    raise  # 3번 실패하면 포기
```

**비유**:
- 전화를 걸었는데 안 받으면 몇 번 더 시도하는 것
- 3번 시도해도 안 되면 포기

---

### 3.7 config.py (설정 파일) - 123줄

**역할**: 프로젝트의 모든 경로와 디렉토리를 관리

```python
# 줄 12-35: 프로젝트 루트 찾기
def find_project_root():
    current = Path(__file__)  # config.py의 위치

    # pyproject.toml이나 .git 폴더를 찾을 때까지 상위로 올라감
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("프로젝트 루트를 찾을 수 없습니다")

# 줄 39: 프로젝트 루트
PROJECT_ROOT = find_project_root()

# 줄 42-56: 주요 디렉토리들
AGENTS_DIR = PROJECT_ROOT / "agents"
TESTS_DIR = PROJECT_ROOT / "tests"
TOOLS_DIR = PROJECT_ROOT / "tools"
MATH_VAULT_DIR = ...  # 수학 노트 저장 위치

# 줄 67-81: 디렉토리 자동 생성
def ensure_directories():
    for directory in [TESTS_DIR, TOOLS_DIR, MATH_VAULT_DIR, ...]:
        directory.mkdir(parents=True, exist_ok=True)

# 줄 108: 프로그램 시작하면 자동 실행
ensure_directories()
```

**초보자를 위한 설명**:
- `Path`: 파일 경로를 다루는 도구
- `exist_ok=True`: "이미 있어도 에러 내지 마"
- `/`: 경로를 이어붙이는 연산자 (예: `PROJECT_ROOT / "tests"`)

**비유**:
- 회사의 주소록
- "문서는 3층 A동, 자료는 2층 B동"

---

## 4. 컴포넌트 상호작용

### 4.1 전체 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────────────────┐
│                        사용자 (You)                                   │
│                    터미널에서 질문 입력                                │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ "피타고라스 정리 파일 만들어줘"
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      main.py (대화 루프)                              │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  while True:                                                   │  │
│  │      user_input = input("You: ")                               │  │
│  │      await client.query(user_input)                            │  │
│  │      async for message in client.receive_response():           │  │
│  │          print(message)                                        │  │
│  └────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ ClaudeSDKClient에게 전달
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│              ClaudeSDKClient (AI 클라이언트)                          │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  • .claude/CLAUDE.md 읽어서 system prompt로 사용               │  │
│  │  • 11개 subagent 관리                                          │  │
│  │  • MCP servers (memory-keeper, sequential-thinking) 연결      │  │
│  │  • Task 도구를 통해 subagent에게 작업 위임                     │  │
│  └────────────────────────────────────────────────────────────────┘  │
└───────────────┬───────────────┬──────────────┬───────────────────────┘
                │               │              │
      ┌─────────┘               │              └─────────┐
      │                         │                        │
      │ Task 위임               │ 로깅/모니터링           │ MCP 통신
      ▼                         ▼                        ▼
┌─────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   Subagents     │   │ Infrastructure   │   │   MCP Servers    │
│  (11개 전문가)   │   │  (지원 시스템)    │   │  (외부 서비스)    │
├─────────────────┤   ├──────────────────┤   ├──────────────────┤
│ • knowledge-    │   │ • StructuredLog  │   │ • memory-keeper  │
│   builder       │   │ • Performance    │   │ • sequential-    │
│ • quality-agent │   │   Monitor        │   │   thinking       │
│ • research-     │   │ • ErrorTracker   │   │                  │
│   agent         │   │ • ContextMgr     │   │                  │
│ • socratic-req  │   │ • AgentRegistry  │   │                  │
│ • neo4j-query   │   │                  │   │                  │
│ • problem-      │   │                  │   │                  │
│   decomposer    │   │                  │   │                  │
│ • problem-      │   │                  │   │                  │
│   scaffolding   │   │                  │   │                  │
│ • personaliz.   │   │                  │   │                  │
│ • self-improver │   │                  │   │                  │
│ • meta-planning │   │                  │   │                  │
│ • meta-query    │   │                  │   │                  │
└─────────────────┘   └──────────────────┘   └──────────────────┘
      │                         │                        │
      │ 도구 사용               │                        │
      ▼                         ▼                        ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          Tools                                       │
│  • Read, Write, Edit (파일 조작)                                     │
│  • Grep, Glob (파일 검색)                                            │
│  • TodoWrite (작업 추적)                                             │
│  • graph_client_tool (Neo4j)                                        │
│  • weight_calculator_tool                                           │
│  • feedback_collector_tool                                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 4.2 실제 작업 흐름 예시

**시나리오**: 사용자가 "피타고라스 정리 파일 만들어줘"라고 입력

```
Step 1: 사용자 입력
┌────────────────┐
│  사용자        │
│  "피타고라스   │
│   정리 파일    │
│   만들어줘"    │
└────────┬───────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ main.py: user_input = input("You: ")                  │
│         await client.query(user_input)                │
└────────┬───────────────────────────────────────────────┘
         │
         ▼

Step 2: Meta-orchestrator 판단 (.claude/CLAUDE.md)
┌────────────────────────────────────────────────────────┐
│ ClaudeSDKClient:                                       │
│ "파일 생성이 필요하네. 먼저 research-agent에게         │
│  피타고라스 정리를 조사하게 하고, 그 결과를            │
│  knowledge-builder에게 넘겨서 파일 생성하자"           │
└────────┬───────────────────────────────────────────────┘
         │
         ├─────────────────────────────────────┐
         │                                     │
         ▼                                     ▼

Step 3a: 연구 단계                    Step 3b: 로깅 시작
┌──────────────────────┐            ┌──────────────────────┐
│ Task 도구 사용:      │            │ StructuredLogger:    │
│ research-agent에게   │            │ agent_start(         │
│ "피타고라스 정리     │            │   "research-agent",  │
│  조사" 요청          │            │   "피타고라스 조사"  │
└──────┬───────────────┘            │ )                    │
       │                            └──────────────────────┘
       ▼
┌──────────────────────────────────────────────────────┐
│ research-agent 실행:                                 │
│  1. WebSearch 도구로 "피타고라스 정리" 검색          │
│  2. 여러 출처에서 정보 수집                          │
│  3. 정의, 증명, 예시, 응용 정리                      │
│  4. 결과 반환                                        │
└──────┬───────────────────────────────────────────────┘
       │
       │ 연구 결과
       ▼

Step 4: 파일 생성
┌──────────────────────────────────────────────────────┐
│ Task 도구 사용:                                      │
│ knowledge-builder에게 연구 결과와 함께               │
│ "Obsidian 파일 생성" 요청                            │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│ knowledge-builder 실행:                              │
│  1. 연구 결과 분석                                   │
│  2. YAML frontmatter 생성                            │
│     - type: theorem                                  │
│     - prerequisites: [[직각삼각형]], [[제곱]]        │
│  3. LaTeX 수식 작성                                  │
│     $$a^2 + b^2 = c^2$$                              │
│  4. Write 도구로 파일 저장                           │
│     /math-vault/Theorems/pythagorean-theorem.md      │
│  5. Read 도구로 검증                                 │
│  6. 완료 보고                                        │
└──────┬───────────────────────────────────────────────┘
       │
       ▼

Step 5: 품질 검증 (선택)
┌──────────────────────────────────────────────────────┐
│ Task 도구 사용:                                      │
│ quality-agent에게 "파일 검증" 요청                   │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│ quality-agent 실행:                                  │
│  1. Read 도구로 파일 읽기                            │
│  2. YAML 문법 검증 ✅                                │
│  3. LaTeX 문법 검증 ✅                               │
│  4. 위키링크 형식 검증 ✅                            │
│  5. 필수 섹션 존재 여부 검증 ✅                      │
│  6. 검증 결과 보고                                   │
└──────┬───────────────────────────────────────────────┘
       │
       ▼

Step 6: 사용자에게 결과 보고
┌──────────────────────────────────────────────────────┐
│ ClaudeSDKClient → main.py:                           │
│ "✅ 피타고라스 정리 파일을 생성했습니다.             │
│  경로: /math-vault/Theorems/pythagorean-theorem.md   │
│  - 정의 ✅                                           │
│  - 증명 ✅                                           │
│  - 예시 3개 ✅                                       │
│  - 선수 지식: [[직각삼각형]], [[제곱]] ✅            │
│  - 응용: [[거리 공식]], [[삼각함수]] ✅              │
│  품질 검증 완료 ✅"                                  │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌────────────────┐
│  사용자        │
│  화면에 결과   │
│  출력됨        │
└────────────────┘
```

---

## 5. 코드 레벨 상세 분석

### 5.1 main.py 핵심 코드 흐름

```python
# ============================================================
# STEP 1: 프로그램 진입점 (최하단, 줄 191-197)
# ============================================================
if __name__ == "__main__":
    """
    이 조건문은 "이 파일이 직접 실행될 때만 아래 코드 실행"
    다른 파일에서 import하면 실행되지 않음
    """

    # 비동기(async) 함수를 중첩해서 사용할 수 있게 설정
    # (Jupyter notebook 등에서 필요)
    import nest_asyncio
    nest_asyncio.apply()

    # asyncio.run()은 비동기 함수를 실행하는 명령
    # main() 함수가 끝날 때까지 기다림
    asyncio.run(main())


# ============================================================
# STEP 2: main() 함수 - 프로그램의 실제 시작 (줄 40-189)
# ============================================================
async def main():
    """
    async def: 비동기 함수 정의
    비동기 = 여러 작업을 동시에 처리할 수 있음
    """

    # -------------------- 초기화 --------------------

    # .env 파일에서 환경변수 읽기 (예: ANTHROPIC_API_KEY)
    load_dotenv()

    # 환영 메시지 출력
    print("=" * 80)
    print("Math Education Multi-Agent System v3.0")
    print("=" * 80)

    # -------------------- 인프라 초기화 (선택) --------------------

    logger = None
    perf_monitor = None
    error_tracker = None

    # infrastructure 모듈이 있으면 초기화
    if INFRASTRUCTURE_AVAILABLE:
        logger = StructuredLogger(log_dir="/tmp/math-agent-logs")
        # → 로그 파일: /tmp/math-agent-logs/agent-20251016.jsonl

        perf_monitor = PerformanceMonitor()
        # → 성능 측정 시작

        error_tracker = ErrorTracker(max_retries=3)
        # → 에러 발생 시 최대 3번 재시도

        logger.system_event("system_start", "Math agent system starting")
        # → 로그에 기록: [2025-10-16 10:30:00] SYSTEM START

    # -------------------- AI 옵션 설정 --------------------

    options = ClaudeAgentOptions(
        # 어떤 AI 모델을 사용할지
        model="claude-sonnet-4-5-20250929",

        # 파일 편집 권한 (acceptEdits = 자동 승인)
        permission_mode="acceptEdits",

        # 시스템 프롬프트: .claude/CLAUDE.md 파일을 읽어서 사용
        system_prompt={
            "type": "preset",
            "preset": "claude_code"
        },
        setting_sources=["project"],  # 프로젝트 설정 읽기

        # Meta-orchestrator가 사용할 수 있는 도구들
        allowed_tools=[
            'Task',      # subagent에게 작업 위임 (핵심!)
            'Read',      # 파일 읽기
            'Write',     # 파일 쓰기
            'Edit',      # 파일 수정
            'Grep',      # 파일 내용 검색
            'Glob',      # 파일 이름 검색
            'TodoWrite', # 작업 목록 관리
            'mcp__sequential-thinking__sequentialthinking',  # 순차 사고
            'mcp__memory-keeper__context_save',    # 메모리 저장
            'mcp__memory-keeper__context_get',     # 메모리 읽기
            'mcp__memory-keeper__context_search',  # 메모리 검색
        ],

        # 11개 subagent 등록
        agents={
            "knowledge-builder": knowledge_builder,  # subagents/file_builder_agent.py
            "quality-agent": quality_agent,          # subagents/validator_agent.py
            "research-agent": research_agent,        # subagents/web_research_agent.py
            # ... 나머지 8개
        },

        # MCP (Model Context Protocol) 서버들
        mcp_servers={
            "memory-keeper": {
                "command": "npx",
                "args": ["-y", "mcp-memory-keeper"]
                # → npx -y mcp-memory-keeper 실행
            },
            "sequential-thinking": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
                # → npx -y @modelcontextprotocol/server-sequential-thinking 실행
            },
        }
    )

    # -------------------- 대화 루프 시작 --------------------

    # ClaudeSDKClient를 초기화하고 대화 시작
    # async with: 작업이 끝나면 자동으로 정리 (리소스 해제)
    async with ClaudeSDKClient(options=options) as client:
        print("🎯 Meta-Orchestrator ready. Type your request below.")
        print()

        conversation_turns = 0  # 대화 횟수 카운터

        # -------------------- 무한 루프 --------------------

        while True:
            """
            while True: 조건이 항상 참이므로 무한 반복
            break를 만날 때까지 계속 실행
            """

            # ========== 사용자 입력 받기 ==========
            try:
                user_input = input("\033[1;34mYou:\033[0m ")
                # \033[1;34m = 파란색, \033[0m = 색상 리셋
                # input()은 사용자가 Enter를 누를 때까지 대기

            except (EOFError, KeyboardInterrupt):
                # Ctrl+D (EOFError) 또는 Ctrl+C (KeyboardInterrupt) 입력 시
                print("\n\nExiting...")
                break  # while 루프 탈출

            # ========== 종료 명령 확인 ==========
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                if logger:
                    logger.system_event("system_shutdown", "User exit")
                if perf_monitor:
                    perf_monitor.print_summary()  # 통계 출력
                break  # while 루프 탈출

            # ========== 빈 입력 무시 ==========
            if not user_input.strip():
                continue  # 다시 while 시작으로 (입력 대기)

            # ========== 대화 횟수 증가 ==========
            conversation_turns += 1

            # ========== AI에게 질문 전송 및 응답 받기 ==========
            try:
                print(f"\n\033[1;32m🎯 Meta-Orchestrator:\033[0m ", end="", flush=True)
                # end="": 줄바꿈 안 함, flush=True: 즉시 출력

                # AI에게 질문 전송 (비동기)
                await client.query(user_input)
                # await: 이 작업이 끝날 때까지 기다림

                # ========== 응답 스트림 처리 ==========
                from claude_agent_sdk import types

                # client.receive_response()는 비동기 제너레이터
                # 응답이 들어올 때마다 하나씩 처리
                async for message in client.receive_response():

                    if isinstance(message, types.AssistantMessage):
                        # AI의 메시지
                        for block in message.content:

                            if isinstance(block, types.TextBlock):
                                # 일반 텍스트
                                print(block.text, end="", flush=True)

                            elif isinstance(block, types.ThinkingBlock):
                                # AI의 사고 과정
                                print(f"\n\n🧠 [Thinking...]\n{block.thinking}", end="", flush=True)

                            elif isinstance(block, types.ToolUseBlock):
                                # 도구 사용 (예: Read, Write, Task)
                                print(f"\n\n🔧 [Tool: {block.name}]", end="", flush=True)

                    elif isinstance(message, types.ResultMessage):
                        # 최종 결과
                        print(f"\n\n✅ Complete (Duration: {message.duration_ms}ms, Turns: {message.num_turns})")

                        if perf_monitor:
                            # 성능 기록
                            perf_monitor.record_execution(
                                "meta-orchestrator",
                                message.duration_ms,
                                True  # success
                            )

                print()  # 응답 끝나면 줄바꿈

            except Exception as e:
                # 에러 발생 시 처리
                print(f"\n\n❌ Error: {e}")

                if error_tracker:
                    error_tracker.record_error(
                        "meta-orchestrator",
                        str(conversation_turns),
                        e,
                        {}
                    )

                if logger:
                    logger.error("meta-orchestrator", type(e).__name__, str(e))

        # while 루프 종료 (break를 만남)
        # async with 블록 종료 → client 자동 정리

    # main() 함수 종료
```

---

### 5.2 Subagent 정의 상세 분석

**file_builder_agent.py**의 AgentDefinition 구조:

```python
from claude_agent_sdk import AgentDefinition

# ============================================================
# AgentDefinition: 에이전트를 정의하는 설계도
# ============================================================
knowledge_builder = AgentDefinition(

    # -------------------- description --------------------
    # 짧은 설명 (meta-orchestrator가 어떤 agent를 선택할지 판단할 때 사용)
    description="Creates Obsidian markdown files for mathematical concepts...",

    # -------------------- prompt --------------------
    # 에이전트에게 주는 상세한 작업 지침서
    # 이 텍스트가 에이전트의 "system prompt"가 됨
    prompt="""
    # 👤 PERSONA

    ## Role
    당신은 **Knowledge File Builder**입니다.

    **당신이 하는 일**:
    - Obsidian 마크다운 파일 생성
    - LaTeX 수식 작성
    - 위키링크로 개념 연결

    **당신이 하지 않는 일**:
    - 연구 (research-agent가 함)
    - 검증 (quality-agent가 함)

    ## Goals
    1. 완전성: 모든 정보 포함
    2. 형식: Obsidian 호환
    3. 정확성: LaTeX 문법 오류 없음

    ## Guardrails (지켜야 할 규칙)
    - 절대 직접 연구하지 마세요
    - 선수 지식(prerequisites)을 빠뜨리지 마세요
    - 위키링크는 [[Concept Name]] 형식으로
    - 최대 12번의 도구 호출 후 종료

    ---

    # WORKFLOW (작업 흐름)

    ## Step 1: 연구 데이터 받기
    research-agent로부터 다음을 받습니다:
    - 정의
    - 선수 지식
    - 응용
    - 난이도

    ## Step 2: 분석 & 분해
    받은 데이터에서 추출:
    - prerequisites: [[개념1]], [[개념2]]
    - used-in: [[응용1]], [[응용2]]
    - domain: algebra, geometry, ...
    - level: middle-school, high-school, ...

    ## Step 3: Obsidian 파일 생성
    템플릿:
    ```markdown
    ---
    type: theorem | definition | ...
    prerequisites: ["[[개념1]]", "[[개념2]]"]
    ---

    # 제목

    ## Definition
    ...

    ## Examples
    ...
    ```

    ## Step 4: 파일 저장
    Write 도구 사용:
    - path: /home/kc-palantir/math/math-vault/Theorems/concept-name.md

    ## Step 5: 검증
    Read 도구로 파일 읽어서 확인
    """,

    # -------------------- model --------------------
    # 어떤 AI 모델을 사용할지
    # "sonnet" = claude-sonnet-3-5 (빠르고 저렴)
    # "opus" = claude-opus (느리지만 강력)
    model="sonnet",

    # -------------------- tools --------------------
    # 이 에이전트가 사용할 수 있는 도구들
    tools=[
        'Read',      # 파일 읽기
        'Write',     # 파일 쓰기
        'Edit',      # 파일 수정
        'Grep',      # 파일 내용 검색
        'Glob',      # 파일 이름 검색
        'TodoWrite', # 작업 목록
    ]
    # 주의: Task 도구는 없음 → 다른 agent에게 위임 불가
)
```

**초보자를 위한 설명**:

1. **description**:
   - "이 에이전트는 뭘 하는 애?"
   - meta-orchestrator가 이걸 보고 어떤 agent를 부를지 결정

2. **prompt**:
   - "에이전트에게 주는 매뉴얼"
   - 역할, 목표, 지켜야 할 규칙, 작업 흐름을 상세히 설명

3. **model**:
   - "sonnet" vs "opus"
   - sonnet = 빠르고 저렴, 대부분의 작업에 충분
   - opus = 느리고 비싸지만 복잡한 작업에 강함

4. **tools**:
   - 에이전트가 "할 수 있는 것"의 목록
   - Task 도구가 없으면 다른 agent를 부를 수 없음

---

### 5.3 Infrastructure 상세 분석

#### StructuredLogger

```python
class StructuredLogger:
    """
    JSON 형식으로 로그를 기록하는 클래스
    """

    def __init__(self, log_dir="/tmp/math-agent-logs", trace_id=None):
        """
        초기화

        Args:
            log_dir: 로그 파일을 저장할 디렉토리
            trace_id: 작업 추적 ID (없으면 자동 생성)
        """
        import uuid

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)  # 디렉토리 생성

        # trace_id: 여러 작업을 추적할 수 있는 고유 번호
        self.trace_id = trace_id or str(uuid.uuid4())[:8]  # 예: "a3f2c1d4"

        # 로그 파일 경로: /tmp/math-agent-logs/agent-20251016.jsonl
        self.log_file = self.log_dir / f"agent-{datetime.now().strftime('%Y%m%d')}.jsonl"

        # trace_id를 context variable에 저장
        # → 모든 비동기 작업에서 같은 trace_id 사용 가능
        trace_id_var.set(self.trace_id)

    def _write_log(self, entry: LogEntry):
        """
        로그 엔트리를 JSONL 파일에 기록

        JSONL = JSON Lines
        각 줄이 하나의 JSON 객체

        예:
        {"timestamp": "2025-10-16T10:30:15", "event": "agent_start", ...}
        {"timestamp": "2025-10-16T10:30:17", "event": "tool_call", ...}
        """
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(entry.to_json() + '\n')  # JSON 문자열 + 줄바꿈

    def agent_start(self, agent_name, task_description, metadata=None):
        """
        에이전트 시작 기록

        Args:
            agent_name: 에이전트 이름 (예: "knowledge-builder")
            task_description: 작업 설명 (예: "피타고라스 정리 파일 생성")
            metadata: 추가 정보 (dict)
        """
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),  # ISO 형식: "2025-10-16T10:30:15"
            trace_id=self.trace_id,                # 작업 추적 ID
            event_type="agent_start",              # 이벤트 종류
            agent_name=agent_name,
            level="INFO",                          # 로그 레벨
            message=f"Starting agent: {agent_name}",
            metadata={"task": task_description, **(metadata or {})}
        )
        self._write_log(entry)
        print(f"[{entry.timestamp}] START {agent_name}: {task_description}")

    def agent_complete(self, agent_name, duration_ms, success, metadata=None):
        """
        에이전트 완료 기록

        Args:
            agent_name: 에이전트 이름
            duration_ms: 소요 시간 (밀리초)
            success: 성공 여부 (True/False)
            metadata: 추가 정보
        """
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="agent_complete",
            agent_name=agent_name,
            level="INFO" if success else "ERROR",
            message=f"Agent {'completed' if success else 'failed'}: {agent_name}",
            duration_ms=duration_ms,
            metadata={"success": success, **(metadata or {})}
        )
        self._write_log(entry)
        status_icon = "✅" if success else "❌"
        print(f"[{entry.timestamp}] {status_icon} {agent_name}: {duration_ms:.0f}ms")
```

**초보자를 위한 설명**:

1. **왜 로그를 기록하나요?**
   - 프로그램이 무슨 일을 했는지 추적
   - 문제가 생기면 원인 파악
   - 성능 분석 (어떤 작업이 느린지)

2. **JSONL 형식이란?**
   - JSON Lines = 각 줄이 하나의 JSON
   - 쉽게 검색하고 분석할 수 있음
   - 예:
     ```jsonl
     {"event": "start", "agent": "research"}
     {"event": "complete", "agent": "research", "duration": 2500}
     ```

3. **trace_id는 왜 필요한가요?**
   - 하나의 작업이 여러 agent를 거침
   - trace_id로 같은 작업인지 추적
   - 예:
     ```
     [trace_id: abc123] research-agent 시작
     [trace_id: abc123] research-agent 완료
     [trace_id: abc123] knowledge-builder 시작
     [trace_id: abc123] knowledge-builder 완료
     ```

---

#### PerformanceMonitor

```python
class PerformanceMonitor:
    """
    각 에이전트의 성능을 측정하는 클래스
    """

    def __init__(self):
        """
        초기화: 빈 딕셔너리 생성

        self.metrics 구조:
        {
            "knowledge-builder": AgentMetrics(...),
            "research-agent": AgentMetrics(...),
            ...
        }
        """
        self.metrics = {}

    def record_execution(self, agent_name, duration_ms, success):
        """
        에이전트 실행 기록

        Args:
            agent_name: 에이전트 이름
            duration_ms: 소요 시간 (밀리초)
            success: 성공 여부
        """
        # 처음 보는 agent면 새로 생성
        if agent_name not in self.metrics:
            self.metrics[agent_name] = AgentMetrics()

        # 통계 업데이트
        self.metrics[agent_name].total_calls += 1            # 총 호출 횟수
        self.metrics[agent_name].total_duration_ms += duration_ms  # 총 소요 시간
        if success:
            self.metrics[agent_name].success_count += 1      # 성공 횟수

    def print_summary(self):
        """
        통계 출력

        예:
        ================================
        Performance Summary
        ================================
        knowledge-builder:
          - Total calls: 10
          - Success rate: 90.0%
          - Avg duration: 2500ms
        research-agent:
          - Total calls: 8
          - Success rate: 100.0%
          - Avg duration: 3200ms
        """
        print("\n" + "=" * 50)
        print("Performance Summary")
        print("=" * 50)

        for agent_name, metrics in self.metrics.items():
            avg_duration = metrics.total_duration_ms / metrics.total_calls
            success_rate = metrics.success_count / metrics.total_calls * 100

            print(f"\n{agent_name}:")
            print(f"  - Total calls: {metrics.total_calls}")
            print(f"  - Success rate: {success_rate:.1f}%")
            print(f"  - Avg duration: {avg_duration:.0f}ms")
```

**초보자를 위한 설명**:

1. **왜 성능을 측정하나요?**
   - 어떤 agent가 느린지 파악
   - 최적화가 필요한 부분 찾기
   - 시간이 지나면서 개선되는지 확인

2. **AgentMetrics란?**
   ```python
   @dataclass
   class AgentMetrics:
       total_calls: int = 0         # 총 몇 번 호출됐나
       success_count: int = 0       # 그 중 몇 번 성공했나
       total_duration_ms: float = 0 # 총 얼마나 걸렸나
   ```

3. **평균 시간 계산**:
   ```
   평균 = 총 시간 / 총 호출 횟수
   예: 5000ms / 2회 = 2500ms (평균 2.5초)
   ```

---

## 6. 핵심 개념 설명

### 6.1 비동기 (Async/Await)

**전통적인 방식 (동기)**:
```python
# 동기: 한 번에 하나씩 처리
result1 = search_web("피타고라스")    # 3초 대기
result2 = search_web("유클리드")      # 3초 대기
# 총 6초 걸림
```

**비동기 방식**:
```python
# 비동기: 동시에 여러 개 처리
result1_task = search_web_async("피타고라스")  # 시작만 하고 넘어감
result2_task = search_web_async("유클리드")    # 동시에 시작
result1 = await result1_task  # 결과 기다림
result2 = await result2_task  # 결과 기다림
# 총 3초 걸림 (동시에 실행되므로)
```

**비유**:
- 동기: 빨래 → 설거지 → 청소 (순서대로 하나씩)
- 비동기: 빨래+설거지+청소 (동시에 시작, 필요할 때 결과 확인)

---

### 6.2 AgentDefinition

**구조**:
```python
AgentDefinition(
    description="짧은 설명",  # meta-orchestrator가 선택할 때 참고
    prompt="상세한 지침서",   # agent에게 주는 매뉴얼
    model="sonnet",         # 어떤 AI 모델?
    tools=["Read", "Write"] # 사용 가능한 도구들
)
```

**비유**: 직원 프로필 카드
- description: "영업팀 김철수"
- prompt: "담당 업무, 업무 방식, 주의사항"
- model: "시니어급 (10년 경력)"
- tools: "사용 가능한 도구: 컴퓨터, 전화, 차량"

---

### 6.3 Task 도구와 Delegation

**Meta-orchestrator의 역할**:
```
사용자 요청 → Meta-orchestrator 분석
  ↓
"이 작업은 research-agent가 잘하겠군"
  ↓
Task 도구 사용: research-agent에게 위임
  ↓
research-agent 실행 후 결과 받음
  ↓
"이제 knowledge-builder에게 파일 생성 요청"
  ↓
Task 도구 사용: knowledge-builder에게 위임
```

**코드**:
```python
# main.py의 allowed_tools에 Task 포함
allowed_tools = ['Task', 'Read', 'Write', ...]

# meta-orchestrator가 Task 도구 사용
Task(
    subagent_type="research-agent",
    prompt="피타고라스 정리를 조사해주세요",
    description="피타고라스 정리 조사"
)
```

---

### 6.4 MCP (Model Context Protocol)

**MCP란?**:
- Model Context Protocol
- AI가 외부 서비스와 통신하는 표준 방식
- 예: memory-keeper, sequential-thinking

**설정**:
```python
mcp_servers={
    "memory-keeper": {
        "command": "npx",
        "args": ["-y", "mcp-memory-keeper"]
    }
}
```

**실행되는 명령**:
```bash
npx -y mcp-memory-keeper
```

**비유**:
- MCP server = 외부 전문 업체
- memory-keeper = 문서 보관소
- sequential-thinking = 논리 컨설팅 회사

---

## 7. 실전 예제: 전체 흐름 추적

### 시나리오: "삼각함수 파일 만들어줘"

```
[사용자 입력]
You: 삼각함수 파일 만들어줘

    ↓ input() 함수가 문자열 받음

[main.py: 줄 138]
user_input = "삼각함수 파일 만들어줘"

    ↓ await client.query(user_input)

[ClaudeSDKClient]
.claude/CLAUDE.md를 system prompt로 로드
사용자 질문 분석...

Meta-orchestrator 판단:
"파일 생성 요청이네. 먼저 research-agent로 조사하고,
그 다음 knowledge-builder로 파일 생성하자"

    ↓ Task 도구 사용

[research-agent 호출]
{
  "subagent_type": "research-agent",
  "prompt": "삼각함수(sine, cosine, tangent)에 대해 조사해주세요",
  "description": "삼각함수 조사"
}

    ↓ research-agent 실행

[research-agent 내부]
1. WebSearch 도구로 "삼각함수 정의" 검색
   → 결과: sin, cos, tan의 정의, 단위원 설명
2. WebSearch 도구로 "삼각함수 공식" 검색
   → 결과: 덧셈정리, 배각공식, 반각공식
3. WebSearch 도구로 "삼각함수 응용" 검색
   → 결과: 파동, 진동, 회전 운동

결과 정리:
"""
# 삼각함수 연구 결과

## 정의
- sin θ = 대변/빗변
- cos θ = 인접변/빗변
- tan θ = 대변/인접변

## 선수 지식
- 직각삼각형
- 비율과 비례
- 각도

## 주요 공식
- sin² θ + cos² θ = 1
- tan θ = sin θ / cos θ

## 응용
- 파동 현상 (물리)
- 회전 운동 (기하)
- 신호 처리 (공학)
"""

    ↓ 연구 결과 반환

[Meta-orchestrator]
연구 결과 받음. 이제 파일 생성 단계.

    ↓ Task 도구 사용

[knowledge-builder 호출]
{
  "subagent_type": "knowledge-builder",
  "prompt": "다음 연구 결과로 Obsidian 파일을 생성해주세요:\n\n[연구 결과 전달]",
  "description": "삼각함수 파일 생성"
}

    ↓ knowledge-builder 실행

[knowledge-builder 내부]
1. 연구 결과 분석
   - type: definition
   - prerequisites: [[직각삼각형]], [[비율]], [[각도]]
   - used-in: [[파동]], [[회전운동]], [[푸리에변환]]

2. Write 도구로 파일 생성
   파일 경로: /math-vault/Definitions/trigonometric-functions.md

   내용:
   ```markdown
   ---
   type: definition
   id: trigonometric-functions
   domain: geometry
   level: high-school
   difficulty: 5
   prerequisites:
     - "[[직각삼각형]]"
     - "[[비율]]"
     - "[[각도]]"
   used-in:
     - "[[파동]]"
     - "[[회전운동]]"
     - "[[푸리에변환]]"
   ---

   # 삼각함수 (Trigonometric Functions)

   ## Definition
   직각삼각형의 변의 비율로 정의되는 함수들.

   $$\sin \theta = \frac{\text{opposite}}{\text{hypotenuse}}$$
   $$\cos \theta = \frac{\text{adjacent}}{\text{hypotenuse}}$$
   $$\tan \theta = \frac{\text{opposite}}{\text{adjacent}}$$

   ...
   ```

3. Read 도구로 파일 검증
   ✅ YAML 문법 올바름
   ✅ LaTeX 수식 올바름
   ✅ 위키링크 형식 올바름

결과 반환: "파일 생성 완료"

    ↓

[Meta-orchestrator]
knowledge-builder 완료. 선택적으로 quality-agent 호출 가능.

    ↓ (선택) Task 도구 사용

[quality-agent 호출]
{
  "subagent_type": "quality-agent",
  "prompt": "/math-vault/Definitions/trigonometric-functions.md 파일을 검증해주세요",
  "description": "파일 품질 검증"
}

    ↓ quality-agent 실행

[quality-agent 내부]
1. Read 도구로 파일 읽기
2. YAML frontmatter 검증
   ✅ 필수 필드 존재 (type, id, domain, level, difficulty)
   ✅ prerequisites 형식 올바름
3. LaTeX 검증
   ✅ $...$ 쌍 맞음
   ✅ $$...$$ 쌍 맞음
4. 위키링크 검증
   ✅ [[...]] 형식 올바름
5. 필수 섹션 검증
   ✅ Definition 섹션 존재
   ✅ Examples 섹션 존재

결과 반환: "검증 완료, 문제 없음"

    ↓

[Meta-orchestrator]
모든 작업 완료. 사용자에게 보고.

    ↓ AssistantMessage 생성

[main.py: 줄 166-180]
async for message in client.receive_response():
    if isinstance(message, types.AssistantMessage):
        for block in message.content:
            if isinstance(block, types.TextBlock):
                print(block.text, end="", flush=True)

    ↓ 화면 출력

[터미널 출력]
🎯 Meta-Orchestrator:

✅ 삼각함수 파일을 생성했습니다!

**파일 정보**:
- 경로: `/math-vault/Definitions/trigonometric-functions.md`
- 타입: definition
- 난이도: 5/10 (고등학교 수준)

**포함된 내용**:
- 정의 (sin, cos, tan)
- 주요 공식 (피타고라스 정리 등)
- 예시 3개
- 선수 지식: [[직각삼각형]], [[비율]], [[각도]]
- 응용: [[파동]], [[회전운동]], [[푸리에변환]]

품질 검증 완료 ✅

✅ Complete (Duration: 4500ms, Turns: 8)

[main.py: 줄 181]
print()  # 줄바꿈

    ↓ 다시 입력 대기

[main.py: 줄 138]
user_input = input("\033[1;34mYou:\033[0m ")
```

---

## 8. 요약

### 프로그램 구조 한눈에

```
python main.py
    ↓
main() 함수 실행
    ↓
ClaudeSDKClient 초기화 (11개 subagent 등록)
    ↓
while True 대화 루프
    ├─ input() → 사용자 질문 받기
    ├─ client.query() → AI에게 질문
    ├─ receive_response() → AI 답변 받기
    │   ├─ Meta-orchestrator 판단
    │   ├─ Task 도구로 subagent 위임
    │   ├─ Subagent 실행 (tools 사용)
    │   └─ 결과 수집 및 종합
    ├─ print() → 사용자에게 결과 출력
    └─ 다시 input()으로
```

### 주요 컴포넌트

| 컴포넌트 | 역할 | 파일 |
|---------|------|------|
| main.py | 진입점, 대화 루프 | main.py |
| ClaudeSDKClient | AI 클라이언트 | (외부 패키지) |
| Meta-orchestrator | 작업 조율자 | .claude/CLAUDE.md |
| 12 Subagents | 전문 AI들 | subagents/*.py |
| Infrastructure | 로깅, 모니터링, 에러 처리 | infrastructure/*.py |
| Tools | 유틸리티 (Mathpix OCR 포함) | tools/*.py |
| Workflows | 피드백 루프 워크플로우 | workflows/*.py |
| Observability | 실시간 모니터링 대시보드 | observability-server/, observability-dashboard/ |
| Config | 경로 설정 | config.py |

### 핵심 메커니즘

1. **Delegation (위임)**:
   - Meta-orchestrator가 Task 도구로 subagent에게 작업 위임
   - 각 subagent는 자기 분야의 전문가

2. **Tool Restriction (도구 제한)**:
   - 각 subagent는 필요한 도구만 사용 가능
   - 예: quality-agent는 Read만 가능 (편집 불가)

3. **Async/Await (비동기)**:
   - 여러 작업을 동시에 처리
   - 예: 웹 검색 중에도 다른 작업 가능

4. **Observability (관찰 가능성)**:
   - StructuredLogger: 모든 작업 기록
   - PerformanceMonitor: 성능 측정
   - ErrorTracker: 에러 추적 및 재시도

---

## 9. 초보자를 위한 팁

### 코드 읽는 법

1. **주석(Comments) 찾기**:
   ```python
   # 이것은 주석입니다 (코드가 아님, 설명)
   ```

2. **함수 정의 찾기**:
   ```python
   def function_name():  # def = define (정의)
       # 함수 본문
   ```

3. **클래스 정의 찾기**:
   ```python
   class ClassName:  # class = 객체를 만드는 설계도
       def __init__(self):  # 생성자 (초기화)
           pass
   ```

4. **조건문 이해하기**:
   ```python
   if condition:      # 만약 condition이 참이면
       do_something()
   elif other:        # 그게 아니고 other가 참이면
       do_other()
   else:              # 그 외 모든 경우
       do_default()
   ```

5. **반복문 이해하기**:
   ```python
   for item in items:  # items의 각 item에 대해
       process(item)

   while condition:    # condition이 참인 동안 계속
       do_something()
   ```

### 디버깅 팁

1. **print() 사용**:
   ```python
   print(f"변수 값: {variable}")  # f-string (formatted string)
   ```

2. **로그 파일 확인**:
   ```bash
   tail -f /tmp/math-agent-logs/agent-20251016.jsonl
   ```

3. **에러 메시지 읽기**:
   ```
   Traceback (most recent call last):
     File "main.py", line 138, in main
       user_input = input("You: ")
   KeyboardInterrupt
   ```
   - 맨 아래가 실제 에러
   - 위로 올라가면서 호출 경로 추적

---

## 10. 다음 단계

이 문서를 이해했다면:

1. **코드 수정 연습**:
   - main.py의 환영 메시지 바꿔보기
   - subagent의 prompt 수정해보기

2. **새 subagent 추가**:
   - subagents/example_agent.py 만들기
   - subagents/__init__.py에 import 추가
   - main.py의 agents에 등록

3. **도구 추가**:
   - tools/example_tool.py 만들기
   - subagent의 tools 목록에 추가

4. **테스트 작성**:
   - tests/test_example.py 만들기
   - pytest로 실행

---

## 부록: 용어 사전

| 용어 | 설명 | 예시 |
|-----|------|------|
| 비동기 (Async) | 여러 작업을 동시에 처리 | await client.query() |
| 에이전트 (Agent) | 특정 작업을 하는 AI | knowledge-builder |
| 도구 (Tool) | 에이전트가 사용하는 기능 | Read, Write, Task |
| 위임 (Delegation) | 다른 agent에게 작업 넘기기 | Task 도구 사용 |
| 로그 (Log) | 작업 기록 | JSONL 파일 |
| 메트릭 (Metric) | 측정값 (시간, 횟수 등) | duration_ms |
| 프롬프트 (Prompt) | AI에게 주는 지시 | system prompt |
| MCP | AI-외부 서비스 통신 프로토콜 | memory-keeper |
| JSONL | JSON Lines (한 줄 = 하나의 JSON) | 로그 파일 형식 |
| Context Variable | 비동기 작업 간 공유되는 변수 | trace_id |

---

## 11. Feedback Loop System (NEW)

### 피드백 기반 학습 시스템

```
사용자가 수학 문제 이미지 제공 (sample.png)
    ↓
Mathpix OCR로 수식 추출 (99.9% 정확도)
    ↓
841개 중학교 수학 개념과 매칭
    ↓
문제 유형별 맞춤 Scaffolding 생성
    - 좌표평면 문제: 10단계 (점 찾기 → 교점 → 넓이)
    - 소인수분해: 9단계 (짝수 판별 → 나누기 → 지수 표기)
    ↓
사용자가 각 단계 평가 (1-5점 + 개선 제안)
    ↓
Feedback-Learning-Agent가 패턴 추출
    - "가장 작은 소수" 강조 패턴
    - "why 질문" 추가 패턴
    ↓
Neo4j에 LearnedPattern으로 저장
    ↓
다음 문제 생성 시 자동 적용
```

### 새로 추가된 파일 (12개)

| 파일 | 역할 |
|-----|------|
| `tools/mathpix_ocr_tool.py` | Mathpix API OCR 통합 |
| `tools/feedback_collector.py` | 대화형 피드백 수집 CLI |
| `tools/observability_hook.py` | Observability 이벤트 전송 |
| `workflows/hook_events.py` | 이벤트 타입 정의 |
| `workflows/concept_matcher.py` | 문제-개념 매칭 (841개) |
| `workflows/feedback_loop_workflow.py` | 전체 워크플로우 |
| `subagents/feedback_learning_agent.py` | 패턴 학습 Agent (12번째) |
| `neo4j/feedback_schema.cypher` | Neo4j 스키마 확장 |
| `scripts/run_feedback_loop.py` | CLI 실행 스크립트 |
| `tests/test_feedback_loop_e2e.py` | E2E 테스트 (10개) |
| `tests/test_actual_problem_scaffolding.py` | 실제 문제 테스트 |
| `tests/test_full_integration.py` | 통합 테스트 |

### Observability 통합

모든 워크플로우 단계가 실시간으로 추적됩니다:
- `ocr_started` → `ocr_completed` (99.9% confidence)
- `concept_match_started` → `concept_match_completed` (841개 중 top-5)
- `scaffolding_started` → `scaffolding_completed` (10 steps)
- `feedback_started` → `feedback_completed` (step-by-step)
- `learning_started` → `pattern_extracted` → `learning_completed`
- `neo4j_write_started` → `neo4j_write_completed`

Dashboard (http://localhost:3000)에서 실시간 확인 가능.

---

## 12. Enhanced Observability System (indydevdan Integration)

### Claude Code Hook System

**목적**: Claude의 모든 행동을 자동으로 추적

```
Claude가 툴 사용 → Hook 발동 → 자동 로깅 → 서버 전송 → 대시보드 표시
```

### Hook 종류 (9가지)

| Hook | 시점 | 기능 |
|------|------|------|
| `SessionStart` | Claude 시작 | 세션 초기화 |
| `UserPromptSubmit` | 사용자 입력 | 질문 추적 |
| `PreToolUse` | 툴 사용 전 | 보안 검증 (rm -rf 차단) |
| `PostToolUse` | 툴 사용 후 | 결과 로깅 |
| `SubagentStop` | Subagent 완료 | Agent 추적 |
| `PreCompact` | 컨텍스트 압축 | 메모리 관리 |
| `Notification` | 사용자 알림 | 상호작용 |
| `Stop` | 응답 완료 | 세션 완료, TTS 알림 |
| `SessionEnd` | Claude 종료 | 정리 작업 |

### 보안 기능

**자동 차단**:
- `rm -rf` (모든 변형)
- `rm --recursive --force`
- 루트 디렉토리 삭제
- `.env` 파일 접근

**작동 방식**:
```python
# pre_tool_use_security.py
if is_dangerous_rm_command(command):
    print("BLOCKED: Dangerous rm command")
    sys.exit(2)  # Exit 2 → Claude가 툴 실행 중단
```

### AI 요약 생성

**예시**:
```
이벤트: PreToolUse - Read tool
페이로드: {"file_path": "sample.png"}
  ↓ AI (Haiku)
요약: "Reads sample.png from project root"
```

### 통합 아키텍처

```
┌─────────────────────────────────────────────┐
│ Level 1: Claude Code Hooks                  │
│ - 모든 툴 사용 자동 추적                     │
│ - 보안 검증                                  │
│ - AI 요약                                    │
└─────────────────┬───────────────────────────┘
                  │
                  ↓ POST /events
┌─────────────────────────────────────────────┐
│ Level 2: Workflow Events                    │
│ - OCR, Scaffolding, Pattern Learning        │
│ - Custom event types                        │
└─────────────────┬───────────────────────────┘
                  │
                  ↓ Both → Same Server
┌─────────────────────────────────────────────┐
│ Enhanced Observability Server               │
│ - FastAPI + WebSocket                       │
│ - SQLite (chat + summary)                   │
│ - Real-time broadcast                       │
└─────────────────┬───────────────────────────┘
                  │
                  ↓ WebSocket
┌─────────────────────────────────────────────┐
│ Vue Dashboard (localhost:3000)              │
│ - 통합 타임라인                              │
│ - AI 요약 표시                               │
│ - 실시간 업데이트                            │
└─────────────────────────────────────────────┘
```

### 데이터 흐름 예시

**시나리오**: Claude가 파일을 읽을 때

```
1. PreToolUse Hook 발동
   → pre_tool_use_security.py: 보안 검증 ✅
   → send_event_observability.py: 서버 전송
   → AI: "Reads sample.png from project root"

2. Tool 실행 (Read)
   → Claude가 파일 읽기

3. PostToolUse Hook 발동
   → post_tool_use_logging.py: 결과 로깅
   → send_event_observability.py: 서버 전송
   → AI: "Successfully read 173 bytes"

4. Dashboard 실시간 표시
   → 🔧 PreToolUse: "Reads sample.png..."
   → ✅ PostToolUse: "Successfully read..."
```

### 추가된 파일 (18개)

**Hook Scripts** (10):
- `send_event_observability.py` - 통합 이벤트 전송기
- `pre_tool_use_security.py` - 보안 검증
- `post_tool_use_logging.py` - 결과 로깅
- `stop_enhanced.py` - 완료 + TTS
- `user_prompt_submit.py` - 사용자 입력
- `subagent_stop.py` - Subagent 추적
- `session_start.py`, `session_end.py`
- `pre_compact.py`, `notification.py`

**Utilities** (5):
- `utils/constants.py`
- `utils/summarizer.py`
- `utils/llm/anth.py`
- `utils/__init__.py`, `utils/llm/__init__.py`

**Tests** (3):
- `tests/test_claude_hooks_integration.py`
- `tests/test_websocket_streaming.py`
- Updated `tests/run_all_tests.py`

---

**문서 작성일**: 2025-10-16
**버전**: 3.2.0 - indydevdan Observability Integration
**업데이트**: Claude Code hooks 통합 (19 hook scripts, WebSocket, AI summaries, Security)
**테스트**: 100% 통과 (5 suites, 20+ tests)
**대상**: 프로그래밍 초보자
