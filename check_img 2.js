const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach((p, index) => {
    if (p.title && (p.title.includes('다정한 디자인') || p.title.includes('만지작거리고') || p.title.includes('양팔에') || p.title.includes('구겨진'))) {
        console.log(\`[\${index}] \${p.title} -> \${p.image} (type: \${p.type})\`);
    }
});
