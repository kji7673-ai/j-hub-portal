const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `고상하다는 것은 <br>부끄러워할 줄 안다는 것이며,<br><br>명예롭다는 것은 <br>거래할 수 없다는 것이며, <br><br>위엄이 있다는것은 <br>살기위한 술수를 부리지않는다는 것이다 <br><br>마을 버스 정류장에 거울이 달려있다 <br>누군가 친절하게 나무 받침을 만들고 <br>그 위에 반원형 거울을 달아 놓았다 <br><br>버스에 앉아 창 밖 떡집을 지날 때면 <br>바삐 손을 움직이며, 함께하는 부부의 모습을 가만히 본다 <br><br>가족과 한동안 떨어져 홀로있는 아비에게 <br>전화로 잘못했다 흐느끼는 아들과 <br>그런 아들을 토닥였다는 아비의 글을 본다 <br><br>오늘 하루가 <br>고맙다 <br>그리고 감사한 일이다<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">현재를 살아가야 겠다. 현재 내 눈에 보이는 것 내가 만나는 사람과 풍경에 감정을 담자 그러면 될것 같다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "고상하다는 것은 부끄러워한다는 것이며,") {
        p.title = "고상하다는 것은";
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 고상하다는 것은");
