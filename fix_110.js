const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let page = data.pages[109];

// Replace string exactly
let oldText = page.text;
let newText = oldText.replace(
    "현실의 시간에 살지 못할 때<br>\n오늘을 살아갈 힘을 잃게 되었을 때<br><br>\n그때가 죽음이지 않을까?",
    "<blockquote class=\"editorial-quote\" style=\"border-left: 4px solid #0066cc; padding-left: 16px; margin: 24px 0; font-size: 1.15em; font-weight: 600; color: #1d1d1f;\">현실의 시간에 살지 못할 때<br>\n오늘을 살아갈 힘을 잃게 되었을 때<br><br>\n그때가 죽음이지 않을까?</blockquote>"
);

data.pages[109].text = newText;
fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log(newText.includes('blockquote') ? "Success" : "Failed");
