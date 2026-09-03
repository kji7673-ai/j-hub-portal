const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newPage = {
    title: "다정한 디자인",
    partCategory: "제 2 부. 현장의 목소리 - 조율의 기술",
    type: "text",
    text: `<p style="text-align: center; line-height: 2.2; font-size: 1.1em; color: #333; margin-top: 40px; margin-bottom: 60px;">
디자인은 어디서 나오는 것일까요?<br>
감각이나 방대한 지식에서 나오는 것일까요?<br><br>

내가 생각하는 디자인은 결국 본인의 인격적 성숙에서 나옵니다.<br><br>

타인에 대한 배려와 관심,<br>
다정함이 있는 사람이라면<br>
그것이 자연스레 공간에 묻어납니다.<br><br>

건물을 청소하는 분, 택배 기사님, 기존 지역 주민,<br>
그리고 바람과 조망에 대한 깊은 공감이 있을 때<br>
진짜 설계가 나옵니다.<br>
거창한 논리보다 먼저 다정한 사람이 되시길 바랍니다.<br><br>

다정한 디자인
</p>

<blockquote>
예전 첫 직장에서 소장님께 계획안을 보여 드렸을 때, 들었던 이야기입니다. 설계하는 것을 보면 마음이 보인다고, 마음을 넓히라고... 그때 그 말에 참 부끄러웠습니다.
</blockquote>`
};

let insertIndex = bookData.pages.findIndex(p => p.title && p.title.includes('양팔에 낀 토시'));
if (insertIndex !== -1) {
    bookData.pages.splice(insertIndex + 1, 0, newPage);
    console.log("Inserted after '양팔에 낀 토시'");
} else {
    bookData.pages.splice(40, 0, newPage);
    console.log("Inserted at index 40");
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
