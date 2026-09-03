const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let report = [];
let jhubCount = 0;
let aiCount = 0;

bookData.pages.forEach(p => {
    if (!p.text) return;
    if (p.text.toLowerCase().includes('j-hub') || p.text.toLowerCase().includes('jhub')) {
        jhubCount++;
    }
    if (p.title && p.title.includes('AI, 그래 넌 AI고 난 JI다')) {
        // Just checking if title is correct
    }
});

console.log(`J-Hub mentions found: ${jhubCount}`);
