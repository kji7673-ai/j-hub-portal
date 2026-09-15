const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// index 26 is Page 27
let page = data.pages[26];
page.text = "<div style=\"text-align: center; font-size: 1.1em; color: #1d1d1f; margin-top: 24px;\">고된 삶을 함께 한 나의 신발</div>";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated page 27 text.");
