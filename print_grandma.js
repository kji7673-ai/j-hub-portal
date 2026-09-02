const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, i) => {
    if (p.text && (p.text.includes("할머니") || p.title.includes("숫자가 눈물을") || p.title.includes("신뢰를 기록하다"))) {
        console.log(`\n\n--- TITLE: ${p.title} ---`);
        console.log(p.text);
    }
});
