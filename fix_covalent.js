const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if(p.text) {
        p.text = p.text.replace(/화학의 공유결합처럼 단단한 신뢰가 구축됩니다\./, "가장 흔들림 없는, 단단한 '공유결합'과 같은 신뢰가 구축됩니다.");
        p.text = p.text.replace(/화학의 "공유 결합\(Covalent Bond\)"으로 설명할 수 있습니다\. 각자 부족한 전자를 내어주고 서로를 단단히 묶어 안정화되는 과정\./, '"공유결합"으로 설명할 수 있습니다. 각자 부족한 것을 내어주고 서로를 단단히 묶어 가장 안정적인 상태를 이루는 과정.');
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Covalent bond text fixed.");
