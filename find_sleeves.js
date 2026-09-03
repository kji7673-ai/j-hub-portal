const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const pages = bookData.pages.filter(p => p.title && p.title.includes('토시'));
console.log("Pages found with '토시':", pages.map(p => p.title));
