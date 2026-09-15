const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let page = data.pages[111];

let text = page.text;

// Remove the blockquote version
let targetToReplace = `때로는 후회와 상실이 찾아오겠지만,<br>\n<blockquote class="editorial-quote" style="border-left: 4px solid #0066cc; padding-left: 16px; margin: 24px 0; font-size: 1.15em; font-weight: 600; color: #1d1d1f;">\n그래도 인생이란<br>\n이미 벌어진 일에 대한 하루의 무게를<br>\n회피하지 않고 온전히 감당해 내는 것이겠지요.\n</blockquote>`;

let newTextStr = `때로는 후회와 상실이 찾아오겠지만, 그래도 <strong>인생이란 이미 벌어진 일에 대한 하루의 무게를 회피하지 않고 온전히 감당해 내는 것</strong>이겠지요.<br><br>`;

if (text.includes(targetToReplace)) {
    data.pages[111].text = text.replace(targetToReplace, newTextStr);
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Reverted blockquote and applied bold formatting.");
} else {
    console.log("Failed to find blockquote exact string.");
}

