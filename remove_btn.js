const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 정규식으로 button 태그 부분 찾아 삭제
html = html.replace(/<button class="cover-btn"[^>]*>[\s\S]*?전시 관람 시작하기[\s\S]*?<\/button>/, '');

fs.writeFileSync('index.html', html);
console.log("Button removed.");
