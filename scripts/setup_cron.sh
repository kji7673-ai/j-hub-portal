#!/bin/bash
# setup_cron.sh
# J-Hub 포털 데이터 동기화 파이프라인(run_daily_sync.sh)을 
# Mac OS Crontab 스케줄러에 등록하는 인스톨러 스크립트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/run_daily_sync.sh"

echo "=========================================="
echo "🕒 J-Hub Crontab 스케줄러 인스톨러"
echo "=========================================="

# run_daily_sync.sh 실행 권한 확인 및 부여
if [ ! -x "$SYNC_SCRIPT" ]; then
    echo "🔑 $SYNC_SCRIPT 실행 권한 부여 중..."
    chmod +x "$SYNC_SCRIPT"
fi

# 기존 Crontab 백업 및 임시 파일 생성
crontab -l > mycron 2>/dev/null

# 이미 등록되어 있는지 확인
if grep -q "$SYNC_SCRIPT" mycron; then
    echo "⚠️ 이미 J-Hub 스케줄러가 등록되어 있습니다."
    echo "현재 설정 내용:"
    grep "$SYNC_SCRIPT" mycron
else
    # 평일(월~금, 1-5) 오전 8시 0분에 실행되도록 등록
    # 0 8 * * 1-5 /경로/run_daily_sync.sh
    CRON_JOB="0 8 * * 1-5 \"$SYNC_SCRIPT\""
    
    echo "$CRON_JOB" >> mycron
    crontab mycron
    
    echo "✅ 성공적으로 Crontab에 등록되었습니다!"
    echo "설정된 시간: 평일 오전 8시 00분"
    echo "실행 경로: $SYNC_SCRIPT"
fi

rm mycron

echo "=========================================="
echo "전체 Crontab 목록 확인을 원하시면 터미널에서 'crontab -l' 을 입력하세요."
