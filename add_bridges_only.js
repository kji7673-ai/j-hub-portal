const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let finalPages = [];

for (let i = 0; i < bookData.pages.length; i++) {
    let p = bookData.pages[i];
    
    // Add 1st bridge before Part 2 interlude
    if (p.type === 'interlude' && p.title && p.title.includes('2부.')) {
        finalPages.push({
            "type": "text_only",
            "title": "1부를 마치며",
            "text": "1부에서 우리가 배운 공유결합의 원리가, 이어지는 2부의 현장 에세이에서 구체적으로 어떻게 깨어나고 상처 받는지 보게 될 것입니다. 이제 우리는 그 공유결합의 철학이 26년 현장에서 얼마나 처절하게 무너지고 다시 일어서는지를 목격할 것입니다.",
            "part": "1부: 플랫폼 마스터플랜"
        });
    }
    
    // Add 2nd bridge before Part 3 interlude
    if (p.type === 'interlude' && p.title && p.title.includes('3부.')) {
        finalPages.push({
            "type": "text_only",
            "title": "2부를 마치며",
            "text": "이 모든 고민과 실패들이 결국 하나의 기술적 해법(J-Hub)으로 응축되기까지의 여정이 3부입니다.",
            "part": "2부: 철학편"
        });
        finalPages.push(p);
        
        finalPages.push({
            "type": "text_only",
            "title": "3부를 시작하며: 기술은 철학을 이기지 못한다",
            "text": "1부의 철학과 2부의 현장 기록이 기술로 어떻게 옮겨지는가를 명시적으로 보여주는 장입니다. 이 장의 기술 섹션마다, J-Hub 개발에 참여한 AI 에이전트가 자신의 관찰을 기록했습니다.<br><br>불완전한 인간들이 완벽한 기계를 통해 다시 인간다워지는 과정. 기술이 해내지 못하는 것은 무엇인가를 중심에 두고 읽어주시길 바랍니다.",
            "part": "3부: 시스템과 비전"
        });
        continue;
    }

    // Keep everything, no deletions
    finalPages.push(p);
}

bookData.pages = finalPages;
const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
