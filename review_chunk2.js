const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let startIndex = 15;
let count = 15;

let textPages = bookData.pages.filter(p => p.type === 'text' || p.type === 'image_top' || p.type === 'image_bottom' || p.type === 'interlude');
let chunk = textPages.slice(startIndex, startIndex + count);

chunk.forEach((p, i) => {
    let globalIndex = bookData.pages.findIndex(bp => bp === p);
    console.log(`\n\n--- PAGE INDEX: ${globalIndex} | TITLE: ${p.title} ---`);
    console.log(p.text || "");
});
