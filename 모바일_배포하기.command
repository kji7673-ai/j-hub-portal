#!/bin/bash
echo "================================================="
echo "   진양엔지니어링 교육 플랫폼 자동 배포 시스템   "
echo "================================================="
cd "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼"

echo "🛠️ 1. 변경된 내용을 모바일용 웹사이트로 변환 중 (새 아키텍처 적용)..."
python3 generate_apple_static.py

echo "📂 2. 배포 서버(j-hub-portal)로 파일 복사 중..."
rm -rf "/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/edu"
# 외부 공개용(docs_apple) 버전을 GitHub Pages에 배포
cp -r docs_apple "/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/edu"

echo "🚀 3. GitHub 글로벌 서버로 전송 중..."
cd "/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal"
git add edu/
git commit -m "교육 플랫폼 업데이트: $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo "================================================="
echo "✅ 배포가 성공적으로 완료되었습니다!"
echo "👉 약 1~2분 뒤 https://kji7673-ai.github.io/j-hub-portal/edu/ 에 반영됩니다."
echo "이 창을 닫으셔도 됩니다."
echo "================================================="
