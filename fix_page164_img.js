const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// Change caption on Index 163 (Page 164).
data.pages[163].keywords = "버려진 곳에서 고개를 내민 너";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated caption on Index 163.");
