const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
for(let i=0; i<15; i++) {
    console.log(`[${i}] ${bookData.pages[i].partCategory || 'No Part'}: ${bookData.pages[i].title}`);
}
