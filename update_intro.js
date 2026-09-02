const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldText = "26년간 신발 밑창이 닳도록 뛰어다니며, 스스로가 누구인지 끊임없이 자문했던 시간의 흔적입니다.";
const newText = "26년간 묵묵히 설계실을 지키며 건축 설계 한 길만을 걸어온, 그래서 건축 외의 모든 것에는 낯설어하며 마치 지구에 사는 외계인처럼 되어버린 지난 시간들의 흔적입니다.";

for (let p of bookData.pages) {
    if (p.text && p.text.includes(oldText)) {
        p.text = p.text.replace(oldText, newText);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated intro text.");
