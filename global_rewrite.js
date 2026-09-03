const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    // Fix the Yongsan Episode Introduction
    if (p.title && p.title.includes('공유결합: 사람을 향한 건축, 용산 현장')) {
        p.text = p.text.replace(/첫째는 내게 무엇이 있는지 아는 것.*?생명력을 얻습니다\./s, 
            `첫째는 조율자로서 흔들리지 않는 중심(기준)을 세우는 것, 둘째는 각기 다른 사람들의 투박한 언어를 둥글게 이해하고 담아내는 것, 그리고 셋째는 눈앞의 대지뿐만 아니라 얽히고설킨 이해관계의 이면(회의 테이블)까지 꿰뚫어 보는 것입니다. 이 세 가지 공유결합의 요소가 만나 서로의 결핍을 채울 때, 건축은 비로소 단순한 구조물을 넘어 생명력을 얻게 됩니다.`);
    }

    // Check for any other lingering "자기 정체성" or "자아" in the early chapters
    if (p.title === '공유결합의 두 번째 질문: 서로 다름을 이해하는 것' || p.title === '공유결합의 세 번째 질문: 현장이라는 반응기') {
        // Just sweeping any missed old phrasings if they exist
        p.text = p.text.replace(/나 자신을 아는 것/g, '조율자로서의 기준을 세우는 것');
        p.text = p.text.replace(/나를 아는 과정/g, '중심을 잡는 과정');
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
