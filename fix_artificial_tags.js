const fs = require('fs');

let content = fs.readFileSync('book_data.js', 'utf8');

// The regex needs to match the whole div block.
// It starts with <div style="background-color: var(--surface-pearl...
// and ends with </div><br>
const tagRegex = /<div style="background-color: var\(--surface-pearl, #fafafc\); padding: 12px 16px; border-radius: 8px; margin-bottom: 24px; border-left: 3px solid var\(--primary, #0066cc\); font-size: 0.9em; color: var\(--ink-muted-80, #333333\); font-weight: 600; display: inline-block;">\s*<svg[^>]*>.*?<\/svg>\s*\[연결된 철학:[^\]]+\]\s*<\/div><br>/g;

let matchCount = (content.match(tagRegex) || []).length;
console.log("Found tags to remove:", matchCount);

content = content.replace(tagRegex, '');

fs.writeFileSync('book_data.js', content, 'utf8');
console.log("Tags removed successfully!");
