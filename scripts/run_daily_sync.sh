#!/bin/bash
# run_daily_sync.sh
# J-Hub 포털 데이터 연동 자동화 파이프라인

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH
export LANG=ko_KR.UTF-8

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/../data/sync.log"

echo "==========================================" >> "$LOG_FILE"
echo "🔄 J-Hub Daily Sync Started at $(date)" >> "$LOG_FILE"

# EXT-01 FIX: 환경변수에서 API Key 읽기
SEOUL_API_KEY="${SEOUL_API_KEY:-}"

echo "[1/4] 서울시 공고 연동 중..."
if [ -n "$SEOUL_API_KEY" ]; then
    python3 "$SCRIPT_DIR/update_workspace_api.py" "$SEOUL_API_KEY" >> "$LOG_FILE" 2>&1
else
    echo "⚠️ SEOUL_API_KEY 미설정 - 더미 데이터 사용" >> "$LOG_FILE"
    python3 "$SCRIPT_DIR/update_workspace_api.py" >> "$LOG_FILE" 2>&1
fi

if [ $? -ne 0 ]; then
    echo "❌ update_workspace_api.py 실행 실패" >> "$LOG_FILE"
else
    echo "✅ 서울시 연동 성공" >> "$LOG_FILE"
fi

# 2. 통합검토보고서 데이터 파싱 및 workspace.json 주입
REPORT_FILE=$(ls -t "$SCRIPT_DIR/../reports/"*주간\ 보고.html 2>/dev/null | head -n 1)

if [ -f "$REPORT_FILE" ]; then
    echo "[2/3] 통합보고서 파싱 중: $REPORT_FILE"
    python3 "$SCRIPT_DIR/sync_report_to_workspace.py" "$REPORT_FILE" >> "$LOG_FILE" 2>&1
    
    if [ $? -ne 0 ]; then
        echo "❌ sync_report_to_workspace.py 실행 실패" >> "$LOG_FILE"
    else
        echo "✅ 보고서 파싱 및 연동 성공" >> "$LOG_FILE"
    fi
else
    echo "⚠️ 통합보고서를 찾을 수 없습니다: $REPORT_FILE" >> "$LOG_FILE"
fi

# 3. 기사 생성 파이프라인 연동 (AUTO-02 FIX: 개별 exit code 확인)
echo "[3/4] 시사 기사 동기화 중..."
python3 "$SCRIPT_DIR/pipeline_daily.py" >> "$LOG_FILE" 2>&1
DAILY_RC=$?

python3 "$SCRIPT_DIR/compile_articles.py" >> "$LOG_FILE" 2>&1
COMPILE_RC=$?

if [ $DAILY_RC -ne 0 ]; then
    echo "❌ pipeline_daily.py 실행 실패 (exit code: $DAILY_RC)" >> "$LOG_FILE"
else
    echo "✅ 기사 수집 성공" >> "$LOG_FILE"
fi

if [ $COMPILE_RC -ne 0 ]; then
    echo "❌ compile_articles.py 실패 (exit code: $COMPILE_RC)" >> "$LOG_FILE"
else
    echo "✅ 기사 컴파일 성공" >> "$LOG_FILE"
fi

# 4. 최종 빌드 (AUTO-04 FIX: workspace 갱신 후 재빌드 보장)
echo "[4/4] index.html 재빌드 중..."
python3 "$SCRIPT_DIR/../build_jhub.py" >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ build_jhub.py 실패" >> "$LOG_FILE"
else
    echo "✅ 재빌드 성공" >> "$LOG_FILE"
fi

echo "✅ J-Hub Daily Sync Finished at $(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

echo "J-Hub 데이터 동기화가 완료되었습니다. 로그: $LOG_FILE"
