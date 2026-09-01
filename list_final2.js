const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let currentPart = "";
bookData.pages.forEach((p, i) => {
    if (p.type === 'interlude' || p.title === '[브릿지] 시스템이 닿지 못하는 곳') {
        console.log(`[${i}] ${p.title}`);
    }
});
