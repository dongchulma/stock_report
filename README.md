# stock_report

한국/미국 증시 리포트 자동 생성 파이프라인. (2026-06-20: `claude_repo`에서 이 저장소로 코드 이전함 —
이전엔 claude.ai Cowork 세션이 이 저장소에 직접 리포트를 올렸으나 그 세션은 중지됨. 이제는 아래 로컬
launchd 파이프라인이 유일한 운영 방식.)

## 구조

- `prompts/` — 각 리포트가 따라야 할 작성 지침 (실행 시마다 이 문서를 읽고 따른다)
  - `korea-market-closing-report.md` — 평일 16:00 KST, 텔레그램만
  - `korea-market-noon-report.md` — 평일 12:00 KST, 텔레그램만
  - `us-market-morning-report.md` — 평일 08:20 KST, 텔레그램만
- `scripts/` — 리포트 전송/저장에 쓰이는 공용 스크립트 (토큰은 코드에 없고 실행 시 환경변수로 주입됨)
  - `send_telegram.py <message_file>` — `TG_BOT_TOKEN`, `TG_CHAT_ID` 필요 (3개 리포트 모두 사용)
  - `update_status.py <key> <date> <status>` — `_status.json`에 마지막 실행 결과 기록 (3개 리포트 모두 사용)
  - `push_to_github.py <local_file> <repo_path> [commit_message]` — `GH_TOKEN`, `GH_REPO` 필요. 현재는 리포트 본문을 push하지 않으므로 사용되지 않는 범용 유틸리티
- `launchd/` — macOS LaunchAgent plist (스케줄 실행 정의). `~/Library/LaunchAgents/`에 복사해 사용
- `stock_report/` — 과거에 생성된 리포트 결과물 (2026-06-16 이전, 현재는 더 이상 갱신되지 않음)
- `_status.json` — 리포트별 마지막 실행 날짜/상태
- `run.sh` — 스케줄 진입점. `.env.example`을 `.env`로 복사해 토큰을 채운 뒤 사용

## 실행 방식 (2026-07-13부터: launchd LaunchAgent)

### 이력
1. 처음엔 claude.ai 클라우드 routine(`/schedule`)으로 돌렸으나, 클라우드 샌드박스의 네트워크 allowlist에
   `api.telegram.org`가 없어 텔레그램 전송이 막혔다. → 로컬 실행으로 전환.
2. 2026-06-18~07-07: 로컬 `crontab` + `claude -p`(headless). **하지만 cron 세션은 macOS 로그인 키체인에
   접근할 수 없어 `claude`가 항상 "Not logged in"으로 실패했다** (즉 cron으로는 한 번도 성공하지 못함).
   또한 cron 데몬 자체의 신뢰성 문제로 며칠씩 조용히 멈추는 사고도 있었다.
3. 2026-07-13부터: **launchd LaunchAgent로 이전.** LaunchAgent는 사용자 GUI 세션에서 실행되어 키체인에
   접근할 수 있으므로 `claude -p` 인증이 정상 동작하고, 잠자기로 놓친 스케줄도 깨어날 때 실행해준다.

### 설정 방법
`launchd/`의 plist 3개를 사용자 LaunchAgents 폴더에 복사한 뒤 로드한다 (한국 증시 휴장일인 주말엔 돌 필요가
없으므로 plist의 `Weekday`는 1~5(월~금)로 제한되어 있다):
```
cp launchd/com.togh002.stockreport.*.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.togh002.stockreport.closing.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.togh002.stockreport.noon.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.togh002.stockreport.premarket.plist
```
- 스케줄: 마감 16:00 / 정오 12:00 / 프리마켓(미국장) 08:20 KST, 평일만.
- 로그: 각 잡별로 `logs/launchd-{closing,noon,premarket}.log`.
- 수동 실행: `launchctl kickstart gui/$(id -u)/com.togh002.stockreport.closing`
- 참고: plist는 경로가 `/Users/togh002/...`로 하드코딩되어 있으므로 다른 사용자/경로에서 쓰려면 `Label`,
  `ProgramArguments`, `StandardOutPath`를 환경에 맞게 수정한다.

## 주의

이 저장소는 public이므로 API 토큰/시크릿은 절대 코드에 직접 넣지 않는다. 모든 스크립트는 환경변수로만 토큰을 받고,
`.env`는 `.gitignore`에 등록해 절대 push하지 않는다.
