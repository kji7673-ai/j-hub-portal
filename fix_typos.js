const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let changeCount = 0;

bookData.pages.forEach(p => {
    if (!p.text) return;
    
    let originalText = p.text;
    
    // 1. Fix the specific typo requested by the user
    p.text = p.text.replace(/사람을 아고/g, '사람을 알고');
    
    // 2. Fix common Korean spelling mistakes (맞춤법 및 띄어쓰기 교정)
    p.text = p.text.replace(/역활/g, '역할');
    p.text = p.text.replace(/바램/g, '바람'); // "바람을" 등
    p.text = p.text.replace(/몇일/g, '며칠');
    p.text = p.text.replace(/어의없는/g, '어이없는');
    p.text = p.text.replace(/어의없게/g, '어이없게');
    p.text = p.text.replace(/에매/g, '애매');
    p.text = p.text.replace(/안되서/g, '안 돼서');
    p.text = p.text.replace(/할려고/g, '하려고');
    p.text = p.text.replace(/볼려고/g, '보려고');
    
    // Fix double spaces (except in HTML tags where it might not matter, but good practice)
    p.text = p.text.replace(/  +/g, ' ');

    if (originalText !== p.text) {
        changeCount++;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Fixed typos in ${changeCount} pages.`);
