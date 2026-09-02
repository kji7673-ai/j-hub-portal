const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newPage = {
    type: "text",
    title: "어느 날, 공유결합이 내게로 왔다",
    text: "<p style=\"margin-bottom:24px; line-height:1.8;\">제가 왜 '공유결합'이라는 철학을 설계의 최우선에 두게 되었는지, 그 단어가 어떻게 제게로 와닿았는지 고백할 필요가 있을 것 같습니다. 제 건축 인생을 관통하는 이 거대한 메타포는 사실, 전혀 상관없어 보이는 세 번의 우연한 '충격'에서 비롯되었습니다.</p><p style=\"margin-bottom:24px; line-height:1.8;\">첫 번째 충격은 고등학교 1학년 때 만난 정하진이라는 친구에게서 왔습니다. 어느 날 그 친구의 집에 놀러 갔는데, 어머니가 부엌에서 \"진아~\" 하고 부르셨습니다. 그러자 하진이는 너무나도 다정하게 \"네~\" 하고 대답했습니다. 대구에서 자란 무뚝뚝한 사내아이들이 으레 \"왜!\"라고 퉁명스럽게 쏘아붙이던 것만 보아온 제게, 그 \"네~\"라는 대답은 신선한 충격이었습니다. 누군가의 부름에 저토록 공손하고 따뜻하게 응답할 수 있구나. 사람과 사람 사이의 관계가 저렇게 아름답게 이어질 수 있구나. 그날 들었던 \"네~\"라는 짧은 대답은 근 40년이 지난 지금까지도 제 기억 속에 선명하게 남아 있습니다.</p><p style=\"margin-bottom:24px; line-height:1.8;\">두 번째 충격은 대학원 시절에 찾아왔습니다. 어느 날 길을 걷다 갑자기 머릿속에 번개가 친 것처럼 \"계단! 그래, 계단이다!\" 하며 소리를 친 적이 있습니다. 상하를 연결하고, 단절된 층위를 극복하며, 공간의 극적인 변화를 이끌어내는 존재. 공간과 공간을 이어주는 매개체의 벅찬 힘을 깨달은 순간이었습니다.</p><p style=\"margin-bottom:24px; line-height:1.8;\">그리고 세 번째 충격. 어느 날, 교회에서 우리나라의 저명한 물리학자 교수님의 설교를 듣게 되었습니다. 교수님은 원소의 결합 방식을 설명하시며 '이온 결합'과 '공유 결합'이라는 단어를 꺼내셨습니다. 그 순간, 제 머릿속에서 과거의 그 \"네~\"라는 대답과 \"계단\"의 깨달음이 하나로 폭발하듯 얽혀 들었습니다.</p><p style=\"margin-bottom:24px; line-height:1.8;\"><strong>'그래, 우리 몸도 결국 공유결합으로 이루어져 있지 않은가. 그렇다면 나와 타인의 관계, 나와 현장의 모든 관계성 역시 결국 하나의 거대한 공유결합이구나.'</strong></p><p style=\"margin-bottom:24px; line-height:1.8;\">하늘과 땅, 그리고 그 사이의 사람. 사람은 타인의 부름에 \"네~\"라고 다정하게 응답할 수 있고, 계단처럼 단절된 것들을 연결 지을 수 있으며, 나아가 스스로가 매개체가 되어 세상을 잇는 창조자의 위치에까지 닿을 수 있는 존재라는 깨달음이 밀려왔습니다.</p><p style=\"margin-bottom:24px; line-height:1.8;\">그날 이후, 저는 \"공유결합\"이라는 단어를 제 건축을 지탱하는 유일한 메타포로 품게 되었습니다. 각자가 가진 불완전함을 기꺼이 내어주고 서로를 묶어 안정을 찾는 과정. 그것이 바로 제가 26년 동안 도면 위에서 증명하고자 했던 건축의 진짜 모습입니다.</p>",
    part: "1부: 설계의 본질 - 공유결합",
    partTitle: "건축이라는 세계",
    partCategory: "1부: 설계의 본질 - 공유결합"
};

// Insert after the Prologue and Part 1 intro
// Let's find index to insert.
let insertIdx = 0;
for (let i = 0; i < bookData.pages.length; i++) {
    if (bookData.pages[i].title === '공유 결합: 사람을 향한 건축, 용산 현장의 기억') {
        insertIdx = i;
        break;
    }
}

bookData.pages.splice(insertIdx, 0, newPage);

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Inserted origin story at index", insertIdx);
