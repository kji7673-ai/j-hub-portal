const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText = `전 둔한 사람입니다.<br>어떤 이는<br>침착하다고 말하지만,<br><br>사실 몸도 마음도 둔하여<br>슬픔과 기쁨에 바로 반응하지 못하기 때문입니다.<br><br>둔하다는 것은 어떤 순간에는 좋을 때도 있으나,<br><br>보통의 경우는<br>이상한 인간이 되어, 외톨이처럼 혼자만의 시간에 멍하니 있습니다.<br><br>이미 지나간 것들이<br>지금 이 시간에 슬픔과 후회로 찾아오기에<br><br>다른 이는 현재의 시간인데<br>나에게는 한 박자씩 늦는 과거의 시간이 현재인 것입니다.<br><br>현재 기쁨의 순간에<br>찾아온 과거의 슬픔에<br><br>난 어느 시점에 나의 중심을 둘지 몰라<br><br>그냥 멍하니 있습니다.<br><br>
<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">"제발, 이상한 인간만은 되지 말자."<br><br>겉으로는 무던한 척하지만, 속으로는 늘 남들보다 한 박자 늦게 도착하는 감정의 시차 때문에 속을 끓인다. 기뻐야 할 때 온전히 기뻐하지 못하고, 슬퍼야 할 때 울지 못해 뒤늦게 혼자 앓는 나 같은 '감정의 시차 부적응자'들이 세상엔 또 얼마나 많을까. 부디 나뿐만 아니라, 이 속도 빠른 세상에서 한 박자 늦게 걷는 모든 이들이 스스로를 너무 '이상한 사람'으로 여기며 자책하지 않았으면 좋겠다.</div>
<div style="margin-top: 40px;">
    <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 24px; color: #1d1d1f; text-align: center;">[조형물] 한 박자 늦게 걷는 사람</h4>
    <img src="static/images/dull_1.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/dull_2.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
</div>`;

for (let p of bookData.pages) {
    if (p.title === "난 슬픔과 기쁨에 반응이 둔한편이다") {
        p.title = "난 둔한 사람입니다";
        p.text = newText;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Properly formatted dull essay.");
