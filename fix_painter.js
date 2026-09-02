const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `그래 <br>그래도 <br>난 붓을 놓을 수가 없다. <br><br>내 속을 <br>채운 체액이 <br>한 방울도 남김없이 다 빠져나가고, <br>그곳에 또다시 피 섞인 다른 것으로 나를 채우고 비워내며, <br><br>나를 닮은 것을 세상에 다시한번 내어놓는다. <br><br>곧 발가벗겨진 채 이리저리 돌려보는 그들의 눈초리에 <br>난 부끄러워 할것이고, <br><br>그 기억에 <br>밤새 뜬눈으로 지새울 것이다.<br><br>미워도 다시한번이 아닌 <br>그래도 다시한번 힘내어 본다.<br><br>그래<br>그렇지<br>나는 쟁이이다. <br><br>이것을 놓는 순간 <br>다시는 붓을 들 수 없을 것이라는 것을 알기에,<br><br>아련한 추억 속에서<br> '내가 그때 그 길을 계속 걸었다면' 하는 후회로 살아가기엔 <br><br>아직은 이른 것 같다. <br><br>그래, 또다시 붓을 들어 <br>나를 다듬어간다.<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">아직까지도 매번 하는 설계가 또 언제나 돌아오는 현상설계(수많은 건축가가 사활을 걸고 디자인 경쟁을 펼쳐 단 하나의 당선작을 뽑는 건축 공모전)를 시작한다는 것에 몹시도 망설여지고 피하고 싶은 마음과, 발가벗겨질 것이라는 두려움이 교차한다. 어린 후배들은 더 하겠지요. 자신의 실력과 능력이 시험받는 느낌을 받을 것이고, 어딘가로 훌쩍 숨고 싶을 것이다.<br><br>그래도 한참 선배로서 말해주고 싶은 것은, 두려워하지 말라는 것이다. 포기하지만 않는다면 잘 할 수 있다. 그렇게 말해 주고싶다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "쟁이의 마음: 두려움을 넘어 다시 붓을 드는 이유") {
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 쟁이의 마음");
