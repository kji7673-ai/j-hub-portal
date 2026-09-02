const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = "사람의 죽음을 이해하는 사람도 있고, <br>평생 먹는 음식의 량이나 숨쉬기의 횟수가 정해져있어 그 한계가 왔을 때 <br>죽음에 이른다는 사람이 있다 <br><br>내가 생각하기엔 <br>자기 인식을 한 이후 <br>본인의 과거 사건과 시간 또는 그 어떠한것에 메여, <br><br>현실의 시간에 살지못할 때 <br>오늘을 살아갈 힘을 잃게되었을 때<br><br>그때가 죽음이지 않을까?";

for (let p of bookData.pages) {
    if (p.title === "에너지의 소진으로") {
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Formatted death essay.");
