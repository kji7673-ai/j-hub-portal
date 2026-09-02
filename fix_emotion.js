const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `슬프다 아프다의 감정에 <br>칼을 댄다 <br><br>아픈건 몸이 아플때 슬픈건 맘이 아플때 <br>근데 이건 슬프지만, 슬픈게 아니다 <br>그냥 서글픈 것이지 <br>그래 잠시 관계속에서 짓눌린거다 <br><br>이런 것을 슬프다라고 생각하지말자 <br><br>칼을 대어 도려내자 잘게 잘게 해체하여 형체를 없애자 <br>사실이란 덩어리만 남아있도록 <br><br>그렇게 감정에 칼을 대자<br><br>사실이란 덩어리만 덩그러니 남도록<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">요즘 만난 사람중에 매우 낯선 표현을 한 친구가 있다. "기저귀차고 마이크에 노래 부르는 사람이 있다" 이게 무슨 말일까 곰곰히 생각해보니, 미성숙한 사람이 자기 기분에 마이크 잡아 말을 하는것을 이렇게 비유했구나 싶다. 참으로 신랄한 표현이다. 나도 혹시 기저귀 차고 다 돌아다니는 것은 아닌지 조심해야겠다.</div>`;

for (let p of bookData.pages) {
    if (p.title === "감정 쪼개기") {
        p.title = "잘게 잘게 나누어 버리자";
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated 감정 쪼개기");
