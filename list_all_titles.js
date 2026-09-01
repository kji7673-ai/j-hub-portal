const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
bookData.pages.forEach((p, i) => {
    if(p.type === 'interlude') console.log(`\n=== ${p.title} ===`);
    else if (p.title) console.log(`[${i}] ${p.title}`);
});
