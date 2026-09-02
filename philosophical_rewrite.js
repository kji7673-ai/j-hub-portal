const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (!p.text) return;
    
    // 1. Rewrite the "AI vs JI" chapter to fix the 99% vs 1% disconnect
    if (p.title === 'AI, 그래 넌 AI고 난 JI다') {
        p.text = p.text.replace(/기계가 99%의 노동\(수십 개의 대안 생성\)을 대신해 줄 때.*?건축가만의 고유 영역이다\./gs, 
            "기계가 수십, 수백 개의 대안을 생성해 낸다 하더라도, 현장의 흙먼지를 마시며 도면 위에 꾹꾹 눌러 담았던 내 손의 온기는 결코 대체될 수 없습니다. 기계가 법규와 용적률이라는 완벽하고 차가운 '데이터'를 연산해 낸다면, 우리는 그 뼈대 위에 사람이 걷고 머무는 동선이라는 '영혼'을 설계해야 합니다.\n\n이것은 기계가 우리의 노동을 99% 대체하는 편리함의 문제가 아닙니다. 가장 차가운 기계의 이성과, 가장 뜨거운 인간의 영혼이 동등하게 만나 또 다른 차원의 **'공유결합'**을 이루어내는 치열한 과정입니다.");
    }
    
    // 2. Add the profound conclusion to the Epilogue / Completion chapter
    if (p.title === '공유결합의 완성') {
        p.text = p.text.replace(/스스로를 성찰하고, 타인을 포용하며, 현장의 불완전함을 껴안는 여정.*?완성해 냅니다\./gs, 
            "스스로를 성찰하고, 타인을 포용하며, 현장의 불완전함을 껴안는 여정. 그리고 마침내 다가온 거대한 기술 앞에서도 도면을 쥐었던 손의 온기를 놓지 않는 것.\n\n**공유결합은 서로가 가지지 못한 것을 기꺼이 내어주는 순간입니다.**\n기술은 이성을 담고, 철학은 영혼을 담습니다. 가장 차가운 기술과 가장 뜨거운 인간의 철학, 그 둘을 동등하게 안을 때 비로소 건축은 단순한 공간의 조합을 넘어 '사랑'이 됩니다.");
    }

    // 3. Update the ending of "기술이 지워진 자리에 남은 것 (비워냄의 미학)"
    if (p.title === '기술이 지워진 자리에 남은 것 (비워냄의 미학)') {
         if(!p.text.includes('기계가 도움을 준다고 해도')) {
             p.text += "\n\n<p style=\"margin-top: 24px;\">기계가 아무리 놀라운 속도로 도면을 그려낸다고 해도, 지난 26년 동안 숱한 밤을 지새우며 연필로 선을 긋던 그 손의 온기와 무게는 결코 대체되지 않습니다. 기술의 발전은 역설적으로 우리에게 '가장 인간적인 것이 무엇인가'를 묻고 있습니다.</p>";
         }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

// Update export
let exportCode = fs.readFileSync('export_markdown.js', 'utf8');
fs.writeFileSync('export_markdown.js', exportCode, 'utf8');

