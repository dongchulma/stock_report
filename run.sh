#!/bin/bash
# 로컬 크론에서 실행하는 진입점. 사용법: ./run.sh <closing|noon|premarket>
# 이 저장소를 ~/stock-report-bot/ 같은 곳에 두고, .env.example을 .env로 복사해
# 실제 토큰 값을 채운 뒤 crontab에 등록해서 사용한다.

REPORT_TYPE="${1:?report type required: closing|noon|premarket}"

cd "$(dirname "$0")"
set -a; source .env; set +a

case "$REPORT_TYPE" in
  closing) PROMPT_FILE="prompts/korea-market-closing-report.md" ;;
  noon) PROMPT_FILE="prompts/korea-market-noon-report.md" ;;
  premarket) PROMPT_FILE="prompts/us-market-morning-report.md" ;;
  *) echo "Unknown report type: $REPORT_TYPE" >&2; exit 1 ;;
esac

claude -p "${PROMPT_FILE} 파일을 읽고 그 안의 지침을 정확히 따라 리포트를 작성하세요. 날짜는 한국시간(Asia/Seoul) 기준 오늘 날짜를 사용하세요. 텔레그램 전송과 상태 기록(_status.json)은 scripts/ 안의 파이썬 스크립트를 그대로 사용해 수행하세요 (필요한 환경변수는 이미 설정되어 있습니다). curl을 새로 작성하지 마세요." --dangerously-skip-permissions
