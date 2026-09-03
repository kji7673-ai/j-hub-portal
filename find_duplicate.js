const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, index) => {
    if (p.text && p.text.includes('연필로 설계를 할때')) {
        console.log(`Found duplicate at index ${index}: Title="${p.title}"`);
    }
});
