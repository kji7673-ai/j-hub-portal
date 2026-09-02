const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.type === 'interlude' || p.type === 'cover' || p.title.includes('부.') || p.title.includes('장.') || p.title.includes('에필로그')) {
        console.log(`Type: ${p.type} | Title: ${p.title} | Image: ${p.image || 'NONE'}`);
    }
});
