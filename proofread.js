const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if(p.text) {
        // Basic spell check & spacing fixes
        p.text = p.text.replace(/됬/g, '됐');
        p.text = p.text.replace(/할려/g, '하려');
        p.text = p.text.replace(/바램/g, '바람');
        p.text = p.text.replace(/틀려/g, '달라'); // context dependent but common mistake
        p.text = p.text.replace(/않하고/g, '안 하고');
        p.text = p.text.replace(/단차이/g, '단차');
        p.text = p.text.replace(/직우너/g, '직원');
        p.text = p.text.replace(/잰 걸을/g, '잰걸음을');
        p.text = p.text.replace(/수르 ㄹ/g, '수를 ');
        p.text = p.text.replace(/공사비르 ㄹ/g, '공사비를 ');
        p.text = p.text.replace(/흔히 있느 ㄴ/g, '흔히 있는 ');
        p.text = p.text.replace(/단치가/g, '단차가');
        p.text = p.text.replace(/걸아가는/g, '걸어가는');
        
        // Remove empty HTML tags if any
        p.text = p.text.replace(/<p><\/p>/g, '');
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Proofread complete.");
