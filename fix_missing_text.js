const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === "공유 결합: 사람을 향한 건축, 용산 현장의 기억") {
        if (!p.text.includes("현장을 둘러보고 인근에서 함께 식사하며")) {
            p.text += "\n\n현장을 둘러보고 인근에서 함께 식사하며 우리는 자연스럽게 서로의 느낌을 나누었습니다. '이렇게 단차가 심한 지형에서 수십 년간 불편을 겪으셨을 분들을 위해 제로 레벨(Zero Level), 즉 평탄한 지형을 최대한 만들어 보자.' 그렇게 우리의 진심을 모아 '서경연화'라는 이름으로 계획안을 제출했습니다.";
        }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
