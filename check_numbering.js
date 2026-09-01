const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let currentPart = "";
bookData.pages.forEach((p, i) => {
    if(p.type === 'interlude') {
        currentPart = p.title;
        console.log(`\n=== ${currentPart} ===`);
    } else if (p.title) {
        console.log(`[${i}] ${p.title}`);
    }
});
