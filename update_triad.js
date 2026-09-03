const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (!p.title) return;

    if (p.title === '공유결합의 첫 질문') {
        p.title = "공유결합의 첫 번째 질문: 조율자로서의 기준 세우기";
        p.text = `<p style="margin-bottom: 24px;">흔히들 건축을 하려면 가장 먼저 '나 자신을 알아야 한다'고 말합니다. 하지만 26년을 현장에서 구르며 내린 저의 결론은 조금 다릅니다. '나'라는 존재는 평생을 두고 죽을 때까지 알아가야 하는 미지의 영역입니다. 현장에서 당장 건축가에게 필요한 것은 나를 찾는 사색이 아니라, <strong>'나의 역할(Role)'을 명확히 인지하고 조율자(Coordinator)로서 흔들리지 않는 기준을 세우는 일</strong>입니다.</p>

<p style="margin-bottom: 24px;">과학의 세계를 상상해 보십시오. 수소(H) 원자 두 개와 산소(O) 원자 하나가 모여 H₂O, 즉 '물'이 됩니다. 서로가 가진 전자를 내어주고 교환하며 가장 안정화된 상태로 결합하는 것, 그것이 바로 공유결합입니다. 이 과정에서 폭발성 강한 수소와 불을 태우는 산소는 각자의 이질적인 뾰족함을 잃고, 세상의 갈증을 해소하는 전혀 새로운 생명수로 재탄생합니다.</p>

<p style="margin-bottom: 24px;">건축가의 역할은 이 거대한 화학반응을 이끌어내는 '촉매제'이자 '기준'입니다. 현장에는 늘 서로 다른 욕망과 한계들이 충돌합니다. 비용 절감을 최우선으로 삼는 자본의 논리, 행정적 편의를 요구하는 제도의 잣대, 그리고 쾌적한 삶을 열망하는 거주자의 요구까지. 만약 건축가가 어느 한쪽의 이익에만 목적을 둔다면 어떻게 될까요? 자본에 휩쓸리면 천박해지고, 제도에만 맞추면 생명력이 사라지며, 요구에만 끌려다니면 건물은 결코 땅 위에 서지 못할 것입니다.</p>

<p style="margin-bottom: 24px;">우리는 이 각기 다른 이질적인 욕망들을 조율하고, 서로가 조금씩 자신의 것을 내어주며 안정화되도록 <strong>'공유결합적 요소'</strong>를 만들어내는 사람입니다. 흔들리지 않는 명확한 설계의 기준을 세워, 이 파편화된 원소들을 건축이라는 단단하고 아름다운 물성으로 빚어내는 것. 그것이 제가 생각하는 공유결합의 첫 번째 조건입니다.</p>`;
    }

    if (p.title === '질문의 확장: "그렇다면 상대는 어떤가?"' || p.title === '공유결합의 두 번째 질문') {
        if (p.title === '공유결합의 두 번째 질문') {
            p.title = "공유결합의 두 번째 질문: 서로 다른 욕망의 포용";
            p.text = p.text.replace(/상대가 어떤 사람인지.*?포용하는 과정입니다\./gs, 
                "조율자로서의 기준이 섰다면, 다음은 반응할 원소들을 깊이 이해할 차례입니다. 현장에서 마주하는 서로 다른 욕망과 결핍을 포용하는 과정입니다.");
        }
    }

    if (p.title === '공유결합의 세 번째 질문') {
        p.title = "공유결합의 세 번째 질문: 현장이라는 반응기";
        p.text = p.text.replace(/현장의 물리적 조건.*?시작됩니다\./gs, 
            "수소와 산소의 결합이 일어나는 궁극적인 무대, 그것이 바로 대지(현장)입니다. 앞서 껴안은 수많은 욕망과 결핍들이 현장의 고유한 맥락 속에서 어떻게 화학반응을 일으키고 순응할 것인지 고민하는 과정입니다.");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

