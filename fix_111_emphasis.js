const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let page = data.pages[111];

let oldText = page.text;
let replacementTarget = `때로는 후회와 상실이 찾아오겠지만, 그래도 인생이란 이미 벌어진 일에 대한 하루의 무게를 회피하지 않고 온전히 감당해 내는 것이겠지요.`;

let newBlock = `때로는 후회와 상실이 찾아오겠지만,<br>
<blockquote class="editorial-quote" style="border-left: 4px solid #0066cc; padding-left: 16px; margin: 24px 0; font-size: 1.15em; font-weight: 600; color: #1d1d1f;">
그래도 인생이란<br>
이미 벌어진 일에 대한 하루의 무게를<br>
회피하지 않고 온전히 감당해 내는 것이겠지요.
</blockquote>`;

let newText = oldText.replace(replacementTarget, newBlock);

if (newText !== oldText) {
    data.pages[111].text = newText;
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Updated page 112 with blockquote successfully.");
} else {
    console.log("Failed to find target string. Check exact whitespace.");
}
