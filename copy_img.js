const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

let idxs = [];
for (let i = 0; i < bookData.pages.length; i++) {
    let p = bookData.pages[i];
    if (p.text && p.text.includes('현상설계')) {
        idxs.push(i);
        console.log("Index", i, "has 현상설계:", p.text.substring(0, 30));
    }
}
