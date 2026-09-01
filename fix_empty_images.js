const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

// Remove the contiguous block of image_full pages that are just sitting there before 쟁이의 마음
bookData.pages = bookData.pages.filter(p => {
    // We noticed user_07 to user_01 are sitting there. Let's just remove them.
    if (p.type === 'image_full' && p.image && (
        p.image.includes('user_07.jpg') ||
        p.image.includes('user_06.jpg') ||
        p.image.includes('user_05.jpg') ||
        p.image.includes('user_04.jpg') ||
        p.image.includes('user_03.jpg') ||
        p.image.includes('user_02.jpg') ||
        p.image.includes('user_01.jpg') ||
        p.image === 'static/images/3.jpg'
    )) {
        return false;
    }
    return true;
});

// Now insert the new image right before "쟁이의 마음: 두려움을 넘어 다시 붓을 드는 이유"
let targetIndex = bookData.pages.findIndex(p => p.title && p.title.includes('쟁이의 마음'));
if (targetIndex !== -1) {
    bookData.pages.splice(targetIndex, 0, {
        "type": "image_full",
        "image": "static/images/mentor_legacy.jpg",
        "partCategory": "2부: 증언과 성찰"
    });
}

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Empty images removed and new image inserted!");
