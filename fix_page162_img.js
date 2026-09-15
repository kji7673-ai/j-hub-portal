const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// Change caption on Index 160 (Page 161) which the user refers to as Page 162.
data.pages[160].keywords = "바위에서 발견한 웃는 저의 모습";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated caption on Index 160.");
