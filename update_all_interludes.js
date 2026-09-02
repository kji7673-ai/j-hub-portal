const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.type === "interlude") {
        if (p.title === "2부. 현장의 목소리, 공유결합의 증거") {
            p.image = "static/images/interlude_part2.jpg";
        } else if (p.title === "부록 A. J-Hub 기술 개요") {
            p.image = "static/images/interlude_appendix_a.jpg";
        } else if (p.title === "부록 B. 자기 조직 진단 체크리스트") {
            p.image = "static/images/interlude_appendix_b.jpg";
        } else if (p.title === "부록 C. 생각을 명확히 하는 법 (마스터 프롬프트)") {
            p.image = "static/images/interlude_appendix_c.jpg";
        }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
