const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldText = "누구에게 보여줄 것도, 누구에게 들려줄 것도 아닌 나만 아는 가장 작은 생존 신고.\n힘내자. 그 한 줄로 오늘도 다시 시작한다. 모두 힘내어요.";

const newReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">참 이상한 일이다. 현재의 나는 오히려 예전보다 더 잦은 빈도로 스스로에게 '힘내자'라고 되뇌고 있다.<br><br>나이가 들고 경력이 쌓이면 이 자기 암시에서 조금은 자유로워질 줄 알았건만, 도대체 왜 아직도 스스로를 세뇌하듯 '힘내자'는 말을 중얼거리지 않으면 안 되는 걸까. 요즘은 유독 가슴 한구석이 무겁다. 그래도 어쩌겠는가. 내일의 낯선 도면을 또 마주하기 위해, 나는 오늘도 억척스럽게 힘을 내어야만 한다.</div>`;

for (let p of bookData.pages) {
    if (p.text && p.text.includes(oldText)) {
        p.text = p.text.replace(oldText, oldText + '\n\n' + newReflection);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended himnaeja reflection.");
