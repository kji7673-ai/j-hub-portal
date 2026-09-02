const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `요즘 난 잠을 잘 수가 없다.<br><br>눈을 감으면,<br>나의 모든 감각 기관이 더욱 예민해진다.<br>어느 날은 자고 있는 상태에서도<br>내 옆에 기어가는 벌레를 인지하고 잡은 적도 있다.<br><br>심지어<br><br>난 눈을 뜨고 잔다.<br>자고 있는 나에게 말을 붙이면 대답을 한다.<br><br>군에서는<br>선임들이 내 머리카락만 건드려도 관등성명을 댄다고 모두들 신기해했지만,<br>사실 난 자면서도 그들의 모든 일거수일투족을 인지하고 있었다.<br><br>나의 이 능력은 사실 지네에게 물렸을 때 생긴 능력이다.<br><br>거미에 물렸다면 스파이더맨이 될 수도 있었는데 아깝다.<br>아무튼,<br>난 지네맨이 되었다.<br><br>지네가 가진 예민한 촉각을 내가 가지게 된 것이다.<br>몹시 예민하다.<br>이런 능력을 가진 후 몇 가지 단점도 생겼다.<br><br>첫째는, 밤에 예민하다 보니 낮에 몹시 둔하다는 것이다.<br>말도 행동도 느리고, 쉽게 다른 사람의 말을 알아듣지도 못하게 되었다.<br>둘째, 너무 많은 정보가 내게 쏟아져 들어온다. 주변의 모든 정보가.<br>그래서, 난 더 둔해진다. 화를 낼 일도 한참 나중에 되어서야 '아! 그때 화를 냈어야 했는데' 하고 후회하곤 한다.<br><br>결국 난 몹시 예민하지만, 몹시도 둔한 사람이 되었다.<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">어떨 땐 너무 둔하고, 또 어떨 땐 너무 예민하게 신경이 곤두서서 나도 모르게 손발이 떨릴 때가 있다. 긴장해서 말마저 더듬거릴 때면, 나는 속으로 중얼거린다. '그래, 나는 지네맨이었지. 아니면 지구에 불시착한 외계인이거나.' 그렇게 나 스스로를 세뇌하며 버텨낸다. 참 하루하루가 고단하고 쉽지 않다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "요즘 잠을 잘 수가 없다") {
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Formatted centipede essay.");
