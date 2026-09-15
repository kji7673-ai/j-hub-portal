const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let pText = data.pages[218].text;

// Delete the first line entirely
data.pages[218].text = pText.replace(/"지속가능한 건축의 원리는 '공유결합'으로 설명할 수 있습니다\."<br>\n?/g, "");

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Successfully updated Index 218.");
