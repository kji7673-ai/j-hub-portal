const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// 1. Fix typo on Page 223 (Index 222)
let text222 = data.pages[222].text;
data.pages[222].text = text222.replace("피할 수 없이 단차가 지는 부분은", "어쩔 수 없이 단차가 생기는 부분은");

// 2. Remove duplicate footnote on Page 225 (Index 224)
let text224 = data.pages[224].text;
data.pages[224].text = text224.replace(/<div class="footnote-box">\n<strong>\* 데크\(Deck\) 설계.*?<\/div>\n/s, "");

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated both pages.");
