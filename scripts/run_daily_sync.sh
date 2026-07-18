#!/bin/bash
# run_daily_sync.sh
# J-Hub 포털 데이터 연동 자동화 파이프라인

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/../data/sync.log"

echo "==========================================" >> "$LOG_FILE"
echo "🔄 J-Hub Daily Sync Started at $(date)" >> "$LOG_FILE"

# 1. 서울시 공고 API 크롤링 및 workspace.json 주입
echo "[1/2] 서울시 공고 연동 중..."
python3 "$SCRIPT_DIR/update_workspace_api.py" >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ update_workspace_api.py 실행 실패" >> "$LOG_FILE"
else
    echo "✅ 서울시 연동 성공" >> "$LOG_FILE"
fi

# 2. 통합검토보고서 데이터 파싱 및 workspace.json 주입
# 최신 통합보고서를 찾아서 인자로 넘김 (여기서는 하드코딩된 경로 예시 사용)
REPORT_FILE="/Users/joongilkim/.gemini/antigravity/brain/a171760b-818f-4d97-a25c-081e358a26d6/scratch/report_0712_standard.html"

if [ -f "$REPORT_FILE" ]; then
    echo "[2/2] 통합보고서 파싱 중: $REPORT_FILE"
    python3 "$SCRIPT_DIR/sync_report_to_workspace.py" "$REPORT_FILE" >> "$LOG_FILE" 2>&1
    
    if [ $? -ne 0 ]; then
        echo "❌ sync_report_to_workspace.py 실행 실패" >> "$LOG_FILE"
    else
        echo "✅ 보고서 파싱 및 연동 성공" >> "$LOG_FILE"
    fi
else
    echo "⚠️ 통합보고서를 찾을 수 없습니다: $REPORT_FILE" >> "$LOG_FILE"
fi

echo "✅ J-Hub Daily Sync Finished at $(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

echo "J-Hub 데이터 동기화가 완료되었습니다. 로그: $LOG_FILE"
