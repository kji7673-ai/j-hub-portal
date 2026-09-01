const fs = require('fs');
const indexPath = 'index.html';
let content = fs.readFileSync(indexPath, 'utf8');

const brokenRegex = /formattedText = formattedText\.replace\(\/!\\\[\(\.\*\?\)\\\]\\\\\(\(\.\*\?\)\\\\\)\/g, '<img src="\$2" alt="\.replace[^>]+>'\);" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba\(0,0,0,0\.1\);">'\);/g;

// Actually simpler: line by line replacement
const lines = content.split('\n');
const fixedLines = lines.map(line => {
    if (line.includes("formattedText = formattedText.replace(/!\\[(.*?)\]\\((.*?)\\)/g, '<img src=\"$2\" alt=\".replace")) {
        return "                        formattedText = formattedText.replace(/!\\[(.*?)\\]\\((.*?)\\)/g, '<img src=\"$2\" alt=\"$1\" style=\"width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1);\">');";
    }
    return line;
});

fs.writeFileSync(indexPath, fixedLines.join('\n'), 'utf8');
console.log("Fixed by line map.");
