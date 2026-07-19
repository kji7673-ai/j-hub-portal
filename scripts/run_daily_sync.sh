#!/bin/bash
# run_daily_sync.sh
# J-Hub 포털 데이터 연동 자동화 파이프라인 (v2.0 — 법규 크롤러 + 주간보고서 파서 통합)

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH
export LANG=ko_KR.UTF-8

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/../data/sync.log"

echo "==========================================" >> "$LOG_FILE"
echo "🔄 J-Hub Daily Sync v2.0 Started at $(date)" >> "$LOG_FILE"

# ======================================================
# STEP 1: 법규/정책 동향 자동 크롤링 (NEW)
# ======================================================
echo "[1/6] 법규/정책 동향 크롤링 중..."
python3 "$SCRIPT_DIR/crawl_law_updates.py" --days 14 >> "$LOG_FILE" 2>&1
LAW_RC=$?

if [ $LAW_RC -ne 0 ]; then
    echo "❌ crawl_law_updates.py 실패 (exit: $LAW_RC)" >> "$LOG_FILE"
else
    echo "✅ 법규 크롤링 성공" >> "$LOG_FILE"
fi

# ======================================================
# STEP 2: 주간 보고서 파싱 → 본부별 현황 + 일정 갱신 (NEW)
# ======================================================
REPORT_FILE=$(ls -t "$SCRIPT_DIR/../reports/"*주간\ 보고.html 2>/dev/null | head -n 1)

echo "[2/6] 주간 보고서 파싱 중..."
if [ -f "$REPORT_FILE" ]; then
    python3 "$SCRIPT_DIR/parse_weekly_report.py" "$REPORT_FILE" >> "$LOG_FILE" 2>&1
    PARSE_RC=$?
    
    if [ $PARSE_RC -ne 0 ]; then
        echo "❌ parse_weekly_report.py 실패 (exit: $PARSE_RC)" >> "$LOG_FILE"
    else
        echo "✅ 주간 보고서 파싱 성공: $(basename "$REPORT_FILE")" >> "$LOG_FILE"
    fi
else
    echo "⚠️ 주간 보고서 미발견 — 건너뜀" >> "$LOG_FILE"
fi

# ======================================================
# STEP 3: 서울시 정보몽땅 API 연동
# ======================================================
SEOUL_API_KEY="${SEOUL_API_KEY:-}"

echo "[3/6] 서울시 공고 연동 중..."
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

# ======================================================
# STEP 4: 100선 시사 기사 크롤링
# ======================================================
echo "[4/6] 시사 기사 100선 크롤링 중..."
python3 "$SCRIPT_DIR/pipeline_daily.py" >> "$LOG_FILE" 2>&1
DAILY_RC=$?

if [ $DAILY_RC -ne 0 ]; then
    echo "❌ pipeline_daily.py 실행 실패 (exit: $DAILY_RC)" >> "$LOG_FILE"
else
    echo "✅ 기사 100건 수집 성공" >> "$LOG_FILE"
fi

# ======================================================
# STEP 5: 기사 컴파일
# ======================================================
echo "[5/6] 기사 컴파일 중..."
python3 "$SCRIPT_DIR/compile_articles.py" >> "$LOG_FILE" 2>&1
COMPILE_RC=$?

if [ $COMPILE_RC -ne 0 ]; then
    echo "❌ compile_articles.py 실패 (exit: $COMPILE_RC)" >> "$LOG_FILE"
else
    echo "✅ 기사 컴파일 성공" >> "$LOG_FILE"
fi

# ======================================================
# STEP 6: 최종 빌드 (index.html 재생성)
# ======================================================
echo "[6/6] index.html 재빌드 중..."
python3 "$SCRIPT_DIR/../build_jhub.py" >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ build_jhub.py 실패" >> "$LOG_FILE"
else
    echo "✅ 재빌드 성공" >> "$LOG_FILE"
fi

# ======================================================
# 결과 요약
# ======================================================
echo "" >> "$LOG_FILE"
echo "📊 파이프라인 결과 요약:" >> "$LOG_FILE"
echo "   법규 크롤링: $([ $LAW_RC -eq 0 ] && echo '✅' || echo '❌')" >> "$LOG_FILE"
echo "   주간보고서:  $([ -f "$REPORT_FILE" ] && echo "$([ ${PARSE_RC:-1} -eq 0 ] && echo '✅' || echo '❌')" || echo '⏭️ 건너뜀')" >> "$LOG_FILE"
echo "   기사 100선:  $([ $DAILY_RC -eq 0 ] && echo '✅' || echo '❌')" >> "$LOG_FILE"
echo "   기사 컴파일: $([ $COMPILE_RC -eq 0 ] && echo '✅' || echo '❌')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "✅ J-Hub Daily Sync v2.0 Finished at $(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

echo "J-Hub 데이터 동기화가 완료되었습니다. 로그: $LOG_FILE"
