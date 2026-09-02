const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

for (let p of bookData.pages) {
    if (p.title) {
        // If it's a continued page, just remove the title so it flows naturally
        if (p.title.includes('(계속)')) {
            p.title = "";
            continue;
        }
        
        // Clean up [도입] and [성찰] tags
        if (p.title.includes('[도입] 테마')) {
            let m = p.title.match(/"(.*)"/);
            if (m) {
                p.title = m[1]; // Extract the inner quoted string, e.g. 공유결합의 첫 질문
            }
        } else if (p.title.includes('[성찰')) {
            // [성찰 3-2] 깊어지는 질문들 -> 깊어지는 질문들
            // [성찰 3] 결론을 향하여: "내+상대+현장이 만날 때" -> 결론을 향하여
            p.title = p.title.replace(/\[성찰[^\]]*\]\s*/, '');
            // If it has quotes after colon, maybe keep it or strip it. Let's just strip the tag.
        } else if (p.title.includes('[최종 성찰]')) {
            p.title = p.title.replace(/\[최종 성찰\]\s*/, '');
        }
    }
}

const newCode = `const bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', newCode, 'utf8');
console.log("Cleaned up titles");
