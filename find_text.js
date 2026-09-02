const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

let found = false;
for (let p of bookData.pages) {
    if (p.text && p.text.includes('숫자가 철학이 되는 순간')) {
        found = true;
        console.log("Found in title:", p.title);
    }
}
if (!found) {
    console.log("NOT FOUND in book_data.js");
}
