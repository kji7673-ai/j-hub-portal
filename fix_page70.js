const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let page = data.pages[69];
page.isImageOnly = false;
page.text = "<div style=\"text-align: center; font-size: 1.1em; color: #1d1d1f; margin-top: 24px;\">휴식</div>";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated page 70 text.");
