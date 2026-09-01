const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

// Remove user_10, user_09, user_08
bookData.pages = bookData.pages.filter(p => {
    if (p.type === 'image_full' && p.image && (
        p.image.includes('user_10.jpg') ||
        p.image.includes('user_09.jpg') ||
        p.image.includes('user_08.jpg')
    )) {
        return false;
    }
    return true;
});

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("More empty images removed!");
