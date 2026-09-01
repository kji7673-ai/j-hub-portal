const fs = require('fs');
const indexPath = 'index.html';

let content = fs.readFileSync(indexPath, 'utf8');

// The replace logic for markdown bold is: .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
// We will insert image parsing right after that.
content = content.replace(/(\.replace\(\/\\\*\\\*\(\.\*\?\)\\\*\\\*\/g, '<strong>\$1<\/strong>'\);)/g, "$1\n                        formattedText = formattedText.replace(/!\\[(.*?)\\]\\((.*?)\\)/g, '<img src=\"$2\" alt=\"$1\" style=\"width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1);\">');");

fs.writeFileSync(indexPath, content, 'utf8');
console.log("Markdown images enabled.");
