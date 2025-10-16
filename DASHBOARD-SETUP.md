# Dashboard 설정 가이드 (선택사항)

> Observability Dashboard는 **선택사항**입니다. 
> 핵심 시스템은 Dashboard 없이도 100% 작동합니다.

---

## Dashboard 필요성

**Dashboard 없이도 가능**:
- ✅ Feedback loop 실행
- ✅ 모든 테스트
- ✅ Main agent 사용
- ✅ 서버 API로 이벤트 조회

**Dashboard 있으면 좋은 점**:
- 📊 실시간 시각화
- 🎨 그래프 차트
- 🔍 이벤트 필터링
- 👁️ 직관적인 모니터링

---

## Option 1: bun 설치 (권장)

### Ubuntu/Debian (snap 사용)
```bash
sudo snap install bun-js
```

### 또는 curl 설치
```bash
curl -fsSL https://bun.sh/install | bash
```

### 설치 확인
```bash
bun --version
```

### Dashboard 실행
```bash
cd /home/kc-palantir/math/observability-dashboard
bun install
bun run dev
# → http://localhost:3000
```

---

## Option 2: npm 사용 (대안)

bun 대신 npm으로 실행 가능:

```bash
cd /home/kc-palantir/math/observability-dashboard
npm install
npm run dev
# → http://localhost:3000
```

---

## Option 3: Dashboard 없이 사용 (권장)

Dashboard 없이 API로 이벤트 확인:

### 최근 이벤트 조회
```bash
curl "http://localhost:4000/events/recent?limit=10" | python3 -m json.tool
```

### 세션 목록
```bash
curl http://localhost:4000/events/sessions | python3 -m json.tool
```

### 특정 이벤트 타입 필터
```bash
curl "http://localhost:4000/events/recent?event_type=ocr_completed" | python3 -m json.tool
```

### 실시간 모니터링 (CLI)
```bash
# Terminal 1: 이벤트 실시간 조회
watch -n 1 'curl -s "http://localhost:4000/events/recent?limit=5" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f\"{e[\"hook_event_type\"]}: {e.get(\"summary\", \"no summary\")[:50]}\") for e in d[\"events\"][:5]]"'

# Terminal 2: 워크플로우 실행
python3 scripts/run_feedback_loop.py --image sample.png
```

---

## 현재 시스템 상태

### 실행 중인 서비스

```bash
# Observability Server 확인
curl http://localhost:4000/health
# {"status":"healthy","websocket_clients":0}
```

### 사용 가능한 기능

✅ **Dashboard 없이 사용 가능**:
- Feedback loop workflow
- Pattern learning
- All tests
- Main agent system
- API로 이벤트 조회

⚠️ **Dashboard 필요 시**:
- 실시간 시각화
- Live Pulse Chart
- Event Timeline UI

---

## 권장 사항

**개발/테스트 단계**:
→ Dashboard 없이 진행 (API + CLI로 충분)

**프로덕션/데모**:
→ Dashboard 설치 (시각적 효과)

**현재 상황**:
→ **Dashboard 없이 계속 진행 가능** ✅

---

**작성일**: 2025-10-16
**상태**: Dashboard는 선택사항, 핵심 시스템 100% 작동 중

