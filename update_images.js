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

// 1. Update cover
const coverDir = '/Users/joongilkim/Downloads/새로운 이미지';
let coverUpdated = false;
if (fs.existsSync(coverDir)) {
    let files = fs.readdirSync(coverDir);
    let coverFile = files.find(f => f.includes('표지') || f.includes('표지'));
    if (coverFile) {
        let coverSource = path.join(coverDir, coverFile);
        fs.copyFileSync(coverSource, path.join(destDir, 'cover_new.jpg'));
        data.pages[0].image = 'static/images/cover_new.jpg';
        console.log('Cover updated via readdirSync:', coverSource);
        coverUpdated = true;
    }
}
if (!coverUpdated) {
    console.log('Cover not found');
}

// 2. Update images
let updatedCount = 0;
for (let page of data.pages) {
    if (page.image) {
        let m = page.image.match(/^static\/images\/(\d+)\.jpg$/);
        if (m) {
            let oldNum = parseInt(m[1]);
            if (oldNum >= 1 && oldNum <= 117) {
                let newNum = 119 - oldNum;
                let newName = newNum < 10 ? `0${newNum}.jpg` : `${newNum}.jpg`;
                let srcPath = path.join(sourceDir, newName);
                let destName = `user_${newName}`;
                let destPath = path.join(destDir, destName);
                
                if (fs.existsSync(srcPath)) {
                    fs.copyFileSync(srcPath, destPath);
                    page.image = `static/images/${destName}`;
                    updatedCount++;
                } else {
                    console.log(`Warning: ${srcPath} not found for page image ${page.image}`);
                }
            }
        }
    }
}

console.log(`Updated ${updatedCount} images.`);

let newContent = content.substring(0, match.index) + 'const bookData = ' + JSON.stringify(data, null, 4) + ';' + content.substring(match.index + match[0].length);

fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log('Done writing');
