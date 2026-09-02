const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === '프롤로그: 건축 외에는 아무것도 모르는 바보의 이야기') {
        p.text = p.text.replace(/안녕하세요\. 도면 위에서.*?전해주고 싶은 이야기입니다\./gs, 
            "도면 위의 완벽하고 매끄러운 선들이, 현장의 거친 흙먼지와 부딪혀 여지없이 깨지고 부서지는 것을 지난 26년간 뼈저리게 지켜보았습니다.\n\n이 책은 화려한 건축물의 조감도 뒤에 가려진, 상처투성이 현장에 대한 솔직한 고백입니다. 동시에 모든 것을 숫자로 치환해 버리는 차가운 데이터의 시대 앞에서, 끝끝내 도면을 쥔 '사람의 온기'를 지켜내려는 한 건축가의 치열한 철학적 투쟁기이기도 합니다.\n\n결핍을 가진 인간과 공간, 그리고 기술이 어떻게 서로를 내어주며 완벽한 하나로 연결될 수 있는가. 저는 그 답을 **'공유결합'**이라 부르기로 했습니다. 화려한 성공담이나 기술서가 아닙니다. 이것은 불완전한 우리가 서로를 포용하며 세상을 짓는 방식에 관한 이야기입니다.");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

