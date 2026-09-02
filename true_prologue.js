const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === '프롤로그: 건축 외에는 아무것도 모르는 바보의 이야기') {
        let disclaimerMatch = p.text.match(/<div style="margin-top: 40px;.*?<\/div>/s);
        let disclaimer = disclaimerMatch ? disclaimerMatch[0] : '';
        
        p.text = `<p style="font-size: 1.1em; line-height: 1.8; margin-bottom: 24px;">사실 오로지 건축 설계만 26년간 해온 사람으로서, 설계자로서의 자존심이 점점 사라져 가는 현실이 안타깝습니다.</p>

<p style="margin-bottom: 24px;">누구나 자신의 본질을 지키기 위해 끝까지 붙들고 있는 단 하나가 있습니다. 특히 50만 원도 채 안 되는 돈을 쥐고 무작정 서울에 올라왔던 저에게, 건축 설계라는 이 일은 단순한 직업을 넘어 곧 '생존' 그 자체였습니다.</p>

<p style="margin-bottom: 24px;">단순히 밥벌이를 위한 생존이 아니었습니다. 나의 본질을 증명해야만 하는 절박함이 생존이라는 무게와 치열하게 맞물리다 보니, 현장에서 저는 어떤 때에는 몹시도 날카로웠고, 또 그만큼 깊이 아파하기도 했습니다. 그래도 세월이 흐르고 나이가 쌓이니, 이제는 모난 모서리를 깎아내고 조금은 둥글둥글해지려고 합니다. 아니, 아주 조금은 그렇게 되어 보려 노력하고 있습니다.</p>

<p style="margin-bottom: 24px;">결핍투성이였던 저의 뾰족함이 현장의 흙먼지와 부딪히고 닳아가며, 마침내 타인과 세상의 불완전함을 껴안는 <strong>'공유결합'</strong>을 이루어내기까지의 과정. 이 책은 그렇게 26년 동안 도면을 쥐고 버텨온, 상처투성이지만 끝끝내 사람의 온기를 지켜내려 했던 한 건축가의 가장 솔직한 고백입니다.</p>

${disclaimer}`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

