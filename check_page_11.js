const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
console.log(bookData.pages[11].text.substring(0, 500));
console.log('...');
console.log("Length of page 11 text:", bookData.pages[11].text.length);
