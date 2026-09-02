const fs = require('fs');
let code = fs.readFileSync('old_book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

let deleted = [];
for (let p of bookData.pages) {
    if (p.title && (p.title.includes('[도입]') || p.title.includes('[성찰]'))) {
        deleted.push({title: p.title, text: p.text});
    }
}
console.log(JSON.stringify(deleted, null, 2));
