const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// Change caption on Index 166 (Page 167).
data.pages[166].keywords = "함께 나누고, 웃고, 즐거워한다";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated caption on Index 166.");
