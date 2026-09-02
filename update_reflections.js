const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const replace1 = "참 하루하루가 고단하고 쉽지 않다.</div>";
const with1 = "참 하루하루가 고단하고 쉽지 않다. 하지만 출근길 만원 지하철, 무표정한 얼굴로 흔들리는 수많은 사람들을 본다. 어쩌면 저들도 겉으로는 둔탁해 보이지만, 속으로는 상처받지 않기 위해 온갖 더듬이를 세운 채 하루를 간신히 버텨내는 또 다른 지네맨들이 아닐까. 둔감함이라는 갑옷을 입고 살아가는 세상의 모든 예민한 영혼들에게, 속으로 남몰래 연대의 위로를 건네본다.</div>";

const replace2 = "단순한 슬픔을 넘어, 삶이라는 것 자체가 유독 애달프게 다가오는 요즘이다.</div>";
const with2 = "단순한 슬픔을 넘어, 삶이라는 것 자체가 유독 애달프게 다가오는 요즘이다. 하지만 이 애달픔은 결코 허무함이 아니다. 끝이 있음을 감각하는 그 순간, 오늘 무심코 마신 커피 한 잔, 스쳐 지나가는 바람, 그리고 내 곁을 지키는 사람들의 온기가 비로소 선명하게 다가온다. 죽음을 곁눈질하며 걷는 일은, 역설적이게도 '오늘'이라는 현실을 가장 눈부시게 살아내기 위한 유일한 방법일지도 모른다.</div>";

const replace3 = "조심스럽게 하루하루를 걷는다.</div>";
const with3 = "조심스럽게 하루하루를 걷는다. 세상은 갈수록 화려하고 현란한 말들로 넘쳐난다. 하지만 결국 닫힌 사람의 마음을 열고 무언가를 굳건히 세우는 것은, 투박할지언정 묵묵히 땀 흘려 약속을 증명해 내는 조용한 뒷모습이다. 오늘 하루, 우리가 허공에 흩뿌린 말들이 부디 땅에 단단히 뿌리내릴 수 있기를.</div>";

for (let p of bookData.pages) {
    if (p.text) {
        if (p.text.includes(replace1)) p.text = p.text.replace(replace1, with1);
        if (p.text.includes(replace2)) p.text = p.text.replace(replace2, with2);
        if (p.text.includes(replace3)) p.text = p.text.replace(replace3, with3);
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated reflections with universal endings.");
