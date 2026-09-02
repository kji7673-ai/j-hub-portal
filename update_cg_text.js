const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldText = "경쟁하던 메이저 업체들은 주동 수를 줄여 공사비를 낮추는 경제성 논리와 흔히 볼 수 있는 뻔한 배치를 들고나왔지만, 우리 진양건축은 달랐습니다.";
const newText = "함께 작업하던 CG 담당자의 말을 빌리자면, 진양건축이 디자인에 얼마나 진심인지는 렌더링을 켜는 순간 알 수 있다며 '정말 이 곳에 살고 싶다'고 말하더군요. 입에 발린 칭찬일 수도 있겠지만, 적어도 우리 회사가 공간을 대하는 태도와 디자인에 담는 진심만큼은 온전히 전해졌다고 믿습니다.";

for (let p of bookData.pages) {
    if (p.text && p.text.includes(oldText)) {
        p.text = p.text.replace(oldText, newText);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated CG text.");
