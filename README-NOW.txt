━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 지금 바로 사용하기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 서버 실행 중: http://localhost:4000 (PID in server.pid)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  추천 실행 순서
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  테스트 실행 (시스템 검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd /home/kc-palantir/math
python3 tests/run_all_tests.py

예상 결과:
  Success Rate: 100.0%
  🎉 ALL TESTS PASSED!


2️⃣  Feedback Loop 실행 (실제 워크플로우)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

python3 scripts/run_feedback_loop.py --image sample.png

과정:
  [1/7] OCR Extraction (Mathpix)
  [2/7] Concept Matching (841개 개념)
  [3/7] Pattern Query (Neo4j)
  [4/7] Scaffolding Generation (10 steps)
  [5/7] Feedback Collection ← 여기서 당신이 평가
  [6/7] Pattern Extraction
  [7/7] Pattern Storage

피드백 입력 예시:
  Rate this step (1-5): 4
  Comment: Good question
  Suggested improvement: (Enter to skip)


3️⃣  이벤트 확인 (API로 모니터링)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 최근 이벤트 5개 (간단히)
curl -s "http://localhost:4000/events/recent?limit=5" | python3 -c "
import sys, json
data = json.load(sys.stdin)
events = data['events']
print(f'Recent Events: {len(events)}')
for e in events:
    print(f\"  {e['hook_event_type']}: {e.get('summary', 'no summary')[:50]}\")
"

# 세션 목록
curl -s http://localhost:4000/events/sessions | python3 -m json.tool


4️⃣  Main Agent 사용 (12 Agents)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

uv run python main.py

예시:
  You: sample.png 분석해줘
  You: 피타고라스 정리 파일 만들어줘
  You: exit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  결과 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

생성된 데이터:
  ls -lh data/ocr_results/
  ls -lh data/feedback_sessions/
  ls -lh data/learned_patterns/

로그:
  tail -f /tmp/obs_server.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  서버 관리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

종료:
  kill $(cat server.pid)

재시작:
  ./QUICK-START-GUIDE.sh

상태 확인:
  curl http://localhost:4000/health

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dashboard는 선택사항입니다 (DASHBOARD-SETUP.md 참고)
핵심 기능은 모두 CLI/API로 사용 가능합니다.

