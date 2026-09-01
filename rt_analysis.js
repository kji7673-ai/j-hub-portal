const fs = require('fs');
let content = fs.readFileSync('book_data.js', 'utf8');
const vm = require('vm');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

let titles = bookData.pages.map(p => p.title).filter(Boolean);
titles.forEach((t, i) => console.log(`[${i}] ${t}`));
