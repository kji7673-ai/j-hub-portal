const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `자신이 거짓인지 모른 상태에서, <br>진실을 만남으로 자신의 거짓됨을 알게된 경우 <br><br>자신이 거짓인지 알고 있는 상태에서, <br>진실을 만남으로 자신의 거짓됨이 알려질 경우 <br><br>스스로는 알겠지. <br><br>자신이 살아 온 삶이 후 한번 불어버리면 <br>날아갈 만큼 가볍다는 것을<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">하루를 조금은 무겁게 살아가자<br>쉽게 날아가버리는 하루의 삶이 되지 않도록</div>`;

for (let p of bookData.pages) {
    if (p.title === "거짓이 진실을 만났을 때") {
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 거짓이 진실을 만났을 때");
