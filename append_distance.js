const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldTextSnippet = "상대와 내가 없는 것처럼 그렇게<br>우리가 이렇게 살아갑니다";

const newReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">적당히 떨어져 있어야 하는데, 우리는 너무 빽빽하게 붙어 있다 보니 외려 문을 굳게 닫고 살아간다. 옆 동 사람과는 쉽게 친해져도 바로 벽 하나를 맞댄 옆 호 사람과는 눈조차 마주치기 어려운 것이 우리의 현실이다.<br><br>설계하는 사람들 중 간혹 개인의 '절대적인 자기 영역'에 대한 이해가 부족한 경우를 본다. 그들은 사람들이 모이기를 기대하며 예쁜 공용 공간을 널찍하게 그려 넣지만, 실상 그곳은 언제나 텅 비어 있다. 좁은 복도에서 이웃과 마주치면 반갑게 인사할 것이라 상상하지만, 사람들은 고개를 푹 숙인 채 그저 그 뻘쭘한 찰나가 빨리 지나가기만을 바란다. 인간이란 원래 그런 존재다. 바라봄을 위한 최소한의 '떨어짐(거리)'이 확보되지 않으면, 인간은 결코 타인에게 다가가지 못한다.</div>`;

for (let p of bookData.pages) {
    if (p.title === '우리가 이렇게 살아갑니다' && p.text && p.text.includes(oldTextSnippet)) {
        p.text = p.text.replace(oldTextSnippet, oldTextSnippet + '\n\n' + newReflection);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended distance reflection.");
