const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let pageText = data.pages[22].text;
if (pageText.includes('첫 번째 원칙은')) {
    data.pages[22].text = pageText.replace('첫 번째 원칙은', '저의 원칙은');
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Updated page 23 successfully.");
} else {
    console.log("String not found!");
}
