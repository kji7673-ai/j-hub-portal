const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

console.log("46:", bookData.pages[46].text);
console.log("47:", bookData.pages[47].text);
console.log("48:", bookData.pages[48].text);
console.log("49:", bookData.pages[49].text);
