const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// Change caption on Index 171 (Page 172).
data.pages[171].keywords = "아이구나";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated caption on Index 171.");
