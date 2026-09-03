const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title && p.title.includes('질문의 확장: "그 상대가 살 현장')) {
        p.title = '질문의 확장: "우리가 마주할 진짜 현장은 어디인가?"';
        p.text = `<p style="margin-bottom: 24px;">상대의 언어를 둥글게 이해하고 담아내는 법을 배웠다면, 이제 우리의 시선은 건축물이 세워질 무대로 향해야 합니다. 우리는 흔히 건축의 현장이라고 하면 흙바닥과 콘크리트가 뒤섞인 공사판을 떠올립니다.</p>

<p style="margin-bottom: 24px;">하지만 설계자로서 26년을 보내며 깨달은 사실이 있습니다. 흙먼지 날리는 물리적 현장의 변수에 대응하는 것은 오히려 쉬운 일입니다. 건축 설계의 거의 모든 운명이 결정되는 진짜 현장은 혼자 모니터 앞의 옐로 페이퍼 위에서 보내는 고독한 시간, 그리고 수많은 이해관계가 격돌하는 <strong>'회의 테이블'</strong>입니다.</p>

<p style="margin-bottom: 24px;">→ 질문은 다시 확장됩니다.</p>

<p style="font-size: 1.1em; font-weight: 600; color: #1d1d1f; margin-bottom: 24px;">"서로 다름을 이해했다면, 이제 이 거대한 욕망과 제도가 격돌하는 '진짜 현장(회의 테이블)'의 이면을 어떻게 직시할 것인가?"</p>`;
    }

    if (p.title === '공유결합의 세 번째 질문: 현장이라는 반응기') {
        p.text = `<p style="margin-bottom: 24px;">수소와 산소의 결합이 일어나는 궁극적인 반응기, 그것은 눈에 보이는 물리적 대지가 아닙니다. 그것은 정치와 정책, 그리고 끝없는 욕망이 뒤엉킨 거대한 '이해관계의 테이블'입니다.</p>

<p style="margin-bottom: 24px;">예를 들어 보겠습니다. 사업을 시행하는 조합 입장에서는 정치권에서 쏟아내는 새로운 부동산 정책에 솔깃해질 수밖에 없습니다. <i>"우리 지역이 2종 일반주거지역이라 재개발하면 3종밖에 안 되는데, 도심복합사업을 하면 400%, 성장거점형을 하면 최대 1,500%까지 용적률을 받을 수 있대!"</i> 이런 이야기가 돌면, 추진하는 입장에서는 당장 그 헛된 희망을 이루어주겠다고 속삭이는 설계사를 우선적으로 찾기 마련입니다.</p>

<p style="margin-bottom: 24px;">하지만 인허가권을 쥔 지자체의 입장은 어떨까요? 그분들은 기본 정책의 유지와 지역의 균형 발전, 도시 전체의 맥락을 보고 판단해야 하는 사람들입니다. 특정 단지에만 1,500%를 무턱대고 허락할 리가 없습니다. 결코 쉽지 않은 길입니다.</p>

<p style="margin-bottom: 24px;">이때 건축가의 진짜 실력이 드러납니다. 설계자는 단순히 눈앞의 제도를 쫓아가거나 달콤한 말로 포장하는 사람이 아니라, <strong>그 제도의 '이면'을 볼 줄 알아야 하며, 그것을 추진하는 사람들에게 냉정하고 투명하게 설명할 수 있어야 합니다.</strong></p>

<p>조합의 절박함, 지자체의 책임감, 시공사의 이윤 추구. 각기 다른 역할을 가진 이들의 이해관계를 깊이 이해하고 조율하지 못하면, 결국 회의 테이블에서는 서로 욕만 하다가 사업은 한 발짝도 나아가지 못합니다. 진짜 현장의 이면을 읽어내는 것, 그것이 현장이라는 반응기를 다루는 공유결합의 세 번째 원칙입니다.</p>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

