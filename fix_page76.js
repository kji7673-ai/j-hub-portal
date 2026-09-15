const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let page = data.pages[75];
page.isImageOnly = false;
page.text = "<div style=\"text-align: center; font-size: 1.1em; color: #1d1d1f; margin-top: 24px;\">사랑: 세상을 바꾸는 힘</div>";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated page 76 text.");
