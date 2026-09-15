const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// If index 100 is just an image page with no text, and index 101 is the text continuation,
// let's just delete index 100 entirely if the user says there was no image anyway.
if (data.pages[100].title === '오뚝이' && data.pages[100].isImageOnly === true) {
    data.pages.splice(100, 1);
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Deleted index 100 completely.");
} else {
    console.log("Index 100 not matching expected pattern.");
}
