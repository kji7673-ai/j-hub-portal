const fs = require('fs');
const path = require('path');

const imgDir = '/Users/joongilkim/Downloads/책이미지';
let availableImages = fs.readdirSync(imgDir).filter(f => f.toLowerCase().endsWith('.jpg'));

// Shuffle
for (let i = availableImages.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [availableImages[i], availableImages[j]] = [availableImages[j], availableImages[i]];
}

let imgIndex = 0;
function getRandomImage() {
    if (availableImages.length === 0) return 'static/images/1.jpg';
    const img = availableImages[imgIndex % availableImages.length];
    imgIndex++;
    return 'static/images/' + img;
}

let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
// Evaluate the JS to get the object
eval(code);

// Update images
bookData.pages.forEach(page => {
    if (page.type === 'interlude' || page.type === 'cover') {
        page.image = getRandomImage();
    }
    if (page.type === 'image_top' || page.type === 'image_full') {
        // Keep original if it's a sketch or diagram or other structural graphics
        if (page.image && (page.image.includes('sketch') || page.image.includes('diagram') || page.image.includes('flowchart') || page.image.includes('arch') || page.image.includes('user'))) {
            // keep
        } else {
            page.image = getRandomImage();
        }
    }
});

// Convert back to JS string
const newCode = `const bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', newCode, 'utf8');
console.log("Updated book_data.js with random images!");
