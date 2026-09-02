const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">나는 오늘 하루를 온전한 '현재'로 살아가고 있는 것일까, 아니면 과거의 회상 속에 머물러 살아가고 있는 것일까. 어쩌면 미래의 죽음을 앞둔 내가 잠시 떠올린 찰나의 기억 속 한 장면은 아닐까.<br><br>멍하니 내 손가락을 꾹꾹 눌러본다. 살결의 통각이 전해진다. 그래, 환영이 아닌 현실의 삶이구나. 단순한 슬픔을 넘어, 삶이라는 것 자체가 유독 애달프게 다가오는 요즘이다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "에너지의 소진으로") {
        if (!p.text.includes('손가락을 꾹꾹')) {
            p.text = p.text + '\n\n' + newReflection;
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended death reflection.");
