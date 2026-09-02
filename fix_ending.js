const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldEnding = `이것이 바로 정비사업을 하면서 제가 실천하고자 했던 '공유 결합'입니다. 우리의 기술과 설계가 그 땅의 아픔, 그곳에 사는 사람들의 고단함과 결합하여 만들어내는 따뜻한 쉼의 공간. 비록 수주라는 결과로 이어지진 못했을지라도, 우리는 그 눈 내리는 용산의 언덕에서 건축의 진짜 본질과 단단하게 결합해 있었습니다.`;

const newEnding = `우리의 계획안에서 '공유결합'은 거창한 구호가 아니었습니다. 주민들의 편의성과 심한 단차가 가진 지형적 약점이 어떻게 서로를 보완할 수 있을지 치열하게 고민한 실체적인 결과물이었습니다. 

단차가 지는 구간의 데크를 조금씩 내밀어 사람들이 머물고 쉴 수 있는 계단식 조경 공간을 만들었고, 지형상 지하지만 외부로는 활짝 열려 있는 테라스형 상가와 커뮤니티 시설을 계획했습니다. 동시에 이를 통해 확보된 용적률을 최대치로 끌어올려 조합의 사업성을 견인할 분양 세대를 촘촘하게 구성했습니다.

![용산 테라스 조경 렌더링](static/images/yongsan_terrace.jpg)

오랜 세월 주민들에게 불편함의 상징이었던 가파른 단차를 오히려 이 아파트만의 독보적인 명소로 뒤바꾸는 것. 서울에 사는 누구나 한 번쯤 찾아와 사진을 찍고 싶어 하는 매력적인 장소로 만드는 것. 지형의 약점, 주민의 쉼, 그리고 조합의 수익이라는 서로 다른 가치들을 하나의 공간 구조로 단단하게 묶어내는 이러한 설계 방향이 바로 제가 믿는 '공유결합'의 실체입니다. 

비록 수주라는 결과로 이어지진 못했을지라도, 우리는 그 눈 내리는 용산의 언덕에서 건축의 진짜 본질과 단단하게 결합해 있었습니다.`;

bookData.pages.forEach(p => {
    if (p.title === "공유 결합: 사람을 향한 건축, 용산 현장의 기억") {
        p.text = p.text.replace(oldEnding, newEnding);
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
