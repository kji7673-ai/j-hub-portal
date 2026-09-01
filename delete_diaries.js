const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

let titlesToDelete = [
    "63. 지하철 내앞 방구쟁이가",
    "69. 결로",
    "72. 아름다운 왕비",
    "76. 너",
    "78. 화",
    "81. 무얼 드리시겠어요?",
    "89. 난 지금 점프중이다",
    "93. 화 내일 현상제출이다",
    "62. 주머니 속에서 진동이 온다."
];

let initialLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => {
    if (!p.title) return true;
    for (let t of titlesToDelete) {
        if (p.title.includes(t)) {
            console.log("Deleting:", p.title);
            return false;
        }
    }
    return true;
});

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log(`Deleted ${initialLength - bookData.pages.length} pages.`);
