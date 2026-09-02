const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

for (let p of bookData.pages) {
    if (p.partCategory && p.partCategory.includes('3부')) {
        console.log("3부:", p.title || "(no title)", "| Type:", p.type);
    }
}
