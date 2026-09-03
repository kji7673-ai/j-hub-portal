const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, index) => {
    if (p.text && (p.text.includes('저주를 받았다') || p.text.includes('토시를 낀다') || p.text.includes('숫자 놀음이 아닌'))) {
        console.log(`Found candidate at index ${index}: Title="${p.title}"`);
        console.log(p.text.substring(0, 100) + '...');
    }
});
