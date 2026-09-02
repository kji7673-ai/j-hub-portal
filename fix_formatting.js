const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

for (let p of bookData.pages) {
    // 1. Fix Titles with brackets
    if (p.title) {
        p.title = p.title.replace(/\[2부 시작\]\s*/g, '');
        p.title = p.title.replace(/\[3부 시작\]\s*/g, '');
        p.title = p.title.replace(/\[부록 A\]\s*/g, '부록 A. ');
        p.title = p.title.replace(/\[부록 B\]\s*/g, '부록 B. ');
        p.title = p.title.replace(/\[부록 C\]\s*/g, '부록 C. ');
    }

    // 2. Fix Text occurrences of brackets
    if (p.text) {
        // Fix field sketches
        p.text = p.text.replace(/<b>\[현장 스케치:\s*(.*?)\]<\/b>/g, '<br><strong style="color: var(--primary);">현장 스케치: $1</strong><br>');
        p.text = p.text.replace(/\[현장 스케치:\s*(.*?)\]/g, '<strong style="color: var(--primary);">현장 스케치: $1</strong>');
        
        // Fix AI log title
        p.text = p.text.replace(/\[J-Hub 코어: 아키 시냅스 시스템 로그\]/g, 'J-Hub 코어: 아키 시냅스 시스템 로그');
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

// Print TOC to verify ordering
bookData.pages.forEach((p, i) => {
    console.log(`${i+1}. [${p.partCategory}] ${p.title || p.type}`);
});
