const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title && p.title.includes('맥락 속의 완벽함')) {
        p.text = `<p style="margin-bottom: 24px;">우리가 CG 업체에서 받은 이미지가 마음에 들지 않는 이유를 생각해 봅시다. 좋은 참고 이미지를 찾아 "이 분위기로 만들어 달라"고 요청해도 늘 어딘가 어색한 이유는, 건축의 아름다움이 단순히 '형태나 색감'만으로 완성되지 않기 때문입니다.</p>

<p style="margin-bottom: 24px;">거기에는 가장 중요한 <strong>'시간에 대한 이해'</strong>가 빠져 있습니다. 조감도나 투시도라는 것은 결국 어느 특정 시간대의 <strong>'빛과 그림자, 그리고 명암'</strong>을 포착해 내는 작업입니다. 건물이 대지 위에 놓였을 때 시간의 흐름에 따라 빛이 어떻게 떨어지고 그림자가 어떻게 깊이를 만들어내는지, 그 미세한 명암을 전체적으로 조율할 줄 알아야만 이미지는 비로소 생명력을 가진 진짜 건축물이 됩니다.</p>

<p style="margin-bottom: 24px;">우리가 한국의 미(美)를 말할 때 '자연스러움'을 이야기합니다. 하지만 이 자연스러움은 자연 그대로 방치된 상태가 아닙니다. 그것은 시간의 흐름과 빛의 각도까지 철저히 계산한, 신중한 고민과 섬세한 조정 끝에 나타나는 완벽한 '무심함'입니다.</p>

<p>창덕궁의 부용정이 완전한 대칭 속에 섬세한 비대칭을 품고 있듯이, 조감도 역시 차가운 형태 위에 시간과 빛이라는 자연의 맥락을 둥글게 조율해 낼 때 비로소 사람의 마음을 움직이는 힘을 갖게 됩니다.</p>`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

