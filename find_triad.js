const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, index) => {
    if (p.text && p.text.includes('내가 누구인지')) {
        console.log(`Found old triad at index ${index}: Title="${p.title}"`);
    }
});
