const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);
let textPages = bookData.pages.filter(p => p.type === 'text' || p.type === 'image_top' || p.type === 'image_bottom' || p.type === 'interlude');
console.log("Total textual pages to review:", textPages.length);
textPages.forEach((p, i) => console.log(`[${i}] Title: ${p.title || 'No Title'} - Length: ${(p.text || '').length}`));
