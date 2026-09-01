const fs = require('fs');
let content = fs.readFileSync('book_data.js', 'utf8');

content = content.replace("1부 [시스템편]", "1부 [실전편]");
content = content.replace("2부 [철학편]", "2부 [증언과 성찰편]");
content = content.replace("3부 [증언과 성찰]", "3부 [미래 비전편]");

fs.writeFileSync('book_data.js', content, 'utf8');
console.log("Literal replace done!");
