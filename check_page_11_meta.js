const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
console.log("Title:", bookData.pages[11].title);
console.log("Type:", bookData.pages[11].type);
