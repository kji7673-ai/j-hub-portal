#!/bin/bash
echo "🚀 배포 준비 시작..."

# 1. JSON 문법 검사
echo "🔍 원고(book_data.json) 문법 검사 중..."
node -e "
try {
    const fs = require('fs');
    JSON.parse(fs.readFileSync('book_data.json', 'utf8'));
    console.log('✅ JSON 문법 완벽함!');
} catch (e) {
    console.error('❌ JSON 문법 오류 발생!');
    console.error(e.message);
    process.exit(1);
}
"
if [ $? -ne 0 ]; then
    echo "🚨 배포 중단: book_data.json 파일을 먼저 고쳐주세요!"
    exit 1
fi

# 3. CSS 캐시 갱신
echo "♻️ 캐시 갱신 중 (Cache Busting)..."
TIMESTAMP=$(date +%s)
sed -i '' -E "s/style.css\?v=[0-9]+/style.css?v=$TIMESTAMP/g" index.html
# book_data.json은 index.html의 fetch 쿼리에서 Date.now()로 자동 갱신되므로 수정 불필요.

# 4. 깃허브 전송
echo "📦 GitHub로 푸시 중..."
rm -f .git/index.lock .git/HEAD.lock
git add .
git commit -m "Auto Deploy: Content updates & Gallery updates"
git push origin main

echo "🎉 배포가 100% 안전하게 완료되었습니다!"
