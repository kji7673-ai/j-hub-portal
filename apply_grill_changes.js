const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// 1. Remove Appendices
bookData.pages = bookData.pages.filter(p => !p.title || !p.title.includes('부록'));

// 2. Eradicate J-Hub and Technical tone
bookData.pages.forEach(p => {
    if (!p.text) return;
    
    // Replace J-Hub references with emotional equivalents
    p.text = p.text.replace(/시스템\(J-Hub\)/g, '디지털 기록장');
    p.text = p.text.replace(/J-Hub/g, '새로운 디지털 설계 도구');
    
    // Smooth out Page 65 (2부를 마치며) which had a big J-Hub transition
    if (p.title === '2부를 마치며') {
        p.text = p.text.replace(/마침내 3부에서 투명한 데이터와 시스템.*?부활합니다\./g, 
            "마침내 3부에서 우리의 땀방울과 철학을 온전히 담아낼 수 있는 '새로운 디지털 기록장'이라는 형태로 부활합니다. 기계를 도구로 삼아 인간의 가치를 더 단단하게 지켜내는 그 기적 같은 전환의 현장으로 여러분을 안내합니다.");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

// 3. Update export_markdown.js to use the new Title
let exportCode = fs.readFileSync('export_markdown.js', 'utf8');
exportCode = exportCode.replace(/# 불완전한 선택: AI 시대 건축가의 성찰/g, '# 공유결합: 26년 건축 쟁이의 현장 기록');
fs.writeFileSync('export_markdown.js', exportCode, 'utf8');

