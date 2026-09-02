const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const targets = [
    "1부. 설계의 본질 – 공유결합",
    "2부. 현장의 목소리, 공유결합의 증거",
    "부록 A. J-Hub 기술 개요",
    "부록 B. 자기 조직 진단 체크리스트",
    "부록 C. 생각을 명확히 하는 법 (마스터 프롬프트)"
];

targets.forEach(t => {
    let page = bookData.pages.find(p => p.title === t);
    if(page) {
        console.log(`Title: ${t} | Image: ${page.image || 'NONE'}`);
    } else {
        console.log(`Title: ${t} | PAGE NOT FOUND`);
    }
});
