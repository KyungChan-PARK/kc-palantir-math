━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Math Education Feedback Loop System - 시작 가이드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

현재 상태: ✅ 서버 실행 중 (PID: $(cat server.pid 2>/dev/null || echo "확인중"))

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  빠른 시작 (1분)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  서버 상태 확인:
   curl http://localhost:4000/health

2️⃣  테스트 실행:
   python3 tests/run_all_tests.py

3️⃣  Feedback Loop 실행:
   python3 scripts/run_feedback_loop.py --image sample.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  서버 관리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 서버 종료:
   kill $(cat /home/kc-palantir/math/server.pid)

🟢 서버 재시작:
   ./QUICK-START-GUIDE.sh

📊 서버 로그 확인:
   tail -f /tmp/obs_server.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  시스템 구성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 12 Agents (Meta-orchestrator + 11 subagents + feedback-learning)
✅ 19 Hook Scripts (indydevdan integration)
✅ 841 Math Concepts (중1-1 ~ 중3-2)
✅ Mathpix OCR (99.9% accuracy)
✅ WebSocket Streaming (real-time)
✅ Pattern Learning (feedback-driven)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  문서
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 START-HERE.md                    - 전체 가이드
📖 FEEDBACK-LOOP-QUICKSTART.md      - Feedback loop 상세
📖 ARCHITECTURE-DIAGRAMS.md         - 시스템 다이어그램
📖 PROJECT-ARCHITECTURE-VISUALIZATION.md - 초보자용 설명

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

