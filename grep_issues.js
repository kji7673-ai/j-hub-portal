const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, i) => {
    if (!p.text) return;
    if (p.text.includes("99")) console.log(`[99%] found in: ${p.title}`);
    if (p.text.includes("할머니") || p.title.includes("숫자가 눈물을")) console.log(`[Grandma] found in: ${p.title}`);
    if (p.text.includes("심의")) console.log(`[심의] found in: ${p.title}`);
});
