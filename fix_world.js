const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `당신은 어떤 세상에 있나요?<br>당신 곁에서 <br>당신의 눈으로 세상을 바라보면 좋겠습니다. <br><br>내가 느끼지못하는 기쁨과 슬픔을 <br>당신을 통해느낄 때 <br><br>우리 서로를 이해할 수 있겠지요? <br><br>당신의 세상은 어떤가요? <br>그 속에 기쁨만이 있지는않겠지만, <br>우리 서로의 시선을 갖고 바라본다면 <br><br>그때 비로소<br>우린 <br>우리가 되겠지요 <br><br>오늘 하루 당신의 시선으로 <br>세상을 바라보는 하루 되었으면 합니다.<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">나를 이해하기위해서라도, 타인을 이해하기 위해서라도 나의 생각과 관념에서 벗어날 필요가 있는것 같습니다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "당신의 세상은 어떤가요?") {
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 당신의 세상은 어떤가요?");
