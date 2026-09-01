const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
for(let i=8; i<=14; i++) {
    console.log(`${i}: [${bookData.pages[i].type}] ${bookData.pages[i].title}`);
}
