const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

bookData.pages.forEach((p, i) => {
    if (p.text && p.text.includes("## Part ")) {
        let match = p.text.match(/## Part [A-Z]\. [^\n]+/);
        if (match) console.log(`${i}: ${match[0]}`);
    }
});
