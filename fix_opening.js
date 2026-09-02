const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// 1. Refine the text of "기획서는 무기가 아니다"
for (let p of bookData.pages) {
    if (p.title === "기획서는 무기가 아니다, 신뢰의 기록이다") {
        p.text = "치열한 수주전에서 살아남기 위해 사람들은 흔히 '기획서가 무기다'라고 말합니다. 하지만 26년간 현장의 흙먼지를 마시며 제가 깨달은 진실은 다릅니다. 기획서는 누군가를 찌르거나 내 약점을 방어하기 위한 무기가 될 수 없습니다. 무기로 지어진 집에는 사람이 살 수 없기 때문입니다.\n\n건축의 본질은 사람에 대한 믿음입니다. 그리고 그 믿음을 증명하는 유일한 수단이 바로 도면이자 기획서입니다. 당장의 심의를 통과하기 위해 화려한 조감도로 포장된 종이 뭉치는 결코 좋은 기획서가 아닙니다. 현장의 예측 불가능한 돌발 변수들, 시공의 현실성, 그리고 무엇보다 그 공간에서 살아갈 사람의 숨결을 깊이 이해하고 담아냈을 때, 치열한 숫자들은 비로소 살아 숨 쉬는 '신뢰의 기록'이 됩니다.\n\n제가 완벽하고 차가운 기계(AI)를 이 진흙탕 같은 현장으로 불러들인 이유도, 기획서를 더 날카로운 무기로 벼리기 위함이 아니었습니다. 오히려 인간의 삶을 담아낼 그 숫자들을 한 치의 오차도 없는, 가장 투명하고 단단한 '신뢰의 기반'으로 만들고 싶었기 때문입니다.";
    }
}

// 2. Reorder Part 1 to make more sense conceptually
let part1 = bookData.pages.filter(p => p.partCategory === "1부: 설계의 본질");
let rest = bookData.pages.filter(p => p.partCategory !== "1부: 설계의 본질");

// Find specific items
const getByTitle = (titleKeyword) => part1.find(p => (p.title || p.type).includes(titleKeyword));

let introText = getByTitle("1부. 설계의 본질");
let covalentIntro = getByTitle("어느 날, 공유결합이 내게로 왔다");
let trustRecord = getByTitle("기획서는 무기가 아니다");
let yongsan = getByTitle("용산 현장의 기억");
let threeQs = getByTitle("세 가지 질문");
let part1Outro = getByTitle("1부를 마치며");

// The remaining random texts from part 1 that were added by me or old structure
let othersPart1 = part1.filter(p => 
    p !== introText && p !== covalentIntro && p !== trustRecord && 
    p !== yongsan && p !== threeQs && p !== part1Outro
);

// New Logical Order for Part 1:
// 1. 1부 시작 (Intro)
// 2. 어느 날, 공유결합이 내게로 왔다 (The overarching realization)
// 3. 기획서는 무기가 아니다, 신뢰의 기록이다 (Refined - The tool/document aspect)
// 4. 공유 결합: 사람을 향한 건축, 용산 현장의 기억 (The application)
// 5. 제2장. 공유결합의 세 가지 질문 (The transition to Part 2)
// 6. 1부를 마치며

let newPart1 = [];
if (introText) newPart1.push(introText);
if (covalentIntro) newPart1.push(covalentIntro);
if (trustRecord) newPart1.push(trustRecord);
if (yongsan) newPart1.push(yongsan);
if (threeQs) newPart1.push(threeQs);
if (part1Outro) newPart1.push(part1Outro);

bookData.pages = [...newPart1, ...othersPart1, ...rest];

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
