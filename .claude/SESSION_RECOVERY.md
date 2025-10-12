# Session Recovery Guide
## Memory-Keeper Edition (v4.0)

---

## 🚀 새 세션 시작 시 (즉시 실행)

### 1단계: Memory-Keeper 세션 시작
```
[Claude에게 요청]
"Start memory-keeper session for math-system project"

→ mcp_context_session_start(
    name: "math-system-2025-10-12",
    description: "Multi-agent math education system",
    projectDir: "/home/kc-palantir/math",
    defaultChannel: "main-workflow"
)
```

### 2단계: 이전 컨텍스트 로드
```
[Claude에게 요청]
"Load latest context from memory-keeper"

→ mcp_context_get(
    category: "session-state",
    sortBy: "timestamp",
    sortOrder: "desc",
    limit: 1
)

Claude will show:
- Current phase
- Completed tasks
- Next tasks
- Agent status
```

### 3단계: 작업 재개
```
"Continue with next task"
```

---

## 💾 작업 중 컨텍스트 저장

### Claude에게 요청
```
"Save current state to memory-keeper: [milestone-name]"

Example:
"Save current state to memory-keeper: phase3-agents-complete"
```

Claude will:
1. Execute `mcp_context_save()` with structured data
2. Set category: "milestone" (or "session-state", "progress", etc.)
3. Set priority: "high" (or "medium", "low")
4. Add tags and metadata
5. Optionally save to local file for backup

### 수동으로 저장 (Advanced)
```python
mcp_context_save(
    key: "phase3-milestone",
    value: {
        "phase": "Phase 3: Specialized Agents",
        "completed": ["agent1", "agent2"],
        "next": ["agent3"],
        "agent_count": 6
    },
    category: "milestone",
    priority: "high",
    channel: "main-workflow",
    tags: ["phase3", "agents"],
    metadata: {"timestamp": "2025-10-12T23:00:00"}
)
```

---

## 🔍 컨텍스트 조회

### 카테고리별 조회
```
"Get all architecture decisions from memory-keeper"
"Get all milestone contexts from memory-keeper"
"Get all session-state contexts from memory-keeper"
```

### 우선순위별 조회
```
"Get high-priority items from memory-keeper"
"Get all medium-priority decisions"
```

### 시간별 조회
```
"Get contexts from last 7 days"
"Get today's progress updates"
```

### 채널별 조회
```
"Get contexts from agent-development channel"
"Get contexts from testing channel"
```

---

## 🔄 세션 간 연속성 보장

### 세션 종료 전 (중요!)
```
[Claude에게 요청]
"Save session-end state to memory-keeper"
```

### 새 세션 시작 시
```
[Claude에게 요청]
1. "Start memory-keeper session"
2. "Load latest context"

→ Automatic recovery from SQLite database
→ All previous context available
→ Continue seamlessly
```

---

## 📋 Memory-Keeper 카테고리 가이드

### session-state
- **용도**: 현재 단계, 작업 진행 상황
- **예시**: "Phase 3 진행 중, 6 agents 구현 완료"
- **Priority**: high

### decisions
- **용도**: 아키텍처 선택, 디자인 결정
- **예시**: "Kenny Liao SDK 패턴 채택 결정"
- **Priority**: high

### tasks
- **용도**: TODO 항목, 다음 단계
- **예시**: "dependency-mapper 테스트 필요"
- **Priority**: medium

### progress
- **용도**: 완료된 작업, 메트릭
- **예시**: "Meta-orchestrator 220 lines 구현 완료"
- **Priority**: medium

### architecture
- **용도**: 시스템 설계, 에이전트 정의
- **예시**: "6 agents: 3 layers 아키텍처"
- **Priority**: high

### milestone
- **용도**: 주요 성과, 단계 완료
- **예시**: "Phase 1 Infrastructure 완료"
- **Priority**: high

### debug
- **용도**: 이슈, 에러, 해결책
- **예시**: "토큰 150K 초과 시 context editing 발생"
- **Priority**: medium/low

---

## 🎯 실전 워크플로우

### 시나리오: Phase 3 작업 중 세션 리셋

#### 이전 세션 (종료 전)
```
user: "Save current state to memory-keeper: phase3-6agents-implemented"

Claude:
→ Saved to memory-keeper with:
  - category: "milestone"
  - priority: "high"
  - channel: "main-workflow"
  - tags: ["phase3", "agents", "architecture"]

→ Also saved local backup:
  .claude/memories/phase-progress/checkpoint-phase3-6agents.json

✅ Context saved to SQLite database
```

#### 새 세션 (시작 시)
```
user: "Start memory-keeper session and load latest context"

Claude:
→ Session started: math-system-2025-10-13
→ Retrieved from memory-keeper:

  ✅ Phase 3: Specialized Agents (6 agents implemented)
  ✅ Completed: meta-orchestrator, dependency-mapper, socratic-planner,
               knowledge-builder, quality-agent, research-agent
  🎯 Next: Test dependency-mapper with 57 topology concepts

Ready to continue!
```

---

## 🛠️ 편의 스크립트

### 상태 확인 스크립트
```bash
cat > .claude/status.sh << 'EOF'
#!/bin/bash
# 현재 상태 빠른 확인

echo "📊 Memory-Keeper Status"
echo "======================="
echo "Ask Claude: 'Load latest context from memory-keeper'"
echo ""

echo "📁 Local Backup Files"
echo "===================="
ls -lt .claude/memories/phase-progress/ | head -5
EOF

chmod +x .claude/status.sh
```

---

## 💡 Tips

### 1. 체계적인 카테고리 사용
```python
# ✅ 좋은 예
category: "session-state"  # 명확한 용도
category: "milestone"      # 주요 성과
category: "debug"          # 문제 해결

# ❌ 나쁜 예
category: "stuff"          # 모호함
category: "misc"           # 검색 어려움
```

### 2. 우선순위 활용
```python
# Critical state
priority: "high"

# Important context
priority: "medium"

# Nice-to-have info
priority: "low"
```

### 3. 풍부한 메타데이터
```python
metadata: {
    "agent": "meta-orchestrator",
    "test_status": "passed",
    "file_count": 6,
    "lines_of_code": 1400
}
```

### 4. 태그로 연결
```python
tags: ["phase3", "agents", "architecture", "tested"]
# → 나중에 쉽게 검색 가능
```

### 5. 채널 구분
```python
channel: "main-workflow"      # 주요 개발
channel: "agent-development"  # 에이전트 구현
channel: "testing"            # 테스트
channel: "documentation"      # 문서화
```

---

## 🆘 문제 해결

### Memory-Keeper 연결 실패
```bash
# MCP 서버 상태 확인
claude mcp list | grep memory-keeper

# ✗ Failed 표시 시:
claude mcp remove memory-keeper
claude mcp add --scope user memory-keeper npx mcp-memory-keeper

# 재확인
claude mcp list
```

### 컨텍스트가 없을 때
```
# 정상 (첫 세션)
user: "Start fresh session and initialize"

Claude:
→ No previous context found
→ Starting fresh
→ Will save progress as we work
```

### SQLite 데이터베이스 위치 확인
```bash
# Memory-keeper database location
ls -la ~/.config/mcp-memory-keeper/context.db

# If not found, will be auto-created on first use
```

### 로컬 백업 활용
```bash
# Memory-keeper 사용 불가 시 로컬 파일 사용
cat .claude/memories/phase-progress/current-state.json

# 또는 PROJECT_CONTEXT.md 참조
cat PROJECT_CONTEXT.md
```

---

## 📖 요약

### 핵심 3단계
```
1. 세션 시작 시
   "Start memory-keeper session and load latest context"

2. 작업 중 (주기적으로)
   "Save to memory-keeper: [milestone-name]"

3. 세션 종료 전
   "Save session-end state to memory-keeper"
```

### Memory-Keeper vs Local Files

| Feature | Memory-Keeper | Local Files |
|---------|---------------|-------------|
| Scope | User (all projects) | Project-specific |
| Storage | SQLite database | JSON files |
| Querying | Advanced filtering | Manual grep |
| Persistence | Permanent | Git-tracked |
| Categories | ✅ Yes | ❌ No |
| Priorities | ✅ Yes | ❌ No |
| Channels | ✅ Yes | ❌ No |
| Tags | ✅ Yes | ❌ No |

**Best Practice**: Use Memory-Keeper as primary, Local Files as backup

---

## 📊 Memory-Keeper 장점

1. **User-Scope**: 모든 프로젝트에서 접근 가능
2. **Advanced Querying**: 카테고리, 우선순위, 시간, 채널별 조회
3. **Structured Data**: 체계적인 컨텍스트 관리
4. **Persistent**: SQLite 데이터베이스, 영구 보존
5. **Git Integration**: Git 브랜치 기반 채널 추적
6. **Metadata & Tags**: 풍부한 메타데이터, 태그 지원

---

**다음 세션에서 이 가이드를 먼저 읽으면 됩니다!**

**Memory System**: MCP Memory-Keeper (SQLite)
**Database**: `~/.config/mcp-memory-keeper/context.db`
**Scope**: User-level (all projects)
