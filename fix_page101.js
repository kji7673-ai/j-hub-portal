const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// Delete keywords from index 100 and 101
if (data.pages[100]) {
    data.pages[100].keywords = "";
}
if (data.pages[101]) {
    data.pages[101].keywords = "";
}

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated page 101 keywords.");
