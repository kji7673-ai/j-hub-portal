const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `흔들릴지언정 넘어지지 않는, <br><br>그래서 <br>재미 삼아 툭툭 건드려도 상관없는 <br><br>난 <br>중심 잡힌 오뚝이인 줄 알았다. <br><br>근데 이젠, 작은 입김에도 휘청이며 중심 잡기 위해 <br>몹시도 흔들거리는, 아파서 흔들거리는 내가 되었다.<br><br><img src="static/images/36.jpg" alt="현장 스케치" style="width:100%; border-radius:12px; margin: 30px 0;"><br><br>세월의 흐름속에  <br>내안에 가라앉은 침잠된 무게가 중심추 되어, <br><br>이젠 <br>웬만한 바람이 불어도 <br>비록 흔들거릴지언정 넘어지지는 않는 <br>난 오뚝이 인데, <br>그래 그렇지. <br><br>내 속에 침잠된 그 묵직함이 <br>오늘의 나를 지켜준다.<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;"><strong>오늘도 사랑한다로 시작한다</strong><br><br>오늘 하루, 난 또 다른 모습으로 뭍의 삶을 살아간다. 태초의 쉼터인 물로 돌아가기 전까지 모두가 그렇게 살아간다. 특별할 것 없다. 매 맞는 말의 모습에서 메시아를 보았던 니체처럼, 언젠가 나도 이 고달픈 쟁이 삶의 끝에서 희열의 본질을 마주하겠지. 오늘도 나는 '사랑한다'는 말로 하루를 시작한다. 그리고 하루의 마지막엔, '나는 사랑했다'로 끝을 맺고 싶다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "흔들리는 오뚝이") {
        p.title = "오뚝이";
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 오뚝이");
