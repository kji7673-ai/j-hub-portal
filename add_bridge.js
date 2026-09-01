const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let pages = bookData.pages;

const bridgePage = {
    "type": "text_only",
    "title": "[브릿지] 시스템이 닿지 못하는 곳",
    "text": "J-Hub가 아무리 정교해도, 데이터가 닿지 못하는 영역이 있다. 그것이 바로 '왜 이 공간에 건물을 지어야 하는가', '이 지역 주민들의 삶이 어떻게 나아질까'라는 질문이다. 다음 장에서는 시스템을 완전히 껐을 때, 건축가만이 할 수 있는 선택들을 이야기한다.",
    "part": "1부: 프롭테크와 정비사업의 미래"
};

let insertIndex = -1;
for(let i=0; i<pages.length; i++) {
    if(pages[i].type === 'interlude' && pages[i].title.includes('2부')) {
        insertIndex = i;
        break;
    }
}

if(insertIndex !== -1) {
    pages.splice(insertIndex, 0, bridgePage);
    let newBookData = `const bookData = {\n    pages: ${JSON.stringify(pages, null, 4)}\n};`;
    fs.writeFileSync('book_data.js', newBookData, 'utf8');
    console.log("Bridge added.");
} else {
    console.log("Could not find Part 2 interlude.");
}
