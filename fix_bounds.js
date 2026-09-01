const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldLoad = `if(!isNaN(parsedChap) && !isNaN(parsedCol)) {
                    currentChapter = parsedChap;
                    currentColumn = parsedCol;
                }`;
const newLoad = `if(!isNaN(parsedChap) && !isNaN(parsedCol)) {
                    currentChapter = Math.max(0, Math.min(parsedChap, bookData.pages.length - 1));
                    currentColumn = parsedCol;
                }`;

html = html.replace(oldLoad, newLoad);
fs.writeFileSync('index.html', html, 'utf8');
console.log("Added bounds checking to localStorage load.");
