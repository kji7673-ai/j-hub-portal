const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === '계획안, 신뢰의 기록') {
        p.text = `<p style="margin-bottom: 24px;">화학에서나 나올 법한 '공유결합'이라는 단어가 도대체 건축 현장에서 어떻게 실체화되는지 묻는다면, 저는 주저 없이 <strong>'계획안'</strong>이라고 답하겠습니다.</p>

<p style="margin-bottom: 24px;">앞서 현장의 사람들이 "그림 좀 그려주세요"라고 간절히 부탁했던 것을 기억하십니까? 그 보이지 않는 수많은 바람들, 서로 다른 언어들, 그리고 회의 테이블 위에서 격돌하던 제도의 이면들이 마침내 구체적인 실체로 번역되어 내려앉은 곳이 바로 계획안(건축 개요와 도면)입니다.</p>

<p style="margin-bottom: 24px;">건축 개요의 숫자 하나에는 조합이 열망하는 사업성과 지자체가 요구하는 공익적 잣대가 팽팽하게 줄다리기를 한 흔적이 담겨 있습니다. 도면의 선 하나에는 거주자의 아늑한 삶과 시공사의 이윤, 그리고 그 모든 것을 조율해 낸 건축가의 뼈아픈 고뇌가 녹아 있습니다.</p>

<p style="margin-bottom: 24px;">이처럼 각기 다른 입장을 가진 이질적인 원소들을 하나로 묶어 물(H₂O)로 만들어주는 매개체가 바로 계획안입니다. 설계자는 흔들리지 않는 기준을 중심에 세우고, 이 첨예한 요구들을 둥글게 다듬고 결합해 냅니다.</p>

<p style="margin-bottom: 24px;">따라서 저에게 계획안이란, 화려하게 치장된 프레젠테이션이나 누군가를 현혹하기 위한 무기가 될 수 없습니다. 그것은 치열한 회의 테이블을 거치며 완성된 <strong>'신뢰의 기록'</strong>입니다.</p>

<p>상대의 뾰족한 불안을 둥글게 안아주고, 헛된 환상에는 냉정한 현실의 이면을 짚어주며 함께 대안을 찾아낸 공유결합의 결정체. 이 치열한 이해와 조율의 과정을 충실히 담아낸 문서만이 거친 현장에서 끝까지 살아남습니다.</p>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

