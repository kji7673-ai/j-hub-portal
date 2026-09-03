const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// Let's standardise the three poetic essays: "구겨진 도면", "양팔에 낀 토시", "다정한 디자인"
bookData.pages.forEach(p => {
    if (p.title && (p.title.includes('구겨진 도면') || p.title.includes('양팔에 낀 토시') || p.title.includes('다정한 디자인'))) {
        
        let textLines = '';
        let authorNote = '';
        
        if (p.title.includes('다정한 디자인')) {
            textLines = `디자인은 어디서 나오는 것일까요?<br>감각이나 방대한 지식에서 나오는 것일까요?<br><br>내가 생각하는 디자인은 결국 본인의 인격적 성숙에서 나옵니다.<br><br>타인에 대한 배려와 관심,<br>다정함이 있는 사람이라면<br>그것이 자연스레 공간에 묻어납니다.<br><br>건물을 청소하는 분, 택배 기사님, 기존 지역 주민,<br>그리고 바람과 조망에 대한 깊은 공감이 있을 때<br>진짜 설계가 나옵니다.<br>거창한 논리보다 먼저 다정한 사람이 되시길 바랍니다.<br><br>다정한 디자인`;
            authorNote = `예전 첫 직장에서 소장님께 계획안을 보여 드렸을 때, 들었던 이야기입니다. 설계하는 것을 보면 마음이 보인다고, 마음을 넓히라고... 그때 그 말에 참 부끄러웠습니다.`;
        } else if (p.title.includes('양팔에 낀 토시')) {
            textLines = `지금 사람들은 이해하기 어렵겠지만,<br>연필로 설계할 때면 팔뚝이 흑연으로 인해 새카맣게 되곤 해서<br>양팔에 토시를 낍니다.<br><br>어느 날<br>회사 임원 분 중에 한 분이<br>넌<br>그 토시를 벗지 않는 한<br><br>평생 남들 설계만 해줄 거라며,<br>빨리 그놈의 토시부터 벗어 버리란 이야기를 했었습니다.<br><br>아마도 설계만이 아닌 기획과 영업 능력을 키우란 말이겠지요.<br>근데, 전 아직도 토시를 벗기에는 모르는 게 너무 많습니다.<br>예전 첫 직장에서 화장실 하나로 일주일을 밤새 고민하던 그 시절이 그립습니다.`;
            authorNote = `전 아직도 설계를 하고 싶습니다. 회의 테이블 위에서의 차가운 숫자 놀음이 아닌... 흑연이 묻어나는 진짜 설계를 말입니다.`;
        } else if (p.title.includes('구겨진 도면')) {
            textLines = `손안에서<br>이리저리 움직여 본다.<br><br>바스락거리며<br>내 손의 움직임 따라<br>나를 간지럽히며, 내는 소리,<br>내 손안에 거미줄 치듯 작은 상처로 내게 말을 걸지만.<br><br>여리디여린 너는 원래 그랬던 것처럼,<br>이리저리 희롱당한 것을 오히려 자랑하듯<br><br>수없이 반짝이는 조각을 자랑하듯.<br>그렇게 그렇게 구겨져<br><br>결국엔 버려지는구나.`;
            authorNote = `사실 이 글은, 어느 날 손안에 남은 얇은 사탕 포장지를 이리저리 쥐었다 폈다 하며 썼던 글입니다. 구겨지고 상처 입으면서도 반짝이는 그 종이 쪼가리가, 어쩌면 나란 사람과 참 닮아있구나 싶어 씁쓸함을 삼켰던 기억이 납니다.`;
        }
        
        p.text = `<div style="text-align: center; max-width: 500px; margin: 0 auto;">
<p style="text-align: left; line-height: 2.2; font-size: 1.1em; color: #333; margin-top: 40px; margin-bottom: 60px; display: inline-block;">
${textLines}
</p>
</div>

<blockquote style="background: rgba(0, 0, 0, 0.04); border-radius: 8px; padding: 20px 24px; font-size: 0.9em; color: #555; line-height: 1.6; border: none; margin-top: 40px;">
${authorNote}
</blockquote>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
