#!/bin/bash
echo "================================================="
echo "   진양엔지니어링 교육 플랫폼 자동 배포 시스템   "
echo "================================================="
cd "/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼"

echo "🛠️ 1. 변경된 내용을 모바일용 웹사이트로 변환 중 (새 아키텍처 적용)..."
python3 generate_apple_static.py
if [ $? -ne 0 ]; then
    echo "🚨 정적 사이트 빌드에 실패했습니다."
    exit 1
fi

echo "👁️ 2. J-Hub UI Auto-Healer 시각적 감리 진행 중..."
python3 scripts/ui_auto_healer.py
if [ $? -ne 0 ]; then
    echo "🚨 [치명적 오류] 시각적 감리(Auto-Healer)에 실패했습니다!"
    echo "   -> 터미널 로그를 확인하고 UI 결함을 수정한 뒤 다시 배포하십시오."
    exit 1
fi

echo "🚀 3. GitHub 글로벌 서버로 전송 중..."
echo "📦 3.1 GitHub Pages 배포용 docs 및 edu 폴더 동기화..."
rm -rf docs
cp -r docs_apple docs
rm -rf edu
cp -r docs_apple edu

git add .
git commit -m "교육 플랫폼 업데이트 (Auto-Healer 감리 통과): $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo "================================================="
echo "✅ 배포가 성공적으로 완료되었습니다!"
echo "👉 약 1~2분 뒤 https://kji7673-ai.github.io/j-hub-portal/ 에 반영됩니다."
echo "이 창을 닫으셔도 됩니다."
echo "================================================="
