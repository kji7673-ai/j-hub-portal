const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title && p.title.includes('구겨진 도면')) {
        p.text = `<p style="text-align: center; line-height: 2.2; font-size: 1.1em; color: #333; margin-top: 40px; margin-bottom: 60px;">
손안에서<br>
이리저리 움직여 본다.<br><br>

바스락거리며<br>
내 손의 움직임 따라<br>
나를 간지럽히며, 내는 소리,<br>
내 손안에 거미줄 치듯 작은 상처로 내게 말을 걸지만.<br><br>

여리디여린 너는 원래 그랬던 것처럼,<br>
이리저리 희롱당한 것을 오히려 자랑하듯<br><br>

수없이 반짝이는 조각을 자랑하듯.<br>
그렇게 그렇게 구겨져<br><br>

결국엔 버려지는구나.
</p>

<blockquote>
<strong>[저자의 메모]</strong><br>
사실 이 글은, 어느 날 손안에 남은 얇은 사탕 포장지를 이리저리 쥐었다 폈다 하며 썼던 글입니다. 구겨지고 상처 입으면서도 반짝이는 그 종이 쪼가리가, 어쩌면 나란 사람과 참 닮아있구나 싶어 씁쓸함을 삼켰던 기억이 납니다.
</blockquote>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
