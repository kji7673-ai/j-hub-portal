const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let found = false;
bookData.pages.forEach(p => {
    if (p.title && p.title.includes('양팔에 낀 토시')) {
        found = true;
        p.text = `<p style="text-align: center; line-height: 2.2; font-size: 1.1em; color: #333; margin-top: 40px; margin-bottom: 60px;">
지금 사람들은 이해하기 어렵겠지만,<br>
연필로 설계할 때면 팔뚝이 흑연으로 인해 새카맣게 되곤 해서<br>
양팔에 토시를 낍니다.<br><br>

어느 날<br>
회사 임원 분 중에 한 분이<br>
넌<br>
그 토시를 벗지 않는 한<br><br>

평생 남들 설계만 해줄 거라며,<br>
빨리 그놈의 토시부터 벗어 버리란 이야기를 했었습니다.<br><br>

아마도 설계만이 아닌 기획과 영업 능력을 키우란 말이겠지요.<br>
근데, 전 아직도 토시를 벗기에는 모르는 게 너무 많습니다.<br>
예전 첫 직장에서 화장실 하나로 일주일을 밤새 고민하던 그 시절이 그립습니다.
</p>

<blockquote>
<strong>[저자의 메모]</strong><br>
전 아직도 설계를 하고 싶습니다. 회의 테이블 위에서의 차가운 숫자 놀음이 아닌... 흑연이 묻어나는 진짜 설계를 말입니다.
</blockquote>`;
    }
});

// If the page was not found, we should probably append it to part 2, but wait, let's just see if it replaces correctly.
// I will check the log. 
if(!found) console.log("WARNING: Page '양팔에 낀 토시' not found!");

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
