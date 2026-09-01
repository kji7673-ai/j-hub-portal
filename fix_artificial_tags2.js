const fs = require('fs');
let content = fs.readFileSync('book_data.js', 'utf8');

// Use a simpler regex that just targets the start and end of this specific div.
const tagRegex = /<div style=\\"background-color: var\(--surface-pearl[^>]*>.*?\[연결된 철학:[^\]]+\]\\n\s*<\/div><br>/g;
let matchCount = (content.match(tagRegex) || []).length;
console.log("Regex 1 match count:", matchCount);

// If regex fails, let's just do a blanket regex from <div style=\"background-color: var(--surface-pearl to </div><br>
// that contains [연결된 철학:
const tagRegex2 = /<div style=\\"background-color: var\(--surface-pearl.*?(?:\[연결된 철학:[^\]]+\]|\[연결된 철학:[^\]]+\]).*?<\/div><br>/g;
let matchCount2 = (content.match(tagRegex2) || []).length;
console.log("Regex 2 match count:", matchCount2);

// What if I just use a string replacement loop for the specific known pattern?
// Since JSON string has \n as literally \\n in the raw file buffer...
const tagRegex3 = /<div style=\\"background-color: var\(--surface-pearl, #fafafc\); padding: 12px 16px; border-radius: 8px; margin-bottom: 24px; border-left: 3px solid var\(--primary, #0066cc\); font-size: 0.9em; color: var\(--ink-muted-80, #333333\); font-weight: 600; display: inline-block;\\">\\n\s*<svg[^>]*>.*?<\/svg>\\n\s*\[연결된 철학:[^\]]+\]\\n\s*<\/div><br>/g;
let matchCount3 = (content.match(tagRegex3) || []).length;
console.log("Regex 3 match count:", matchCount3);

content = content.replace(tagRegex3, '');

fs.writeFileSync('book_data.js', content, 'utf8');
console.log("Tags removed.");
