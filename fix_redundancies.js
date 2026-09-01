const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

// 1. Delete redundant/empty pages
bookData.pages = bookData.pages.filter(p => {
    if (p.title === '11장. 엔터프라이즈 엘레강스 (Enterprise Elegance)') return false;
    if (p.title === '88. 과거의 기억을 현재의 목적에 맞추어 이용한다') return false;
    if (p.title === '물방울, 그리고 시지프스의 언덕') return false; // Redundant with the main Sisyphus essay
    return true;
});

// 2. Rename 12장 -> 11장, 13장 -> 12장
bookData.pages.forEach(p => {
    if (p.title && p.title.includes('12장. 5060 경영진을')) {
        p.title = p.title.replace('12장.', '11장.');
    }
    if (p.title && p.title.includes('13장. 사진과 여백')) {
        p.title = p.title.replace('13장.', '12장.');
    }
});

// 3. Move "쟁이의 마음: 두려움을 넘어 다시 붓을 드는 이유" to the end of Part 2
let mindIndex = bookData.pages.findIndex(p => p.title && p.title.includes('쟁이의 마음:'));
if (mindIndex !== -1) {
    let mindPage = bookData.pages.splice(mindIndex, 1)[0];
    mindPage.partCategory = "2부: 증언과 성찰";
    
    // Find where Part 2 ends (before Part 3 Interlude)
    let part3InterludeIndex = bookData.pages.findIndex(p => p.type === 'interlude' && p.title.includes('3부. 프롭테크와'));
    if (part3InterludeIndex !== -1) {
        bookData.pages.splice(part3InterludeIndex, 0, mindPage);
    }
}

// 4. Update the "마치는 글: 쟁이들에게 보내는 위로" to be a cover type so it renders nicely like an Epilogue quote.
let closingQuote = bookData.pages.find(p => p.title && p.title.includes('마치는 글:'));
if (closingQuote) {
    closingQuote.type = "text_only"; // Keep it as text_only, it's styled nicely
}

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Cleanup done!");
