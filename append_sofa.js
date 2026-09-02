const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldTextSnippet = "당신은 피자 햄버거 핫도그 등등이 계속 그려지는 군요?”<br>음……";
const newReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">예전에 쓴 글들을 보면 '참 엉뚱한 상상도 많이 했구나' 싶어 피식 웃음이 난다.<br><br>신약성경 마태복음을 보면 두 아들 이야기가 나온다. 포도원에 가서 일하라는 아버지의 말에 앞에서는 '네' 하고 대답만 해놓고 가지 않은 아들과, 처음엔 '싫다'며 퉁명스럽게 굴었지만 뉘우치고 결국 밭으로 나간 아들의 이야기다. 특히 나처럼 수많은 조합원과 주민들을 만나 정비사업을 이끌어가는 사람들은 매 순간 수많은 '약속'과 '말'을 내뱉게 된다. 그럴 때마다 혀끝에서 맴도는 가벼운 말보다, 내 생각과 입 밖으로 낸 말, 그리고 앞으로 나의 '행동'이 기어코 일치하기를 간절히 바라며 조심스럽게 하루하루를 걷는다.</div>`;

for (let p of bookData.pages) {
    if (p.text && p.text.includes(oldTextSnippet)) {
        if (!p.text.includes('마태복음')) {
            p.text = p.text.replace(oldTextSnippet, oldTextSnippet + '\n\n' + newReflection);
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended sofa reflection.");
