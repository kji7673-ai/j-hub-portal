const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title && p.title.includes('공유결합의 세 가지 질문')) {
        p.text = "설계는 단지 도면을 그리는 행위가 아닙니다. 그것은 '조율자로서의 확고한 기준'을 세우고, '서로 다른 이들의 투박한 언어를 둥글게 이해'하며, 욕망이 격돌하는 '현장(회의 테이블)의 이면'을 꿰뚫어 보는 세 가지 철학에서 출발합니다. 이 세 가지가 하나로 만날 때 비로소 가장 흔들림 없는, 단단한 '공유결합'과 같은 신뢰가 구축됩니다.";
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
