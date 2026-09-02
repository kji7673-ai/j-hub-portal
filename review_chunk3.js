const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let textPages = bookData.pages.filter(p => p.type === 'text' || p.type === 'image_top' || p.type === 'image_bottom' || p.type === 'interlude' || p.type === 'text_only');
let chunk = textPages.slice(45, 60);

chunk.forEach((p, i) => {
    let globalIndex = bookData.pages.findIndex(bp => bp === p);
    console.log(`\n\n--- PAGE INDEX: ${globalIndex} | TITLE: ${p.title} ---`);
    console.log(p.text || "");
});
