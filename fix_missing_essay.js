const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

// Get original page
const oldContent = require('child_process').execSync('git show HEAD^:book_data.js').toString();
const oldMatch = oldContent.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const oldPages = eval('(' + oldMatch[2] + ')').pages;
const missingPage = oldPages.find(p => p.title === '졸음이 옵니다');
missingPage.partCategory = '2부: 증언과 성찰';

// Insert it into Theme 1 (after '오늘을 살아라는' or at the end of Theme 1)
const insertIndex = data.pages.findIndex(p => p.title === '오늘을 살아라는');
if(insertIndex > -1) {
    data.pages.splice(insertIndex, 0, missingPage);
} else {
    data.pages.push(missingPage);
}

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
