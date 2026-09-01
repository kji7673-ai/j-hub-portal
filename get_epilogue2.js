const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let epi = bookData.pages.find(p => p.title && p.title.includes('에필로그: 26년의 경험'));
if (epi) console.log(epi.text);
