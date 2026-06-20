# claude_repo

한국/미국 증시 리포트 자동 생성 파이프라인.

## 구조

- `prompts/` — 각 리포트가 따라야 할 작성 지침 (로컬 크론이 매 실행마다 이 문서를 읽고 따른다)
  - `korea-market-closing-report.md` — 평일 16:00 KST, 텔레그램만
  - `korea-market-noon-report.md` — 평일 12:00 KST, 텔레그램만
  - `us-market-morning-report.md` — 평일 08:20 KST, 텔레그램만
- `scripts/` — 리포트 전송/저장에 쓰이는 공용 스크립트 (토큰은 코드에 없고 실행 시 환경변수로 주입됨)
  - `send_telegram.py <message_file>` — `TG_BOT_TOKEN`, `TG_CHAT_ID` 필요 (3개 리포트 모두 사용)
  - `update_status.py <key> <date> <status>` — `_status.json`에 마지막 실행 결과 기록 (3개 리포트 모두 사용)
  - `push_to_github.py <local_file> <repo_path> [commit_message]` — `GH_TOKEN`, `GH_REPO` 필요. 현재는 리포트 본문을 push하지 않으므로 사용되지 않는 범용 유틸리티
- `stock_report/` — 과거에 생성된 리포트 결과물 (2026-06-16 이전, 현재는 더 이상 갱신되지 않음)
- `_status.json` — 리포트별 마지막 실행 날짜/상태
- `run.sh` — 로컬 크론 진입점. `.env.example`을 `.env`로 복사해 토큰을 채운 뒤 사용

## 실행 방식 (2026-06-18부터: 로컬 크론)

처음엔 claude.ai 클라우드 routine(`/schedule`)으로 돌렸으나, 클라우드 샌드박스의 네트워크 allowlist에
`api.telegram.org`가 없어 텔레그램 전송이 막혔다. 그래서 이 머신의 로컬 crontab + `claude -p`(headless)
실행 방식으로 전환했다 (네트워크 제한 없음). 클라우드 routine 3개는 비활성화 상태로 남겨둠.

로컬 설정 예시 (한국 증시 휴장일인 주말엔 돌 필요 없으므로 평일만):
```
crontab -e
# 아래 3줄 추가
0 16 * * 1-5 /path/to/this/repo/run.sh closing >> /path/to/this/repo/logs/cron.log 2>&1
0 12 * * 1-5 /path/to/this/repo/run.sh noon >> /path/to/this/repo/logs/cron.log 2>&1
20 8 * * 1-5 /path/to/this/repo/run.sh premarket >> /path/to/this/repo/logs/cron.log 2>&1
```

## 주의

이 저장소는 public이므로 API 토큰/시크릿은 절대 코드에 직접 넣지 않는다. 모든 스크립트는 환경변수로만 토큰을 받고,
`.env`는 `.gitignore`에 등록해 절대 push하지 않는다.
