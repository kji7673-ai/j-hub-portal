const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// 1. Remove duplicate at index 93
const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => !(p.title && p.title === '만지작거리고 바스락거린다.'));

// 2. Set the image for our new '만지작거리고 바스락거린다' at index 30
bookData.pages.forEach(p => {
    if (p.title && p.title.includes('만지작거리고 바스락거린다')) {
        p.image = 'static/images/crumpled_wrapper.jpg';
        p.type = 'image_top';
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Removed ${originalLength - bookData.pages.length} duplicate pages. Assigned image.`);
