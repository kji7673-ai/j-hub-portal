const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, i) => {
    console.log(`[${i}] type: ${p.type}, title: ${p.title || 'No Title'}`);
});
