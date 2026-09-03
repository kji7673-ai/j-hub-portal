const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === '질문의 확장: "그렇다면 상대는 어떤가?"') {
        p.text = `<p style="margin-bottom: 24px;">이해관계가 얽히고설킨 흙먼지 날리는 현장에서, 중심을 잡고 공유결합을 이끌어낼 '조율자'로서의 기준을 세웠습니다.</p>

<p style="margin-bottom: 24px;">→ 그렇다면 다음 질문은 자연스럽게 이어집니다.</p>

<p style="font-size: 1.1em; font-weight: 600; color: #1d1d1f; margin-bottom: 24px;">"조율자로서 중심을 잡았다면, 이제 나의 도면이 닿아야 할 그 '상대'들은 과연 어떤 분들인가?"</p>

<p style="margin-bottom: 24px;">여기서 오해하면 안 되는 것이 있습니다. 조율자라는 것은 결코 무지한 군중을 이끌고 통제하는 전지전능한 능력자가 아닙니다. 시공사, 관공서, 조합이라는 이름 아래 모여 있지만, 사람이 모인 무리에서는 누구나 각자의 자리에서 조율자의 역할을 해내기 마련입니다. 어떤 개인을 그가 속한 '이익 집단'이라는 꼬리표 하나로 일체화시켜 치부해 버려서는 안 됩니다.</p>

<p style="margin-bottom: 24px;">소통은 서로를 알아가는 것에서 시작됩니다. 내가 부족한 것을 상대가 채워주고, 상대가 모르는 것을 내가 짚어주며, <strong>서로를 이용 대상이 아닌 '귀중한 존재'로 대할 때 비로소 건축이라는 위대한 공유결합이 일어납니다.</strong></p>

<p style="margin-bottom: 24px;">건축가는 그저 흔들리지 않는 중심을 잡아주는 사람입니다. 그리고 그분들의 눈에 보이지 않는 이상과 목표를 '보이도록' 만들어 주는 사람입니다.</p>

<p style="margin-bottom: 24px;">한때, 현장에서 만난 분들이 제게 "대표님, 그림 좀 잘 그려주세요"라고 부탁할 때면, 속으로 '내가 화가도 아니고 웬 그림을 그려달라고 하나'라며 뾰족하게 날을 세우던 시절이 있었습니다. 하지만 지금은 다릅니다. 그 투박한 말속에 담긴 진심을 압니다. <strong>"우리의 보이지 않는 실체를 제발 구체화 시켜주세요"</strong>라는 간절한 바람을, 그저 그분들의 가장 편안하고 일상적인 언어로 표현했을 뿐이라는 것을요.</p>

<p style="margin-bottom: 24px;">언젠가 한 회의 석상에서 누군가 이런 말을 한 적이 있습니다.<br>
<strong style="color: #0066cc;">"생각하시는 바를 그냥 편하게 펼쳐 놓으십시오. 제가 잘 담아내겠습니다."</strong></p>

<p style="margin-bottom: 24px;">이 얼마나 멋진 태도입니까? 상대의 언어가 거칠든 곱든, 뾰족하든 투박하든, 조율자인 제가 그것을 둥글게 잘 담아내기만 하면 되는 것이었습니다.</p>

<p>그들의 언어를 둥글게 이해하고, 거친 생각들조차 온전히 그릇에 담아 귀중한 존재로 껴안는 것. 그것이 바로 상대를 이해하는 진정한 방식이며, 현장을 향한 공유결합의 두 번째 발걸음입니다.</p>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

