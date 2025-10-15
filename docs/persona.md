<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Claude Code 2.0 서브에이전트와 페르소나 시스템 상세 가이드

Claude Code 2.0의 서브에이전트 기능은 전문화된 AI 페르소나를 생성하여 복잡한 개발 작업을 효율적으로 처리할 수 있는 강력한 시스템입니다. 아래에서 구체적인 구현 방법과 활용 사례를 자세히 설명하겠습니다.

## 서브에이전트 파일 구조와 YAML 설정

### 기본 파일 형식

서브에이전트는 YAML 프론트매터가 포함된 마크다운 파일로 정의됩니다:[^1]

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # 선택사항 - 생략시 모든 도구 상속
model: sonnet  # 선택사항 - 모델 별칭 또는 'inherit' 지정
---

서브에이전트의 시스템 프롬프트가 여기에 들어갑니다.
여러 단락으로 작성할 수 있으며, 서브에이전트의 역할, 능력,
문제 해결 접근 방식을 명확히 정의해야 합니다.

구체적인 지침, 모범 사례, 제약 조건을 포함하세요.
```


### 설정 필드 상세 설명

**필수 필드:**

- **name**: 소문자와 하이픈을 사용한 고유 식별자 (예: `code-reviewer`, `test-automator`)
- **description**: 서브에이전트의 목적과 호출 시점을 설명하는 자연어 설명문. 이 설명이 Claude Code가 자동으로 적절한 서브에이전트를 선택하는 핵심 기준이 됩니다[^1]

**선택 필드:**

- **tools**: 쉼표로 구분된 도구 목록. 생략시 메인 스레드의 모든 도구(MCP 도구 포함)를 상속합니다[^1]
- **model**: `sonnet`, `opus`, `haiku` 중 선택하거나 `'inherit'`로 메인 대화의 모델을 따를 수 있습니다[^1]
- **color**: UI에서 서브에이전트를 구분하기 위한 색상 (예: `purple`) - 문서에는 명시되지 않았지만 실제 생성된 에이전트에 포함됩니다[^2]


## 저장 위치와 우선순위

서브에이전트는 두 가지 레벨에서 관리할 수 있습니다:[^1]


| 유형 | 경로 | 범위 | 우선순위 |
| :-- | :-- | :-- | :-- |
| 프로젝트 서브에이전트 | `.claude/agents/` | 현재 프로젝트에만 사용 | 최상위 |
| 사용자 서브에이전트 | `~/.claude/agents/` | 모든 프로젝트에서 사용 | 하위 |

프로젝트 레벨 에이전트는 버전 관리에 포함하여 팀과 공유할 수 있습니다.[^1]

## 실전 페르소나 예시

### 1. 코드 리뷰어 페르소나

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```


### 2. 디버거 페르소나

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.
```


### 3. 시스템 아키텍트 페르소나

프로덕션 환경에서 사용되는 실제 예시:[^3]

```markdown
---
name: architect-review
description: Validates design against platform constraints. Use PROACTIVELY after pm-spec completes. Reviews architecture decisions and produces ADR.
tools: Read, Write, Grep, Glob
model: sonnet
---

You are a senior systems architect specializing in scalable real-time applications.

When invoked:
1. Read the working spec from docs/claude/working-notes/
2. Validate design against platform constraints
3. Consider performance and cost limits
4. Produce an Architecture Decision Record (ADR)
5. Set status to READY_FOR_BUILD

Key responsibilities:
- Ensure architectural consistency
- Identify scalability concerns
- Recommend optimal design patterns
- Document trade-offs and alternatives
- Validate against best practices

Output format:
- ADR saved to docs/claude/decisions/ADR-<slug>.md
- Clear justification for design choices
- Performance and cost considerations
- Next steps for implementation
```


## \$ARGUMENTS를 사용한 동적 매개변수

### 기본 사용법

커스텀 명령어에서 `$ARGUMENTS`를 사용하여 동적 값을 전달할 수 있습니다:[^4][^5]

```markdown
# .claude/commands/fix-issue.md
---
description: Fix a specific issue following coding standards
argument-hint: issue-number priority
---

Fix issue #$ARGUMENTS following our coding standards
```

**사용 예시:**

```
> /fix-issue 123 high-priority
```

`$ARGUMENTS`는 "123 high-priority"로 치환됩니다.

### 개별 인자 접근

위치 매개변수 `$1`, `$2`, `$3` 등을 사용하여 개별 인자에 접근할 수 있습니다:[^4]

```markdown
# .claude/commands/review-pr.md
Review PR #$1 with priority $2 and assign to $3
```

**사용 예시:**

```
> /review-pr 456 high alice
```

- `$1` = "456"
- `$2` = "high"
- `$3` = "alice"


### 다중 인자 파싱 기법

공식 문서에서 명시하지 않은 실용적인 방법으로, 마크다운 참조 링크 문법을 활용한 변수 파싱이 있습니다:[^5]

```markdown
## Context
[name]: $ARGUMENTS "Component name"
[summary]: $ARGUMENTS "Component summary"

## Task
Create a UI component:
- Folder name: [name]
- Component name: [name]
- Use [summary] for implementation details
```

이 방법은 여러 인자를 구조화된 방식으로 추출하여 프롬프트의 다른 부분에서 사용할 수 있게 합니다.

## 서브에이전트 생성 및 관리

### 대화형 생성 (권장 방법)

`/agents` 명령어를 사용하여 대화형으로 서브에이전트를 생성할 수 있습니다:[^1]

1. `/agents` 입력
2. "Create New Agent" 선택
3. 프로젝트 레벨 또는 사용자 레벨 선택
4. Claude가 초안 생성 → 커스터마이징 (권장 워크플로우)
5. 설명과 도구 접근 권한 설정
6. 시스템 프롬프트 편집 (에디터에서 `e` 키 입력)

### 직접 파일 생성

```bash
# 프로젝트 서브에이전트 생성
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, 
proactively run the appropriate tests. If tests fail, analyze 
the failures and fix them while preserving the original test intent.
EOF

# 사용자 서브에이전트 생성
mkdir -p ~/.claude/agents
# ... 파일 생성
```


### CLI를 통한 동적 정의

세션별 또는 자동화 스크립트용으로 CLI에서 JSON으로 서브에이전트를 정의할 수 있습니다:[^1]

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```


## 서브에이전트 호출 방법

### 자동 위임

Claude Code는 다음 요소를 기반으로 자동으로 작업을 위임합니다:[^1]

- 요청의 작업 설명
- 서브에이전트 설정의 `description` 필드
- 현재 컨텍스트와 사용 가능한 도구

**프로액티브 사용을 촉진하려면** `description` 필드에 "use PROACTIVELY" 또는 "MUST BE USED" 같은 문구를 포함하세요.[^1]

### 명시적 호출

특정 서브에이전트를 명시적으로 요청할 수 있습니다:[^1]

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```


### 서브에이전트 체이닝

복잡한 워크플로우를 위해 여러 서브에이전트를 체인으로 연결할 수 있습니다:[^3][^1]

```
> First use the code-analyzer subagent to find performance issues, 
  then use the optimizer subagent to fix them
```

**프로덕션 파이프라인 예시** (PubNub에서 사용):[^3]

1. **pm-spec** → 요구사항 읽고 작업 스펙 작성, 상태를 `READY_FOR_ARCH`로 설정
2. **architect-review** → 플랫폼 제약사항에 대한 설계 검증, ADR 생성, 상태를 `READY_FOR_BUILD`로 설정
3. **implementer-tester** → 코드 및 테스트 구현, 문서 업데이트, 상태를 `DONE`으로 변경

## 고급 활용 패턴

### 멀티 에이전트 오케스트레이션

**순차 실행 패턴**:[^6]

```
requirements-analyst → system-architect → code-reviewer
```

**병렬 처리 패턴**:[^6]

```
ui-engineer + api-designer + database-schema-designer 동시 실행
```

Claude Code는 최대 **10개의 서브에이전트를 병렬로** 실행할 수 있으며, 지능형 큐잉 시스템을 통해 100개 이상의 작업으로 확장 가능합니다.[^7]

### 컨텍스트 관리의 핵심 원리

서브에이전트의 가장 중요한 특징은 **독립적인 컨텍스트 윈도우**입니다:[^8][^9]

- 각 서브에이전트는 자체 200K 토큰 컨텍스트 윈도우를 갖습니다[^7]
- 메인 대화는 고수준 목표에 집중하고, 세부 작업은 서브에이전트가 처리
- 서브에이전트는 **이전 대화 컨텍스트가 없음** - 메인 에이전트가 전달한 정보만 사용[^9]

**중요:** 서브에이전트는 사용자가 아닌 **메인 에이전트에게 응답**합니다. 이는 시스템 프롬프트 작성 방식에 영향을 미칩니다.[^9]

### HITL (Human-in-the-Loop) 패턴

자율성을 유지하면서도 인간의 통제를 보장하는 방법:[^3]

1. **명확한 핸드오프**: 후크(hook)가 다음 단계를 제안하면 인간이 승인
2. **완료 정의(DoD)**: 각 에이전트의 프롬프트에 체크리스트 포함
3. **감사 추적**: 각 개선사항에 "slug" 부여하여 추적
    - Queue: `enhancements/_queue.json`에 slug → status 기록
    - PM 노트: `docs/claude/working-notes/<slug>.md`
    - ADR: `docs/claude/decisions/ADR-<slug>.md`

## 모범 사례

**Claude 생성 에이전트로 시작**: 초기 서브에이전트를 Claude가 생성하도록 한 후 커스터마이징하는 것을 강력히 권장합니다.[^1]

**단일 책임 설계**: 하나의 명확한 책임을 가진 서브에이전트를 만들어 예측 가능성과 성능을 향상시킵니다.[^6]

**상세한 프롬프트 작성**: 구체적인 지침, 예시, 제약 조건을 시스템 프롬프트에 포함합니다.[^1]

**도구 접근 제한**: 필요한 도구만 부여하여 보안을 강화하고 포커스를 유지합니다.[^1]

**버전 관리**: 프로젝트 서브에이전트를 버전 관리에 포함하여 팀 전체가 협업하고 개선할 수 있도록 합니다.[^1]

**프로액티브 트리거 키워드 사용**: description에 "use PROACTIVELY", "MUST BE USED" 같은 키워드를 포함하여 자동 호출을 촉진합니다.[^10]

## 실제 사용 사례

현재 100개 이상의 전문화된 서브에이전트가 커뮤니티에서 공유되고 있으며, 주요 카테고리는 다음과 같습니다:[^11][^12][^6]

- **개발 역할**: Frontend Engineer, Backend Engineer, DevOps Specialist
- **품질 보증**: Test Automator, Code Reviewer, Security Auditor
- **분석 및 최적화**: Performance Engineer, Data Scientist, Architecture Reviewer
- **문서화**: Technical Writer, API Documentation Specialist
- **프로젝트 관리**: PM Spec Writer, Project Orchestrator

이러한 페르소나 시스템은 Claude Code를 단순한 코딩 도구가 아닌, **전문가 팀을 오케스트레이션하는 AI 운영 체제**로 변모시킵니다.[^13][^7]
<span style="display:none">[^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31]</span>

<div align="center">⁂</div>

[^1]: https://docs.claude.com/en/docs/claude-code/sub-agents

[^2]: https://github.com/anthropics/claude-code/issues/8501

[^3]: https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/

[^4]: https://docs.claude.com/en/docs/claude-code/slash-commands

[^5]: https://www.youtube.com/watch?v=52KBhQqqHuc

[^6]: https://www.superprompt.com/blog/best-claude-code-agents-and-use-cases

[^7]: https://www.cursor-ide.com/blog/claude-code-subagents

[^8]: https://github.com/VoltAgent/awesome-claude-code-subagents

[^9]: https://www.youtube.com/watch?v=7B2HJr0Y68g

[^10]: https://www.youtube.com/watch?v=HJ9VvIG3Rps

[^11]: https://github.com/wshobson/agents

[^12]: https://github.com/lst97/claude-code-sub-agents

[^13]: https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide

[^14]: https://www.youtube.com/watch?v=Phr7vBx9yFQ

[^15]: https://subagents.app

[^16]: https://www.reddit.com/r/ClaudeAI/comments/1m8gl6b/you_can_now_create_custom_subagents_for/

[^17]: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

[^18]: https://www.anthropic.com/engineering/claude-code-best-practices

[^19]: https://www.youtube.com/watch?v=DNGxMX7ym44

[^20]: https://www.reddit.com/r/ClaudeAI/comments/1lojyky/just_tried_using_subagents_this_unlocks_the_true/

[^21]: https://www.eesel.ai/blog/claude-code-subagents

[^22]: https://www.reddit.com/r/ClaudeAI/comments/1mdyc60/whats_your_best_way_to_use_subagents_in_claude/

[^23]: https://docs.claude.com/en/docs/claude-code/settings

[^24]: https://www.reddit.com/r/ClaudeAI/comments/1md7066/passing_multiple_parameters_to_custom_command/

[^25]: https://dev.to/voltagent/100-claude-code-subagent-collection-1eb0

[^26]: https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/

[^27]: https://www.builder.io/blog/claude-code

[^28]: https://docs.claude.com/en/api/agent-sdk/subagents

[^29]: https://www.youtube.com/watch?v=tSD96-mNrlQ

[^30]: https://github.com/hesreallyhim/awesome-claude-code

[^31]: https://aiengineerguide.com/blog/claude-code-custom-command/

