const fs = require('fs');
const path = require('path');

const bookDataPath = 'docs/book_data.js';
const sourceDir = '/Users/joongilkim/Downloads/책이미지';
const destDir = 'docs/static/images';

// Make sure destDir exists
if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
}

let content = fs.readFileSync(bookDataPath, 'utf8');

// Parse JS object
let match = content.match(/const bookData = (\{[\s\S]*?\});/);
if (!match) {
    console.log("Could not find bookData");
    process.exit(1);
}

let dataStr = match[1];
let data;
try {
    data = new Function('return ' + dataStr)();
} catch(e) {
    console.log("Error parsing JS:", e);
    process.exit(1);
}

// Update images ending with .png
let pngCounter = 1; // From 1 to 116
let updatedCount = 0;

for (let page of data.pages) {
    if (page.image && page.image.endsWith('.png')) {
        let newNum = 118 - pngCounter; // 1st PNG = 117.jpg, 116th PNG = 02.jpg
        let newName = newNum < 10 ? `0${newNum}.jpg` : `${newNum}.jpg`;
        let srcPath = path.join(sourceDir, newName);
        let destName = `user_${newName}`;
        let destPath = path.join(destDir, destName);
        
        if (fs.existsSync(srcPath)) {
            fs.copyFileSync(srcPath, destPath);
            page.image = `static/images/${destName}`;
            updatedCount++;
        } else {
            console.log(`Warning: ${srcPath} not found for page image ${page.image} (pngCounter=${pngCounter})`);
        }
        pngCounter++;
    }
}

console.log(`Updated ${updatedCount} images. Total .png processed: ${pngCounter - 1}`);

let newContent = content.substring(0, match.index) + 'const bookData = ' + JSON.stringify(data, null, 4) + ';' + content.substring(match.index + match[0].length);

fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log('Done writing');
