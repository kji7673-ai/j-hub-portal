const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title && p.title.includes('100년의 기억을 덮는다는 것')) {
        p.text += `\n\n하지만 도면에서 펜을 떼는 순간, 진짜 현실의 벽이 숨통을 조여왔다.\n\n'상부를 공원으로 덮는 이 막대한 공사비를 조합이 기꺼이 감당할 것인가?'\n'3년이 넘는 공사 기간 동안, 하루 벌어 하루 먹고사는 상인들은 어디로 가서 생존해야 하는가?'\n'현행법상 이 전례 없는 복합 구조물을 지자체가 인허가해 줄 것인가?'\n\n종이 위에서 100년의 기억을 보존하는 선을 긋는 것은 건축가의 아름다운 낭만이었지만, 그것을 실체로 만들어내기 위해서는 낭만을 넘어선 처절한 '조율'이 필요했다. 자본의 이윤을 설득하고, 행정의 경직성을 깨뜨리며, 무엇보다 상인들의 3년 치 생존 대책을 함께 껴안지 않는 한 나의 스케치는 그저 위선적인 그림 쪼가리에 불과했다.\n\n건축은 선으로 낭만을 그리는 일이 아니다. 100년의 기억을 덮으려면, 그 기억의 무게만큼이나 무거운 현실의 고통을 짊어질 각오가 되어 있어야 한다. 대전의 그 낡은 시장 골목에서, 나는 도면 위에 그은 선 한 줄이 얼마나 무서운 책임감을 요구하는지 뼈저리게 배웠다.`;
        
        // Wrap with proper HTML tags for consistency if needed, but since it's markdown-like in this chapter, it's fine. 
        // Let's actually ensure it uses the <p> tags if the rest of the text doesn't use it, or just raw text. The current text uses plain text with \n\n.
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

