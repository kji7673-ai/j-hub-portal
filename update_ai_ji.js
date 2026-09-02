const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldTitle = "무제";
const oldTextSnippet = "결국 AI는 우리의 '생각'을 지배하거나 대체하는 것이 아니다.";
const oldTextEnd = "그것이 바로 미래의 건축이다.";

const newReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">외로움을 타지 않는 네가, 창작의 괴로움에 밤을 새워본 적 없는 네가, 이 유한한 삶의 시간을 온몸으로 견뎌오지 않은 네가 과연 인간을 위한 공간을 '설계'할 수 있을까.<br><br>설계는 결코 차가운 수치의 조합이 아니다. 공간에 깃드는 것은 결국 그 공간을 치열하게 빚어낸 사람의 온도이기 때문이다.</div>`;

for (let p of bookData.pages) {
    if (p.title === oldTitle && p.text && p.text.includes(oldTextSnippet)) {
        p.title = "AI, 그래 넌 AI고 난 JI다";
        p.text = p.text.replace(oldTextEnd, oldTextEnd + '\n\n' + newReflection);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated AI vs JI.");
