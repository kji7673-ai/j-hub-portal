const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

let results = [];
for (let p of bookData.pages) {
    if (p.title && (p.title.includes('공유결합의 첫 질문') || p.title.includes('공유결합의 두 번째 질문') || p.title.includes('공유결합의 세 번째 질문') || p.title.includes('공유결합의 순간들') || p.title.includes('질문의 확장:'))) {
        results.push({title: p.title, text: p.text});
    }
}
console.log(JSON.stringify(results, null, 2));
