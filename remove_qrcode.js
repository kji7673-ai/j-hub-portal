const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

const initialLength = data.pages.length;

// Filter out the QR code page
data.pages = data.pages.filter(p => !(p.title && p.title.includes('QR코드: Y구역 전체 보고서 원문')));

const newLength = data.pages.length;

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log(`QR code page removed. Pages went from ${initialLength} to ${newLength}.`);
