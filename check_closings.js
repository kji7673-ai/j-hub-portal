const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let closing1 = bookData.pages.find(p => p.title && p.title.includes('쟁이의 마음'));
let closing2 = bookData.pages.find(p => p.title && p.title.includes('마치는 글'));
if(closing1) console.log("--- 쟁이의 마음 ---\n", closing1.text.substring(0,200));
if(closing2) console.log("\n--- 마치는 글 ---\n", closing2.text.substring(0,200));
