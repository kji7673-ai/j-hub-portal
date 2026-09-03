const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let p = bookData.pages.find(p => p.title && p.title.includes('100년의 기억을 덮는다는 것'));
if (p) {
    console.log("Found page text:");
    console.log(p.text);
} else {
    console.log("Page not found.");
}
