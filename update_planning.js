const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === "기획서는 무기가 아니다, 신뢰의 기록이다") {
        // Change title since the weapon metaphor is being removed
        p.title = "계획안, 신뢰의 기록";
        
        // Rewrite the body text
        p.text = `<p style="margin-bottom: 24px;">화학 또는 물리에서나 나와야 할 '공유결합'이라는 단어가 어떻게 건축 개념으로 사용될지 의아해하실 분들이 있을 것 같습니다.</p>
<p style="margin-bottom: 24px;">설계자가 설계를 의뢰하는 조합 사람들이나 각기 다른 분야의 사람들과 소통하는 매개체는 결국 <strong>'계획안'</strong>입니다. 계획안에는 크게 건축 개요와 건축 도면이 있습니다. 건축 개요에서는 전체 사업 규모의 확정과 사업성에 대한 분석이 서로의 연결점이 될 것이고, 건축 도면에서는 이곳에 입주하는 사람들의 편의성과 거주성, 그리고 시공자 또는 조합 관계자들에게는 분양성이 가장 중요한 핵심 관점이 될 것입니다.</p>
<p style="margin-bottom: 24px;">이처럼 각기 다른 입장을 가진 사람들의 다양한 관점과 욕망을 하나로 모아주는 개념이 바로 '공유결합'입니다. 설계자에게는 건축사로서 공익을 우선시하는 마음이 기본적으로 깔려 있습니다. 그것을 굳건한 뼈대로 삼아, 각기 만나는 사람들의 첨예한 요구점들을 적절히 조절하고 결합해 내는 것입니다.</p>
<p style="margin-bottom: 24px;">따라서 저에게 계획안이란, 화려하게 치장된 제안서나 누군가를 공격하기 위한 수단이 될 수 없습니다. 그것은 치열한 의견 조율의 결과물이자 <strong>'신뢰의 기록'</strong>입니다. 도면에 그어진 선 하나, 면적표의 숫자 하나에는 나와 건축주, 시공자, 그리고 미래의 거주자가 맺은 묵시적 약속이 담겨 있습니다.</p>
<p style="margin-bottom: 24px;">완벽한 기획서란 오차 없는 숫자로 꽉 채워진 문서가 아닙니다. 때로는 숫자가 조금 틀어지더라도, 그 안에 담긴 '사람을 향한 의도'가 투명하게 공유될 때 비로소 훌륭한 기록이 됩니다. 상대의 불안을 읽어내고, 나의 불완전함을 솔직하게 내보이며 함께 대안을 찾아가는 과정. 이 거친 공유결합의 과정을 충실히 담아낸 문서만이 현장에서 끝까지 살아남습니다.</p>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
