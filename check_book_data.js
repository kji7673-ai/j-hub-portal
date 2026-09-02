const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);
console.log(bookData.pages.slice(0, 3));
