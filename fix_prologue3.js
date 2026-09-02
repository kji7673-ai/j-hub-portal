const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldText = "<strong>내 아들에게 전해주고 싶은 이야기</strong>입니다.";
const newText = "<strong>내 가족들에게 전해주고 싶은 이야기</strong>입니다.";

for (let p of bookData.pages) {
    if (p.text) {
        if (p.text.includes(oldText)) {
            p.text = p.text.replace(oldText, newText);
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Prologue '가족들에게' updated.");
