const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let p = bookData.pages.find(p => p.title && p.title.includes('프롤로그'));
console.log("PROLOGUE TEXT:");
console.log(p.text);
