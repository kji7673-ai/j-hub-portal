const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldText = "나는 생각을 잘하고 스케치를 잘하는, 그런 진짜 건축쟁이가 되고 싶었다. 잊지 말자. 명심하자.";
const newText = "나는 생각을 잘하고 스케치를 잘하는, 그런 진짜 건축쟁이가 되고 싶었다. 잊지 말자. 명심하자.\n\n우스운 이야기지만, 현재의 나는 애써 운동화를 탓하던 과거의 그 모습에서 조금도 더 강해지지 않은 것 같다. 서울시 건축심의위원이라는 번듯한 직함을 달고 회의 자리에서 내 의견을 이야기할 때조차, 여전히 목소리가 미세하게 떨리는 나 자신을 발견할 때면 '너는 참 어쩔 수 없구나' 하며 쓴웃음을 짓게 된다.\n\n하지만 어쩌면 다행인지도 모른다. 그때나 지금이나 나는 무장한 듯 완벽하고 빈틈없는 전문가로 보이기보다는, 여전히 치열하게 생각하고, 진심으로 스케치하고, 묵묵히 글을 쓰며, 사람의 마음과 감정을 소중히 다룰 줄 아는 그런 사람으로 남고 싶으니까.";

for (let p of bookData.pages) {
    if (p.text && p.text.includes(oldText)) {
        p.text = p.text.replace(oldText, newText);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended sneaker reflection.");
