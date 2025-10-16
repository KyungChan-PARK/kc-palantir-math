<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Claude Code Multi-Agent Observability 구현 - 상세 실행 가이드

AI 에이전트가 자동으로 실행할 수 있도록 **5단계 구현 프로세스**를 완전히 문서화했습니다.

## 📦 생성된 리소스

### 1. **상세 PDF 매뉴얼** (13페이지)

**포함 내용**:

- WSL Ubuntu 환경 설정부터 완전한 시스템 구동까지
- 각 단계별 명령어와 예상 출력
- 트러블슈팅 가이드
- 성능 로그 분석 방법


### 2. **체크리스트 기반 가이드** (위 출력 참조)

**5개 Phase로 구성**:

- **Phase 1**: 환경 준비 (15분) - Node.js, Python, Bun, Claude Code
- **Phase 2**: IndyDevDan Observability (15분) - 서버/클라이언트 설정
- **Phase 3**: kenneth-liao Agent SDK (10분) - Python SDK 모듈
- **Phase 4**: 통합 테스트 (10분) - 실시간 모니터링 검증
- **Phase 5**: 커스텀 Hook 개발 (10분) - 안전 가드 \& 성능 모니터


## 🎯 AI Agent가 따라야 할 핵심 단계

### Phase 1: 환경 준비 (체크박스 체크 필수)

```bash
# 1.1 WSL 확인
wsl --status

# 1.2 패키지 업데이트
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git unzip build-essential

# 1.3 Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 1.4 npm 경로 설정
npm config set prefix ~/.npm-global
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 1.5-1.6 uv + Python 3.13
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv python install 3.13

# 1.7 Bun
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc

# 1.8 Claude Code
npm install -g @anthropic-ai/claude-code
claude auth login
```


### Phase 2: Observability 시스템

```bash
# 2.1 저장소 클론
cd ~
git clone https://github.com/disler/claude-code-hooks-multi-agent-observability.git
cd claude-code-hooks-multi-agent-observability

# 2.2-2.3 의존성 설치
cd apps/server && bun install && mkdir -p data
cd ../client && npm install

# 2.4 환경변수 (.env 파일에 실제 API 키 입력 필요)
cd ~/claude-code-hooks-multi-agent-observability
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-actual-key
VITE_MAX_EVENTS_TO_DISPLAY=100
SERVER_PORT=4000
CLIENT_PORT=5173
EOF

# 2.5-2.6 시스템 시작 (터미널 2개 필요)
# 터미널 1:
cd ~/claude-code-hooks-multi-agent-observability/apps/server
bun run src/index.ts

# 터미널 2:
cd ~/claude-code-hooks-multi-agent-observability/apps/client
npm run dev

# 2.7 브라우저: http://localhost:5173
```


### Phase 3: Agent SDK

```bash
cd ~
git clone https://github.com/kenneth-liao/claude-agent-sdk-intro.git
cd claude-agent-sdk-intro
uv sync

# settings.json 수정 (Linux 사운드 경로)
nano .claude/settings.json

# 테스트
python 0_querying.py
python 1_messages.py
```


### Phase 4: 통합 테스트

```bash
# Hook 스크립트 복사
mkdir -p ~/.claude/hooks
cp ~/claude-code-hooks-multi-agent-observability/.claude/hooks/*.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py

# 테스트 프로젝트
mkdir ~/test-multi-agent
cd ~/test-multi-agent

# settings.json 생성 (Hook 연결)
mkdir .claude
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "uv run ~/.claude/hooks/send_event.py --source-app test-project --event-type PreToolUse --summarize"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "uv run ~/.claude/hooks/send_event.py --source-app test-project --event-type PostToolUse --summarize"
      }]
    }]
  }
}
EOF

# 테스트 실행 (Observability 서버/클라이언트 실행 중이어야 함)
export ANTHROPIC_API_KEY=your-key
uv run test_agent.py
```


### Phase 5: 커스텀 Hook

```bash
# 안전 가드 Hook
cat > ~/.claude/hooks/safety_guard.py << 'EOF'
#!/usr/bin/env python3
import json, sys
DANGEROUS = ['rm -rf /', 'sudo rm', 'dd if=', 'mkfs']
event = json.load(sys.stdin)
if event.get('tool_name') == 'Bash':
    for p in DANGEROUS:
        if p in str(event.get('tool_input', '')):
            print(f"🚫 BLOCKED: {p}", file=sys.stderr)
            sys.exit(2)
sys.exit(0)
EOF
chmod +x ~/.claude/hooks/safety_guard.py

# 성능 모니터 Hook
cat > ~/.claude/hooks/performance_monitor.py << 'EOF'
#!/usr/bin/env python3
import json, sys, os
from datetime import datetime
event = json.load(sys.stdin)
with open(os.path.expanduser("~/.claude/performance.log"), 'a') as f:
    f.write(f"{datetime.now().isoformat()} | {event.get('tool_name')}\n")
sys.exit(0)
EOF
chmod +x ~/.claude/hooks/performance_monitor.py
```


## ✅ 검증 체크리스트 (AI Agent가 확인해야 할 항목)

### 시스템 상태

- [ ] `curl http://localhost:4000` 응답 (서버 정상)
- [ ] `curl http://localhost:5173` 응답 (클라이언트 정상)
- [ ] `ls ~/claude-code-hooks-multi-agent-observability/apps/server/data/*.db` (DB 생성됨)


### 기능 검증

- [ ] 브라우저에서 실시간 이벤트 표시됨
- [ ] PreToolUse 이벤트 (🔧 아이콘)
- [ ] PostToolUse 이벤트 (✅ 아이콘)
- [ ] Stop 이벤트 (🛑 아이콘)
- [ ] 필터링 기능 작동


### Hook 시스템

- [ ] `cat ~/.claude/performance.log` (로그 기록 확인)
- [ ] `ls -l ~/.claude/hooks/*.py` (실행 권한 확인)
- [ ] 위험 명령 차단 테스트 통과


## 🚨 트러블슈팅 우선순위

1. **"command not found" 에러**: `source ~/.bashrc` 실행
2. **포트 충돌**: `lsof -i :4000` 및 `lsof -i :5173` 확인 후 프로세스 종료
3. **Hook 실행 안 됨**: `chmod +x ~/.claude/hooks/*.py`
4. **API 키 오류**: `claude auth login` 재실행

## 📊 성공 확인 방법

```bash
# 최종 검증 스크립트
echo "=== System Check ==="
curl -s http://localhost:4000 && echo "✓ Server OK"
curl -s http://localhost:5173 && echo "✓ Client OK"
ls ~/.claude/hooks/*.py | wc -l && echo "Hook scripts"
cat ~/.claude/performance.log | tail -3 && echo "✓ Logs working"
```

**예상 출력**:

```
=== System Check ===
✓ Server OK
✓ Client OK
7 Hook scripts
2025-10-16T... | Write
2025-10-16T... | Bash
2025-10-16T... | Read
✓ Logs working
```


## 🎯 다음 단계

구현 완료 후 AI Agent가 수행할 수 있는 고급 기능:

1. **Module 5-6 실행**: MCP 통합 및 서브에이전트
2. **병렬 에이전트 테스트**: 3-5개 에이전트 동시 실행
3. **프로덕션 배포**: Docker 컨테이너화 및 PostgreSQL 마이그레이션

모든 명령어는 복사-붙여넣기 가능하도록 작성되었으며, 각 단계의 예상 출력과 검증 방법이 명시되어 있습니다.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://gist.github.com/Kirchlive/184cdd96a56bfd7a6c67997836495f3c

[^2]: https://docs.astral.sh/uv/guides/install-python/

[^3]: https://github.com/oven-sh/bun

[^4]: https://www.reddit.com/r/ClaudeAI/comments/1kv4mfx/how_to_use_claude_code_in_vs_code_in_windows_via/

[^5]: https://pydevtools.com/handbook/how-to/how-to-install-python-with-uv/

[^6]: https://hono.dev/docs/getting-started/bun

[^7]: https://claude.ai/public/artifacts/03a4aa0c-67b2-427f-838e-63770900bf1d

[^8]: https://www.digitalocean.com/community/conceptual-articles/uv-python-package-manager

[^9]: https://www.tecmint.com/install-bun-on-linux/

[^10]: https://www.youtube.com/watch?v=dkyQswyidhg

[^11]: https://realpython.com/python-uv/

[^12]: https://www.sitepoint.com/bun-javascript-runtime-introduction/

[^13]: https://docs.claude.com/en/docs/claude-code/setup

[^14]: https://docs.astral.sh/uv/getting-started/installation/

[^15]: https://www.youtube.com/watch?v=Goa02gPhFBY

[^16]: https://www.youtube.com/watch?v=lQmsLSR13ac

[^17]: https://github.com/astral-sh/uv

[^18]: https://bun.com

[^19]: https://stackoverflow.com/questions/79626096/unable-to-install-claude-code-in-windows-with-wsl

[^20]: https://www.youtube.com/watch?v=AMdG7IjgSPM

