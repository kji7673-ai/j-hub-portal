const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code += '\nconsole.log(bookData.pages[140]);';
eval(code);
