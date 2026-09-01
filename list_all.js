const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
bookData.pages.forEach((p, i) => {
    if (i < 30) console.log(`[${i}] ${p.type} / ${p.title} / part: ${p.partCategory}`);
});
