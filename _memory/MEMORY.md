# Claude 전역 메모리 — 마동철 (tough002@gmail.com)
> 최종 업데이트: 2026-06-16

---

## 인증 정보 참조 (Credentials Reference)

### GitHub
- **활성 레포**: dongchulma/stock_report (리포트 저장소, 2026-06-16 신규)
- **구 레포**: dongchulma/claude_repo (더 이상 리포트 저장 안 함)
- **토큰 타입**: Fine-grained PAT (github_pat_11... 형식)
  - stock_report / claude_repo / open-claw Contents 쓰기 권한
  - 2026-06-16 교체됨 (이전 ghp_ 토큰은 Contents 쓰기 불가였음)
  - 실제 토큰값은 스케줄 태스크 SKILL.md에 내장됨

### Telegram
- **Bot Token**: 894353...Mtiw (8943539983:AAFFSeg... 형식)
- **Chat ID**: 8646094396
- **용도**: 증시 리포트 자동 전송 (미국 07:00, 한국 12:00·16:00)
- 실제 토큰값은 스케줄 태스크 SKILL.md에 내장됨

---

## 자동화 워크플로우

### 스케줄 태스크 (3개)
| 태스크 ID | 시간 | 내용 |
|---|---|---|
| us-market-morning-report | 매일 07:00 | 미국 증시 리포트 |
| korea-market-noon-report | 매일 12:00 | 한국 증시 오전 리포트 |
| korea-market-closing-report | 매일 16:00 | 한국 증시 마감 리포트 |

### 공통 동작 흐름
1. WebSearch로 데이터 수집
2. Cowork 아티팩트 업데이트
3. 리포트 파일 세션 outputs 저장
4. Chrome MCP (javascript_tool + fetch)로 GitHub push + 텔레그램 전송

### GitHub 저장 구조 (stock_report)
- us-market/YYYY-MM-DD.md
- korea-noon/YYYY-MM-DD.md
- korea-closing/YYYY-MM-DD.md
- _memory/MEMORY.md

### 핵심 기술 사항
- 샌드박스(bash)는 외부 API 차단 → Chrome MCP로 우회
- chrome:// 탭이면 google.com 이동 후 fetch 실행
- GitHub API: Authorization: Bearer {token} 형식
- 텔레그램: HTML parse_mode, & → &amp; 이스케이프 필요

---

## 사용자 정보
- 이름: 마동철 / 이메일: tough002@gmail.com
- 네이버 블로그: blog.naver.com/retrogradelife
