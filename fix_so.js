const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `그렇게 하실 것 같습니다. <br><br>계속 아파하실 것 같습니다 <br>그렇게 <br><br>계속 사랑하실 것 같습니다 <br>그렇게 <br><br>계속 살아가실 것 같습니다 <br><br>과연 그럴까 <br>당신은 고정된 사람아닐 것 같습니다 <br><br>다르게 살아가실 수 있습니다 <br>그렇게`;

for (let p of bookData.pages) {
    if (p.title === "그렇게 하실 것 같습니다.") {
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 그렇게 하실 것 같습니다");
