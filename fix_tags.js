const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if (p.partCategory === '프롤로그' && p.title && p.title.includes('완벽한 시스템이 아닌')) {
        p.text = p.text.replace(
            /<strong>1부 \[플랫폼의 탄생\] 은/,
            "<strong>1부 [플랫폼의 탄생]</strong> 은"
        );
        p.text = p.text.replace(
            /<strong>2부 \[불완전함 속에서 완전함을 찾다\] 는/,
            "<strong>2부 [불완전함 속에서 완전함을 찾다]</strong> 는"
        );
        p.text = p.text.replace(
            /<strong>3부 \[불완전한 선택의 용기\] 는/,
            "<strong>3부 [불완전한 선택의 용기]</strong> 는"
        );
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Tags fixed.");
