const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === '질문의 확장: "그렇다면 상대는 어떤가?"') {
        p.text = `<p style="margin-bottom: 24px;">이해관계가 얽히고설킨 흙먼지 날리는 현장에서, 중심을 잡고 공유결합을 이끌어낼 '조율자'로서의 기준을 세웠습니다.</p>

<p style="margin-bottom: 24px;">→ 그렇다면 다음 질문은 자연스럽게 이어집니다.</p>

<p style="font-size: 1.1em; font-weight: 600; color: #1d1d1f; margin-bottom: 24px;">"조율자로서의 기준을 세웠으니, 이제 현장에서 나와 사사건건 부딪히며 충돌을 만들어내는 저 상대(시공사, 관공서, 조합 등)들은 도대체 어떤 집단인가?"</p>

<p style="margin-bottom: 24px;">건축가가 아무리 고상한 철학과 완벽한 기준을 품고 있다 한들, 날것의 욕망을 품고 움직이는 이 현실의 집단들을 직시하지 못한다면, 우리의 도면은 결국 종이 쪼가리 위의 몽상으로 끝나고 말 것입니다.</p>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
